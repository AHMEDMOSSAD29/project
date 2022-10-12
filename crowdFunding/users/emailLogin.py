from django.contrib.auth.backends import BaseBackend
# This Will Get The Authentication from settings.py From All Users 

from django.contrib.auth import get_user_model
# Required To Get ID From user 

from django.db.models import Q 
#Query For Find The Mail or the username while login with Upper or lower case or mixed 

class Email_Or_Username(BaseBackend):
    #GET USER ID

    def get_user(self, user_id):
        try :
            return get_user_model().objects.get(pk=user_id)
        except get_user_model().DoesNotExist :
            return None

    # This Function created for login within email or username : 
    def authenticate(self, request, username= None , password = None ):
        UserModel = get_user_model()
        try : 
            user = UserModel.objects.get(Q(username__iexact=username) |  Q(email__iexact=username))
            if user.check_password(password):
                return user
        except UserModel.DoesNotExist:
            return None
            