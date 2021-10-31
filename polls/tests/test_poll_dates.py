import datetime

from django.test import TestCase
from django.utils import timezone

from polls.models import Question

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