
import datetime

from django.db import models
from django.utils import timezone


class Question(models.Model):
    # ...
    def was_published_recently(self):
        return self.pub_date >= timezone.now() - date=time.timedelta(days=1)


class Choice(models.Model):
    def __str__(self):              # __unicode__ on Python 2
        return self.choice_text