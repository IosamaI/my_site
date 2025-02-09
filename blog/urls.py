from django.urls import path
from django.contrib.auth import views as auth_views  # Import auth views for login and logout
from . import views

urlpatterns = [
    path("", views.starting_page, name='starting-page'),
    path("posts/", views.posts, name='posts-page'),
    path("posts/<slug:slug>/", views.post_detail, name="post-detail-page"),
     path("register/", views.register, name="register"),  # New registration URL
    path("login/", auth_views.LoginView.as_view(template_name='blog/login.html'), name='login'),  # Login path
    path("logout/", views.logout_view, name='logout'),  # Logout path
]
