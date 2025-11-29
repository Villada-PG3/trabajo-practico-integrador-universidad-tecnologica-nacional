from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView, View, View
from django.urls import reverse_lazy
from .models import Alumno, AlumnoMateriaCurso, Carrera, Curso, Materia, MateriaCurso, Inscripcion, TipoEvaluacion, CondicionFinal, Evaluacion, CarreraMateria
from django.db.models import Q
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError

def logout_view(request):
    logout(request)
    return redirect('/')

@method_decorator(login_required, name='dispatch')
class PostLoginCheckView(View):
    """Redirects user to alumno_form if incomplete, or inicio if complete."""

    def get(self, request, *args, **kwargs):
        alumno = getattr(request.user, 'alumno', None)

        if alumno and alumno.dni != None and alumno.anio_universitario and alumno.carrera != None:
            return redirect('inicio')  # already complete → home
        else:
            return redirect('alumno_create')  # needs to finish form
class InicioView(TemplateView):
    template_name = "inicio.html"
# Views for Alumno

class AlumnoDetailView(DetailView):
    model = Alumno
    template_name = 'alumno/alumno_detail.html'

class AlumnoCreateView(CreateView):
    model = Alumno
    fields = ['dni', 'anio_universitario', 'carrera']
    template_name = 'alumno/alumno_form.html'
    success_url = reverse_lazy('inicio')   

    def get_alumno_instance(self):
        """
        Return the Alumno instance for the current user if it exists,
        otherwise return None.
        """
        try:
            return getattr(self.request.user, 'alumno', None)
        except Exception:
            return None
        
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        instance = self.get_alumno_instance()
        if instance is not None:
            kwargs['instance'] = instance
        return kwargs

    def form_valid(self, form):
        obj = form.save(commit=False)

        # make sure the Alumno is linked to the logged-in user
        if obj.user is None:
            obj.user = self.request.user
        obj.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        # helpful debug output while you're testing
        print("=== FORM INVALID ===")
        print("POST:", self.request.POST)
        print("Errors:", form.errors.as_json())
        return super().form_invalid(form)

class AlumnoUpdateView(UpdateView):
    model = Alumno
    fields = '__all__'
    template_name = 'alumno/alumno_form.html'
    success_url = reverse_lazy('inicio')

class AlumnoDeleteView(DeleteView):
    model = Alumno
    template_name = 'alumno/alumno_confirm_delete.html'
    success_url = reverse_lazy('inicio')

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

class MateriaReinscripcionView(TemplateView):
    template_name = "materia/reinscripcion_materia.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        alumno_id = self.kwargs.get('alumno_id')

        # Buscar el alumno
        alumno = Alumno.objects.get(id_alumno=alumno_id)

        # 1. Búsqueda de materias según la carrera y año del alumno (CORRECTO)
        materias_relacionadas = CarreraMateria.objects.filter(
            carrera=alumno.carrera,
            materia__ciclo_lectivo__lte=alumno.anio_universitario
        ).select_related('materia')

        # Extraer las materias de esa relación
        materias = [cm.materia for cm in materias_relacionadas]

        # 2. ELIMINAR esta sección redundante que sobrescribe 'materias':
        # # Obtener las materias a reinscribirse (como ya lo hacías)
        # materias = Materia.objects.all() 
        # context['materias'] = materias 

        context['alumno'] = alumno
        context['materias'] = materias # Usamos la lista filtrada

        cursos_disponibles = MateriaCurso.objects.filter(materia__in=materias)
        context['cursos_disponibles'] = cursos_disponibles

        # 3. Nuevo: materias en las que ya está reinscripto (USAMOS SIGLA)
        # Usamos el nombre 'materias_reinscriptas' tal como lo usa tu HTML
        materias_reinscriptas = AlumnoMateriaCurso.objects.filter(alumno=alumno).values_list('materia_curso__materia__sigla', flat=True)
        context['materias_reinscriptas'] = list(materias_reinscriptas)
        
        # 4. 🔥 NUEVO: Obtenemos el ID de MateriaCurso de la inscripción activa
        # Esto es crucial para poder mostrar la comisión actual y pasar el ID a "Cancelar"
        inscripciones_activas = AlumnoMateriaCurso.objects.filter(alumno=alumno).select_related('materia_curso', 'materia_curso__curso')
        
        # Diccionario: {sigla_materia: objeto_AlumnoMateriaCurso}
        context['inscripciones_por_materia'] = {
            insc.materia_curso.materia.sigla: insc for insc in inscripciones_activas
        }
        
        return context

def reinscribir_materia(request, alumno_id, materia_id):
    alumno = get_object_or_404(Alumno, id_alumno=alumno_id)
    materia = get_object_or_404(Materia, sigla=materia_id)

    # Verificar si ya está reinscripto
    ya_existe = AlumnoMateriaCurso.objects.filter(
        alumno=alumno,
        materia_curso__materia=materia
    ).exists()

    if ya_existe:
        messages.warning(request, "Ya estás reinscripto en esta materia.")
        return redirect('materia_reinscripcion', alumno_id=alumno.id_alumno)

    curso_id = request.POST.get('curso_id')
    materia_curso = get_object_or_404(MateriaCurso, id_materia_curso=curso_id)

    # 🚨 Validación de choque de horarios
    inscripcion = AlumnoMateriaCurso(
        alumno=alumno,
        materia_curso=materia_curso
    )

    try:
        inscripcion.full_clean()  # 🔥 EJECUTA clean() y valida horarios
        inscripcion.save()
        messages.success(request, f"Te reinscribiste a {materia.nombre} correctamente.")
    except ValidationError as e:
        messages.error(request, e.messages[0])

    return redirect('materia_reinscripcion', alumno_id=alumno.id_alumno)


def cancelar_reinscripcion(request, alumno_id, materia_id):
    alumno = get_object_or_404(Alumno, id_alumno=alumno_id)
    materia = get_object_or_404(Materia, sigla=materia_id)

    inscripcion = AlumnoMateriaCurso.objects.filter(
        alumno=alumno,
        materia_curso__materia=materia
    ).first()

    if inscripcion:
        inscripcion.delete()
        messages.success(request, f"Se canceló la reinscripción a {materia.nombre}.")
    else:
        messages.warning(request, "No estabas reinscripto en esta materia.")

    return redirect('materia_reinscripcion', alumno_id=alumno.id_alumno)

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