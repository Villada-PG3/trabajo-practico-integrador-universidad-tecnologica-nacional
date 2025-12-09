from django.contrib import admin
from .models import (
    MateriaCurso, Alumno, Materia, Inscripcion, Curso, 
    TipoEvaluacion, Carrera, CondicionFinal, Evaluacion, 
    Profesor, ProfesorMateriaCurso, AlumnoMateriaCurso, CarreraMateria, AlumnoMateria
)

class CarreraMateriaInline(admin.TabularInline):
    # Este Inline permite editar la relación CarreraMateria
    model = CarreraMateria
    extra = 1 # Muestra 1 fila vacía adicional para nuevas asignaciones

# Paso 2: Configurar la clase MateriaAdmin
class MateriaAdmin(admin.ModelAdmin):
    # CLAVE: list_display muestra estas columnas en la tabla de listado
    list_display = (
        'sigla', 
        'nombre', 
        'ciclo_lectivo', 
        'get_carreras_admin'  # <-- ¡Esto es lo que querías!
    )
    
    # Campo de solo lectura para la vista de edición/formulario
    readonly_fields = ('get_carreras_admin',)
    
    # Campos que se muestran en el formulario de edición
    fields = ('sigla', 'nombre', 'ciclo_lectivo', 'correlativas_requeridas', 'get_carreras_admin')
    
    # Incluir el Inline en la vista de edición
    inlines = [CarreraMateriaInline] 

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
admin.site.register(AlumnoMateria)

# ---------------------------------------------------------------------
# 🔥 AGREGADO: Inline para asignar materias a un profesor
# ---------------------------------------------------------------------


admin.site.register(Profesor, ProfesorAdmin)
