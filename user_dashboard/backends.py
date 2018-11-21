from .models import CustomUser
from bcrypt import checkpw
from django.core.exceptions import ValidationError
import hashlib

class UserModelAuth(object):
    def authenticate(username, password):
        try:
            user = CustomUser.objects.get(email=username)
            if checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
                api_token = hashlib.sha256((username + password).encode()).hexdigest()
                CustomUser.objects.filter(email=username).update(api_token=api_token)
                return user
            else:
                print ('Email atau Password Anda Salah')

        except CustomUser.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            user = CustomUser.objects.get(id=user_id)
            return user

        except CustomUser.DoesNotExist:
            return None