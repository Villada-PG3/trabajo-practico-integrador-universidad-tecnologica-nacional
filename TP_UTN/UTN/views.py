from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView, View
from django.urls import reverse_lazy
from .models import (
    Alumno, AlumnoMateriaCurso, Carrera, Curso, Materia, MateriaCurso,
    Inscripcion, TipoEvaluacion, CondicionFinal, Evaluacion, CarreraMateria
)
from django.db.models import Q
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.db import transaction
from .form import RegistroForm


# ============================
#   LOGOUT LIMPIO
# ============================
def logout_view(request):
    logout(request)
    return redirect('/')


# ============================
#   POST LOGIN CHECK
# ============================
@method_decorator(login_required, name='dispatch')
class PostLoginCheckView(View):
    def get(self, request, *args, **kwargs):
        alumno = getattr(request.user, 'alumno', None)

        if alumno and alumno.dni and alumno.anio_universitario and alumno.carrera:
            return redirect('inicio')
        else:
            return redirect('alumno_create')


# ============================
#   INICIO
# ============================
class InicioView(TemplateView):
    template_name = "inicio.html"


# ============================
#   ALUMNO DETAIL
# ============================
class AlumnoDetailView(DetailView):
    model = Alumno
    template_name = 'alumno/alumno_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        alumno = self.object

        inscripciones = alumno.materias_curso.select_related("materia_curso")

        semana = {
            "Lunes": [], "Martes": [], "Miércoles": [],
            "Jueves": [], "Viernes": [], "Sábado": [],
        }

        for ins in inscripciones:
            mc = ins.materia_curso
            try:
                dias, hora_inicio, hora_fin = mc.parse_horario()
            except:
                continue

            entrada = {
                "materia": mc.materia.nombre,
                "horario": f"{hora_inicio.strftime('%H:%M')}–{hora_fin.strftime('%H:%M')}",
                "turno": mc.turno_cursado.capitalize(),
                "nota": ins.nota,
                "aprobado": ins.aprobado,
            }

            for dia in dias:
                dia = dia.strip()
                if dia in semana:
                    semana[dia].append(entrada)

        context["semana"] = semana
        return context


# ============================
#   ALUMNO CREATE
# ============================
class AlumnoCreateView(CreateView):
    model = Alumno
    fields = ['dni', 'anio_universitario', 'carrera']
    template_name = 'alumno/alumno_form.html'
    success_url = reverse_lazy('inicio')

    def get_alumno_instance(self):
        return getattr(self.request.user, 'alumno', None)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        instance = self.get_alumno_instance()
        if instance is not None:
            kwargs['instance'] = instance
        return kwargs

    def form_valid(self, form):
        obj = form.save(commit=False)
        if obj.user is None:
            obj.user = self.request.user
        obj.save()
        return super().form_valid(form)


class AlumnoUpdateView(UpdateView):
    model = Alumno
    fields = '__all__'
    template_name = 'alumno/alumno_form.html'
    success_url = reverse_lazy('inicio')


class AlumnoDeleteView(DeleteView):
    model = Alumno
    template_name = 'alumno/alumno_confirm_delete.html'
    success_url = reverse_lazy('inicio')


# ============================
#   MATERIAS
# ============================
class MateriaListView(ListView):
    model = Materia
    template_name = 'materia/materia_list.html'
    context_object_name = 'materias'

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q')

        if query:
            queryset = queryset.filter(Q(nombre__icontains=query))
        return queryset


