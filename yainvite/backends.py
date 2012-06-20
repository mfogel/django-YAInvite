"InviteBackend framework, sample implementations"

from django.conf import settings
from django.contrib.sites.models import Site
from django.core.exceptions import ImproperlyConfigured
from django.utils.importlib import import_module


def get_backend_class():
    "Get a class object of the currently configured InviteBackend class"

    # logic flow to find and import the configured backend class
    # taken from django-registration

    path = settings.YAINVITE_BACKEND
    i = path.rfind('.')
    module, attr = path[:i], path[i+1:]
    try:
        mod = import_module(module)
    except ImportError, e:
        raise ImproperlyConfigured('Error loading invite backend %s: "%s"' % (module, e))
    try:
        backend_class = getattr(mod, attr)
    except AttributeError:
        raise ImproperlyConfigured('Module "%s" does not define a registration backend named "%s"' % (module, attr))
    return backend_class


def get_backend(request):
    "Get an instance of the currently configured InviteBackend"
    return get_backend_class()(request)


class InviteBackend(object):
    """
    Base Class for InviteBackends. For custom InviteBackends, subclass
    me and adjust ``YAINVITE_BACKEND`` appropriately.

    An InviteBackend takes either an django HTTP Request for initialization.
    It provides two properties:

        self.inviter                    (readonly)
        self.number_invites_remaining   (read/write)

    See the examples below for futher clarification.
    """

    def __init__(self, request):
        super(InviteBackend, self).__init__()
        self.request = request

    @property
    def inviter(self):
        raise NotImplemented('Subclass and override me')

    def _get_number_invites_remaining(self):
        raise NotImplemented('Subclass and override me')
    def _set_number_invites_remaining(self, number):
        raise NotImplemented('Subclass and override me')
    number_invites_remaining = property(
            _get_number_invites_remaining, _set_number_invites_remaining)


class UnlimitedInvitesMixin(object):
    "Mixin that allows unlimited invites to be sent"
    the_answer = 42

    def _get_number_invites_remaining(self):
        return self.the_answer
    def _set_number_invites_remaining(self, number):
        pass
    number_invites_remaining = property(
            _get_number_invites_remaining, _set_number_invites_remaining)


class UserInviterMixin(object):
    "Mixin that implements auth.User objects being used to send Invites"
    def __init__(self, request):
        super(UserInviterMixin, self).__init__(request)
        self.user = request.user

    @property
    def inviter(self):
        return self.user


######## Sample Backends ########


class SiteBackend(UnlimitedInvitesMixin, InviteBackend):
    """
    A backend implementation for the following scenario:
        1. Invites come from Site objects
        2. Everyone always has 42 invites left.

    Require settings:
        * YAINVITE_INVITER_CLASS = 'sites.Site'
        * YAINVITE_INVITER_DB_TABLE = 'django_site'
    """

    def __init__(self, request):
        super(SiteBackend, self).__init__(request)
        self.site = Site.objects.get_current()

    @property
    def inviter(self):
        return self.site


class UserUnlimitedBackend(
        UserInviterMixin, UnlimitedInvitesMixin, InviteBackend):
    """
    A backend implementation for the following scenario:
        1. Invites come from User objects
        2. Everyone always has 42 invites left.

    Requires settings.YAINVITE_INVITER_CLASS = 'auth.User'
    """
    pass


class UserProfileBackend(UserInviterMixin, InviteBackend):
    """
    A backend implementation for the following scenario:
        1. Invites come from User objects
        2. There is a 'number_invites_remaining' property on the User's
           profile object. All Users are assumed to have profiles.

    Requires settings.YAINVITE_INVITER_CLASS = 'auth.User'
    """

    def _get_number_invites_remaining(self):
        return self.user.get_profile().number_invites_remaining
    def _set_number_invites_remaining(self, number):
        profile = self.user.get_profile()
        profile.number_invites_remaining = number
        profile.save()
    number_invites_remaining = property(
            _get_number_invites_remaining, _set_number_invites_remaining)
