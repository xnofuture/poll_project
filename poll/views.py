from django.shortcuts import render, get_object_or_404, redirect
from .models import Poll, Answer
from django.utils import timezone
from django.db import IntegrityError


def home(request):
    polls = Poll.objects.filter(is_published=True)
    context = {
        'polls': polls,
    }
    # Удаление голосования из списка активных
    for time in polls:
        if time.date_end <= timezone.now() :
            time.is_published = False
            time.save()
    return render(request, 'poll/home.html', context=context)


def vote(request, poll_id):
    question = get_object_or_404(Poll, pk=poll_id)
    answers = Answer.objects.filter(answer_id=poll_id)
    context = {
        'question': question,
        'answers': answers,
    }

#   Добавление голоса для участника голосования
    if request.method == 'POST':
        for i in answers:
            if i.name == (request.POST.get("poll", False)):
                i.vote += 1
                i.save()
                return redirect('results', question.id)

#   Проверка на победителя и удаления опроса из списка всех вопросов
    for i in answers:
        if i.vote >= question.max_amount:
            question.winner = request.POST.get("poll", False)
            question.is_published = False
            question.save()

    return render(request, 'poll/vote.html', context=context)


def results(request, poll_id):
    result = get_object_or_404(Poll, pk=poll_id)
    answers = Answer.objects.filter(answer_id=poll_id)

    context = {
        'result': result,
        'answers': answers,
    }
    return render(request, 'poll/results.html', context=context)



