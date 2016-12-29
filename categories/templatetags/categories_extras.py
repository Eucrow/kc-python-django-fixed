from django import template

from categories.models import Category

register = template.Library()

@register.inclusion_tag('categories/categories_menu.html')
def list_categories(category):
    """
    Create a dictionary with all the categories
    :param category: this is a Category object
    :return: a dictionary with the categories
    """
    categories = Category.objects.all()
    return {'categories': categories}