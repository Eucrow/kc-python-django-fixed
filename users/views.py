from django.contrib.auth import authenticate, login as django_login, logout as django_logout
from django.contrib.auth.models import User
from django.shortcuts import redirect, render
from django.utils.safestring import mark_safe
from django.views import View
from django.views.generic import TemplateView

from users.forms import SignUpForm


def login(request):
    """
    Presenta el formulario de login y gestiona el login de un usuario
    Args:
        request: objeto httpRequest con los datos de la petición
    Returns: objeto HttpResponse con los datos de la respuesta

    """
    error_message = ""

    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('pwd')
        user = authenticate(username=username, password=password)
        if user is None:
            error_message = "Usuario o contraseña incorrecta"
        else:
            if user.is_active:
                # le decimos que el usuario user está autenticado para las siguientes peticiones que haga
                django_login(request, user)
                return redirect('/')
            else:
                error_message = "Cuenta de usuario inactiva"

    return render(request, 'users/login.html', {'error': error_message})


def logout(request):
    """
    Hace el logout del usuario
    :param request:
    :return:
    """
    if request.user.is_authenticated():
        django_logout(request)

    return redirect('/')


class SignupSuccessfulView(TemplateView):
    """
    Muestra la plantilla signup_success
    """
    template_name = 'users/signup_success.html'


class SignUpView(View):
    def get(self, request):
        """
        Method get to create a new user
        :param request: HttpRequest object
        :return: HttpResponse object with the response
        """
        message = None

        user_form = SignUpForm()
        context = {'form': user_form, 'message': message}
        return render(request, 'users/signup.html', context)

    def post(self, request):
        """
        Muestra el formulario para crear un usuario nuevo
        :param request:
        :return:
        """
        user_form = SignUpForm(request.POST)

        if user_form.is_valid():
            user = User()
            user.username = user_form.cleaned_data.get('username')
            user.first_name = user_form.cleaned_data.get('first_name')
            user.last_name = user_form.cleaned_data.get('last_name')
            user.email = user_form.cleaned_data.get('email')
            user.password = user_form.cleaned_data.get('password1')

            user.save()

            return redirect('signup_success')
        else:
            context = {'form': user_form}

            return render(request, 'users/signup.html', context)
