from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
import time
from ControlUsuarios.forms import *
from ControlUsuarios.models import UserProfile
# Create your views here.
from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import redirect

from django import forms
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect

@csrf_exempt
def index(request):
        return render(request, 'registration/login.html',{})
@csrf_exempt
def sesion(request):
    return HttpResponse("Rango says hey there world!")

######################### REGISTRO DE USUARIOS ############################################

@csrf_exempt
def androidLogin(request):
    if request.method=='POST':

        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(username=username, password=password)

        if user:
            # Is the account active? It could have been disabled.
            if user.is_active:
                u=User.objects.get(username=user.username)
                user_profile = UserProfile.objects.get(user=user)
                login(request, user)
                #data="nombre_usuario :"+username
                return HttpResponse(user_profile.__dni__())
            else:
                return HttpResponse("Your  account is disabled.")
        else:
            print "Invalid login details: {0}, {1}".format(username, password)
            return HttpResponse("Invalid login details supplied.")
    else:
        print "entrando por get"
    return HttpResponse()


@csrf_exempt
def androidRegister(request):
    if request.method=='POST':

        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        if user_form.is_valid():
            if profile_form.is_valid():
                user = user_form.save()
                user.set_password(user.password)
                user.save()

                profile = profile_form.save(commit=False)
                profile.user = user
                profile.save()
                return HttpResponse("success")
            else:
                return HttpResponse("Invalid User or Dni")
        else:
            return HttpResponse("Username exist or Invalid Email")
    else:
        print "entrando por get"
    return HttpResponse()


def register(request):

    # A boolean value for telling the template whether the registration was successful.
    # Set to False initially. Code changes value to True when registration succeeds.
    registered = False

    # If it's a HTTP POST, we're interested in processing form data.
    if request.method == 'POST':
        # Attempt to grab information from the raw form information.
        # Note that we make use of both UserForm and UserProfileForm.
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        # If the two forms are valid...
        if user_form.is_valid() and profile_form.is_valid():
            # Save the user's form data to the database.
            user = user_form.save()

            # Now we hash the password with the set_password method.
            # Once hashed, we can update the user object.
            user.set_password(user.password)
            user.save()

            # Now sort out the UserProfile instance.
            # Since we need to set the user attribute ourselves, we set commit=False.
            # This delays saving the model until we're ready to avoid integrity problems.
            profile = profile_form.save(commit=False)
            profile.user = user

            # Now we save the UserProfile model instance.
            profile.save()

            # Update our variable to tell the template registration was successful.
            registered = True
        #else:

            #return HttpResponseRedirect('/')
        # Invalid form or forms - mistakes or something else?
        # Print problems to the terminal.
        # They'll also be shown to the user.
        else:
            print user_form.errors, profile_form.errors

            #return redirect('registration/register.html',{'user_form': user_form, 'profile_form': profile_form, 'registered': registered} )

            #print user_form.errors, profile_form.errors

    # Not a HTTP POST, so we render our form using two ModelForm instances.
    # These forms will be blank, ready for user input.
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    # Render the template depending on the context.
    return render(request, 'registration/register.html',{'user_form': user_form, 'profile_form': profile_form, 'registered': registered} )

@csrf_exempt
def user_login(request):

    # If the request is a HTTP POST, try to pull out the relevant information.
    if request.method == 'POST':
        # Gather the username and password provided by the user.
        # This information is obtained from the login form.
                # We use request.POST.get('<variable>') as opposed to request.POST['<variable>'],
                # because the request.POST.get('<variable>') returns None, if the value does not exist,
                # while the request.POST['<variable>'] will raise key error exception
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Use Django's machinery to attempt to see if the username/password
        # combination is valid - a User object is returned if it is.
        user = authenticate(username=username, password=password)

        # If we have a User object, the details are correct.
        # If None (Python's way of representing the absence of a value), no user
        # with matching credentials was found.
        if user:
            # Is the account active? It could have been disabled.
            if user.is_active:
                u=User.objects.get(username=user.username)
                request.session['username'] = u.username
                user_profile = UserProfile.objects.get(user=user)
                #print user_profile.__organizacion__()
                request.session['dni'] = user_profile.__dni__()
                login(request, user)
                return HttpResponseRedirect('/sesion/')
            else:
                # An inactive account was used - no logging in!
                return HttpResponse("Your account is disabled.")
        else:
            # Bad login details were provided. So we can't log the user in.
            print "Invalid login details: {0}, {1}".format(username, password)
            return HttpResponse("Invalid login details supplied.")

    # The request is not a HTTP POST, so display the login form.
    # This scenario would most likely be a HTTP GET.
    else:
        # No context variables to pass to the template system, hence the
        # blank dictionary object...
        return render(request, 'registration/login.html', {})


@login_required
def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    del request.session['username']
    del request.session['dni']
    logout(request)

    # Take the user back to the homepage.
    return HttpResponseRedirect('/')
