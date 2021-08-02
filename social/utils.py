from . import models 
from django.utils import timezone
from datetime import timedelta

one_week = timezone.now() - timedelta(7)  

def trending_posts():
    posts = models.Post.objects.filter(created_on__range=[one_week, timezone.now()])

    likes_count = 0
    post_count = 0
    for post in posts:
        likes_count += post.likes.count()
        post_count += 1

    try:
        base_likes = int(likes_count / post_count)
    except ZeroDivisionError:
        base_likes = 0

    trending_posts = []
    for post in posts:
        if post.likes.count() >= base_likes:
            trending_posts.append(post)
    
    return trending_posts

