from django.urls import path
from .views import author_views, follow_view
urlpatterns = [
    # author
    path('api/author/', author_views.register),
    path('api/author/<str:author_id>/', author_views.author_detail),
    # follower & following
    path('api/author/<str:author_id>/followers/', follow_view.follower_list),
    path('api/author/<str:author_id>/followers/<str:author_id2>/', follow_view.follower),
    
    path('api/author/<str:author_id>/followings/', follow_view.following_list),
    path('api/author/<str:author_id>/unfollow/<str:author_id2>/', follow_view.unfollow),

]