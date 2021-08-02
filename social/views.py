from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.http import HttpResponseRedirect, HttpResponse

from django.db.models import Q
from django.utils import timezone

from django.views.generic import View, TemplateView, ListView, DetailView, DeleteView, UpdateView
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin

from django.utils import timezone

from . import models, forms
from groups import models as group_models

from django.contrib.auth import get_user_model
User = get_user_model()

from .utils import trending_posts

import random

# Create your views here.
class PostListView(LoginRequiredMixin, View):

    login_url = '/accounts/login/'

    def get(self, request, *args, **kwargs):
        posts = models.Post.objects.all().order_by('-created_on')
        form = forms.PostForm
        share_form = forms.ShareForm()
        
        follow = list(models.UserProfile.objects.all())
        follow = random.choices(follow,  k = 5)
        follow = set(follow)

        context = {
            'post_list':posts,
            'follow':follow,
            'form':form,
            'shareform':share_form, 
        }

        return render(request, 'social/post_list.html', context)

    def post(self, request, *args, **kwargs):
        posts = models.Post.objects.all().order_by('-created_on')
        form = forms.PostForm(request.POST, request.FILES)
        share_form = forms.ShareForm()

        if form.is_valid():
            # form.instance.author = request.user
            new_post =  form.save(commit=False)
            new_post.author = request.user
            new_post.save()
            
            new_post.create_tags()

        context = {
            'post_list':posts,
            'form':form,
            'shareform':share_form, 
        }

        return redirect(reverse("post_list"))

class SharedPostView(View):
    def post(self, request, pk,*args, **kwargs):
        orignal_post = models.Post.objects.get(pk=pk)
        
        if orignal_post.author != request.user and orignal_post.shared_user != request.user:
            form = forms.ShareForm(request.POST)
            if form.is_valid():
                new_post = models.Post(
                    shared_body = self.request.POST.get('body'),
                    body = orignal_post.body,
                    author = orignal_post.author,
                    shared_user=request.user,  
                    og_post_date=orignal_post.created_on,
                    image = orignal_post.image,
                )

            new_post.save()

        return redirect('post_list')
    
class SharedPostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):

    login_url = '/accounts/login/'

    model = models.Post
    template_name = 'social/post_delete.html'
    success_url = reverse_lazy("post_list")

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.shared_user

class PostDetailView(LoginRequiredMixin, View):

    login_url = '/accounts/login/'

    def get(self, request, pk, *args, **kwargs):
        post = models.Post.objects.get(pk=pk)
        form = forms.CommentForm

        context = {
            'post': post,
            'form':form,
        }

        return render(request, 'social/post_detail.html', context)


    def post(self, request, pk,*args, **kwargs):
        post = models.Post.objects.get(pk=pk)
        form = forms.CommentForm(request.POST)

        if form.is_valid():
            # form.instance.author = request.user
            # form.instance.post = post
            # form.save()
            new_comment = form.save(commit=False)
            new_comment.author = request.user
            new_comment.post = post
            new_comment.save()

            new_comment.create_tags()
            
            models.Notification.objects.create(notification_type = 2, from_user = request.user, to_user = post.author, post=post)

        context = {
            'post_list':post,
            'form':form
        }

        return redirect(reverse("post_detail", kwargs={'pk':post.pk}))

class commentReplyView(LoginRequiredMixin, View):
    def post(self, request, pk, id,*args, **kwargs):
        post = models.Post.objects.get(pk=pk)
        parent_comment = models.Comment.objects.get(id=id)
        form = forms.CommentForm(request.POST)

        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.author = request.user
            new_comment.post = post
            new_comment.parent = parent_comment
            new_comment.save()

            return redirect('post_detail', pk=post.pk)

class PostEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):

    login_url = '/accounts/login/'

    model = models.Post
    fields = ('body', )
    template_name = 'social/post_edit.html'

    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse_lazy("post_detail", kwargs={'pk':pk})

    #basically this function comes with UserPassesTestMixin, so if the boolean value is ture
    #in the below statement then only the class will work else we will get 403
    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):

    login_url = '/accounts/login/'

    model = models.Post
    template_name = 'social/post_delete.html'
    success_url = reverse_lazy("post_list")

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

class CommentDelete(LoginRequiredMixin, UserPassesTestMixin, DeleteView):

    login_url = '/accounts/login/'

    model = models.Comment
    template_name = 'social/comment_delete.html'

    def get_success_url(self):
        comment = self.get_object()
        pk = comment.post.pk
        return reverse_lazy("post_detail", kwargs={'pk':pk})

    def test_func(self):
        comment = self.get_object()

        post = comment.post
        return self.request.user == comment.author or self.request.user == post.author 
      

class ProfileView(View):
    def get(self, request, pk,*args, **kwargs):
        profile = models.UserProfile.objects.get(pk=pk)
        user = profile.user
        posts = models.Post.objects.filter(author=user).order_by('-created_on')
        form = forms.PostForm(request.POST)
        refer = ''

        groups = group_models.Group.objects.filter(members=user)

        if profile.gender == 'Male':
            refer = 'his'
        elif profile.gender == 'Female':
            refer = 'her'
        else:
            refer = 'their'

        context = {
            'profile':profile,
            'posts':posts,
            'refer':refer,
            'form':form,
            'group_list':groups,
        }
        return render(request, 'social/profile.html', context)




