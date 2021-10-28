from django.urls import path
from rest_framework.documentation import include_docs_urls
from .views import author_views, follow_views, post_views, inbox_view

urlpatterns = [
    # author
    path('docs/', include_docs_urls(title='Social Distribution Api')),
    path('api/author/', author_views.author_list),
    path('api/author/<str:author_id>/', author_views.author_detail),

    #register/login/out
    path('api/login/', author_views.login_view),
    path('api/register/', author_views.register),

    # followers of author_id
    path('api/author/<str:author_id>/followers/', follow_views.follower_list),
    # followings of author_id
    path('api/author/<str:author_id>/followings/', follow_views.following_list),
    # author_id2 follows author_id
    path('api/author/<str:author_id>/followers/<str:author_id2>/', follow_views.follower),

    # post/ post-detail
    path('api/posts/', post_views.all_post_view),
    path('api/author/<str:author_id>/posts/', post_views.post_view),
    path('api/author/<str:author_id>/posts/<str:post_id>/', post_views.post_detail_view),

    # inbox
    path('api/author/<str:author_id>/inbox/', inbox_view.inbox_detail),
    # friends
    path('api/author/<str:author_id>/friends/', inbox_view.friend),



]