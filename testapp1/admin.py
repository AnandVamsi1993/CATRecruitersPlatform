from django.contrib import admin
from testapp1.models import Consultant, Recruiter, Submissions

# Register your models here.
admin.site.register(Consultant)
admin.site.register(Recruiter)
admin.site.register(Submissions)
