from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db import models

from django.contrib.auth import get_user_model, login
from django.views.generic.edit import DeleteView
User = get_user_model()

from django.db.models.signals import post_save, pre_save
from django.shortcuts import get_object_or_404
from django.dispatch import receiver

from django.utils.text import slugify

from django.urls import reverse
# Create your models here.


class Group(models.Model):
    name = models.CharField(max_length=20, unique=True)
    slug = models.SlugField(allow_unicode=True, unique=True)
    description = models.TextField(blank=True, default='')
    admin = models.ForeignKey(User, blank=True, related_name='admin', on_delete= models.CASCADE)
    moderators = models.ManyToManyField(User, blank=True, related_name='group_moderators')
    ban = models.ManyToManyField(User, blank=True, related_name='group_ban')
    members = models.ManyToManyField(User, through='GroupMember')
    cover = models.ImageField(upload_to='uploads/covers', default='uploads/covers/default.jpg', blank=True)
    created_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('detail-group', kwargs={'slug':self.slug})

    class Meta():
        ordering = ["-created_on"]


class GroupMember(models.Model):
    group = models.ForeignKey(Group, related_name='membership', on_delete = models.CASCADE)
    user = models.ForeignKey(User, related_name='user_groups', on_delete = models.CASCADE)
    joined_since = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username
    
    class Meta():
        unique_together = ('user', 'group')



@receiver(pre_save, sender=Group)
def Group_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = slugify(instance.name)
    
@receiver(post_save, sender=Group)
def group_save_member(sender, instance, created, *args, **kwargs):
    if not GroupMember.objects.filter(user=instance.admin, group=instance).exists():
        GroupMember.objects.create(user=instance.admin, group=instance)

class GroupPost(models.Model):
    author = models.ForeignKey(User, related_name='group_posts', on_delete=models.CASCADE)
    content = models.TextField()
    image = models.ImageField(upload_to='uploads/groupposts', blank=True, null=True)
    group = models.ForeignKey(Group, related_name='groupposts', null=True, blank=True, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.content

    def get_absolute_url(self):
        return reverse('detail-group', kwargs={'slug':self.group.slug})

    class Meta:
        ordering = ['-timestamp']



