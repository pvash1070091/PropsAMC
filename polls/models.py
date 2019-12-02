from django.db import models

# Create your models here.

class Question(models.Model):
    ques_text=models.CharField(max_length=100)
    pub_date=models.DateTimeField('date pub')
    def __str__(self):
        return self.ques_text

class Choice(models.Model):
    question=models.ForeignKey(Question,on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=100)
    votes=models.IntegerField(default=0)
    def __str__(self):
        return self.choice_text

class Document(models.Model):
    description = models.CharField(max_length=255, blank=True)
    document = models.FileField(upload_to='documents/')
    def __str__(self):
        return self.description

class Address(models.Model):
    add = models.CharField(max_length=200)
    lat=models.FloatField()
    lon=models.FloatField()
    def __str__(self):
        return self.add