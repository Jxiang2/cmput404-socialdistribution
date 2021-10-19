from django.urls import path
from .views import author_views
urlpatterns = [
    # author
    path('api/author/', author_views.register),
    path('api/author/<str:author_id>/', author_views.author_detail),
]   