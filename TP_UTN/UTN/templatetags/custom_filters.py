from django import template

register = template.Library()

@register.filter
def get_item(dictionary, key):
    """Permite acceder a un elemento de un diccionario usando la clave en el template."""
    return dictionary.get(key)