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
    Ingenieria_quimica, Ingenieria_sistema,

    # PROFESORES - nuevas vistas
    
    login_profesores, desasignar_materia, dashboard, mis_clases, cargar_nota, logout_profesores, materias_disponibles, asignar_materia_profesor,  
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
    path('carreras/ingenieria_sistema/', Ingenieria_sistema.as_view(), name='Ingenieria_sistema'),

    
    # ==========================
    # PROFESORES - URLs nuevas
    # ==========================
    path("profesores/panel/<int:pk>/", dashboard, name="dashboard"),
    path("profesores/mis-clases/", mis_clases, name="mis_clases"),
    path("profesores/cargar-nota/<int:clase_id>/", cargar_nota, name="cargar_nota"),
    path("profesores/logout/", logout_profesores, name="logout_profesores"),
    path("profesores/materias-disponibles/", materias_disponibles, name="materias_disponibles"),
    path("profesores/asignar/<int:id_materia_curso>/", asignar_materia_profesor, name="asignar_materia_profesor"),
    path("desasignar/<int:id_materia_curso>/", desasignar_materia, name="desasignar_materia")

]
