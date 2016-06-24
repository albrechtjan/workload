from shibboleth.backends import ShibbolethRemoteUserBackend
from models import Student
from django.contrib.auth import get_user_model
import re
import logging
logger = logging.getLogger(__name__)


class CustomShibboBackend(ShibbolethRemoteUserBackend):
    """ This class extends the use backend from the django-shibboleth-adapter app.

        It implements the clean_username method and attempts to determine and save the 
        semester of study in the authenticate() method
        This also meant that the semester of study is only updated for the user when
        he authenticates.
    """

    def authenticate(self, remote_user, meta):
        """ Returns the User object with the given username

        The username passed as `remote_user` is considered trusted.  This
        method simply returns the `User` object with the given username,
        creating a new `User` object if `create_unknown_user` is `True`.
        Returns None if `create_unknown_user` is `False` and a `User`
        object with the given username is not found in the database.
        """
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
        try:
            logger.info(meta)
            regex = re.compile("\$ (\d*)") #capturing the semester of study which seems to follow a number indicating the course of study and a $ sign.
            student.semesterOfStudy = int( regex.findall(meta["terms-of-study"])[0] )
        except KeyError:
            # if the study term is not defined, set it to zero
            student.semesterOfStudy = 0
        except ValueError:
            #unable to convert value to integer
            student.semesterOfStudy = 0
        student.save()
        return user

    def clean_username(self,value):
        """ This method extracts a substring from the shibboleth
            attribute used for user identification.
            Its implementation must be updated depending the 
            shibboleth attribute used for authentication.

            This implmentation assumes that the 
            `remote_user` attribute is passed as `value`.
            This is a rather long string with many special characters. 
            A substring of it is enough to uniquely identify the user.
            This substring is 
        """
        # find relevant substring of shibboleth attribute
        regex = re.compile("de/shibboleth\!(.*)=")
        value = regex.findall(value)[-1]
        # remove special characters
        value = ''.join(e for e in value if e.isalnum())
        return value
