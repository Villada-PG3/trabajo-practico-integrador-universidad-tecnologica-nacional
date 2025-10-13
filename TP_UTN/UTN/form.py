from django import forms
from .models import (
    Alumno, Carrera, Curso, Materia, MateriaCurso,
    AlumnoCurso, Inscripcion, TipoEvaluacion, CondicionFinal, Evaluacion
)


class AlumnoForm(forms.ModelForm):
    class Meta:
        model = Alumno
        fields = '__all__'
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre'}),
            'apellido': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Apellido'}),
            'dni': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'DNI'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Correo electrónico'}),
            'anio_universitario': forms.NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 10}),
            'carrera': forms.Select(attrs={'class': 'form-select'}),
        }


class CursoForm(forms.ModelForm):
    class Meta:
        model = Curso
        fields = '__all__'
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'nivel': forms.TextInput(attrs={'class': 'form-control'}),
            'numero': forms.NumberInput(attrs={'class': 'form-control'}),
        }


class MateriaForm(forms.ModelForm):
    class Meta:
        model = Materia
        fields = '__all__'
        widgets = {
            'nivel': forms.NumberInput(attrs={'class': 'form-control'}),
            'tipo_materia': forms.TextInput(attrs={'class': 'form-control'}),
            'ciclo_lectivo': forms.NumberInput(attrs={'class': 'form-control'}),
            'turno_cursado': forms.Select(attrs={'class': 'form-select'}),
            'horario': forms.TextInput(attrs={'class': 'form-control'}),
            'modulo': forms.TextInput(attrs={'class': 'form-control'}),
            'carrera': forms.Select(attrs={'class': 'form-select'}),
        }


class MateriaCursoForm(forms.ModelForm):
    class Meta:
        model = MateriaCurso
        fields = '__all__'
        widgets = {
            'curso': forms.Select(attrs={'class': 'form-select'}),
            'materia': forms.Select(attrs={'class': 'form-select'}),
        }


class AlumnoCursoForm(forms.ModelForm):
    class Meta:
        model = AlumnoCurso
        fields = '__all__'
        widgets = {
            'alumno': forms.Select(attrs={'class': 'form-select'}),
            'curso': forms.Select(attrs={'class': 'form-select'}),
        }


class InscripcionForm(forms.ModelForm):
    class Meta:
        model = Inscripcion
        fields = '__all__'
        widgets = {
            'alumno': forms.Select(attrs={'class': 'form-select'}),
            'materia_curso': forms.Select(attrs={'class': 'form-select'}),
            'estado': forms.Select(attrs={'class': 'form-select'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class TipoEvaluacionForm(forms.ModelForm):
    class Meta:
        model = TipoEvaluacion
        fields = '__all__'
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class CarreraForm(forms.ModelForm):
    class Meta:
        model = Carrera
        fields = '__all__'
        widgets = {
            'nombre': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }


class CondicionFinalForm(forms.ModelForm):
    class Meta:
        model = CondicionFinal
        fields = '__all__'
        widgets = {
            'reporte': forms.Select(attrs={'class': 'form-select'}),
            'condicion': forms.Select(attrs={'class': 'form-select'}),
            'fecha': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }


class EvaluacionForm(forms.ModelForm):
    class Meta:
        model = Evaluacion
        fields = '__all__'
        widgets = {
            'nota': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'max': 10}),
            'comentario': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'tipo_evaluacion': forms.Select(attrs={'class': 'form-select'}),
            'fecha': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'condicion_final': forms.Select(attrs={'class': 'form-select'}),
        }
