from django.db import models


class Poll(models.Model):
    question = models.TextField()
    date_start = models.DateTimeField(auto_now=True)
    date_end = models.DateTimeField()
    max_amount = models.IntegerField(default=0)
    is_published = models.BooleanField(default=True)
    winner = models.CharField(max_length=50, default='Nobody')

    def __str__(self):
        return self.question


class Answer(models.Model):
    answer = models.ForeignKey('Poll', on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    #photo = models.ImageField(upload_to='photos/')
    age = models.IntegerField()
    biography = models.TextField(blank=True)
    vote = models.IntegerField(default=0)

    def __str__(self):
        return self.name
