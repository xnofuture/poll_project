from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404, redirect
from .models import Poll, Answer
from django.utils import timezone
from django.db import IntegrityError
from rest_framework import generics
from .serializers import *


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
        print(request.POST["poll"])
        for i in answers:
            if i.name == request.POST["poll"]:
                i.vote += 1
                i.save()
                return redirect('results', question.id)
    return render(request, 'poll/vote.html', context=context)


def results(request, poll_id):
    result = get_object_or_404(Poll, pk=poll_id)
    answers = Answer.objects.filter(answer_id=poll_id)
    #Определение победителя голосования и изменение публикации активных голосований
    for i in answers:
        if i.vote >= result.max_amount:
            result.winner = i.name
            result.is_published = False
            result.save()
    context = {
        'result': result,
        'answers': answers,
    }
    return render(request, 'poll/results.html', context=context)


def loginuser(request):
    if request.method == 'GET':
        return render(request, 'poll/loginuser.html', {'form': AuthenticationForm()})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'poll/loginuser.html', {'form': AuthenticationForm(), 'error': 'Неверный логин или пароль'})
        else:
            login(request, user)
            return redirect('home')


def signupuser(request):
    if request.method == 'GET':
        return render(request, 'poll/signupuser.html', {'form': UserCreationForm()})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
                user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect('home')
            except IntegrityError:
                return render(request, 'poll/signupuser.html', {'form': UserCreationForm(), 'error': 'Имя пользователя уже занято, выберите другое имя'})
        else:
            return render(request, 'poll/signupuser.html', {'form': UserCreationForm(), 'error': 'Пароли не совпадают,проверьте'})


def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')


class InformationAPIView(generics.ListAPIView):
    queryset = Poll.objects.all()
    serializer_class = InformationSerializer


class QuestionAPIView(generics.ListAPIView):
    queryset = Poll.objects.all()
    serializer_class = QuestionSerializer


class WinnerAPIView(generics.ListAPIView):
    queryset = Poll.objects.filter(is_published=False)
    serializer_class = WinnerSerializer


class VotesAPIView(generics.ListAPIView):
    queryset = Answer.objects.filter()
    serializer_class = VotesSerializer
