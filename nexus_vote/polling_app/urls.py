from django.urls import path
from polling_app import views

urlpatterns = [
    path("", views.home, name="home view"),
    path("user/<int:id>",views.UserView.as_view(), name="user detail"),
    path("users/",views.UserListViews.as_view(), name="view all users"),
]
