"""Tests for user voting."""
import datetime

from django.test import TestCase
from django.utils import timezone
from django.shortcuts import reverse
from django.contrib.auth.models import User

from polls.models import Question


class VotingTest(TestCase):
    """Test cases for voting the polls."""

    def setUp(self):
        """Initialize logged in user and the question with choices."""
        self.question = Question.objects.create(
            question_text='Test question',
            pub_date=timezone.now(),
            end_date=timezone.now() + datetime.timedelta(days=30)
        )
        for i in range(4):
            self.question.choice_set.create(choice_text='test choice {i}')
        self.user = {
            'username': 'danyouknowme',
            'password': 'dannysk123'
        }
        self.user1 = User.objects.create_user(**self.user)
        self.user1.save()

    def test_authenticated_vote(self):
        """The authenticated user can vote for the polls."""
        self.client.post(reverse('login'), self.user)
        url = reverse('polls:vote', args=(self.question.id,))
        response = self.client.get(url)
        self.assertTrue(response.context['user'].is_active)
        self.assertEqual(response.status_code, 200)
        response = self.client.post(url, {'choice': 2})
        self.assertTrue(self.question.vote_set.filter(question=self.question).exists)
        self.assertEqual(response.status_code, 302)

    def test_unauthenticated_vote(self):
        """The vote will be restrict for unauthenticated user."""
        self.client.post(reverse('logout'))
        url = reverse('polls:index')
        response = self.client.get(url)
        self.assertFalse(response.context['user'].is_active)
        self.assertEqual(response.status_code, 200)
        url = reverse('polls:vote', args=(self.question.id,))
        response = self.client.post(url, {'choice': 4})
        self.assertEqual(response.status_code, 302)
