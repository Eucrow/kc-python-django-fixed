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

import pytz
from django.urls import reverse

from datetime import datetime


class Home(View):
    def get(self, request):
        """
        Renderiza el home con un listado de posts
        Args:
            request: objeto httpRequest con los datos de la petición
        Returns: objeto HttpResponse con los datos de la respuesta

        """

        posts = PostListQuerySet.get_posts_by_user(request.user)

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
        elif user.is_authenticated() and not user.is_superuser:  # si está autenticado y no es superusuario ve todos los publicados y los suyos no publicados
            possible_posts = possible_posts.filter(
                Q(publication_date=date_now, publication_time__lte=time_now) | Q(owner=user))
        elif user.is_authenticated() and user.is_superuser:# y si está autenticado y es superusuario, entonces devuelverá todos
            possible_posts = Post.objects.all()

        return possible_posts.order_by('-publication_at')  # possible_post es una queryset


class PostDetail(View):
    def get(self, request, pk):
        """
        Recupera el detalle del post
        :param request: objeto httpRequest con los datos de la petición
        :return: objeto httpResponse con los datos de la respuesta
        """
        date_now = strftime("%Y-%m-%d", localtime())
        time_now = strftime("%H:%M:%S", localtime())

        # possible_post = Post.objects.all().filter(
        #     Q(publication_date=date_now, publication_time__lte=time_now, pk=pk) | Q(publication_date__lt=date_now,
        #                                                                             pk=pk))

        possible_post = PostListQuerySet.get_posts_by_user(request.user).filter(pk=pk)

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


        complete_date = request.POST.get("publication_date") + " " + request.POST.get("publication_time")


        validate_date = datetime.strptime(complete_date, "%Y-%m-%d %H:%M")

        # Add timezone (avoid warning):
        utc = pytz.utc
        validate_date_utc = utc.localize(validate_date)

        if post_form.is_valid():
            post_form.instance.publication_at = validate_date_utc
            post_form.save()
            # post_form = PostCreationForm()  # vaciamos el formulario
        else:
            context = {'form': post_form, 'message': message}
            return render(request, 'posts/post_creation.html', context)

        messages.add_message(request, messages.INFO, "Artículo creado satisfactoriamente")
        return redirect(reverse('post_detail', args=[post_form.instance.pk]))
