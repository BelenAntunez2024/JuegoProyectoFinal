"""Formularios de autenticación del juego.

Define los formularios personalizados para el registro y login de usuarios,
aplicando estilos de Bootstrap a cada campo para que se integren con la
estética visual del juego.
"""

from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User


class FormularioRegistro(UserCreationForm):
    """Formulario de registro de nuevo usuario.

    Extiende el UserCreationForm de Django agregando el campo 'email'
    como obligatorio (lo necesitamos para recuperación de contraseña).
    Cada campo recibe la clase CSS 'form-control' de Bootstrap para
    que se vea consistente con el diseño del juego.
    """

    # Agregamos el campo email como obligatorio.
    # En el UserCreationForm original, email no está incluido.
    email = forms.EmailField(
        required=True,
        help_text='Obligatorio. Se usa para recuperar tu contraseña.'
    )

    class Meta:
        # Le decimos a Django que este formulario crea objetos del modelo User
        model = User
        # Estos son los campos que se van a mostrar en el formulario, en orden
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        """Agrega clases CSS de Bootstrap a todos los campos del formulario.

        Recorre cada campo visible y le asigna la clase 'form-control'
        para que se renderice con el estilo de input de Bootstrap.
        También agrega placeholders descriptivos para guiar al usuario.
        """
        super().__init__(*args, **kwargs)
        # Placeholders personalizados para cada campo
        placeholders = {
            'username': 'Elegí tu nombre de jugador',
            'email': 'tu@email.com',
            'password1': 'Mínimo 8 caracteres',
            'password2': 'Repetí la contraseña',
        }
        for campo, placeholder in placeholders.items():
            self.fields[campo].widget.attrs.update({
                'class': 'form-control',       # Clase de Bootstrap
                'placeholder': placeholder,     # Texto guía dentro del input
            })

    def save(self, commit=True):
        """Guarda el usuario asegurando que el email se almacene.

        El UserCreationForm por defecto no guarda el email porque no
        lo incluye en sus campos. Acá lo asignamos manualmente antes
        de guardar en la base de datos.
        """
        user = super().save(commit=False)
        # Asignamos el email que ingresó el usuario al objeto User
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user


class FormularioLogin(AuthenticationForm):
    """Formulario de inicio de sesión.

    Extiende el AuthenticationForm de Django aplicando estilos Bootstrap
    y placeholders a los campos de usuario y contraseña.
    """

    def __init__(self, *args, **kwargs):
        """Agrega clases CSS y placeholders a los campos de login."""
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Tu nombre de jugador',
        })
        self.fields['password'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Tu contraseña',
        })
