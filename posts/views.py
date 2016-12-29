from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.db.models import F
from django.db.models import Q
from django.http import HttpResponse
from django.http import HttpResponseNotFound
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.views import View
from time import localtime, strftime

from categories.models import Category
from posts.forms import PostCreationForm
from posts.models import Post

from django.urls import reverse


class Home(View):
    def get(self, request):
        """
        Renderiza el home con un listado de posts
        Args:
            request: objeto httpRequest con los datos de la petición
        Returns: objeto HttpResponse con los datos de la respuesta

        """
        # recupera todos los posts de la base de datos
        date_now = strftime("%Y-%m-%d", localtime())
        time_now = strftime("%H:%M:%S", localtime())
        posts = Post.objects.all().filter(
            Q(publication_date=date_now, publication_time__lte=time_now) | Q(publication_date__lt=date_now)).order_by(
            '-created_at')
        context = {'posts_list': posts}
        return render(request, 'posts/home.html', context)


class PostListQuerySet(object):  # crea la queryset con el listado de artículos
    @staticmethod
    def get_posts_by_user(user):
        """
        Create the queryset whith the posts list inside blog
        :param user:
        :return:
        """
        date_now = strftime("%Y-%m-%d", localtime())
        time_now = strftime("%H:%M:%S", localtime())

        possible_posts = Post.objects.all().select_related("owner")
        if not user.is_authenticated():  # si no está autenticado, puede ver sólo aquellos ya publicados
            possible_posts = possible_posts.filter(
                Q(publication_date=date_now, publication_time__lte=time_now) | Q(publication_date__lt=date_now))
        elif not user.is_superuser:  # si está autenticado y no es superusuario ve todos los publicados y los suyos no publicados
            possible_posts = possible_posts.filter(
                Q(publication_date=date_now, publication_time__lte=time_now) | Q(publication_date__lt=date_now) | Q(
                    owner=user))
        # y si está autenticado y es superusuario, entonces devuelverá todos
        return possible_posts  # possible_post es una queryset


class PostDetail(View):
    def get(self, request, pk):
        """
        Recupera el detalle del post
        :param request: objeto httpRequest con los datos de la petición
        :return: objeto httpResponse con los datos de la respuesta
        """
        date_now = strftime("%Y-%m-%d", localtime())
        time_now = strftime("%H:%M:%S", localtime())

        possible_post = Post.objects.all().filter(
            Q(publication_date=date_now, publication_time__lte=time_now, pk=pk) | Q(publication_date__lt=date_now,
                                                                                    pk=pk))
        if len(possible_post) == 0:
            return HttpResponseNotFound("Ese post que buscas no existe")
        elif len(possible_post) > 1:
            return HttpResponse("Múltiples opciones", status=300)

        post = possible_post[0]
        context = {'post': post}
        return render(request, 'posts/post_detail.html', context)


class PostCreationView(View):
    @method_decorator(login_required())
    def get(self, request):
        """
        Method get to create a new post
        :param request: HttpRequest object
        :return: HttpResponse object with the response
        """
        message = None

        categories = Category.objects.all()

        post_form = PostCreationForm()
        context = {'form': post_form, 'categories_list': categories, 'message': message}
        return render(request, 'posts/post_creation.html', context)

    @method_decorator(login_required())
    def post(self, request):
        """
       Presenta el formuario para crear un post y en el caso de que la petición sea post la valida
       y la crea en el caso de que sea válida
       Args:
       request:
       returns:
       """
        message = None
        post_with_user = Post(owner=request.user)
        post_form = PostCreationForm(request.POST, instance=post_with_user)

        if post_form.is_valid():
            new_post = post_form.save()
            # post_form = PostCreationForm()  # vaciamos el formulario
            message = 'Artículo creado satisfactoriamente <a href="{0}">Ver artículo</a>'.format(
                reverse('post_detail', args=[new_post.pk]))

        context = {'form': post_form, 'message': message}
        # return render(request, 'posts/post_creation.html', context)
        messages.add_message(request, messages.INFO, "Artículo creado satisfactoriamente")
        return redirect(reverse('post_detail', args=[new_post.pk]))
