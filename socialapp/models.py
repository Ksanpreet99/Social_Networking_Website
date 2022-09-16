from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django_countries.fields import CountryField

# Create your models here.

gender=(('M','Male'),('F','Female'),('O','Other'))


class Profile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE,primary_key=True)
    first_name=models.CharField(max_length=20,null=False)
    last_name=models.CharField(max_length=20,null=False)
    phone_no=models.CharField(max_length=15,null=True,blank=True)
    DOB=models.DateField(null=True)
    gender=models.CharField(max_length=10,choices=gender,default='Male')
    city=models.CharField(max_length=20,null=False)
    country=CountryField()
    about_me=models.CharField(max_length=150)
    graduate=models.BooleanField(default=False,null=True,blank=True)
    post_graduate=models.BooleanField(default=False,null=True,blank=True)
    g_course=models.CharField(max_length=20,null=True,blank=True)
    p_course=models.CharField(max_length=20,null=True,blank=True)
    study_at=models.CharField(max_length=20,null=True,blank=True)
    p_study_at=models.CharField(max_length=20,null=True,blank=True)
    work_as=models.CharField(max_length=20,null=True,blank=True)
    work_at=models.CharField(max_length=20,null=True,blank=True)
    work_city=models.CharField(max_length=20,null=True,blank=True)
    work_country=CountryField(null=True,blank=True)
    profile_photo=models.ImageField(default='default.png',upload_to='Files/pics',null=True,blank=True)
    cover_photo=models.ImageField(default='defaultcover.jpg',upload_to='Files/pics',null=True,blank=True)
    added_on=models.DateTimeField(auto_now_add=True,null=True)
    updated_on=models.DateTimeField(auto_now=True,null=True)
    friends=models.ManyToManyField(User,blank=True,related_name='friends')
    is_verified=models.BooleanField(default=False)
    
    def __str__(self):
        return f'{self.user.username} Profile'
    
    def get_friends(self):
        return self.friends.all()

    def get_friends_no(self):
        return self.friends.all().count()

class user_interest(models.Model):
    user = models.ForeignKey(User,on_delete = models.CASCADE,null=True)
    interest=models.CharField(max_length=20,null=False)
    updated_on=models.DateTimeField(auto_now=True,null=True)

    def __str__(self):
        return f'{self.user.username} Interest'

class Post(models.Model):
    user = models.ForeignKey(User,on_delete = models.CASCADE,null=True)
    post_text=models.TextField(max_length=300)
    post_img=models.ImageField(upload_to='Files/pics',null=True,blank=True)
    post_video=models.FileField(upload_to='Files/videos',null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)    
    updated_on=models.DateTimeField(auto_now=True,null=True)
    like=models.ManyToManyField(User,related_name='user_post',blank=True)
   

    def __str__(self):
        return f'{self.user.username} Post {self.id}'
    
    @property
    def like_count(self):
        return self.like.all().count()

class Comments(models.Model):
    user = models.ForeignKey(User,on_delete = models.CASCADE,null=True)
    post = models.ForeignKey(Post,on_delete = models.CASCADE,null=True)
    comment_text = models.TextField(default="",max_length=2000)
    created_at = models.DateTimeField(auto_now_add=True) 

    def __str__(self):
        return f'{self.user.username} on {self.post}'


class Friend_Request(models.Model):
    sender= models.ForeignKey(User,on_delete=models.CASCADE,related_name='sender')
    receiver= models.ForeignKey(User,on_delete=models.CASCADE,related_name='reciever')
    created_at = models.DateTimeField(auto_now_add=True)    
    updated_on=models.DateTimeField(auto_now=True,null=True)

    def __str__(self):
        return f'{self.sender} to {self.receiver}'

    


