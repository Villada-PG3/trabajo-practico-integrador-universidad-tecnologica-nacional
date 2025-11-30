from django.contrib import admin
from .models import (
    MateriaCurso, Alumno, Materia, Inscripcion, Curso, 
    TipoEvaluacion, Carrera, CondicionFinal, Evaluacion, 
    Profesor, ProfesorCurso, AlumnoMateriaCurso, CarreraMateria
)

class AlumnoMateriaCursoAdmin(admin.ModelAdmin):
    list_display = ("alumno", "materia_curso", "nota", "aprobado")
    list_filter = ("materia_curso", "aprobado")
    search_fields = ("alumno__nombre", "materia_curso__materia__nombre")
    list_editable = ("nota",)  # 🔥 Permite editar notas desde el listado del admin

admin.site.register(AlumnoMateriaCurso, AlumnoMateriaCursoAdmin)

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

