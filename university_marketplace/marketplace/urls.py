from tkinter.font import names

from django.urls import path
from . import views
from .views import LearnMoreView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),  # Homepage URL
    path('about/', views.about, name='about'),  # About page
    path('contact/', views.contact, name='contact'),  # Contact page
    path('signup/', views.signup, name='signup'),  # Signup page
    path('login/', views.login_view, name='login'),  # Login page
    path('logout/', views.logout_view, name='logout'),

    # Separate URLs for item list and item detail
    path('items/', views.item_list, name='item_list'),  # URL to view all items
    path('items/edit/<int:item_id>/', views.edit_item, name='edit_item'),  # URL for editing
    path('items/delete/<int:item_id>/', views.delete_item, name='delete_item'),
    path('items/<int:item_id>/', views.item_detail, name='item_detail'),  # URL to view specific item details
    path('items/submit/', views.submit_item, name='submit_item'),  # URL for submitting a new item
    path('item/<int:item_id>/contact/', views.contact_owner, name='contact_owner'),  # Contact item owner
    path('community-chat/', views.community_chat, name='community_chat'),
    path('learn-more/', LearnMoreView.as_view(), name='learn_more'),
    path('profile/', views.profile_view, name='profile'),
]
