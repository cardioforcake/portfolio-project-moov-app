from django.urls import path
from django.urls.resolvers import URLPattern
from . import views

urlpatterns = [
    path('accounts/signup/', views.signup, name='signup'),
    path('', views.greeting, name='greeting'),
    path('home/', views.home, name='home'),
]