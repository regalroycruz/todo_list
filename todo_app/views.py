from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from .forms import TodoForm
from .models import Todo
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.contrib.auth.decorators import login_required


# Create your views here.
def home(request):
    return render (request, 'todo_app/home.html')

def sign_up_user(request):
    if request.method == 'GET':
        return render(request, 'todo_app/sign_up_user.html', {'form':UserCreationForm()})
    else:
        # create a new user
        if request.POST['password1'] == request.POST['password2']:
            try:
                user= User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect(current_to_do)
            except IntegrityError:
                return render(request, 'todo_app/sign_up_user.html', {'form':UserCreationForm(), 'error':'username already used'})

        else:
            return render(request, 'todo_app/sign_up_user.html', {'form':UserCreationForm(), 'error':'Password did not match'})

def loginuser(request):
    if request.method == 'GET':
        return render(request, 'todo_app/login_user.html', {'form':AuthenticationForm()})
    else:
        user = authenticate (request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'todo_app/login_user.html', {'error':'User name and password did not match'})
        else:
            login(request, user)
            return redirect(current_to_do)

@login_required
def logoutuser(request):
    if request.method=='POST':
        logout(request)
        return redirect('home') # redirect(home) or redirect('home') can be used

@login_required
def current_to_do(request):
    todos = Todo.objects.filter(user=request.user, datecompleted__isnull=True)
    return render(request, 'todo_app/currenttodos.html', {'todo': todos})

@login_required
def createtodo(request):
    if request.method=='GET':
        return render(request, 'todo_app/createtodo.html', {'form':TodoForm()})
    else: # request is POST
        try:
            form = TodoForm(request.POST)
            newtodo=form.save(commit=False)
            newtodo.user=request.user
            newtodo.save()
            return redirect(current_to_do)
        except ValueError:
            return render(request, 'todo_app/createtodo.html', {'form':TodoForm(), 'error':"bad data"})

@login_required
def view_to_do(request, todo_pk):
    todos = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method == 'GET':
        form=TodoForm(instance=todos)
        return render(request, 'todo_app/viewtodo.html', {'todo': todos, 'form':form})
    else:
        try:
            form = TodoForm(request.POST, instance=todos)
            form.save()
            return redirect(current_to_do)
        except ValueError:
            return render (request, 'todo_app/viewtodo.html', {'todo':todos, 'form':form, 'error':"Bad info"})


@login_required
def complete_to_do(request, todo_pk):
    todos = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method == 'POST':
        todos.datecompleted=timezone.now()
        todos.save()
        return redirect(current_to_do)
@login_required
def delete_to_do(request, todo_pk):
    todos = get_object_or_404(Todo, pk=todo_pk, user=request.user)
    if request.method == 'POST':
        todos.delete()
        return redirect(current_to_do)

@login_required
def show_completed(request):
    todos = Todo.objects.filter(user=request.user, datecompleted__isnull=False).order_by('datecompleted')
    return render(request, 'todo_app/show_completed.html', {'todo': todos})