from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView, View
from django.urls import reverse_lazy
from .models import Alumno, AlumnoMateriaCurso, Carrera, Curso, Materia, MateriaCurso, Inscripcion, TipoEvaluacion, CondicionFinal, Evaluacion, CarreraMateria
from django.db.models import Q

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

    def get_queryset(self):
        # 1. Obtener el queryset base (todas las carreras)
        queryset = super().get_queryset()
        
        # 2. Obtener el parámetro de búsqueda 'q' de la URL
        query = self.request.GET.get('q')

        if query:
            # 3. Filtrar el queryset si hay un término de búsqueda
            # Usamos Q objects para construir una consulta más compleja si es necesario (ej: buscar en nombre O ID)
            # 'nombre__icontains=query' busca la cadena en el campo 'nombre'
            queryset = queryset.filter(
                Q(nombre__icontains=query) 
                # Opcional: Si quieres buscar también por ID:
                # | Q(id_carrera__icontains=query) 
            )
        
        # 4. Devolver el queryset (filtrado o completo)
        return queryset

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

class MateriaReinscripcionView(TemplateView):
    template_name = "materia/reinscripcion_materia.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        alumno_id = self.kwargs.get('alumno_id')

        # Buscar el alumno
        alumno = Alumno.objects.get(id_alumno=alumno_id)

        # Buscar las materias asociadas a la carrera del alumno
        # y que correspondan a su año o anterior
        materias_relacionadas = CarreraMateria.objects.filter(
            carrera=alumno.carrera,
            materia__ciclo_lectivo__lte=alumno.anio_universitario
        ).select_related('materia')

        # Extraer las materias de esa relación
        materias = [cm.materia for cm in materias_relacionadas]

        context['alumno'] = alumno
        context['materias'] = materias

        cursos_disponibles = MateriaCurso.objects.filter(materia__in=materias)
        context['cursos_disponibles'] = cursos_disponibles
        return context

def reinscribir_materia(request, alumno_id, materia_id):
    alumno = get_object_or_404(Alumno, id_alumno_id=alumno_id)
    materia = get_object_or_404(Materia, id_materia=materia_id)

    # Verificar si ya está reinscripto
    ya_existe = AlumnoMateriaCurso.objects.filter(
        alumno=alumno,
        materia_curso__materia=materia
    ).exists()

    if ya_existe:
        messages.warning(request, "Ya estás reinscripto en esta materia.")
        return redirect('materia_reinscripcion', alumno_id=alumno_id)

    curso_id = request.POST.get('curso_id')  # Viene desde el botón elegido
    materia_curso = get_object_or_404(MateriaCurso, id_materia_curso=curso_id)

    AlumnoMateriaCurso.objects.create(
        alumno=alumno,
        materia_curso=materia_curso
    )

    messages.success(request, f"Te reinscribiste a {materia.nombre} correctamente.")
    return redirect('materia_reinscripcion', alumno_id=alumno_id)

def cancelar_reinscripcion(request, alumno_id, materia_id):
    alumno = get_object_or_404(Alumno, id_alumno_id=alumno_id)
    materia = get_object_or_404(Materia, id_materia=materia_id)

    inscripcion = AlumnoMateriaCurso.objects.filter(
        alumno=alumno,
        materia_curso__materia=materia
    ).first()

    if inscripcion:
        inscripcion.delete()
        messages.success(request, f"Se canceló la reinscripción a {materia.nombre}.")
    else:
        messages.warning(request, "No estabas reinscripto en esta materia.")

    return redirect('materia_reinscripcion', alumno_id=alumno_id)

#carreras
CARRERA_URL_MAP = {
    "Ingeniería Civil": "Ingenieria_civil",
    "Ingeniería Electrónica": "Ingenieria_electronica",
    "Ingeniería en Energía Eléctrica": "Ingenieria_energia",
    "Ingeniería Industrial": "Ingenieria_industrial",
    "Ingeniería Mecánica": "Ingenieria_mecanica",
    "Ingeniería Metalúrgica": "Ingenieria_metalurgica",
    "Ingeniería Química": "Ingenieria_quimica",
    # Asegúrate de que el nombre aquí coincida con el nombre en tu URL
    "Ingeniería en Sistemas de Información": "ingenieria_sistemas", 
}

class CarreraListView(ListView):
    model = Carrera
    template_name = 'carreras/carrera_list.html'
    context_object_name = 'carreras'

    def get_queryset(self):
        # 1. Obtener el queryset base (todas las carreras)
        queryset = super().get_queryset()
        
        # 2. Obtener el parámetro de búsqueda 'q' de la URL
        query = self.request.GET.get('q')

        if query:
            # 3. Filtrar el queryset si hay un término de búsqueda
            # Usamos Q objects para construir una consulta más compleja si es necesario (ej: buscar en nombre O ID)
            # 'nombre__icontains=query' busca la cadena en el campo 'nombre'
            queryset = queryset.filter(
                Q(nombre__icontains=query) 
                # Opcional: Si quieres buscar también por ID:
                # | Q(id_carrera__icontains=query) 
            )
        
        # 4. Devolver el queryset (filtrado o completo)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Iterar sobre la lista de carreras y añadir la propiedad 'url_name'
        for carrera in context['carreras']:
            nombre = carrera.nombre
            # Añade una nueva propiedad al objeto carrera
            # Usa .get() para evitar errores si una carrera no está en el mapa
            carrera.url_name = CARRERA_URL_MAP.get(nombre, 'carrera_list') # 'carrera_list' como URL de fallback
            
        return context

# El resto de tus clases TemplateView quedan igual (Ingenieria_civil, etc.)
# ...
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