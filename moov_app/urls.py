from django.urls import path
from django.urls.resolvers import URLPattern
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns


urlpatterns = [
    path('accounts/signup/', views.signup, name='signup'),
    path('', views.greeting, name='greeting'),
    path('home/', views.home, name='home'),
    path('floorplans/', views.floorplan_index, name='floorplan_index'),

    path("floorplans/create", views.FloorplanCreate.as_view(), name="floorplan_create"),
    path('floorplans/<int:floorplan_id>', views.floorplan_details, name="floorplan_details"),
    path('floorplans/<int:pk>/update', views.FloorPlanUpdate.as_view(), name="floorplan_update"),
    path('floorplans/<int:pk>/delete', views.FloorplanDelete.as_view(), name="floorplan_delete"),
    path('floorplans/<int:floorplan_id>/assoc_furniture/<int:furniture_id>/', views.assoc_furniture, name='assoc_furniture'),
    path('floorplans/<int:floorplan_id>/remove_furniture/<int:furniture_id>/', views.remove_furniture, name='remove_furniture'),


    path('furniture/create/', views.FurnitureCreate.as_view(), name="furniture_create"),
    path('furniture/<int:pk>/update/', views.FurnitureUpdate.as_view(), name='furniture_update'),
    path('furniture/<int:pk>/delete/', views.FurnitureDelete.as_view(), name='furniture_delete'),
    path('floorplandemo/', views.floorplan_demo, name='demo'),

    path('floorplans/<int:floorplan_id>/add_photo/', views.add_photo, name='add_photo'),

]   
