"""
URL configuration for TP_UTN project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth.views import LogoutView
from django.urls import path
from django.urls import path, include
from UTN.views import logout_view
from UTN.views import (
    AlumnoDetailView, AlumnoCreateView, AlumnoUpdateView, AlumnoDeleteView, CarreraListView,
    CursoListView, CursoDetailView, CursoCreateView, CursoUpdateView, CursoDeleteView,
    MateriaListView, MateriaDetailView, MateriaCreateView, MateriaUpdateView, MateriaDeleteView,
    InicioView, CarreraListView, Ingenieria_civil, Ingenieria_electronica, Ingenieria_energia,
    Ingenieria_industrial, Ingenieria_mecanica, Ingenieria_metalurgica, Ingenieria_quimica, Ingenieria_sistemas,
    PostLoginCheckView
)

class CustomLogoutView(LogoutView):
    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

urlpatterns = [
    path('auth/', include('social_django.urls', namespace='social')),
    path('logout/', logout_view, name='logout'),
    path('admin/', admin.site.urls),
    path("", InicioView.as_view(), name="inicio"), 
    path('post-login-check/', PostLoginCheckView.as_view(), name='post_login_check'),
    # Alumno URLs
    path('alumnos/<int:pk>/', AlumnoDetailView.as_view(), name='alumno_detail'),
    path('alumnos/create/', AlumnoCreateView.as_view(), name='alumno_create'),
    path('alumnos/<int:pk>/update/', AlumnoUpdateView.as_view(), name='alumno_update'),
    path('alumnos/<int:pk>/delete/', AlumnoDeleteView.as_view(), name='alumno_delete'),
    # Curso URLs
    path('cursos/', CursoListView.as_view(), name='curso_list'),
    path('cursos/<int:pk>/', CursoDetailView.as_view(), name='curso_detail'),
    path('cursos/create/', CursoCreateView.as_view(), name='curso_create'),
    path('cursos/<int:pk>/update/', CursoUpdateView.as_view(), name='curso_update'),
    path('cursos/<int:pk>/delete/', CursoDeleteView.as_view(), name='curso_delete'),
    # Materia URLs
    path('materias/', MateriaListView.as_view(), name='materia_list'),
    path('materias/<int:pk>/', MateriaDetailView.as_view(), name='materia_detail'),
    path('materias/create/', MateriaCreateView.as_view(), name='materia_create'),
    path('materias/<int:pk>/update/', MateriaUpdateView.as_view(), name='materia_update'),
    path('materias/<int:pk>/delete/', MateriaDeleteView.as_view(), name='materia_delete'),
    #Carrera URLs
    path('carreras/', CarreraListView.as_view(), name='carrera_list'),
    path('carreras/ingenieria_civil/', Ingenieria_civil.as_view(), name='Ingenieria_civil'),
    path('carreras/ingenieria_electronica/', Ingenieria_electronica.as_view(), name='Ingenieria_electronica'),
    path('carreras/ingenieria_energia/', Ingenieria_energia.as_view(), name='Ingenieria_energia'),
    path('carreras/ingenieria_industrial/', Ingenieria_industrial.as_view(), name='Ingenieria_industrial'),
    path('carreras/ingenieria_mecanica/', Ingenieria_mecanica.as_view(), name='Ingenieria_mecanica'),
    path('carreras/ingenieria_metalurgica/', Ingenieria_metalurgica.as_view(), name='Ingenieria_metalurgica'),
    path('carreras/ingenieria_quimica/', Ingenieria_quimica.as_view(), name='Ingenieria_quimica'),
    path('carreras/ingenieria_sistemas/', Ingenieria_sistemas.as_view(), name='ingenieria_sistemas'),

]
