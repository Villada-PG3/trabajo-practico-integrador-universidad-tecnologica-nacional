from django.contrib import admin
from .models import (
    MateriaCurso, Alumno, Curso, Materia, Inscripcion, 
    TipoEvaluacion, Carrera, CondicionFinal, Evaluacion, 
    Profesor, ProfesorCurso, AlumnoMateriaCurso, CarreraMateria
)

admin.site.register(MateriaCurso)
admin.site.register(Alumno)
admin.site.register(Curso)
admin.site.register(Materia)
admin.site.register(CarreraMateria)
admin.site.register(Inscripcion)
admin.site.register(TipoEvaluacion)
admin.site.register(Carrera)
admin.site.register(CondicionFinal)
admin.site.register(Evaluacion)
admin.site.register(Profesor)
admin.site.register(ProfesorCurso)
admin.site.register(AlumnoMateriaCurso)
