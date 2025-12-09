from django.db import models
from django.urls import reverse
from django.core.validators import MinValueValidator, MaxValueValidator
from datetime import date
from django.conf import settings
import datetime, re
from django.core.exceptions import ValidationError

# Create your models here.

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
    
    def tiene_aprobada(self, materia):
        return AlumnoMateria.objects.filter(
            alumno=self,
            materia=materia,
            aprobado=True
        ).exists()

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
    
    def parse_nombre(self):
        """
        Separa el nombre en: base (texto) y número.
        Ejemplo:
            "Física 2" -> ("Física", 2)
            "Programación Web 1" -> ("Programación Web", 1)
        """
        match = re.match(r"^(.*?)[ ]?(\d+)$", self.nombre.strip())
        if match:
            base = match.group(1).strip()
            numero = int(match.group(2))
            return base, numero
        return self.nombre, None


    def get_correlativa(self):
        """
        Devuelve la materia correlativa anterior automáticamente.

        Ejemplos:
            "Física 2"  -> devuelve Materia "Física 1"
            "Inglés 3"  -> devuelve Materia "Inglés 2"
            "Química 1" -> devuelve None (no tiene anterior)
        """
        base, numero = self.parse_nombre()

        if not numero or numero == 1:
            return None  # No tiene correlativa

        nombre_correlativa = f"{base} {numero - 1}"

        return Materia.objects.filter(nombre__iexact=nombre_correlativa).first()
    
class AlumnoMateria(models.Model):
    alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE, related_name='materias_estado')
    materia = models.ForeignKey(Materia, on_delete=models.CASCADE, related_name='estado_alumnos')
    nota_final = models.PositiveSmallIntegerField(null=True, blank=True)
    aprobado = models.BooleanField(default=False)

    class Meta:
        unique_together = ('alumno', 'materia')

    def save(self, *args, **kwargs):
        if self.nota_final is not None:
            self.aprobado = self.nota_final >= 4
        super().save(*args, **kwargs)

    def __str__(self):
            return f"{self.alumno} - {self.materia} - {'Aprobado' if self.aprobado else 'No aprobado'}"
    
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
        """
        Devuelve:
        - lista de días  -> ["Lunes","Miércoles"]
        - hora_inicio    -> time
        - hora_fin       -> time
        """

        partes = self.horario.split(" ")
        # Última parte es el rango horario "08:00-10:00"
        rango = partes[-1]
        dias_str = " ".join(partes[:-1])

        # Parsear días (puede venir "Lunes y Miércoles")
        dias = [d.strip() for d in dias_str.split("y")]

        # Parsear horas
        inicio_str, fin_str = rango.split("-")
        h_inicio = datetime.datetime.strptime(inicio_str, "%H:%M").time()
        h_fin = datetime.datetime.strptime(fin_str, "%H:%M").time()

        return dias, h_inicio, h_fin
    def __str__(self):
        return f"{self.materia.nombre} - {self.curso.nombre}"

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

    # Validación de choque horario
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
 


class CondicionFinal(models.Model):
    id_condicion_final = models.AutoField(primary_key=True)
    # estaba duplicado - lo dejo con un único campo alumno
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


#####################################################

class Profesor(models.Model):
    id_profesor = models.AutoField(primary_key=True)
    # vinculo con user para usar el auth
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profesor', null=True, blank=True)
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    email = models.EmailField()

    def __str__(self):
        display = f"{self.nombre} {self.apellido}"
        if self.user:
            display += f" ({self.user.username})"
        return display
    
class TipoEvaluacion(models.Model):
    id_tipo_evaluacion = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=50)
    descripcion = models.TextField(blank=True)

    def __str__(self):
        return self.nombre

######################################################

class Evaluacion(models.Model):
    id_evaluacion = models.AutoField(primary_key=True)
    nota = models.PositiveIntegerField(validators=[MinValueValidator(0), MaxValueValidator(10)])
    comentario = models.TextField(blank=True)
    TIPOS_EVALUACION = [
        ('parcial_teorico', 'Parcial Teórico'),
        ('parcial_practico', 'Parcial Práctico'),
        ('trabajo_practico', 'Trabajo Práctico'),
    ]
    tipo_evaluacion = models.ForeignKey(TipoEvaluacion, on_delete=models.CASCADE)
    fecha = models.DateField(default=date.today)
    condicion_final = models.ForeignKey(CondicionFinal, on_delete=models.CASCADE, related_name='evaluaciones')

    def __str__(self):
        return f"{self.tipo_evaluacion} - {self.nota}"


class ProfesorCurso(models.Model):
    id_profesor_curso = models.AutoField(primary_key=True)
    profesor = models.ForeignKey(Profesor, on_delete=models.CASCADE, related_name='cursos')
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE, related_name='profesores')

    class Meta:
        unique_together = ('profesor', 'curso')

    def __str__(self):
        return f"{self.profesor} - {self.curso}"
    
from django.core.exceptions import ValidationError
from django.db import models

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

    # --- Nuevos campos ---
    nota = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        help_text="Nota del 1 al 10"
    )

    aprobado = models.BooleanField(default=False)

    class Meta:
        unique_together = ('alumno', 'materia_curso')

    def clean(self):
        # Horario y turno de la materia que intenta inscribir
        nuevo_horario = self.materia_curso.horario
        nuevo_turno = self.materia_curso.turno_cursado

        # Buscar materias donde ya está inscripto en ese turno + horario
        materias_existentes = AlumnoMateriaCurso.objects.filter(
            alumno=self.alumno,
            materia_curso__horario=nuevo_horario,
            materia_curso__turno_cursado=nuevo_turno
        ).exclude(pk=self.pk)  # <-- IMPORTANTE para evitar conflictos al editar

        if materias_existentes.exists():
            raise ValidationError(
                "Ya estás inscripto en una materia en el mismo día y horario."
            )

    def save(self, *args, **kwargs):
        # Si hay nota → se calcula automáticamente si aprobó
        if self.nota is not None:
            self.aprobado = self.nota >= 6

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.alumno} en {self.materia_curso}"
    

