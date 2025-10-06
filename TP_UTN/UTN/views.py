from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.urls import reverse_lazy
from .models import Alumno, Curso, Materia, MateriaCurso, AlumnoCurso, Inscripcion, TipoEvaluacion, CondicionFinal, Evaluacion
from django.contrib.auth import logout
from django.shortcuts import redirect

def logout_view(request):
    logout(request)
    return redirect('/')

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
    fields = '__all__'
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
