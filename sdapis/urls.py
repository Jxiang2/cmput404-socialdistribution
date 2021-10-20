from django.urls import path
from .views import author_views, follow_view
urlpatterns = [
    # author
    path('api/author/', author_views.register),
    path('api/author/<str:author_id>/', author_views.author_detail),

    # followers of author_id
    path('api/author/<str:author_id>/followers/', follow_view.follower_list),
    # followings of author_id
    path('api/author/<str:author_id>/followings/', follow_view.following_list),
    # author_id2 follows author_id
    path('api/author/<str:author_id>/followers/<str:author_id2>/', follow_view.follower),

]