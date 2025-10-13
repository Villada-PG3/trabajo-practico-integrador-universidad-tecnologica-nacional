from django.db import models
from django.urls import reverse
from django.core.validators import MinValueValidator, MaxValueValidator
from datetime import date

# Create your models here.

class Carrera(models.Model):
    id_carrera = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100, null=True, blank=True)
    duracion_anios = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return self.nombre

class Alumno(models.Model):
    id_alumno = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50, default="")
    apellido = models.CharField(max_length=50, default="")
    contrasenia = models.CharField(max_length=100, default="")
    dni = models.CharField(max_length=20, unique=True, default="")
    email = models.EmailField(default="")
    anio_universitario = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)], default=1)
    carrera = models.ForeignKey(Carrera, on_delete=models.CASCADE, related_name='alumnos', null=True, blank=True)

    def __str__(self):
        carrera_nombre = self.carrera.nombre if self.carrera else "Sin carrera"
        return f"{self.apellido}, {self.nombre} ({carrera_nombre})"

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
    nombre = models.CharField(max_length=100, default="")
    sigla = models.CharField(max_length=10, primary_key=True)
    ciclo_lectivo = models.PositiveIntegerField()
    def __str__(self):
        return f"{self.nombre} ({self.sigla})"

    def get_absolute_url(self):
        return reverse('materia_detail', kwargs={'pk': self.pk})
    
class CarreraMateria(models.Model):
    carrera = models.ForeignKey(Carrera, on_delete=models.CASCADE)
    materia = models.ForeignKey(Materia, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('carrera', 'materia')

    def __str__(self):
        return f"{self.materia} - {self.carrera}"


class MateriaCurso(models.Model):
    id_materia_curso = models.AutoField(primary_key=True)
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE, related_name='materias')
    materia = models.ForeignKey(Materia, on_delete=models.CASCADE, related_name='cursos')
    Opciones_Turno = [
    ('manana', 'Mañana'),
    ('tarde', 'Tarde'),
    ('noche', 'Noche'),
    ]
    turno_cursado = models.CharField(max_length=10, choices= Opciones_Turno)
    horario = models.CharField(max_length=50)
    modulo = models.CharField(max_length=50)


    def __str__(self):
        return f"{self.curso.nombre} - {self.materia.nombre} - {self.horario}"

class Inscripcion(models.Model):
    ESTADOS_INSCRIPCION = [
    ('inscripto', 'Inscripto'),
    ('finalizado', 'Finalizado'),
    ('anulado', 'Anulado'),
]
    estado = models.CharField(max_length=20, choices=ESTADOS_INSCRIPCION, default='inscripto')

    id_codigo_alfanumerico = models.AutoField(primary_key=True)
    alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE, related_name='inscripciones')
    materia = models.ForeignKey(MateriaCurso, on_delete=models.CASCADE, related_name='inscripciones', default=None)
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE, related_name='inscripciones', default=None)
    estado = models.CharField(max_length=20, choices=ESTADOS_INSCRIPCION, default='inscripto')
    descripcion = models.TextField(blank=True)

    def __str__(self):
        return f"{self.alumno} inscrito en {self.materia_curso}"


class TipoEvaluacion(models.Model):
    id_tipo_evaluacion = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    descripcion = models.TextField(blank=True)

    def __str__(self):
        return self.nombre

class CondicionFinal(models.Model):
    id_condicion_final = models.AutoField(primary_key=True)
    alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE, related_name='condiciones')
    CONDICIONES_FINAL = [
        ('regular', 'Regular'),
        ('libre', 'Libre'),
        ('aprobacion_directa', 'Aprobación Directa'),
        ('promocion_practica', 'Promoción Práctica'),
    ]
    condicion = models.CharField(max_length=50, choices=CONDICIONES_FINAL)
    fecha = models.DateField(default=date.today)
    profesor = models.ForeignKey('Profesor', on_delete=models.CASCADE, related_name='condiciones')

    def __str__(self):
        return f"{self.alumno} - {self.materia_curso} - {self.condicion}"



class Evaluacion(models.Model):
    id_evaluacion = models.AutoField(primary_key=True)
    nota = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(10)])
    comentario = models.TextField(blank=True)
    TIPOS_EVALUACION = [
    ('parcial_teorico', 'Parcial Teórico'),
    ('parcial_practico', 'Parcial Práctico'),
    ('trabajo_practico', 'Trabajo Práctico'),
]
    tipo_evaluacion = models.ForeignKey(TipoEvaluacion, on_delete=models.CASCADE, choices=TIPOS_EVALUACION)
    fecha = models.DateField(default=date.today)
    condicion_final = models.ForeignKey(CondicionFinal, on_delete=models.CASCADE, related_name='evaluaciones')

    def __str__(self):
        return f"{self.tipo_evaluacion} - {self.nota}"

class Profesor(models.Model):
    id_profesor = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    email = models.EmailField()

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

class ProfesorCurso(models.Model):
    id_profesor_curso = models.AutoField(primary_key=True)
    profesor = models.ForeignKey(Profesor, on_delete=models.CASCADE, related_name='cursos')
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE, related_name='profesores')

    def __str__(self):
        return f"hace un html con el estilo del anterior y que sea simple con un titulo que yo voy a ingresar una descripcion que yo tmb voy a ingresar y un boton de insribirse y eso ademas que debajo de la descripcion yo agrego el horario los turnos y los profesself.profesor - {self.curso}"
    
class AlumnoMateriaCurso(models.Model):
    id_alumno_materia_curso = models.AutoField(primary_key=True)
    alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE, related_name='materias_curso')
    materia_curso = models.ForeignKey(MateriaCurso, on_delete=models.CASCADE, related_name='alumnos')

    def __str__(self):
        return f"{self.alumno} en {self.materia_curso}"