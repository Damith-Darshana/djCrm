from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models.signals import post_save #import the signal 

class User(AbstractUser):
  # let's check if the user is a Organizer or an Agent videoTimeline : 05:37
  is_organizer=models.BooleanField(default=True)
  is_agent = models.BooleanField(default=False)

# Every User has a userprofile or known as userprofile
class UserProfile(models.Model):
  user  = models.OneToOneField(User,on_delete=models.CASCADE)

  def __str__(self) -> str:
    return self.user.username

class Lead(models.Model):
  first_name = models.CharField(max_length=20)
  last_name = models.CharField(max_length=20)
  age = models.IntegerField(default=0)
  # agent = models.ForeignKey("Agent",on_delete=models.CASCADE)
  # here going to change the above line to as follows for the filtering purpose
  organization = models.ForeignKey(UserProfile,on_delete=models.CASCADE)
  agent = models.ForeignKey("Agent",null=True,blank=True,on_delete=models.SET_NULL)
  category = models.ForeignKey("Category",null=True,blank=True,on_delete=models.SET_NULL,related_name="leads") #the related name helps to get Lead details within the category(revese relationship)


  def __str__(self):
    return f"{self.first_name} {self.last_name}"
  
class Agent(models.Model):
  user = models.OneToOneField(User,on_delete=models.CASCADE) 
  organization = models.ForeignKey(UserProfile,on_delete=models.CASCADE)


  def __str__(self):
    return self.user.username
  


class Category(models.Model):
  name = models.CharField(max_length=30)
  organization = models.ForeignKey(UserProfile,on_delete=models.CASCADE)

  def __str__(self):
    return self.name
  


















#we use post save to Automatically create UserProfile for each User when a User is Created
def post_user_created(sender,instance,created, **kwargs): #this method will be called when the post_save signal implements
  if(created):
    UserProfile.objects.create(user = instance)  # this will create a UserProfile for the newly created user instance

post_save.connect(post_user_created,sender=User) #implements when a New User is created or saved some changes into a User in the above user Model