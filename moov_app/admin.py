from django.contrib import admin

# Register your models here.


# admin.site.register(Photo)
from .models import FloorPlan, Furniture, Photo

admin.site.register(FloorPlan)
admin.site.register(Furniture)
admin.site.register(Photo)