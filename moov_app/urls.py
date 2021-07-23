from django.urls import path
from django.urls.resolvers import URLPattern
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


urlpatterns = [
    path('accounts/signup/', views.signup, name='signup'),
    path('', views.greeting, name='greeting'),
    path('home/', views.home, name='home'),
    path('floorplans/', views.floorplan_index, name='floorplan_index'),
    path("floorplans/<int:floorplans_id>/", views.floorplan_detail, name="floorplan_detail"),
    path('furniture/create/', views.FurnitureCreate.as_view(), name="add_furniture"),
    path('floorplandemo/', views.floorplan_demo, name='demo'),
]   

urlpatterns += staticfiles_urlpatterns()