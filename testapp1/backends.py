from django.contrib.auth.backends import ModelBackend
from testapp1.models import Recruiter


class RecruiterBackend(ModelBackend):
    def authenticate(self, request, username = None, password = None, **kwargs):
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            recruiter = Recruiter.objects.get(R_UserName = username)
            if recruiter.check_password(password):
                return recruiter
        except Recruiter.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return Recruiter.objects.get(pk = user_id)
        except Recruiter.DoesNotExist:
            return None
