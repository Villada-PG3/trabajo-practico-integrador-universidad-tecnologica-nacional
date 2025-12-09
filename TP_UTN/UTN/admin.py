from django.contrib import admin
from .models import (
    MateriaCurso, Alumno, Materia, Inscripcion, Curso, 
    TipoEvaluacion, Carrera, CondicionFinal, Evaluacion, 
    Profesor, ProfesorMateriaCurso, AlumnoMateriaCurso, CarreraMateria
)

class AlumnoMateriaCursoAdmin(admin.ModelAdmin):
    list_display = ("alumno", "materia_curso", "nota", "aprobado")
    list_filter = ("materia_curso", "aprobado")
    search_fields = ("alumno__nombre", "materia_curso__materia__nombre")
    list_editable = ("nota",)

class ProfesorMateriaCursoInline(admin.TabularInline):
    model = ProfesorMateriaCurso
    extra = 1

class ProfesorAdmin(admin.ModelAdmin):
    inlines = [ProfesorMateriaCursoInline]


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
admin.site.register(ProfesorMateriaCurso)

# ---------------------------------------------------------------------
# 🔥 AGREGADO: Inline para asignar materias a un profesor
# ---------------------------------------------------------------------


admin.site.register(Profesor, ProfesorAdmin)
