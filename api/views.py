from django.shortcuts import get_object_or_404, redirect
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.request import Request

from polls.models import Question, Choice
from .serializers import QuestionSerializer, ChoiceSerializer


class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer


class ChoiceViewSet(viewsets.ModelViewSet):
    queryset = Choice.objects.all()
    serializer_class = ChoiceSerializer


@api_view(['POST'])
def choice_vote(request: Request, question_id: int) -> str:
    question = get_object_or_404(Question, pk=question_id)
    selected_choice = get_object_or_404(question.choices, pk=request.data['choice'])
    selected_choice.votes += 1
    selected_choice.save()
    return redirect('question-detail', question_id)
