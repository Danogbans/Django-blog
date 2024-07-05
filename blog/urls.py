from django.urls import path
from . import views



urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('post/new/', views.post_create, name='post_create'),
    path('post/<slug:slug>/', views.post_detail, name='post_detail'),
    path('post/<slug:slug>/edit/', views.post_edit, name='post_edit'),
    path('tag/<slug:tag_slug>/', views.post_list_by_tag, name='post_list_by_tag'),
    path('post/<slug:slug>/delete/', views.post_confirm_delete, name='post_confirm_delete'),
    path('post/<slug:slug>/like/', views.like_post, name='like_post'),
    path('post/<int:post_id>/share/', views.post_share, name='post_share'),
    path('search/', views.search, name='search'),
]