class MateriaReinscripcionView(TemplateView):
    template_name = "materia/reinscripcion_materia.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        alumno_id = self.kwargs.get('alumno_id')

        alumno = Alumno.objects.get(id_alumno=alumno_id)

        materias_relacionadas = CarreraMateria.objects.filter(
            carrera=alumno.carrera,
            materia__ciclo_lectivo__lte=alumno.anio_universitario
        ).select_related('materia')

        materias = [cm.materia for cm in materias_relacionadas]

        context['alumno'] = alumno
        context['materias'] = materias

        cursos = MateriaCurso.objects.filter(materia__in=materias)
        context['cursos_disponibles'] = cursos

        materias_reins = AlumnoMateriaCurso.objects.filter(alumno=alumno) \
            .values_list('materia_curso__materia__sigla', flat=True)

        context['materias_reinscriptas'] = list(materias_reins)

        insc_activas = AlumnoMateriaCurso.objects.filter(alumno=alumno) \
            .select_related('materia_curso')

        context['inscripciones_por_materia'] = {
            ins.materia_curso.materia.sigla: ins for ins in insc_activas
        }

        return context


def reinscribir_materia(request, alumno_id, materia_id):
    alumno = get_object_or_404(Alumno, id_alumno=alumno_id)
    materia = get_object_or_404(Materia, sigla=materia_id)

    if AlumnoMateriaCurso.objects.filter(
        alumno=alumno,
        materia_curso__materia=materia
    ).exists():
        messages.warning(request, "Ya estás reinscripto en esta materia.")
        return redirect('materia_reinscripcion', alumno_id=alumno.id_alumno)

    curso_id = request.POST.get('curso_id')
    materia_curso = get_object_or_404(MateriaCurso, id_materia_curso=curso_id)

    inscripcion = AlumnoMateriaCurso(alumno=alumno, materia_curso=materia_curso)

    try:
        inscripcion.full_clean()
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


# ============================
#   CARRERAS
# ============================
CARRERA_URL_MAP = {
    "Ingeniería Civil": "Ingenieria_civil",
    "Ingeniería Electrónica": "Ingenieria_electronica",
    "Ingeniería en Energía Eléctrica": "Ingenieria_energia",
    "Ingeniería Industrial": "Ingenieria_industrial",
    "Ingeniería Mecánica": "Ingenieria_mecanica",
    "Ingeniería Metalúrgica": "Ingenieria_metalurgica",
    "Ingeniería Química": "Ingenieria_quimica",
    "Ingeniería en Sistemas de Información": "ingenieria_sistemas",
}


class CarreraListView(ListView):
    model = Carrera
    template_name = 'carreras/carrera_list.html'
    context_object_name = 'carreras'

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q')

        if query:
            queryset = queryset.filter(Q(nombre__icontains=query))
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        for carrera in context['carreras']:
            carrera.url_name = CARRERA_URL_MAP.get(carrera.nombre, 'carrera_list')

        return context

def register_view(request):
    if request.method == "POST":
        form = RegistroForm(request.POST)
        if form.is_valid():
            nombre = form.cleaned_data["nombre"]
            apellido = form.cleaned_data["apellido"]
            dni = form.cleaned_data["dni"]
            email = form.cleaned_data["email"]
            password = form.cleaned_data["password"]
            anio = form.cleaned_data["anio_universitario"]
            carrera = form.cleaned_data["carrera"]

            # -----------------------------
            # CREAR USUARIO (usa email como username)
            # -----------------------------
            user = User.objects.create_user(
                username=email,   # obligatorio = evita tu error
                email=email,
                password=password,
                first_name=nombre,
                last_name=apellido
            )

            # -----------------------------
            # CREAR ALUMNO
            # -----------------------------
            Alumno.objects.create(
                user=user,
                nombre=nombre,
                apellido=apellido,
                dni=dni,
                email=email,
                anio_universitario=anio,
                carrera=carrera
            )

            # -----------------------------
            # LOGEAR AUTOMÁTICAMENTE
            # -----------------------------
            login(request, user)
            return redirect("inicio")  # o "/"
    else:
        form = RegistroForm()

    return render(request, "register.html", {"form": form})

# --------------------------
#  LOGIN
# --------------------------
def login_view(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("home")   # Cambiá "home" por tu página principal
        else:
            messages.error(request, "Credenciales incorrectas.")

    return render(request, "login.html")


# --------------------------
#  LOGOUT
# --------------------------
def logout_view(request):
    logout(request)
    return redirect("login")
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
