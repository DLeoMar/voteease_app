from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Position)
admin.site.register(Candidate)
admin.site.register(Education)
admin.site.register(LeadershipExperience)
admin.site.register(Award)
admin.site.register(CustomUser)
admin.site.register(Vote)