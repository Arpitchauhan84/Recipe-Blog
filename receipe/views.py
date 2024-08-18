from django.shortcuts import render, redirect
from .models import Receipe 
from django.contrib.auth.models import *
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
 # Import the Receipe model

@login_required(login_url='/login/')
def receipe(request):
    if request.method == "POST":
        # Get data from POST request
        receipe_name = request.POST.get('Receipe_name')
        Receipe_discription = request.POST.get('Receipe_discription')
        receipe_images = request.FILES.get('Receipe_images')

        # Create a new Receipe instance
        Receipe.objects.create(
            Receipe_name=receipe_name,
            Receipe_discription=Receipe_discription,
            Receipe_images=receipe_images
        )

        # Redirect to the recipe list or another appropriate page
        return redirect('/receipe/')

    # If the request method is GET or after POST redirection
    query_set = Receipe.objects.all()  # Fetch all recipes
    context = {'context': query_set}
    return render(request, 'receipe.html', context)

@login_required(login_url='/login/')
def update_receipe(request,id):
    query_set = Receipe.objects.get(id = id)
    if request.method == "POST":
        # Get data from POST request
        receipe_name = request.POST.get('Receipe_name')
        Receipe_discription = request.POST.get('Receipe_discription')
        receipe_images = request.FILES.get('Receipe_images')

        query_set.receipe_name = receipe_name
        query_set.Receipe_discription = Receipe_discription

        if receipe_images:
            query_set.receipe_images
            query_set.save()
            return redirect('/receipe/')

    context = {'context': query_set}   
    return render(request, 'update_receipe.html',context)

def delete_receipe(request,id):
    query_set = Receipe.objects.get(id = id)
    query_set.delete()
    return redirect('/receipe/')



def login_page(request):
    if request.method != "POST":
        return render(request, 'login.html')
    username = request.POST.get('username')
    password = request.POST.get('password')

    if not User.objects.filter(username = username).exists():
        messages.error(request ,'Invalid Username')
        return redirect('/login/')

    user = authenticate(username=username, password=password)

    if user is None:
        messages.error(request, 'Invalid username or password')
        return redirect('/login/')

    else:
        login(request,user)
        return redirect('/receipe/')


def logout_page(request):
    logout(request)
    return redirect('/login/')


def register(request):
    if request.method == "POST":

        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = User.objects.filter(username = username)
        if user.exists():
            messages.info(request,'username already register')
            return redirect('/register/')

        user = User.objects.create(
           first_name = first_name,
           last_name = last_name,
           username = username,
        )

        user.set_password(password)
        user.save()
        messages.info(request,'Account create successfully')
    return render(request, 'register.html')
