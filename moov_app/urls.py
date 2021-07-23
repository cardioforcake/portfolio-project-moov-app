from django.urls import path
from django.urls.resolvers import URLPattern
from . import views

urlpatterns = [
    path('accounts/signup/', views.signup, name='signup'),
    path('', views.greeting, name='greeting'),
    path('home/', views.home, name='home'),
    path('floorplans/', views.floorplan_index, name='floorplan_index'),
    path("floorplans/<int:floorplans_id>/", views.floorplan_detail, name="floorplan_detail"),

    path("floorplans/create", views.FloorplanCreate.as_view(), name="floorplans_create"),
    path('floorplans/<int:floorplans_id>', views.floorplans_detail, name="floorplans_detail"),
    path('floorplans/<int:pk>/update', views.FloorPlanUpdate.as_view(), name="floorplans_update"),
    path('floorplans/<int:pk>/delete', views.FloorplanDelete.as_view(), name="floorplans_delete"),


    path('furniture/create/', views.FurnitureCreate.as_view(), name="add_furniture"),
    path('floorplandemo/', views.floorplan_demo, name='demo'),

    path('floorplans/<int:floorplans_id>/add_photo/', views.add_photo, name='add_photo'),

]   