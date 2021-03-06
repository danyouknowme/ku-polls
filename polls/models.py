"""The models for polls application."""
import datetime

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Question(models.Model):
    """Question model to representing the polls question."""

    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    end_date = models.DateTimeField('date ended', default=timezone.now)

    def was_published_recently(self):
        """Check the question was published recently.

        Returns:
            bool: True if the question was published recently False otherwise
        """
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now
    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = "Published recently ?"

    def is_published(self):
        """Check the current date is on the published date.

        Returns:
            bool: True if current date is on published date, False otherwise
        """
        now = timezone.now()
        return now >= self.pub_date

    def can_vote(self):
        """Check the current date is between published date and end date.

        Returns:
            bool: True if the current date can vote, False otherwise
        """
        now = timezone.now()
        return self.pub_date <= now <= self.end_date

    def __str__(self):
        """Return the content of question text."""
        return self.question_text


class Choice(models.Model):
    """Choice model to representing the choice of polls question."""

    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)

    def __str__(self):
        """Return the content of choice text."""
        return self.choice_text

    @property
    def votes(self):
        """Return the number of votes on the choice of polls question."""
        return Vote.objects.filter(choice=self).count()


class Vote(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=0)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE, default=0)
