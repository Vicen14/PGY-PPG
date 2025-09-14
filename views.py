from django.shortcuts import render , redirect
from django.contrib.auth import login_required
from django.views import View
from .forms import RegisterFrom, ProfileForm
from .models import User, Profile

def index(request):
    return render(request, 'index.html')
  
class RegisterView(View):
  def get(self, request):
    form = RegisterFrom()
    profile_form = ProfileForm()
    return render(request, 'register.html', {'form': form, 'profile_form': profile_form})
  
  def post(self, request):
    form = RegisterFrom(request.POST)
    profile_form = ProfileForm(request.POST)
    if form.is_valid() and profile_form.is_valid():
      user = form.save()
      profile = profile_form.save(commit=False)
      profile.user = user
      profile.save()
      return redirect('login')
    return render(request, 'register.html', {'form': form, 'profile_form': profile_form})
  
@login_required
def profile(request):
  profile = Profile.objects.get(user=request.user)
  if request.method == 'POST':
    profile_form = ProfileForm(request.POST, instance=profile)
    if profile_form.is_valid():
      profile_form.save()
      return redirect('profile')
  else:
    profile_form = ProfileForm(instance=profile)
  return render(request, 'profile.html', {'profile_form': profile_form}) 