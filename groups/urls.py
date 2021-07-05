from django.urls import path

from . import views

urlpatterns = [
    path('create/', views.CreateGroup.as_view(), name='create-group'),
    path('', views.ListGroup.as_view(), name='list-group'),
    path('<slug>/', views.DetailGroup.as_view(), name='detail-group'),
    path('update/<slug>/', views.UpdateGroup.as_view(), name='update-group'),

    path("join/<slug>/",views.JoinGroup.as_view(),name="join"),
    path("leave/<slug>/",views.LeaveGroup.as_view(),name="leave"),

    path('search/all/', views.GroupSearch.as_view(), name='group-search'),

    path('remove/<group>/<person>/', views.deletemember, name='remove-member'),
    path('ban/<group>/<person>/', views.banmember, name='ban-member'),
    path('add/mod/<group>/<person>/', views.makemod, name='make-mod-member'),

    path('post/delete/<pk>/', views.DeleteGroupPost.as_view(), name='delete-group-post'),
    path('post/edit/<pk>/', views.EditGroupPost.as_view(), name='edit-group-post'),
]