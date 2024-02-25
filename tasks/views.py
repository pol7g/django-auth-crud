from django.shortcuts import render, redirect, get_object_or_404
# from django.http import HttpResponse
# modulo para crear formularios de autenticacion
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User  # para registrar usuarios
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .forms import TaskForm
from .models import Task
from django.utils import timezone
from django.contrib.auth.decorators import login_required

# Create your views here.

"""def helloworld(request):
    return HttpResponse('Hello world')"""


def signup(request):
    # si quiero pasar la variable a la plantilla creo un dicci desp de nomb de la plantilla
    title = "Hello prueba (lo dejo por ahora)"
    if request.method == "GET":  # nombre del metodo en mayúsculas GET !!!
        print("Enviando formulario desde el servidor al cliente (método GET).")
        return render(request, 'signup.html', {
            'mytitle': title,
            'form': UserCreationForm})   # formulario.

    else:
        if request.POST["password1"] == request.POST["password2"]:
            # register user
            try:
                user = User.objects.create_user(
                    username=request.POST['username'], password=request.POST['password1'])
                user.save()
                # es para que cree sessionid, coloque datos de usuario
                login(request, user)
                # redirecciona al nombre name=... de la ruta, no url.
                return redirect('tasksn')
                # HttpResponse son procesados por django, HTTPResponse por python(?)
                # return HttpResponse("User created successfully")
            except IntegrityError:
                return render(request, 'signup.html', {
                    'mytitle': title,
                    'form': UserCreationForm,
                    "error": 'Username already exist'})
            '''except:
                    return render(request, 'signup.html', {
                    'mytitle': title,
                    'form': UserCreationForm,
                    "error": 'Username already exist'})'''

        return render(request, 'signup.html', {
            'mytitle': title,
            'form': UserCreationForm,
            "error": 'Password do not match'})
        # return HttpResponse("Password do not match")
        '''print(request.POST)
        print("Obteniendo datos, cliente envia datos al servidor")'''


@login_required  # decorador que protege la función que solo se puede acceder logueado
# ver agregar la propiedad LOGIN_URL en settings.py
def tasks(request):
    tareas = "Tareas pendientes, tasks pending"
    tasks = Task.objects.filter(user=request.user, datecompleted__isnull = True)
    return render(request, "tasks.html", {"tasks":tasks, "tareas":tareas})

@login_required
def tasks_completed(request):
    tareas = "Tareas completadas, tasks completed"
    tasks = Task.objects.filter(user=request.user, datecompleted__isnull = False).order_by('-datecompleted')
    return render(request, "tasks.html", {"tasks":tasks, "tareas":tareas})


@login_required
def create_task(request):
    if request.method == 'GET':
        return render(request, 'create_task.html', {
            'form':TaskForm
        })
    else:
        try:
            form = TaskForm(request.POST)
            new_task = form.save(commit=False)
            new_task.user = request.user
            new_task.save()
            return redirect('tasksn')
        except ValueError:
            return render(request, 'create_task.html', {
            'form':TaskForm,
            'error':'Please provide valid data'
        })

@login_required        
def task_detail(request, task_id):
    if request.method == "GET":
        task = get_object_or_404(Task, pk=task_id, user = request.user)
        form = TaskForm(instance=task)
        #print(f"Id de la tarea: {task_id}")
        return render(request, "task_detail.html", {"task":task, "form":form})
    else:
        try:
            task = get_object_or_404(Task, pk=task_id, user = request.user)
            form = TaskForm(request.POST, instance=task)
            form.save()
            return redirect('tasksn')
        except ValueError:
            return render(request, "task_detail.html", {"task":task, "form":form, "error":"Error updating task"})

@login_required        
def complete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user = request.user)
    if request.method == 'POST':
        task.datecompleted =  timezone.now()
        task.save()
        return redirect('tasksn')

@login_required    
def delete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user = request.user)
    if request.method == 'POST':
        task.delete()
        return redirect('tasksn')

                


def home(request):
    return render(request, 'home.html')


def pagina_prueba(request):
    variable = "vista de variable"
    # nombre de página completo, con extención
    return render(request, "cualquiera.html", {"mivariable": variable})

@login_required
def signout(request):  # logout
    logout(request)
    return redirect("home")


def signin(request):
    if request.method == "GET":
        return render(request, 'signin.html', {
            "form": AuthenticationForm
        })
    else:
        user = authenticate(
            request, username=request.POST["username"], password=request.POST["password"])
        if user is None:
            return render(request, 'signin.html', {
            "form": AuthenticationForm,
            "error":'Username or password is wrong'
        })
        else:
            login(request, user)
            return redirect('tasksn')

        