from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, authenticate, logout
from worstFilms import urls
from worstFilms.models import Film
from .models import Profile, Relation
from .forms import EditProfileForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse


def signupUser(request):
    if request.method == "GET":
        return render(request, 'auth/signupUser.html', {'form':UserCreationForm})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'] , password=request.POST['password1'])
                user.save()
                login(request, user)
                return HttpResponseRedirect('http://localhost:8000/worstFilms/')

            except IntegrityError:
                return render(request, 'auth/signupUser.html', {'form':UserCreationForm, 'error': 'This username registerd before. please chenge username!'})

        else:
            return render(request, 'auth/signupUser.html', {'form':UserCreationForm , 'error':'Do not match passwords!'})

def loginUser(request):
    if request.method == 'GET':
        return render(request, 'auth/loginUser.html', {'form':AuthenticationForm})
    else:
        user = authenticate(request, username= request.POST['username'], password= request.POST['password'])

        if user is None:
            context= {
                'form':AuthenticationForm, 
                'error':'username or password is wrong. maybe You do not sign up yet!'
            }
            return render(request, 'auth/loginUser.html', context)
        
        else:
            login(request, user)
            return HttpResponseRedirect('http://localhost:8000/worstFilms/')

def logoutUser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('account:loginUser')

@login_required
def dashboard(request, user_id):
    user = get_object_or_404(User, pk=user_id)
    is_relation = False
    relation = Relation.objects.filter(from_user=request.user, to_user=user)
    if relation.exists():
        is_relation= True
    films= Film.objects.filter(author__id= user.id)
    profile = Profile.objects.filter(user__id=user.id)
    return render(request, 'auth/dashboard.html', {'user':user, 'films':films, 'profile':profile, 'is_relation':is_relation})

@login_required
def edit_profile(request , user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance= user.profile)
        if form.is_valid():
            form.save()
            user.email= form.cleaned_data['email']
            user.save()
            messages.success(request, 'Your profile edited successfully!', 'success')
            return redirect('account:dashboard', user_id)
    else:
        form = EditProfileForm(instance= user.profile, initial= {'email':request.user.email})
    return render(request, 'auth/edit_profile.html', {'form':form, 'user':user})

@login_required
def follow(request):
    if request.method == 'POST':
        user_id = request.POST['user_id']
        following = get_object_or_404(User, pk=user_id)
        check_relation = Relation.objects.filter(from_user=request.user, to_user=following)
        if check_relation.exists():
            return JsonResponse({'status':'exists'})
        else:
            Relation(from_user=request.user, to_user=following).save()
            return JsonResponse({'status':'ok'})

@login_required
def unfollow(request):
    if request.method == 'POST':
        user_id = request.POST['user_id']
        following= get_object_or_404(User, pk=user_id)
        check_relation = Relation.objects.filter(from_user=request.user, to_user=following)
        if check_relation.exists():
            check_relation.delete()
            return JsonResponse({'status':'ok'})
        else:
            return JsonResponse({'status':'notexists'})



