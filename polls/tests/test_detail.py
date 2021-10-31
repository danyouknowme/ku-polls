import datetime

from django.test import TestCase
from django.utils import timezone
from django.shortcuts import reverse

from polls.models import Question

def create_question(question_text, days):
    """Create a question with question_text and published date."""
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)

class QuestionDetailViewTests(TestCase):
    """Test for question in detail view."""

    def test_future_question(self):
        """The detail view of a question with a pub_date in the future.

        This is should return 404 not found.
        """
        future_question = create_question(
                question_text="Future question.",
                days=5
            )
        url = reverse('polls:detail', args=(future_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    def test_past_question(self):
        """The detail view of a question with a pub_date in the past."""
        past_question = create_question(
                question_text="Past question.",
                days=-5
            )
        past_question.end_date = timezone.now() + datetime.timedelta(days=-4)
        url = reverse('polls:detail', args=(past_question.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)
