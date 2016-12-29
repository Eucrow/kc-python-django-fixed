from blogs.models import Blogs
from django.forms import ModelForm

class BlogCreationForm(ModelForm):

    class Meta:
        model = Blogs
        exclude =['owner']

    def clean(self):
        """
        Valida que la descripción no tenga tacos
        Returns: diccionario con los datos limpios y validados
        """
        cleaned_data = super().clean()
        return cleaned_data #el método clean tiene que devolver los datos validados
