from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.shortcuts import redirect, render
from .models import FloorPlan, Furniture, Photo, LinkedFurniture, CurrentFloorPlan

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
    furnitures = []
    floorplan = FloorPlan.objects.get(id=3)
    furns = floorplan.furnitures.all()
    linkedFurniture = LinkedFurniture.objects.filter(floorplan=3)
    for furn in furns:
      furn_type = furn.type[0:2].capitalize()
      furnitures.append({'id': furn.id, 'type': furn_type, 'width': furn.width, 'length':furn.length, 'color':furn.color, 'rotated':linkedFurniture.get(furniture=furn.id).rotated})
    return render(request, 'floorplan/demo.html', {'furnitures': furnitures, 'floorplan': floorplan})


def demo_nav(request):
    furnitures2 = []
    floorplan2 = FloorPlan.objects.get(id=3)
    furns2 = floorplan2.furnitures.all()
    linkedFurniture = LinkedFurniture.objects.filter(floorplan=3)
    for furn in furns2:
      furnitures2.append({'id': furn.id, 'type': furn.type, 'width': furn.width, 'length':furn.length, 'color':furn.color, 'rotated':linkedFurniture.get(furniture=furn.id).rotated})
    return render(request, 'floorplan/demo-nav.html', {'furnitures': furnitures2, 'floorplan': floorplan2})


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

@login_required
def home(request):
    if CurrentFloorPlan.objects.filter(user=request.user) != 0:
      currentFP = CurrentFloorPlan.objects.get(user=request.user).currentfloorplan
    else:
      currentFP = {}
    return render(request, 'home.html', {'currentFP': currentFP})

def floorplan_index(request):
  floorplans = FloorPlan.objects.all()
  return render(request, 'floorplan/floorplan_index.html', {'floorplans': floorplans})

@login_required
def floorplan_details(request, floorplan_id):
  floorplan = FloorPlan.objects.get(id=floorplan_id)
  if len(CurrentFloorPlan.objects.filter(user=request.user)) == 0:
    curr = CurrentFloorPlan(user=request.user, currentfloorplan = floorplan)
    curr.save()
    currentFP = CurrentFloorPlan.objects.get(user=request.user).currentfloorplan
  else:
    curr = CurrentFloorPlan.objects.get(user=request.user)
    curr.currentfloorplan = floorplan
    curr.save()
    currentFP = CurrentFloorPlan.objects.get(user=request.user).currentfloorplan
  furnitures_floorplan_doesnt_have = Furniture.objects.exclude(id__in = floorplan.furnitures.all().values_list('id'))
  return render(request, 'floorplan/floorplan_details.html', {
    "floorplan":floorplan,
    "furnitures": furnitures_floorplan_doesnt_have,
    "currentFP": currentFP,
  })

def assoc_furniture(request, floorplan_id, furniture_id):
  FloorPlan.objects.get(id=floorplan_id).furnitures.add(furniture_id)
  return redirect("floorplan_details", floorplan_id = floorplan_id)
  
def remove_furniture(request, floorplan_id, furniture_id):
  FloorPlan.objects.get(id=floorplan_id).furnitures.remove(furniture_id)
  return redirect("floorplan_details", floorplan_id = floorplan_id)
  
def rotate_furniture(request, floorplan_id, furniture_id):
  linked = LinkedFurniture.objects.filter(floorplan=floorplan_id).get(furniture=furniture_id)
  linked.rotated *= -1
  linked.save()
  return redirect('demo')



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
