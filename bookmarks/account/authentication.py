from django.contrib.auth.models import User

"""
We are customizing the Authentication backend so users can enter email id instead of username incase they forgot.
to login into our site.

so edit AUTHENTICATION_BACKENDS in settings.py and add this 'account.authentication.EmailAuthBackend'
"""
class EmailAuthBackend(object):
    """
    Authenticate using e-mail account.
    """
    def authenticate(self, username=None, password=None):
        try:
            user = User.objects.get(email=username)
            if user.check_password(password):
                return user
            return None
        except User.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None