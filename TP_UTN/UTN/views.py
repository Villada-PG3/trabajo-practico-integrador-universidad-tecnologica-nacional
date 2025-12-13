from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView, View
from django.urls import reverse_lazy
from .models import (
    Alumno, AlumnoMateriaCurso, Carrera, Curso, Materia, MateriaCurso,
    Inscripcion, TipoEvaluacion, CondicionFinal, Evaluacion, CarreraMateria,
    Profesor, ProfesorMateriaCurso,
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

        # ============================================
        # CORRELATIVAS + CHEQUEO DE APROBACIÓN
        # ============================================
        materias_info = []

        for materia in materias:
            estado = "ok"      # habilitada por defecto
            mensaje = ""
            correlativa = materia.get_correlativa()  # método que creaste «Fisica 2 → Fisica 1»

            # 1) No permitir reinscribirse si ya aprobó la materia
            aprobada = AlumnoMateriaCurso.objects.filter(
                alumno=alumno,
                materia_curso__materia=materia,
                nota__gte=4
            ).exists()

            if aprobada:
                estado = "aprobada"
                mensaje = "Ya aprobaste esta materia."
            
            # 2) Si tiene correlativa, verificar si está aprobada
            if correlativa and not aprobada:
                correlativa_aprobada = AlumnoMateriaCurso.objects.filter(
                    alumno=alumno,
                    materia_curso__materia__nombre__iexact=correlativa.nombre,
                    nota__gte=6
                ).exists()

                if not correlativa_aprobada:
                    estado = "correlativa"
                    mensaje = f"No podés cursar {materia.nombre} sin aprobar {correlativa.nombre}."

            materias_info.append({
                "materia": materia,
                "estado": estado,
                "mensaje": mensaje,
            })

        context["materias_info"] = materias_info

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
    carreras = Carrera.objects.all()

    if request.method == "POST":
        nombre = request.POST.get("nombre")
        apellido = request.POST.get("apellido")
        dni = request.POST.get("dni")
        email = request.POST.get("email")
        anio = request.POST.get("anio_universitario")
        carrera_id = request.POST.get("carrera")
        password = request.POST.get("password")
        password2 = request.POST.get("password2")

        # Validar contraseñas
        if password != password2:
            return render(request, "register.html", {
                "carreras": carreras,
                "error": "Las contraseñas no coinciden."
            })

        # Crear usuario Django
        user = User.objects.create_user(
            username=email,   # obligatorio
            email=email,
            password=password
        )

        # Guardar alumno
        Alumno.objects.create(
            user=user,
            nombre=nombre,
            apellido=apellido,
            dni=dni,
            email=email,
            anio_universitario=anio,
            carrera_id=carrera_id  # 🔥🔥 ESTO ES LO IMPORTANTE
        )

        return redirect("login")

    return render(request, "register.html", {"carreras": carreras})


# --------------------------
#  LOGIN
# --------------------------
def login_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        # Buscar usuario por email
        try:
            user_obj = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, "Email o contraseña incorrectos.")
            return render(request, "login.html")

        # Autenticación usando username interno
        user = authenticate(request, username=user_obj.username, password=password)

        if user is not None:
            login(request, user)

            # ================================
            # REDIRECCIÓN SEGÚN ROL
            # ================================

            # Si es alumno → ir a alumno_detail
            if hasattr(user, "alumno"):
                return redirect("/", pk=user.alumno.id_alumno)

            # Si es profesor → ir a dashboard de profesor
            if hasattr(user, "profesor"):
                return redirect("dashboard", pk=user.profesor.id_profesor)

            # Si no tiene rol asociado
            messages.error(request, "Tu cuenta no tiene un rol asignado.")
            return redirect("login")

        else:
            messages.error(request, "Email o contraseña incorrectos.")

    return render(request, "login.html")




# ============================
#  Páginas de Carrera (TemplateViews)
# ============================
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


# ============================
#  VISTAS DE PROFESORES
# ============================
def get_profesor_or_redirect(request):
    """ Devuelve profesor o redirige si el usuario NO es profesor. """
    profesor = getattr(request.user, "profesor", None)
    if profesor is None:
        messages.error(request, "Debés iniciar sesión como profesor.")
        return None
