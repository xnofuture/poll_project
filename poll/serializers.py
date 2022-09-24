from rest_framework import serializers
from .models import Poll


class InformationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Poll
        fields = ['pk', 'question', 'is_published']


class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Poll
        fields = ['pk', 'question', 'date_start', 'date_end', 'max_amount', 'winner', 'is_published']


class WinnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Poll
        fields = ['pk', 'question', 'winner']


class VotesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Poll
        fields = ['pk', 'question', 'winner']