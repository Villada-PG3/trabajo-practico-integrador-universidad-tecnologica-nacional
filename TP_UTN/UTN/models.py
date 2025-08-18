from django.db import models
from django.urls import reverse
from django.core.validators import MinValueValidator, MaxValueValidator
from datetime import date

# Create your models here.

class Alumno(models.Model):
    id_alumno = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    dni = models.CharField(max_length=20, unique=True)
    email = models.EmailField()
    anio_universitario = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)])

    def __str__(self):
        return f"{self.apellido}, {self.nombre}"

    def get_absolute_url(self):
        return reverse('alumno_detail', kwargs={'pk': self.pk})


class Curso(models.Model):
    id_curso = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    nivel = models.CharField(max_length=20)
    numero = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.nombre} - Nivel {self.nivel} ({self.numero})"

    def get_absolute_url(self):
        return reverse('curso_detail', kwargs={'pk': self.pk})


class Materia(models.Model):
    sigla = models.AutoField(primary_key=True)
    nivel = models.PositiveIntegerField()
    tipo_materia = models.CharField(max_length=50)
    ciclo_lectivo = models.PositiveIntegerField()
    turno_cursado = models.CharField(max_length=20)
    horario = models.CharField(max_length=50)
    modulo = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.tipo_materia} ({self.sigla})"

    def get_absolute_url(self):
        return reverse('materia_detail', kwargs={'pk': self.pk})


class MateriaCurso(models.Model):
    id_materia_curso = models.AutoField(primary_key=True)
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE, related_name='materias')
    materia = models.ForeignKey(Materia, on_delete=models.CASCADE, related_name='cursos')

    def __str__(self):
        return f"{self.curso.nombre} - {self.materia.tipo_materia}"


class AlumnoCurso(models.Model):
    id_alumno_curso = models.AutoField(primary_key=True)
    alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE, related_name='cursos')
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE, related_name='alumnos')

    def __str__(self):
        return f"{self.alumno} en {self.curso}"


class Inscripcion(models.Model):
    ESTADOS = [
        ('activo', 'Activo'),
        ('finalizado', 'Finalizado'),
        ('anulado', 'Anulado'),
    ]

    id_codigo_alfanumerico = models.AutoField(primary_key=True)
    alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE, related_name='inscripciones')
    materia_curso = models.ForeignKey(MateriaCurso, on_delete=models.CASCADE, related_name='inscripciones')
    estado = models.CharField(max_length=20, choices=ESTADOS, default='activo')
    descripcion = models.TextField(blank=True)

    def __str__(self):
        return f"{self.alumno} inscrito en {self.materia_curso}"


class TipoEvaluacion(models.Model):
    id_tipo_evaluacion = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    descripcion = models.TextField(blank=True)

    def __str__(self):
        return self.nombre


class Reporte(models.Model):
    id_reporte = models.AutoField(primary_key=True)
    alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE, related_name='reportes')
    materia = models.ForeignKey(Materia, on_delete=models.CASCADE, related_name='reportes')
    observaciones = models.TextField(blank=True)

    def __str__(self):
        return f"Reporte de {self.alumno} en {self.materia}"


class CondicionFinal(models.Model):
    id_condicion_final = models.AutoField(primary_key=True)
    reporte = models.ForeignKey(Reporte, on_delete=models.CASCADE, related_name='condiciones')
    condicion = models.CharField(max_length=50)
    fecha = models.DateField(default=date.today)

    def __str__(self):
        return f"{self.reporte} - {self.condicion}"


class Evaluacion(models.Model):
    id_evaluacion = models.AutoField(primary_key=True)
    nota = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(10)])
    comentario = models.TextField(blank=True)
    tipo_evaluacion = models.ForeignKey(TipoEvaluacion, on_delete=models.CASCADE, related_name='evaluaciones')
    fecha = models.DateField(default=date.today)
    condicion_final = models.ForeignKey(CondicionFinal, on_delete=models.CASCADE, related_name='evaluaciones')

    def __str__(self):
        return f"{self.tipo_evaluacion} - {self.nota}"