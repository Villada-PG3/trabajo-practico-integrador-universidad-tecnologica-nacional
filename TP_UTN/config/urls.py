from django.contrib import admin
from django.urls import path

from UTN.views import (
    # Login/registro
    login_view, register_view, logout_view,

    # Vistas principales
    InicioView, PostLoginCheckView,

    # Alumno
    AlumnoDetailView, AlumnoCreateView, AlumnoUpdateView,
    AlumnoDeleteView,

    # Materias
    MateriaListView, MateriaReinscripcionView,
    cancelar_reinscripcion, reinscribir_materia,

    # Carreras
    CarreraListView,
    Ingenieria_civil, Ingenieria_electronica, Ingenieria_energia,
    Ingenieria_industrial, Ingenieria_mecanica, Ingenieria_metalurgica,
    Ingenieria_quimica, Ingenieria_sistemas,

    # PROFESORES - nuevas vistas
    ProfesorDashboardView,
    ProfesorAsignarClaseView,
    ProfesorCursoEstudiantesView,
    ProfesorEditarNotaView,
)

urlpatterns = [
    # Login / Registro
    path("login/", login_view, name="login"),
    path("register/", register_view, name="register"),
    path("logout/", logout_view, name="logout"),

    # Admin Django
    path('admin/', admin.site.urls),

    # Inicio
    path("", InicioView.as_view(), name="inicio"),
    path('post-login-check/', PostLoginCheckView.as_view(), name='post_login_check'),

    # Alumno
    path('alumnos/<int:pk>/', AlumnoDetailView.as_view(), name='alumno_detail'),
    path('alumnos/create/', AlumnoCreateView.as_view(), name='alumno_create'),
    path('alumnos/<int:pk>/update/', AlumnoUpdateView.as_view(), name='alumno_update'),
    path('alumnos/<int:pk>/delete/', AlumnoDeleteView.as_view(), name='alumno_delete'),

    # Materias / reinscripción
    path('materias/', MateriaListView.as_view(), name='materia_list'),
    path('reinscripcion/<int:alumno_id>/', MateriaReinscripcionView.as_view(), name='materia_reinscripcion'),
    path('reinscripcion/<int:alumno_id>/materia/<path:materia_id>/confirmar/', reinscribir_materia, name='materia_reinscribir'),
    path('reinscripcion/<int:alumno_id>/materia/<path:materia_id>/cancelar/', cancelar_reinscripcion, name='cancelar_reinscripcion'),

    # Carreras
    path('carreras/', CarreraListView.as_view(), name='carrera_list'),
    path('carreras/ingenieria_civil/', Ingenieria_civil.as_view(), name='Ingenieria_civil'),
    path('carreras/ingenieria_electronica/', Ingenieria_electronica.as_view(), name='Ingenieria_electronica'),
    path('carreras/ingenieria_energia/', Ingenieria_energia.as_view(), name='Ingenieria_energia'),
    path('carreras/ingenieria_industrial/', Ingenieria_industrial.as_view(), name='Ingenieria_industrial'),
    path('carreras/ingenieria_mecanica/', Ingenieria_mecanica.as_view(), name='Ingenieria_mecanica'),
    path('carreras/ingenieria_metalurgica/', Ingenieria_metalurgica.as_view(), name='Ingenieria_metalurgica'),
    path('carreras/ingenieria_quimica/', Ingenieria_quimica.as_view(), name='Ingenieria_quimica'),
    path('carreras/ingenieria_sistemas/', Ingenieria_sistemas.as_view(), name='ingenieria_sistemas'),

    # PROFESORES - URLs nuevas
    path('profesor/dashboard/', ProfesorDashboardView.as_view(), name='profesor_dashboard'),
    path('profesor/asignar_clase/', ProfesorAsignarClaseView.as_view(), name='profesor_asignar_clase'),
    path('profesor/curso/<int:curso_id>/estudiantes/', ProfesorCursoEstudiantesView.as_view(), name='profesor_curso_estudiantes'),
    path('profesor/curso/<int:curso_id>/estudiante/<int:alumno_materia_id>/nota/', ProfesorEditarNotaView, name='profesor_editar_nota'),
]
