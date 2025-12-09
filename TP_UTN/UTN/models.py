from django.db import models
from django.urls import reverse
from django.core.validators import MinValueValidator, MaxValueValidator
from datetime import date
from django.conf import settings
import datetime
from django.core.exceptions import ValidationError

# ============================================
#   MODELOS BASE
# ============================================

class Carrera(models.Model):
    id_carrera = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100, null=True, blank=True)
    duracion_anios = models.PositiveIntegerField(null=True, blank=True)

    def __str__(self):
        return self.nombre or "Sin nombre"


class Alumno(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='alumno', null=True)
    id_alumno = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50, default="")
    apellido = models.CharField(max_length=50, default="")
    dni = models.CharField(max_length=20, unique=True, default="")
    email = models.EmailField(default="")
    anio_universitario = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(10)], default=1)
    carrera = models.ForeignKey(Carrera, on_delete=models.CASCADE, related_name='alumnos', null=True, blank=True)

    def __str__(self):
        carrera_nombre = self.carrera.nombre if self.carrera else "Sin carrera"
        return f"{self.id_alumno}, {self.apellido}, {self.nombre} ({carrera_nombre})"

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
    materia = models.ForeignKey(Materia, on_delete=models.CASCADE, related_name='cursos_ofrecidos')

    Opciones_Turno = [
        ('manana', 'Mañana'),
        ('tarde', 'Tarde'),
        ('noche', 'Noche'),
    ]
    turno_cursado = models.CharField(max_length=10, choices=Opciones_Turno)
    horario = models.CharField(max_length=50)
    modulo = models.CharField(max_length=50)
    grupo = models.CharField(max_length=50, null=True, blank=True)

    def parse_horario(self):
        partes = self.horario.split(" ")
        rango = partes[-1]
        dias_str = " ".join(partes[:-1])

        dias = [d.strip() for d in dias_str.split("y")]

        inicio_str, fin_str = rango.split("-")
        h_inicio = datetime.datetime.strptime(inicio_str, "%H:%M").time()
        h_fin = datetime.datetime.strptime(fin_str, "%H:%M").time()

        return dias, h_inicio, h_fin

    def __str__(self):
        return f"{self.materia.nombre} - {self.curso.nombre}"


# ============================================
#   INSCRIPCIONES
# ============================================

class Inscripcion(models.Model):
    ESTADOS_INSCRIPCION = [
        ('inscripto', 'Inscripto'),
        ('finalizado', 'Finalizado'),
        ('anulado', 'Anulado'),
    ]

    id_codigo_alfanumerico = models.AutoField(primary_key=True)
    alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE, related_name='inscripciones')
    materia_curso = models.ForeignKey(MateriaCurso, on_delete=models.CASCADE, related_name='inscripciones')
    estado = models.CharField(max_length=20, choices=ESTADOS_INSCRIPCION, default='inscripto')
    descripcion = models.TextField(blank=True)

    def __str__(self):
        return f"{self.alumno.nombre} {self.alumno.apellido} – {self.materia_curso}"

    def clean(self):
        nueva_materia = self.materia_curso
        nuevos_dias, nuevo_inicio, nuevo_fin = nueva_materia.parse_horario()

        inscripciones_existentes = Inscripcion.objects.filter(
            alumno=self.alumno,
            estado="inscripto"
        ).exclude(pk=self.pk)

        for insc in inscripciones_existentes:
            materia = insc.materia_curso
            dias, inicio, fin = materia.parse_horario()

            for dia in dias:
                if dia in nuevos_dias:
                    if not (nuevo_fin <= inicio or nuevo_inicio >= fin):
                        raise ValidationError(
                            f"Conflicto de horario: ya estás inscripto en "
                            f"{materia.materia.nombre} el día {dia} "
                            f"de {inicio.strftime('%H:%M')} a {fin.strftime('%H:%M')}."
                        )

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)


# ============================================
#   PROFESORES
# ============================================

class Profesor(models.Model):
    id_profesor = models.AutoField(primary_key=True)
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profesor', null=True, blank=True)
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    email = models.EmailField()

    def __str__(self):
        display = f"{self.nombre} {self.apellido}"
        if self.user:
            display += f" ({self.user.username})"
        return display


# ============================================
#   NUEVO — ASIGNACIÓN PROFESOR → MATERIA CURSO
# ============================================

class ProfesorMateriaCurso(models.Model):
    id_profesor_mc = models.AutoField(primary_key=True)
    profesor = models.ForeignKey(Profesor, on_delete=models.CASCADE, related_name='materias_asignadas')
    materia_curso = models.ForeignKey(MateriaCurso, on_delete=models.CASCADE, related_name='profesores_asignados')

    class Meta:
        unique_together = ('profesor', 'materia_curso')

    def __str__(self):
        return f"{self.profesor} → {self.materia_curso}"


# ============================================
#   RESTO DE LOS MODELOS
# ============================================

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
        return f"{self.alumno} - {self.condicion}"


class Evaluacion(models.Model):
    id_evaluacion = models.AutoField(primary_key=True)
    nota = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(10)])
    comentario = models.TextField(blank=True)
    tipo_evaluacion = models.ForeignKey(TipoEvaluacion, on_delete=models.CASCADE)
    fecha = models.DateField(default=date.today)
    condicion_final = models.ForeignKey(CondicionFinal, on_delete=models.CASCADE, related_name='evaluaciones')

    def __str__(self):
        return f"{self.tipo_evaluacion} - {self.nota}"


class AlumnoMateriaCurso(models.Model):
    id_alumno_materia_curso = models.AutoField(primary_key=True)

    alumno = models.ForeignKey(
        Alumno,
        on_delete=models.CASCADE,
        related_name='materias_curso'
    )

    materia_curso = models.ForeignKey(
        MateriaCurso,
        on_delete=models.CASCADE,
        related_name='alumnos'
    )

    nota = models.PositiveSmallIntegerField(null=True, blank=True)
    aprobado = models.BooleanField(default=False)

    class Meta:
        unique_together = ('alumno', 'materia_curso')

    def clean(self):
        nuevo_horario = self.materia_curso.horario
        nuevo_turno = self.materia_curso.turno_cursado

        materias_existentes = AlumnoMateriaCurso.objects.filter(
            alumno=self.alumno,
            materia_curso__horario=nuevo_horario,
            materia_curso__turno_cursado=nuevo_turno
        ).exclude(pk=self.pk)

        if materias_existentes.exists():
            raise ValidationError(
                "Ya estás inscripto en una materia en el mismo día y horario."
            )

    def save(self, *args, **kwargs):
        if self.nota is not None:
            self.aprobado = self.nota >= 6
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.alumno} en {self.materia_curso}"
