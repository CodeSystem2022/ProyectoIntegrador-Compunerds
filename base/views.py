from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy

from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

from .models import Task


# Create your views here.
class CustomLoginView(LoginView):
    template_name = "base/login.html" ## Especifica la plantilla que va a utilizar
    fields = "__all__" ## __all__ muestra todos los campos del formularios. En otro caso, se proporciona una lista
    redirect_authenticated_user = True ## Evita que usuarios autenticados vuelvan a la pág inicio de sesión

    def get_success_url(self): ## Este método se utiliza para obtener la URL de éxito luego de un inicio de sesión exitoso
        return reverse_lazy("tasks")


class RegisterPage(FormView):
    template_name = "base/register.html"
    form_class = UserCreationForm ## Este es un formulario predefinido de Django para el registro de usuarios
    redirect_authenticated_user = True
    success_url = reverse_lazy("tasks")

    def form_valid(self, form): ## Aquí se guarda el usuario registrado y se realiza el inicio de sesión automático
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(RegisterPage, self).form_valid(form)

    def get(self, *args, **kwargs): ## Esto evita que los usuarios autenticados accedan a la página de registro
        if self.request.user.is_authenticated:
            return redirect("tasks")
        return super(RegisterPage, self).get(*args, **kwargs)


class TaskList(LoginRequiredMixin, ListView): 
    model = Task
    context_object_name = "tasks"

    def get_context_data(self, **kwargs): ## Modifica el contexto para filtrar, cuenta las tareas incompletas y realiza una búsqueda si se solicita
        context = super().get_context_data(**kwargs)  
        context["tasks"] = context["tasks"].filter(user=self.request.user)
        context["count"] = context["tasks"].filter(complete=False).count()

        search_input = self.request.GET.get("search-area") or ""
        if search_input:
            context["tasks"] = context["tasks"].filter(title__startswith=search_input)

        context["search_input"] = search_input

        return context


# Vista que hereda de la vista Details
class TaskDetail(LoginRequiredMixin, DetailView):
    model = Task
    context_object_name = "task"
    template_name = "base/task.html"  # Establezco nombre a la planilla


# clase para crear las tareas
class TaskCreate(LoginRequiredMixin, CreateView):
    model = Task  ##establecemos el modelo
    fields = ["title", "description", "complete"]  ## establecemos los campos
    success_url = reverse_lazy("tasks")  ##establecemos valor de redireccion

    def form_valid(self, form): ## Esto asegura que la tarea creada esté asociada al usuario que la creó
        form.instance.user = self.request.user
        return super(TaskCreate, self).form_valid(form)


##clase para editar la tarea creada
class TaskUpdate(UpdateView):
    model = Task
    fields = "__all__"
    success_url = reverse_lazy("tasks")


##clase para eliminar una tarea
class DeleteView(DeleteView):
    model = Task
    context_object_name = "task"
    success_url = reverse_lazy("tasks")
