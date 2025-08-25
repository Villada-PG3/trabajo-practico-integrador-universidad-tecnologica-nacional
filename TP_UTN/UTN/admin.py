from django.contrib import admin
from .models import MateriaCurso, Alumno, Curso, Materia, AlumnoCurso, Inscripcion, TipoEvaluacion, Reporte, CondicionFinal, Evaluacion

# Register your models here.
admin.site.register(MateriaCurso)
admin.site.register(Alumno)
admin.site.register(Curso)
admin.site.register(Materia)
admin.site.register(AlumnoCurso)
admin.site.register(Inscripcion)
admin.site.register(TipoEvaluacion)
admin.site.register(Reporte)
admin.site.register(CondicionFinal)
admin.site.register(Evaluacion)
