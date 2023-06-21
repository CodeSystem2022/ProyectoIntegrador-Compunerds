from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from .models import Task


# Create your views here.
class TaskList(ListView):
    model = Task
    context_object_name = "tasks"


# Vista que hereda de la vista Details
class TaskDetail(DetailView):
    model = Task
    context_object_name = "task"
    template_name = "base/task.html"  # Establezco nombre a la planilla

#clase para crear las tareas
class TaskCreate(CreateView):
    model = Task ##establecemos el modelo
    fields='__all__' ## establecemos los campos
    success_url= reverse_lazy("tasks") ##establecemos valor de redireccion