from django.db import models
from django.conf import settings

class Profile(models.Model):
    _gender = (
        ('M', 'Male', ),
        ('F', 'Female', ),
    )

    # Django의 User 모델과 1:1 관계로 생성.
    user = models.OneToOneField(settings.AUTH_USER_MODEL)
    gender = models.CharField(max_length=1, choices=_gender)