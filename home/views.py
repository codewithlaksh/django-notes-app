from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .models import Note

# Create your views here.
def index(request):
    if request.user.is_authenticated:
        user = request.user
        notes = Note.objects.filter(user=user)
    else:
        notes = ''
    return render(request, 'index.html', {'notes': notes})

def handlesignup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        cpassword = request.POST['cpassword']

        if User.objects.filter(username=username).first():
            messages.error(request, "This username already exists");
            return redirect('/')

        if not str(username).isalnum():
            messages.error(request, "Username should contain both alphabets and numbers")
            return redirect('/')

        if str(username).isnumeric():
            messages.error(request, "Username must not contain only numbers")
            return redirect('/')

        if len(username)>12:
            messages.error(request, "Username should be under 12 characters")
            return redirect('/')

        if str(password).isnumeric():
            messages.error(request, "Password should not contain only numbers")
            return redirect('/')

        if len(password)<6:
            messages.error(request, "Password should contain atleast 8 characters")  
            return redirect('/')          
        
        if (password!= cpassword):
            messages.error(request, "Both the password fields should match")
            return redirect('/')

        user = User.objects.create_user(username, email, password)
        user.save()
        messages.success(request, "Your account has been successfully created")
        return redirect('/')
    else:
        return HttpResponse("<h1>Bad Request (400)</h1>")

def handlelogin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "You have been successfully logged in")
            return redirect('/')
        else:
            messages.error(request, "Inavlid Credentials! Please try again")
            return redirect('/')

    else:
        return HttpResponse("<h1>Bad Request (400)</h1>")

def handlelogout(request):
    logout(request)
    messages.success(request, "You have been successfully logged out")
    return redirect('/')

def addnote(request):
    if request.method == 'POST':
        title = request.POST['notetitle']
        description = request.POST['notedesc']
        user = request.user

        if len(title)<6 or len(description)<8:
            messages.error(request, "Please fill the form correctly")
            return redirect('/')
        else:
            note = Note(title=title, description=description, user=user)
            note.save()
            messages.success(request, "Your note has been added successfully")
            return redirect('/')

    else:
        return HttpResponse("<h1>Bad Request (400)</h1>")

def editnote(request, note_id):
    if request.user.is_authenticated:
        user = request.user
        note = Note.objects.filter(id=note_id).first()

        if not user == note.user: # check if the loggedin user matches the note user, else forbid the loggedin user to edit other user's note. This line is very much important.
            messages.error(request, "Editing other user's notes is forbidden")
            return redirect('/')
        else:
            return render(request, 'edit.html', {'note': note})
    else:
        return redirect('/')

def updatenote(request, note_id):
    if request.method == "POST":
        note = Note.objects.filter(id=note_id).first()
        title = request.POST['notetitle']
        description = request.POST['notedesc']

        if len(title)<6 or len(description)<8:
            messages.error(request, "Please fill the form correctly")
            return redirect(f'/edit/note/{note.id}')
        else:
            note.title = title
            note.description = description
            note.save()
            messages.success(request, "Your note has been updated successfully")
            return redirect(f'/edit/note/{note.id}')
    else:
        return HttpResponse("<h1>Bad Request (400)</h1>")

def deletenote(request, note_id):
    if request.user.is_authenticated:
        user = request.user
        note = Note.objects.filter(id=note_id).first()

        if not user == note.user: # check if the loggedin user matches the note user, else forbid the loggedin user to delete other user's note. This line is very much important.
            messages.error(request, "Deleting other user's notes is forbidden")
            return redirect('/')
        else:
            note.delete()
            messages.success(request, "Your note has been deleted successfully")
            return redirect('/')
    else:
        return redirect('/')