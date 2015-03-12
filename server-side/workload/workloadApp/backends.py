from shibboleth.backends import ShibbolethRemoteUserBackend
from models import Student
from django.contrib.auth import get_user_model
import re


class CustomShibboBackend(ShibbolethRemoteUserBackend):

    def authenticate(self, remote_user, meta):
        if not remote_user:
            return
        user = None
        username = self.clean_username(remote_user)
        UserModel = get_user_model()

        user, created = UserModel._default_manager.get_or_create(**{
            UserModel.USERNAME_FIELD: username
        })
        if created:
            user = self.configure_user(user,meta)
        student , _ = Student.objects.get_or_create(user=user)
        # update student object on every load
        student.semesterOfStudy = int(meta["terms-of-study"])
        student.save()
        return user

    def clean_username(self,value):
        # find relevant substring of shibboleth attribute
        regex = re.compile("de/shibboleth\!(.*)=")
        value = regex.findall(value)[-1]
        # remove special characters
        value = ''.join(e for e in value if e.isalnum())
        return value
