from django.shortcuts import redirect, render

from django.urls import reverse, reverse_lazy
from django.shortcuts import get_object_or_404, redirect

from django.contrib import messages

from . import models, forms

from django.db.models import Q, Max

from django.views.generic import (TemplateView,
                                  View,
                                  ListView,
                                  CreateView, 
                                  UpdateView,
                                  DetailView, 
                                  DeleteView,
                                  RedirectView) 

from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin

from django.contrib.auth import get_user_model
User = get_user_model()


# Create your views here.

class CreateGroup(LoginRequiredMixin, CreateView):
    template_name = 'groups/group_create.html'
    model = models.Group
    form_class = forms.CreateGroupForm

    def post(self, request, *args, **kwargs):
        form = forms.CreateGroupForm(request.POST, request.FILES)
        if form.is_valid():
            form = form.save(commit=False)
            form.admin = self.request.user
            form.save() 
    
            return redirect(reverse("list-group"))
        else:
            form = forms.CreateGroupForm

class DetailGroup(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    template_name = 'groups/group_detail.html'
    model = models.Group

    def get_context_data(self, **kwargs):

        oldest_members = models.GroupMember.objects.filter(group=self.get_object()).order_by('joined_since')[0:3]

        context = super().get_context_data(**kwargs)
        context['post_form'] = forms.createpostform
        context['oldest_members'] = oldest_members

        return context
    
    def test_func(self):
        if self.request.user not in self.get_object().ban.all():
            return True 
    
    def post(self, request, *args, **kwargs):
        form = forms.createpostform(request.POST, request.FILES)
        if form.is_valid():
            form = form.save(commit=False)
            form.author = self.request.user
            form.group = self.get_object()
            form.save()

            return redirect(reverse("detail-group", kwargs={
                'slug': self.get_object().slug
            }))


class UpdateGroup(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    template_name = 'groups/group_update.html'
    model = models.Group
    form_class = forms.UpdateGroupForm

    def get_form_kwargs(self, **kwargs):
        kwargs = super(UpdateGroup, self).get_form_kwargs(**kwargs)
        kwargs.update({
            "request":self.request,
            "grp":self.get_object(),
        })
        return kwargs

    def test_func(self):
        return self.get_object().admin == self.request.user

class ListGroup(LoginRequiredMixin, ListView):
    template_name = 'groups/group_list.html'
    model = models.Group

class JoinGroup(LoginRequiredMixin, RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        return reverse_lazy("detail-group",kwargs={"slug": self.kwargs.get("slug")})

    def get(self, request, *args, **kwargs):
        group = get_object_or_404(models.Group, slug=self.kwargs.get("slug"))

        try:
            if self.request.user not in group.ban.all():
                models.GroupMember.objects.create(user=self.request.user, group=group)

        except:
            messages.warning(self.request,("Warning, already a member of {}".format(group.name)))

        else:
            if self.request.user in group.ban.all():
                messages.warning(self.request,("Sorry but you have been banned from {}".format(group.name)))
            else:
                messages.success(self.request,"You are now a member of the {} group.".format(group.name))

        return super().get(request, *args, **kwargs)


class LeaveGroup(LoginRequiredMixin, RedirectView):

    def get_redirect_url(self, *args, **kwargs):
        return reverse("detail-group",kwargs={"slug": self.kwargs.get("slug")})

    def get(self, request, *args, **kwargs):
        try:
            membership = models.GroupMember.objects.filter(
                user=self.request.user,
                group__slug=self.kwargs.get("slug")
            ).get()

        except models.GroupMember.DoesNotExist:
            messages.warning(
                self.request,
                "You can't leave this group because you aren't in it."
            )

        else:
            
            if membership.user == membership.group.admin:
                messages.success(
                self.request,
                "You cannot leave the group you are the admin!"
                )
                return super().get(request, *args, **kwargs)
            
            if membership.user in membership.group.moderators.all():
                membership.group.moderators.remove(membership.user)

            membership.delete()
            messages.success(
                self.request,
                "You have left {} group.".format(membership.group.name)
            )
        return super().get(request, *args, **kwargs)


def makemod(request, group, person):
    group = models.Group.objects.get(name=group)
    person = User.objects.get(username=person)
    if request.user == group.admin and person != group.admin:

        group.moderators.add(person)
    
        return redirect(reverse('detail-group', kwargs={
                'slug': group.slug
            }))
    else:
        messages.warning(request, "You cannot perform that action!")

        return redirect(reverse('detail-group', kwargs={'slug': group.slug}))

def deletemember(request, group, person):
    group = models.Group.objects.get(name=group)
    person = User.objects.get(username=person)
    if request.user == group.admin or request.user in group.moderators.all() and person != group.admin:

        if person in group.moderators.all():
            group.moderators.remove(person)


        to_be_deleted = models.GroupMember.objects.get(user=person.pk, group=group)
        to_be_deleted.delete()

        return redirect(reverse('detail-group', kwargs={
                'slug': group.slug
            }))
    else:
        messages.warning(request, "You cannot perform that action!")

        return redirect(reverse('detail-group', kwargs={'slug': group.slug}))

def banmember(request, group, person):
    group = models.Group.objects.get(name=group)
    person = User.objects.get(username=person)
    if request.user == group.admin or request.user in group.moderators.all() and person != group.admin:
        
        group.ban.add(person.pk)
        
        if person in group.moderators.all():
            group.moderators.remove(person)

        to_be_banned = models.GroupMember.objects.get(user=person.pk, group=group)
        to_be_banned.delete()

    
        return redirect(reverse('detail-group', kwargs={
                'slug': group.slug
            }))
    else:
        messages.warning(request, "You cannot perform that action!")

        return redirect(reverse('detail-group', kwargs={'slug': group.slug}))


class GroupSearch(View):
    def get(self, request, *args, **kwargs):
        query = self.request.GET.get('query')
        group_list = models.Group.objects.filter(Q(name__icontains=query))

        context={
            'groups':group_list,

        }

        return render(request, 'groups/group_search.html', context)

class DeleteGroupPost(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    template_name = 'groups/posts/post_delete.html'
    model = models.GroupPost

    def get_success_url(self):

        group = self.get_object().group.slug
        
        return reverse_lazy('detail-group', kwargs={
                'slug': group
            })

    def test_func(self):
        post = self.get_object()
        return self.request.user in post.group.moderators.all() or self.request.user == post.group.admin or self.request.user == post.author  

class EditGroupPost(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    template_name = 'groups/posts/post_edit.html'
    model = models.GroupPost
    fields = ('content',)

    def get_success_url(self):

        group = self.get_object().group.slug
        
        return reverse_lazy('detail-group', kwargs={
                'slug': group
            })

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author  
