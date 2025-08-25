from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Alumno, Curso, Materia, MateriaCurso, AlumnoCurso, Inscripcion, TipoEvaluacion, Reporte, CondicionFinal, Evaluacion

# Views for Alumno
class AlumnoListView(ListView):
    model = Alumno
    template_name = 'alumno_list.html'

class AlumnoDetailView(DetailView):
    model = Alumno
    template_name = 'alumno_detail.html'

class AlumnoCreateView(CreateView):
    model = Alumno
    fields = '__all__'
    template_name = 'alumno_form.html'
    success_url = reverse_lazy('alumno_list')

class AlumnoUpdateView(UpdateView):
    model = Alumno
    fields = '__all__'
    template_name = 'alumno_form.html'
    success_url = reverse_lazy('alumno_list')

class AlumnoDeleteView(DeleteView):
    model = Alumno
    template_name = 'alumno_confirm_delete.html'
    success_url = reverse_lazy('alumno_list')

class CursoListView(ListView):
    model = Curso
    template_name = 'curso_list.html'

class CursoDetailView(DetailView):
    model = Curso
    template_name = 'curso_detail.html'

class CursoCreateView(CreateView):
    model = Curso
    fields = '__all__'
    template_name = 'curso_form.html'
    success_url = reverse_lazy('curso_list')

class CursoUpdateView(UpdateView):
    model = Curso
    fields = '__all__'
    template_name = 'curso_form.html'
    success_url = reverse_lazy('curso_list')

class CursoDeleteView(DeleteView):
    model = Curso
    template_name = 'curso_confirm_delete.html'
    success_url = reverse_lazy('curso_list')

# Repeat for Materia, MateriaCurso, AlumnoCurso, Inscripcion, TipoEvaluacion, Reporte, CondicionFinal, Evaluacion