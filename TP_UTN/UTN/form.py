from django import forms
from .models import (
    Alumno, Carrera, Curso, Materia, MateriaCurso,
    Inscripcion, TipoEvaluacion, CondicionFinal, Evaluacion
)


class RegistroForm(forms.Form):
    nombre = forms.CharField(max_length=50)
    apellido = forms.CharField(max_length=50)
    dni = forms.CharField(max_length=20)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())
    password2 = forms.CharField(widget=forms.PasswordInput(), label="Confirmar contraseña")
    anio_universitario = forms.IntegerField(min_value=1, max_value=10)
    carrera = forms.ModelChoiceField(queryset=Carrera.objects.all())

    def clean(self):
        cleaned = super().clean()
        if cleaned.get("password") != cleaned.get("password2"):
            raise forms.ValidationError("Las contraseñas no coinciden.")
        return cleaned


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
