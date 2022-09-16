from django.shortcuts import render,redirect,get_list_or_404
from django.utils.safestring import mark_safe
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate,login as auth_login,logout as django_logout
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.urls import reverse
from .forms import *
from .decorators import unauthenticated_user
from django.http import HttpResponse, HttpResponseForbidden, HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
# Create your views here.

def can_not_view(request):
    return render(request,"can_not_view.html")

@unauthenticated_user
def login(request):
    if request.method == 'POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        user=authenticate(request,username=username,password=password)
        if user is not None:
            auth_login(request,user)
            url = reverse('index',kwargs = {'username':username})
            return redirect(url) 
        else:
            messages.info(request,'Username OR Password is Incorrect')
    form= AuthenticationForm()
    context={'form':form}
    return render(request,"login.html",context)

@unauthenticated_user
def register(request):
    form=CreateUserForm()
    if request.method=='POST':
        form=CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            username=request.POST.get('username')
            emails = request.POST.get('email')
            mail_list = emails.split()
            print(mail_list)
            title = "Welcome! Thanks for creating an account at Junction."
            message = "\nHello " +username+",\n\nWelcome! We’d like to confirm that your account was created successfully.\nIf you experience any issues logging into your account, reach out to us at junction.skb@gmail.com.\n\nRegards,\n\nThe Junction Team"
            send_mail(
                title,
                message,
                '',
                mail_list,
                fail_silently=False,
            )
            return redirect('login')    
    context={'form':form}
    return render(request,"register.html",context)


def logout(request):
    django_logout(request)
    return redirect('login')

@login_required(login_url='login')
def index(request,username):
    if username != request.user.username:
        return redirect(can_not_view) 
    profile=Profile.objects.all()
    post=Post.objects.all().order_by('-created_at')
    comment=Comments.objects.all()
    interest=user_interest.objects.filter(user=request.user)
    recent_comment=Comments.objects.all().order_by('-created_at')[:5]
    if request.method=="POST":
        form=create_post_form(request.POST,request.FILES)
        if form.is_valid():
            user=request.POST['user']
            form.save()
            url = reverse('index',kwargs = {'username':username})
            return redirect(url)
        
        comm_form=comment_form(request.POST) 
        if comm_form.is_valid():
            user=request.POST['user']
            post=request.POST['post']
            comm_form.save()
            url = reverse('index',kwargs = {'username':username})
            return redirect(url)
    else:      
        form=create_post_form()
        comm_form=comment_form()
        context={
                'username':username,
                'profile':profile,
                'form':form,
                'post':post,
                'comm_form':comm_form,
                'comment':comment,
                'interest':interest,
                'recent_comment':recent_comment
                }
        return render(request,"index.html",context)


@login_required(login_url='login')
def my_profile(request,username):
    if username != request.user.username:
        return redirect(can_not_view) 
    user=User.objects.get(username=username)
    profile=Profile.objects.get(user=user)
    interest=user_interest.objects.filter(user=user)
    context={'profile':profile,
             'interest':interest,
             'username':username
             }
    return render(request,"my_profile.html",context)
   
@login_required(login_url='login')
def friends_profile(request,username):
    user=User.objects.get(username=username)
    profile=Profile.objects.get(user=user)
    interest=user_interest.objects.filter(user=user)
    context={'profile':profile,'interest':interest,'username':username}
    return render(request,"friends_profile.html",context)

@login_required(login_url='login')
def edit_profile(request,username):
    if username != request.user.username:
        return redirect(can_not_view) 
    user=request.user
    profile=Profile.objects.get(user=user)
    recent_comment=Comments.objects.all().order_by('-created_at')[:5]
    if request.method=='POST':
        profile = Profile()
        form=profile_form(request.POST, instance=request.user)
        p_form=edit_profile_form(request.POST,request.FILES,instance=request.user.profile)
        if form.is_valid() and p_form.is_valid():
            form.save()
            p_form.save()
            messages.success(request, f'Your Profile has been Updated!')
            url = reverse('edit_profile',kwargs = {'username':username})
            return redirect(url)
    else:
        form=profile_form(instance=request.user)
        p_form = edit_profile_form(instance=request.user.profile)
        context={'form':form,
                 'p_form':p_form,
                 'username':username,
                 'profile':profile,
                 'recent_comment':recent_comment 
                 }
        return render(request,"edit_profile.html",context)

