from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Course(models.Model):
    name = models.TextField(max_length=200)
    start_at = models.DateTimeField()
    finish_at = models.DateTimeField()
    description = models.TextField(max_length=500)
    created_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=0)

    class Meta:
        ordering = ('start_at',)

    def __str__(self):
        return self.name


class Theme(models.Model):
    course_id = models.ForeignKey(Course, related_name='themes', on_delete=models.CASCADE)
    title = models.TextField(max_length=20)
    description = models.TextField(max_length=100)
    theory = models.TextField()
    order = models.IntegerField(default=1)

    def __str__(self):
        return self.title

    class Meta:
        unique_together = ('course_id', 'order')
        ordering = ['order']

    def __unicode__(self):
        return '%d: %s' % (self.order, self.title)


class UsersCourse(models.Model):
    user_id = models.ForeignKey(User)
    course_id = models.ForeignKey(Course)


class Test(models.Model):
    course_id = models.ForeignKey(Course, related_name='tests', on_delete=models.CASCADE)
    order = models.IntegerField(default=1)
    name = models.TextField()

    class Meta:
        unique_together = ('course_id', 'order')
        ordering = ['order']

    def __unicode__(self):
        return '%d: %s' % (self.order, self.name)


class Question(models.Model):
    test_id = models.ForeignKey(Test, related_name='questions', on_delete=models.CASCADE)
    text = models.TextField()
    order = models.IntegerField(default=1)

    class Meta:
        unique_together = ('test_id', 'order')
        ordering = ['order']

    def __unicode__(self):
        return '%d: %s' % (self.order, self.text)


class TestPossibleAnswers(models.Model):
    question_id = models.ForeignKey(Question, related_name='answers', on_delete=models.CASCADE, default=1)
    answer = models.TextField()
    is_true = models.BooleanField()


class TestResults(models.Model):
    user_id = models.ForeignKey(User)
    test_id = models.ForeignKey(Test)
    result = models.IntegerField(default=0)
