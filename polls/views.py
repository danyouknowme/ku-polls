"""Views to render templates for Poll application."""
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.views import generic
from django.utils import timezone
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import Question, Choice


class IndexView(generic.ListView):
    """Index page represent the latest question."""

    template_name = 'polls/index.html'
    context_object_name = 'latest_question_list'

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:5]

def detail(request, question_id):
    """Question detail page represent the question text and choice to vote."""
    question = get_object_or_404(Question, pk=question_id)
    if not question.can_vote():
        messages.error(request, 'Voting is not allowed!')
        return redirect('polls:index')
    prev_choice = question.vote_set.get(user=request.user).choice
    return render(request, 'polls/detail.html', {'question': question, 'previous_choice': prev_choice})


class ResultsView(generic.DetailView):
    """Poll results page represent the result of each choice for a question."""

    model = Question
    template_name = 'polls/results.html'


@login_required
def vote(request, question_id):
    """Increase a value of vote and save to vote result."""
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice."
        })
    else:
        if question.vote_set.filter(user=request.user).exists():
            vote = question.vote_set.get(user=request.user)
            vote.choice = selected_choice
            vote.save()
        else:
            selected_choice.vote_set.create(user=request.user, question=question)
        return HttpResponseRedirect(
            reverse('polls:results', args=(question.id,))
        )