@login_required(login_url='login')
def edit_interest(request,username):
    if username != request.user.username:
        return redirect(can_not_view) 
    user=request.user
    profile=Profile.objects.get(user=user)
    interest=user_interest.objects.filter(user=user)
    recent_comment=Comments.objects.all().order_by('-created_at')[:5]
    if request.method=='POST':
        form=user_interest_form(request.POST)
        if form.is_valid():
            user=request.POST['user']
            form.save()
            messages.success(request, f'Your Profile has been Updated!')
            url = reverse('edit_interest',kwargs = {'username':username})
            return redirect(url)
    else:
        form=user_interest_form()
        context={'form':form,
                'interest':interest,
                'profile':profile,
                'recent_comment':recent_comment 
                }
        return render(request,"edit_interest.html",context)

@login_required(login_url='login')
def delete_interest(request,id):
    interest=user_interest.objects.get(id=id)
    next=request.GET.get("next",None)
    interest.delete()
    if next and next!='':    
        return HttpResponseRedirect(redirect_to=next)

@login_required(login_url='login')
def timeline(request,username):
    if username != request.user.username:
        return redirect(can_not_view) 
    user=User.objects.get(username=username)
    profile=Profile.objects.get(user=user)
    post=Post.objects.filter(user=user).order_by('-created_at')
    comment=Comments.objects.all()
    recent_comment=Comments.objects.all().order_by('-created_at')[:5]
    if request.method=="POST":
        form=create_post_form(request.POST,request.FILES)
        if form.is_valid():
            user=request.POST['user']
            form.save()
            url = reverse('timeline',kwargs = {'username':username})
            return redirect(url)
        
        comm_form=comment_form(request.POST) 
        if comm_form.is_valid():
            user=request.POST['user']
            post=request.POST['post']
            comm_form.save()
            url = reverse('timeline',kwargs = {'username':username})
            return redirect(url)
    else:      
        form=create_post_form()
        comm_form=comment_form()
        context={'username':username,
                'profile':profile,
                'form':form,
                'post':post,
                'comm_form':comm_form,
                'comment':comment,
                'recent_comment':recent_comment

                }
        return render(request,"time-line.html",context)

@login_required(login_url='login')
def delete_post(request,id):
    post=Post.objects.get(id=id)
    next=request.GET.get("next",None)
    post.delete()
    if next and next!='':    
        return HttpResponseRedirect(redirect_to=next)

@login_required(login_url='login')
def friends_time_line(request,username):
    user=User.objects.get(username=username)
    profile=Profile.objects.get(user=user)

    post=Post.objects.filter(user=user).order_by('-created_at')
    comment=Comments.objects.all()
    
    if request.method=="POST":
        form=create_post_form(request.POST,request.FILES)
        if form.is_valid():
            user=request.POST['user']
            form.save()
            url = reverse('friends_time_line',kwargs = {'username':username})
            return redirect(url)
        
        comm_form=comment_form(request.POST) 
        if comm_form.is_valid():
            user=request.POST['user']
            post=request.POST['post']
            comm_form.save()
            url = reverse('timeline',kwargs = {'username':username})
            return redirect(url)
    else:      
        form=create_post_form()
        comm_form=comment_form()
        context={'username':username,
                'profile':profile,
                'form':form,
                'post':post,
                'comm_form':comm_form,
                'comment':comment,
                
                }
        return render(request,"friends_time_line.html",context)


@login_required(login_url='login')
def like_post(request,username):
    username=User.objects.get(username=username)
    next=request.GET.get("next",None)
    if request.method=='POST':
        post_id=request.POST.get('post')
        post=Post.objects.get(id=post_id)
        if username in post.like.all():
            post.like.remove(username)
        else:
            post.like.add(username)
    if next and next!='':
            messages.success(request, f'Request Sent')
            return HttpResponseRedirect(redirect_to=next)    

