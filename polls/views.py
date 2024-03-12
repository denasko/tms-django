from django.shortcuts import render, HttpResponse, get_object_or_404, redirect
from django.utils import timezone
from django.views import generic
from django_rq import job
from django.db.models import F

from polls.forms import QuestionForm, FeedbackForm
from polls.models import Question, Choice

feedback = []


@job
def get_view_count(question: Question):
    print(f'start {question.view_count}')
    question.view_count = F('view_count') + 1
    question.save()
    print(f'finish {question.view_count}')


class IndexView(generic.ListView):
    template_name = "polls/index.html"
    context_object_name = "latest_question_list"

    def get_queryset(self):
        """Return the last five published questions."""
        return Question.objects.filter(pub_date__lte=timezone.now()).order_by("pub_date")[:5]


class DetailView(generic.DetailView):
    model = Question
    template_name = "polls/detail.html"

    def get(self, request, *args, **kwargs):
        question = self.get_object()
        get_view_count.delay(question)
        return super().get(request, *args, **kwargs)


class ResultsView(generic.DetailView):
    model = Question
    template_name = "polls/results.html"


def about(request: HttpResponse) -> str:
    return render(request, 'polls/about.html')


def vote(request: HttpResponse, question_id: int) -> str:
    question = get_object_or_404(Question, id=question_id)
    try:
        selected_choice = question.choices.get(id=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'polls/detail.html', {
            'error_message': "You didn't select a choice",
            'question': question})
    selected_choice.votes += 1
    selected_choice.save()
    return redirect('polls:results', question.id)


def create_question(request: HttpResponse) -> str:
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        if form.is_valid():
            question_text = form.cleaned_data['question_text']
            pub_date = form.cleaned_data['publication_date']
            question = Question(question_text=question_text,
                                pub_date=pub_date)
            question.save()
            for choice_text in form.cleaned_data['choices'].split('\n'):
                question.choices.create(choice_text=choice_text, votes=0)
            return redirect('polls:detail', question.id)
    else:
        form = QuestionForm()
        data = {'form': form}
        return render(request, 'polls/create_question.html', context=data)


def create_feedback(request: HttpResponse) -> str:
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback_text = form.cleaned_data['feedback_text']
            feedback.append(feedback_text)
            print(feedback)
            return redirect('polls:index')
    else:
        form = FeedbackForm()
        data = {'form': form}
    return render(request, 'polls/feedback.html', context=data)
