from django.core.exceptions import ImproperlyConfigured
from django.utils.importlib import import_module

def import_class(dotted_path):
    """
    Import and return the class described by the given standard
    python dotted path.
    """

    # logic flow to find and import the configured backend class
    # taken from django-registration

    i = dotted_path.rfind('.')
    module, attr = dotted_path[:i], dotted_path[i+1:]

    try:
        mod = import_module(module)
    except ImportError, e:
        raise ImproperlyConfigured(
                "Error loading module {}: '{}'".format(module, e))
    try:
        klass = getattr(mod, attr)
    except AttributeError:
        raise ImproperlyConfigured(
                "Module '{}' does not define '{}'".format(module, attr))
    return klass
