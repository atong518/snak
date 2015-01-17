from django.contrib.auth.models import check_password
from app.models import GenericUser

class EmailAuthBackend(object):
    """
    Email Authentication Backend
    
    Allows a user to sign in using an email/password pair rather than
    a username/password pair.
    """
    
    def authenticate(self, email=None, password=None):
        """ Authenticate a user based on email address as the user name. """
        try:
            user = GenericUser.objects.get(email=email)
            if user.check_password(password):
                return user
        except GenericUser.DoesNotExist:
            return None 

    def get_user(self, user_id):
        """ Get a User object from the user_id. """
        try:
            return GenericUser.objects.get(pk=user_id)
        except GenericUser.DoesNotExist:
            return None
