from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.shortcuts import redirect, render
from .models import FloorPlan, Furniture

# from django.http import HttpResponse
# from .models import Deck, Card 
# from .forms import FeedingForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

def floorplan_demo(request):
    furnitures = Furniture.objects.all()
    return render(request, 'floorplan/demo.html', {'furnitures': furnitures})

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
    success_url = '/home/'

def greeting(request):
    return render(request, 'greeting.html')

def home(request):
    return render(request, 'home.html')

def floorplan_index(request):
  floorplans = FloorPlan.objects.all()
  return render(request, 'floorplan/floorplan_index.html', {'floorplans': floorplans})

def floorplan_detail(request, floorplan_id):
  floorplan = FloorPlan.objects.get(id=floorplan_id)
  return render(request, 'floorplan/floorplan_detail.html', {
    "floorplan":floorplan,
  })