@login_required(login_url='login')
def share_post(request,id):
    post=Post.objects.get(id=id)
    recent_comment=Comments.objects.all().order_by('-created_at')[:5]
    comment=Comments.objects.all()
    interest=user_interest.objects.filter(user=request.user)
    if request.method=="POST":
        comm_form=comment_form(request.POST) 
        if comm_form.is_valid():
            user=request.POST['user']
            post=request.POST['post']
            comm_form.save()
            url = reverse('share_post',kwargs = {'id':id})
            return redirect(url)
            
    else:      
        comm_form=comment_form()
    context={"post":post,
    "recent_comment":recent_comment,
    "comment":comment,
    "comm_form":comm_form,
    "interest":interest
    }
    return render(request,"post.html",context)



@login_required(login_url='login')
def timelinefriends(request,username):
    if username != request.user.username:
        return redirect(can_not_view) 
    recent_comment=Comments.objects.all().order_by('-created_at')[:5]
    if request.user.username==username:
        all_users=User.objects.all().exclude(id=request.user.id)
        user=User.objects.get(username=username)
        profile=Profile.objects.get(user=user)
        friend_request=Friend_Request.objects.all() 
        f_request=Friend_Request.objects.filter(receiver=request.user).count()
        context={'username':username,
                    'profile':profile,
                    'friend_request':friend_request,
                    'f_request':f_request,
                    'all_users':all_users,
                    'recent_comment':recent_comment
                    }
        return render(request,"timeline-friends.html",context)
    else:
        user=User.objects.get(username=username)
        profile=Profile.objects.get(user=user)
        context={'username':username,
                'profile':profile,
                'recent_comment':recent_comment
                }
        return render(request,"timeline-friends.html",context)


@login_required(login_url='login')
def send_friend_request(request,userID):
    sender=request.user
    receiver=User.objects.get(id=userID)
    next=request.GET.get("next",None)
    friend_request, created=Friend_Request.objects.get_or_create(sender=sender,receiver=receiver)
    if created:
        if next and next!='':
            messages.success(request, f'Request Sent')
            return HttpResponseRedirect(redirect_to=next)
    else:
        if next and next!='':
            messages.success(request, f'Request Already Sent')
            return HttpResponseRedirect(redirect_to=next)

@login_required(login_url='login')
def accept_friend_request(request,requestID):
    friend_request=Friend_Request.objects.get(id=requestID)
    if friend_request.receiver==request.user:
        friend_request.sender.friends.add(friend_request.receiver.id)
        friend_request.receiver.friends.add(friend_request.sender.id)
        friend_request.delete()
        messages.success(request, f'Request Accepted')
        url = reverse('timelinefriends',kwargs = {'username':request.user.username})
        return redirect(url)
    else:
        messages.success(request, f'Request Not Accepted')
        return redirect('timelinefriends')

@login_required(login_url='login')
def delete_friend_request(request,requestID):
    friend_request=Friend_Request.objects.get(id=requestID)
    friend_request.delete()
    messages.success(request, f'Request Deleted')
    url = reverse('timelinefriends',kwargs = {'username':request.user.username})
    return redirect(url)

@login_required(login_url='login')
def delete_friend(request,requestID):
    user=request.user
    friend=User.objects.get(id=requestID)
    user.friends.remove(friend.id)
    friend.friends.remove(user.id)
    messages.success(request, f'Unfriended')
    url = reverse('timelinefriends',kwargs = {'username':request.user.username})
    return redirect(url)

@login_required(login_url='login')
def photos(request,username):
    if username != request.user.username:
        return redirect(can_not_view) 
    user=User.objects.get(username=username)
    profile=Profile.objects.get(user=user)
    interest=user_interest.objects.filter(user=user)
    post=Post.objects.filter(user=user).order_by('-created_at')
    context={'profile':profile,'username':username,'interest': interest,'post':post}
    return render(request,"timeline-photos.html",context)

@login_required(login_url='login')
def videos(request,username):
    if username != request.user.username:
        return redirect(can_not_view) 
    user=User.objects.get(username=username)
    profile=Profile.objects.get(user=user)
    interest=user_interest.objects.filter(user=user)
    post=Post.objects.filter(user=user).order_by('-created_at')
    context={'profile':profile,'username':username,'interest': interest,'post':post}
    return render(request,"timeline-videos.html",context)


