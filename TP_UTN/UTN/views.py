from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.urls import reverse_lazy
from .models import Alumno, Carrera, Curso, Materia, MateriaCurso, Inscripcion, TipoEvaluacion, CondicionFinal, Evaluacion

class InicioView(TemplateView):
    template_name = "inicio.html"
# Views for Alumno
class AlumnoListView(ListView):
    model = Alumno
    template_name = 'alumno/alumno_list.html'

class AlumnoDetailView(DetailView):
    model = Alumno
    template_name = 'alumno/alumno_detail.html'

class AlumnoCreateView(CreateView):
    model = Alumno
    # Usa los campos que realmente quieres que el usuario ingrese
    fields = ['nombre', 'apellido', 'dni', 'email', 'contrasenia', 'anio_universitario', 'carrera']
    template_name = 'alumno/alumno_form.html'
    success_url = reverse_lazy('alumno_list')   

class AlumnoUpdateView(UpdateView):
    model = Alumno
    fields = '__all__'
    template_name = 'alumno/alumno_form.html'
    success_url = reverse_lazy('alumno_list')

class AlumnoDeleteView(DeleteView):
    model = Alumno
    template_name = 'alumno/alumno_confirm_delete.html'
    success_url = reverse_lazy('alumno_list')

# Views for Curso
class CursoListView(ListView):
    model = Curso
    template_name = 'curso/curso_list.html'
    context_object_name = 'cursos'

class CursoDetailView(DetailView):
    model = Curso
    template_name = 'curso/curso_detail.html'

class CursoCreateView(CreateView):
    model = Curso
    fields = '__all__'
    template_name = 'curso/curso_form.html'
    success_url = reverse_lazy('curso_list')

class CursoUpdateView(UpdateView):
    model = Curso
    fields = '__all__'
    template_name = 'curso/curso_form.html'
    success_url = reverse_lazy('curso_list')

class CursoDeleteView(DeleteView):
    model = Curso
    template_name = 'curso/curso_confirm_delete.html'
    success_url = reverse_lazy('curso_list')

# Views for Materia
class MateriaListView(ListView):
    model = Materia
    template_name = 'materia/materia_list.html'
    context_object_name = 'materias'

class MateriaDetailView(DetailView):
    model = Materia
    template_name = 'materia/materia_detail.html'

class MateriaCreateView(CreateView):
    model = Materia
    fields = '__all__'
    template_name = 'materia/materia_form.html'
    success_url = reverse_lazy('materia_list')

class MateriaUpdateView(UpdateView):
    model = Materia
    fields = '__all__'
    template_name = 'materia/materia_form.html'
    success_url = reverse_lazy('materia_list')

class MateriaDeleteView(DeleteView):
    model = Materia
    template_name = 'materia/materia_confirm_delete.html'
    success_url = reverse_lazy('materia_list')

#carreras
class CarreraListView(ListView):
    model = Carrera
    template_name = 'carreras/carrera_list.html'
    context_object_name = 'carreras'
class Ingenieria_civil(TemplateView):
    template_name = "carreras/Ingenieria_civil.html"
class Ingenieria_electronica(TemplateView):
    template_name = "carreras/Ingenieria_electronica.html"
class Ingenieria_energia(TemplateView):
    template_name = "carreras/Ingenieria_energia.html"
class Ingenieria_industrial(TemplateView):
    template_name = "carreras/Ingenieria_industrial.html"
class Ingenieria_mecanica(TemplateView):
    template_name = "carreras/Ingenieria_mecanica.html"
class Ingenieria_metalurgica(TemplateView):
    template_name = "carreras/Ingenieria_metalurgica.html"
class Ingenieria_quimica(TemplateView):
    template_name = "carreras/Ingenieria_quimica.html"
class Ingenieria_sistemas(TemplateView):
    template_name = "carreras/Ingenieria_sistema.html"