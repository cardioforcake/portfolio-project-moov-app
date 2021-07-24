from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.shortcuts import redirect, render
from .models import FloorPlan, Furniture, Photo

# from django.http import HttpResponse
# from .models import Deck, Card 
# from .forms import FeedingForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

from django.template.defaulttags import register
import boto3
import uuid

S3_BASE_URL = 'https://s3-us-east-2.amazonaws.com/'
BUCKET = 'final-project-team'



@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)

@register.filter
def scale_furniture(furnitureLength, floorplanLength):
  return f'{furnitureLength/floorplanLength*100}%'

def floorplan_demo(request):
    widths = {}
    lengths = {}
    furnitures = Furniture.objects.all()
    for furn in furnitures:
        widths[furn.id] = furn.width
        lengths[furn.id] = furn.length
    return render(request, 'floorplan/demo.html', {'furnitures': furnitures, 'widths': widths, 'lengths': lengths})

def signup(request):
  error_message = ''
  if request.method == 'POST':
    form = UserCreationForm(request.POST)
    if form.is_valid():
      user = form.save()
      login(request, user)
      return redirect('home')
    else:
      error_message = "Invalid sign up - Try again"
  form = UserCreationForm()
  return render(request, 'registration/signup.html', {'form': form, 'error_message' : error_message})

class FurnitureCreate(LoginRequiredMixin, CreateView):
    model = Furniture
    fields = ['type','length','width','color']
    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class FurnitureUpdate(LoginRequiredMixin, UpdateView):
    model = Furniture
    fields = ['type','length','width','color']

class FurnitureDelete(LoginRequiredMixin, DeleteView):
    model = Furniture
    success_url = '/floorplandemo/'






def greeting(request):
    return render(request, 'greeting.html')

def home(request):
    return render(request, 'home.html')

def floorplan_index(request):
  floorplans = FloorPlan.objects.all()
  return render(request, 'floorplan/floorplan_index.html', {'floorplans': floorplans})

def floorplan_details(request, floorplan_id):
  floorplan = FloorPlan.objects.get(id=floorplan_id)
  return render(request, 'floorplan/floorplan_details.html', {
    "floorplan":floorplan,
  })







class FloorplanCreate(LoginRequiredMixin,CreateView):
    model = FloorPlan
    fields = ['name','length', 'width', 'comment']

    def form_valid(self, form):
      form.instance.user = self.request.user
      return super().form_valid(form)


  
class FloorPlanUpdate(LoginRequiredMixin,UpdateView):
    model = FloorPlan
    fields = ['length', 'width', 'comment']
    # success_url = '/floorplans/floorplan_detail'



class FloorplanDelete(LoginRequiredMixin,DeleteView):
    model = FloorPlan
    success_url = '/floorplans/'

  
  



def add_photo(request, floorplan_id):
  photo_file = request.FILES.get('photo-file', None)
  if photo_file:
    s3 = boto3.client('s3')
    key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]

    try:
      s3.upload_fileobj(photo_file, BUCKET, key)
      url = f"{S3_BASE_URL}{BUCKET}/{key}"
      photo = Photo(url= url, floorplan_id= floorplan_id)
      photo.save()

    except Exception as e:
      print('an error occurred uploading files to S3')
      print(e)
    return redirect('floorplan_details', floorplan_id = floorplan_id)