# =======================================
#   LOGIN PROFESORES (exclusivo)
# =======================================
def login_profesores(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")

        user = authenticate(request, username=email, password=password)

        if user is not None:
            if hasattr(user, "profesor"):
                login(request, user)
                return redirect("dashboard")
            else:
                messages.error(request, "Este usuario no está registrado como profesor.")
        else:
            messages.error(request, "Credenciales incorrectas.")

    return render(request, "profesores/login_profesores.html")



# ===========================================
#   LOGOUT PROFESORES
# ===========================================

def logout_profesores(request):
    logout(request)
    return redirect("login_profesores")



# ===========================================
#   DASHBOARD PROFESORES
# ===========================================

@login_required
def dashboard(request, pk):
    profesor = Profesor.objects.get(user=request.user)
    asignaciones = ProfesorMateriaCurso.objects.filter(profesor=profesor)

    return render(request, "profesores/dashboard.html", {
        "profesor": profesor,
        "asignaciones": asignaciones
    })



# ===========================================
#   LISTAR MATERIAS DISPONIBLES
# ===========================================

@login_required
def materias_disponibles(request):
    profesor = request.user.profesor

    materias = MateriaCurso.objects.exclude(
        profesores__profesor=profesor
    )

    return render(request, "profesores/materias_disponibles.html", {
        "materias": materias
    })






# ===========================================
#   ASIGNAR MATERIA A PROFESOR
# ===========================================

@login_required
def asignar_materia_profesor(request, id_materia_curso):
    profesor = request.user.profesor
    materia_curso = get_object_or_404(MateriaCurso, pk=id_materia_curso)

    asignacion, creada = ProfesorMateriaCurso.objects.get_or_create(
        profesor=profesor,
        materia_curso=materia_curso
    )

    if creada:
        messages.success(request, f"Te asignaste a {materia_curso.materia.nombre}.")
    else:
        messages.warning(request, "Ya estabas asignado a esta materia.")

    return redirect("materias_disponibles")



# ===========================================
#   DESASIGNAR MATERIA
# ===========================================

@login_required
def desasignar_materia(request, materia_id):
    profesor = request.user.profesor

    asignacion = get_object_or_404(
        ProfesorMateriaCurso,
        profesor=profesor,
        materia_curso_id=materia_id
    )

    asignacion.delete()

    messages.success(request, "La materia fue desasignada correctamente.")
    return redirect("mis_clases")



# ===========================================
#   MIS CLASES – LISTA DE CLASES ASIGNADAS
# ===========================================

@login_required
def mis_clases(request):
    profesor = request.user.profesor

    asignaciones = ProfesorMateriaCurso.objects.filter(
        profesor=profesor
    ).select_related("materia_curso", "materia_curso__materia", "materia_curso__curso")

    return render(request, "profesores/mis_clases.html", {
        "asignaciones": asignaciones
    })




# ===========================================
#   CARGAR NOTAS (sólo armado del endpoint)
# ===========================================

@login_required
def cargar_nota(request, clase_id):
    profesor = request.user.profesor

    # 🔒 Seguridad: el profesor DEBE estar asignado
    asignacion = get_object_or_404(
        ProfesorMateriaCurso,
        profesor=profesor,
        materia_curso_id=clase_id
    )

    materia_curso = asignacion.materia_curso

    alumnos_cursando = AlumnoMateriaCurso.objects.filter(
        materia_curso=materia_curso
    ).select_related('alumno')

    if request.method == "POST":
        for inscripcion in alumnos_cursando:
            campo = f"nota_{inscripcion.id_alumno_materia_curso}"
            valor = request.POST.get(campo)

            if valor != "" and valor is not None:
                inscripcion.nota = int(valor)
                inscripcion.save()

        messages.success(request, "Notas guardadas correctamente.")
        return redirect("mis_clases")

    return render(request, "profesores/cargar_nota.html", {
        "materia_curso": materia_curso,
        "alumnos": alumnos_cursando
    })
@login_required
def desasignar_materia(request, id_materia_curso):
    profesor = request.user.profesor

    asignacion = get_object_or_404(
        ProfesorMateriaCurso,
        profesor=profesor,
        materia_curso_id=id_materia_curso
    )

    asignacion.delete()
    messages.success(request, "Dejaste de dar la materia correctamente.")

    return redirect("mis_clases")