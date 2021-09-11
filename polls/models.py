import datetime

from django.db import models
from django.utils import timezone

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    end_date = models.DateTimeField('date ended')

    def was_published_recently(self):
        """Check the question was published recently

        Returns:
            bool: True if the question was published recently False otherwise
        """
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.pub_date <= now
    was_published_recently.admin_order_field = 'pub_date'
    was_published_recently.boolean = True
    was_published_recently.short_description = "Published recently ?"

    def is_published(self):
        """Check the current date is on the published date

        Returns:
            bool: True if the current date is on published date, False otherwise
        """
        now = timezone.now()
        return now >= self.pub_date

    def can_vote(self):
        """Check the current date is between published date and end date
        
        Returns:
            bool: True if the current date can vote, False otherwise
        """
        now = timezone.now()
        return self.pub_date <= now <= self.end_date

    def __str__(self):
        return self.question_text

class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text