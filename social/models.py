from django.db import models

from django.db.models.signals import post_save
from django.dispatch import receiver

from django.contrib.auth import get_user_model
User = get_user_model()

# Create your models here.
class Post(models.Model):
    author = models.ForeignKey(User, on_delete = models.CASCADE)
    image = models.ImageField(upload_to='uploads/posts', blank=True, null=True)
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, blank = True, related_name='likes')
    
    shared_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="+",blank=True, null=True)
    shared_body = models.TextField(blank=True, null=True)
    og_post_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        ordering = ['-created_on']

class Comment(models.Model):
    author = models.ForeignKey(User, on_delete = models.CASCADE)
    comment = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey('Post', on_delete = models.CASCADE, related_name='comments')
    likes = models.ManyToManyField(User, blank = True, related_name="comment_likes")
 
    parent = models.ForeignKey('self', on_delete=models.CASCADE, blank = True, null= True, related_name='+')

    @property
    def child(self):
        return Comment.objects.filter(parent=self).order_by('created_on').all()

    @property
    def is_main_comment(self):
        if self.parent is None:
            return True
        return False
        
class UserProfile(models.Model):
    user = models.OneToOneField(User, primary_key=True, related_name='profile', on_delete=models.CASCADE)
    name = models.CharField(max_length = 150, blank = True, null = True)
    bio = models.TextField(max_length = 350, blank = True, null = True)
    GENDER_CHOICES = (
        ('', 'Choose Your Gender'),
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Rather Not Say', 'Rather Not Say')
    )
    gender = models.CharField(max_length=14, choices=GENDER_CHOICES)
    birth_date = models.DateField(blank = True, null = True)
    location = models.CharField(max_length = 150, blank = True, null = True)
    profile_background = models.ImageField(upload_to='uploads/profile_background', default='uploads/profile_background/default.jpg', blank=True)
    profile_pic = models.ImageField(upload_to='uploads/profile_pictures', default='uploads/profile_pictures/default_img.png', blank=True)
    followers = models.ManyToManyField(User, related_name='followers', blank = True)
    verified = models.BooleanField(default=False)


#We can make a django signal that when a user signs up we make a profile for them
#sender - User
#reciever - decorator (@reciever)
# instance = User/ object being saved
#created = True/False

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()



class Notification(models.Model):
    # 1 = like
    # 2 = comment 
    # 3 = follow

    notification_type = models.IntegerField()
    
    to_user = models.ForeignKey(User, related_name = 'notification_to', null=True, on_delete=models.CASCADE)
    from_user = models.ForeignKey(User, related_name = 'notification_from', null=True, on_delete=models.CASCADE)  

    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='+', blank=True, null=True)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='+', blank=True, null=True) # plus will remove reverse mapping

    timestamp = models.DateTimeField(auto_now_add=True)

    user_has_seen = models.BooleanField(default=False)