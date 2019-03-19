from django.db import models


GENDER = (
    (1, "Female"),
    (2, "Male")
)

GEO = (
    (1, "Europe"),
    (2, "North America"),
    (3, "South America"),
    (4, "Asia"),
    (5, "Africa"),
    (6, "Australia & Oceania"),
    (7, "Antarctica")
)

class Continent(models.Model):
    continent = models.IntegerField(choices=GEO, verbose_name="Continent", default=1)

    def __str__(self):
        return GEO[self.continent-1][1]

class Country(models.Model):
    country = models.CharField(max_length=100,verbose_name="Country",null=True)
    continent = models.ForeignKey(Continent,on_delete=models.CASCADE,null=True)

class StereotypeQuestions(models.Model):
    question = models.CharField(max_length=300)

class PersonalQuestion(models.Model):
    question = models.CharField(max_length=300)

class Participant(models.Model):
    name = models.CharField(max_length=64,verbose_name="Name",default="Stranger")
    gender = models.IntegerField(choices=GENDER, verbose_name="Gender")
    email = models.CharField(max_length=200,null=True,verbose_name="E-mail")
    share_stats = models.BooleanField(default=False, verbose_name="Statistics")
    continent = models.ForeignKey(Continent,on_delete=models.CASCADE,verbose_name="Continent", null=True)
    country = models.ForeignKey(Country,on_delete=models.CASCADE,verbose_name="Country",null=True)
    user_id = models.CharField(max_length=255,null=True)

class AnswersStereo(models.Model):
    participant = models.ForeignKey(Participant,on_delete=models.CASCADE)
    question_stereo = models.ForeignKey(StereotypeQuestions,on_delete=models.CASCADE)
    answer_stereo = models.IntegerField(choices=GENDER)

class AnswersPersonal(models.Model):
    participant = models.ForeignKey(Participant,on_delete=models.CASCADE)
    question_personal = models.ForeignKey(PersonalQuestion,on_delete=models.CASCADE)
    answer_personal = models.BooleanField(null=True)
