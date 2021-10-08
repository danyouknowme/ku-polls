"""Test function to test in Polls applicartion."""
import datetime

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from .models import Question


def create_question(question_text, days):
    """Create a question with question_text and published date."""
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)


class QuestionModelTests(TestCase):
    """Class to test question models."""

    def test_was_published_recently_with_future_question(self):
        """Returns False for questions whose pub_date is in the future."""
        time = timezone.now() + datetime.timedelta(days=30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)

    def test_was_published_recently_with_old_question(self):
        """Returns False for questions whose pub_date is older than 1 day."""
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        """Returns True for questions whose pub_date is within the last_day."""
        time = timezone.now() - \
            datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)

    def test_is_published_with_future_question(self):
        """Returns False for question whose pub_date is in the future."""
        future_question = create_question("Future Question", 15)
        self.assertFalse(future_question.is_published())

    def test_is_published_with_old_question(self):
        """Returns True for question whose pub_date is in the past."""
        older_question = create_question("Older Question", -1)
        self.assertTrue(older_question.is_published())

    def test_is_published_with_recent_question(self):
        """Returns True for question whose pub_date is on current date."""
        recent_question = create_question("Recent Question", 0)
        self.assertTrue(recent_question.is_published())

    def test_can_vote_with_future_question(self):
        """Returns False for question whose date is after a period time."""
        pub_date = timezone.now() + datetime.timedelta(days=5)
        end_date = timezone.now() + datetime.timedelta(days=5)
        future_question = Question(
                "Future Question",
                pub_date=pub_date,
                end_date=end_date
            )
        self.assertFalse(future_question.can_vote())

    def test_can_vote_with_old_question(self):
        """Returns False for question whose date is before a period time."""
        pub_date = timezone.now() - datetime.timedelta(days=5)
        end_date = timezone.now() - datetime.timedelta(days=5)
        old_question = Question(
                "Old Question",
                pub_date=pub_date,
                end_date=end_date
            )
        self.assertFalse(old_question.can_vote())

    def test_can_vote_with_recent_question(self):
        """Return True for question whose current date is on time."""
        pub_date = timezone.now() - datetime.timedelta(days=15)
        end_date = timezone.now() + datetime.timedelta(days=15)
        recent_question = Question(
                "Question on time",
                pub_date=pub_date,
                end_date=end_date
            )
        self.assertTrue(recent_question.can_vote())


class QuestionIndexViewTests(TestCase):
    """Test for question in index view."""

    def test_no_question(self):
        """If no questions exists, an appropriate message is displayed."""
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_past_question(self):
        """Questions with a pub_date in the past will display on page."""
        create_question(question_text="Past question.", days=-30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question.>']
        )

    def test_future_question(self):
        """Questions with a pub_date in the future will not displayed."""
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, "No polls are available.")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_future_question_and_past_question(self):
        """Display only past questions."""
        create_question(question_text="Past question.", days=-30)
        create_question(question_text="Future question.", days=30)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question.>']
        )

    def test_two_past_questions(self):
        """The questions index page may display multiple questions."""
        create_question(question_text="Past question 1.", days=-30)
        create_question(question_text="Past question 2.", days=-5)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            ['<Question: Past question 2.>', '<Question: Past question 1.>']
        )


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
        self.assertEqual(response.status_code, 404)

    def test_past_question(self):
        """The detail view of a question with a pub_date in the past."""
        past_question = create_question(
                question_text="Past question.",
                days=-5
            )
        url = reverse('polls:detail', args=(past_question.id,))
        response = self.client.get(url)
        self.assertContains(response, past_question.question_text)