class ProfileEditView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):

    login_url = '/accounts/login/'

    model = models.UserProfile
    form_class = forms.ProfileForm
    template_name  = 'social/profile_edit.html'

    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse_lazy('profile_view', kwargs={'pk':pk})

    def test_func(self):
        profile = self.get_object()
        return self.request.user == profile.user

class AddFollower(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        profile = models.UserProfile.objects.get(pk=pk)
        profile.followers.add(request.user)
        models.Notification.objects.create(notification_type = 3, from_user = request.user, to_user = profile.user)

        return redirect(reverse_lazy('profile_view', kwargs={'pk':pk}))

class RemoveFollower(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        profile = models.UserProfile.objects.get(pk=pk)
        profile.followers.remove(request.user)

        return redirect(reverse_lazy('profile_view', kwargs={'pk':pk}))

class AddLike(LoginRequiredMixin, View):
    def post(self, request, pk, *args, **kwargs):
        post = models.Post.objects.get(pk=pk)

        is_like = False

        for like in post.likes.all():
            if like == request.user:
                is_like = True
                break

        if not is_like:
            post.likes.add(request.user)
            models.Notification.objects.create(notification_type = 1, from_user = request.user, to_user = post.author, post=post)

        if is_like:
            post.likes.remove(request.user)

        next = request.POST.get('next', '/')
        return HttpResponseRedirect(next)

class LikeListView(LoginRequiredMixin, ListView):
    def get(self, request, pk, *args, **kwargs):
        post = models.Post.objects.get(pk=pk)

        context = {
        'post':post,
        }
        return render(request, 'social/like_list.html', context)

class UserSearch(View):
    def get(self, request, *args, **kwargs):
        query = self.request.GET.get('query')
        profile_list = models.UserProfile.objects.filter(
            Q(user__username__icontains=query) |
            Q(name__icontains=query)|
            Q(location__icontains=query)
        )

        context={
            'profile_list':profile_list,

        }

        return render(request, 'social/search.html', context)

class AllFollowers(LoginRequiredMixin, View):
    login_url = '/accounts/login/'

    def get(self, request, pk, *args, **kwargs):
        profile = models.UserProfile.objects.get(pk=pk)
        followers = profile.followers.all()

        context = {
            'profile':profile,
            'followers':followers,
        }

        return render(request, 'social/followers.html', context)

class AddCommentLike(LoginRequiredMixin, View):
    def post(self, request, id, *args, **kwargs):
        comment = models.Comment.objects.get(id=id)

        is_like = False

        for like in comment.likes.all():
            if like == request.user:
                is_like = True
                break

        if not is_like:
            comment.likes.add(request.user)
            models.Notification.objects.create(notification_type = 1, from_user = request.user, to_user = comment.author, comment=comment)

        if is_like:
            comment.likes.remove(request.user)

        next = request.POST.get('next', '/')
        return HttpResponseRedirect(next)


class RemoveNotification(View, LoginRequiredMixin):

    login_url = 'accounts/login/'

    def delete(self, request, notif_pk, *args, **kwargs):
        notification = models.Notification.objects.get(pk=notif_pk)

        notification.user_has_seen = True
        notification.save()

        return HttpResponse('Success', content_type= 'text/plain')

class explore(LoginRequiredMixin,View):

    def get(self, request, *args, **kwargs):
        query = self.request.GET.get('query')
        if not query:
            query = ''
        tag = models.Tag.objects.filter(name=query).first()
        group = group_models.Group.objects.filter(
            Q(name__icontains=query)
        )
        users = models.UserProfile.objects.filter(
            Q(user__username__icontains=query) |
            Q(name__icontains=query)|
            Q(location__icontains=query)
        )
        posts = models.Post.objects.filter(
            Q(body=query) |
            Q(shared_body=query)
        )

        tag_posts = models.Post.objects.filter(tags__in=[tag]) #any post with that tag will come in this qs

        print(group)

        explore_form = forms.exploreForm()

        context = {
            "tag_posts":tag_posts,
            "posts":posts,
            "users":users,
            "groups":group,

            "explore_form": explore_form,
        }

        return render(request, 'social/explore/explore.html', context)
    
    def post(self, request, *args, **kwargs):

        explore_form = forms.exploreForm(request.POST)

        if explore_form.is_valid():
            
            query = explore_form.cleaned_data['query']
            
            tag = models.Tag.objects.filter(name=query).first()
            group = group_models.Group.objects.filter(name=query)
            
            users = models.UserProfile.objects.filter(
                Q(user__username__icontains=query) |
                Q(name__icontains=query)|
                Q(location__icontains=query)
            )
            posts = models.Post.objects.filter(
                Q(body=query) |
                Q(shared_body=query)
            )

            tag_posts = models.Post.objects.filter(tags__in=[tag]) #any post with that tag will come in this qs

            explore_form = forms.exploreForm()

            context = {
                "tag_posts":tag_posts,
                "posts":posts,
                "users":users,
                "groups":group,

                "explore_form": explore_form,
            }
            

        return render(request, 'social/explore/explore.html', context)