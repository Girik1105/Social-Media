from django.conf import settings
from django.conf.urls.static import static

from django.urls import path

from . import views

urlpatterns = [
    path('posts/all/', views.PostListView.as_view(), name='post_list'),
    path('posts/<pk>/', views.PostDetailView.as_view(), name='post_detail'),
    path('posts/<pk>/edit/', views.PostEditView.as_view(), name='post_edit'),
    path('posts/<pk>/Delete/', views.PostDeleteView.as_view(), name='post_delete'),
    path('posts/share/<pk>/', views.SharedPostView.as_view(), name='share_post'),
    path('posts/shared//delete/<pk>/', views.SharedPostDeleteView.as_view(), name='share_post_delete'),

    path('post/<pk>/like/', views.AddLike.as_view(), name='Add-Like'),
    path('post/<pk>/likes/', views.LikeListView.as_view(), name='people-liked'),

    path('post/<pk>/comment/<id>/like/', views.AddCommentLike.as_view(), name='comment-like'),
    path('post/<pk>/comment/<id>/reply/', views.commentReplyView.as_view(), name="comment-reply"),

    path('posts/<pk>/comment/delete/', views.CommentDelete.as_view(), name='comment_delete'),

    path('profile/<pk>/', views.ProfileView.as_view(), name='profile_view'),
    path('profile/<pk>/edit/', views.ProfileEditView.as_view(), name='profile_edit'),

    path('profile/<pk>/followers/all', views.AllFollowers.as_view(), name='AllFollowers'),
    path('profile/<pk>/follower/new', views.AddFollower.as_view(), name='Add-Follower'),
    path('profile/<pk>/follower/remove', views.RemoveFollower.as_view(), name='Remove-Follower'),

    path('search/', views.UserSearch.as_view(), name='search'),

    path('remove/notification/<notif_pk>/', views.RemoveNotification.as_view(), name='remove-notification'),

    path('explore/', views.explore.as_view(), name='explore'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
