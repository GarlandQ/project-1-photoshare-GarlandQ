from django.http import HttpResponseRedirect
from django.conf import settings

# wrapper function to redirect authenticated users
# the opposite of login_required
def anonymous_required(view_function):
    return AnonymousRequired(view_function)

class AnonymousRequired(object):
    def __init__(self, view_function):
        self.view_function = view_function
        self.redirect_to = settings.LOGIN_REDIRECT_URL

    def __call__(self, request, *args, **kwargs):
        if request.user is not None and request.user.is_authenticated:
            return HttpResponseRedirect(self.redirect_to)
        return self.view_function(request, *args, **kwargs)
