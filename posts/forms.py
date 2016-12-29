from posts.models import Post
from django.forms import ModelForm

class PostCreationForm(ModelForm):

    class Meta:
        model = Post
        exclude =['owner']

    def clean(self):
        """
        Valida los datos
        Returns: diccionario con los datos limpios y validados
        """
        cleaned_data = super().clean()
        return cleaned_data #el método clean tiene que devolver los datos validados
