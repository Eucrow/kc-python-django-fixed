from django.shortcuts import render
from django.template.defaulttags import register

from categories.models import Category


def home(request):
    """
    Show list of categories
    :param request: httpRequest object with the asked data
    :return: httpResponse object with the response data
    """

    categories = Category.objects.all().order_by('-name')
    context = {'categories_list': categories}

    return render(request, 'categories/categories.html', context)



