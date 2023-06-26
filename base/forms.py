from django import forms

class MiFormulario(forms.Form):
    username = forms.CharField(
        label="Nombre de usuario",
        error_messages={
            'required': 'El campo nombre de usuario es obligatorio.',
        }
    )
    password1 = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput,
        error_messages={
            'required': 'El campo contraseña es obligatorio.',
            'min_length': 'La contraseña debe tener al menos %(limit_value)d caracteres.',
        }
    )
    password2 = forms.CharField(
        label="Confirmar contraseña",
        widget=forms.PasswordInput,
        error_messages={
            'required': 'El campo confirmar contraseña es obligatorio.',
            'min_length': 'La contraseña debe tener al menos %(limit_value)d caracteres.',
            'different': 'Las contraseñas no coinciden.',
        }
    )

