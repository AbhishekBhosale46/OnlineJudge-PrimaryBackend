from django.contrib import admin
from core import models

admin.site.register(models.User)
admin.site.register(models.Problem)
admin.site.register(models.Language)
admin.site.register(models.TestCase)
admin.site.register(models.Submission)
admin.site.register(models.TestCaseResult)