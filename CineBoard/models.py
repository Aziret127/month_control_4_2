from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
# Create your models here.

class CustomUser(User):
    photo = models.ImageField(upload_to='users/')
    photo_number = models.CharField(max_length=15, default="+996")
    GENDER = (
        ('MALE', 'MALE'),
        ('FEMALE', 'FEMALE'),
    )

    gender = models.CharField(max_length=100, choices=GENDER, default='MALE')
    city = models.CharField(max_length=100, default='бишкек')

    def __str__(self):
        return self.username
    

    
class Movie(models.Model):

    title = models.CharField(max_length=100, verbose_name="название фильма")

    description = models.TextField(verbose_name="описание фильма")

    crated_date_lang = models.PositiveIntegerField(verbose_name="год выпуска фильма", blank=True, null=True)
   
    views = models.PositiveIntegerField(default=0, null=True)

    created_at = models.DateTimeField(auto_now_add=True,)

    name_genre = models.CharField(max_length=100, verbose_name="жанр", null=True, blank=True)
    
    ratiog = models.PositiveBigIntegerField(verbose_name="рейтинг фильма", blank=True, null=True)

    def __str__(self):
         return self.title

    class Meta:
        verbose_name = "Фильм"
        verbose_name_plural = "Фильмы"

    def get_absolute_url(self):
        return reverse('cineboard:movie_detail', kwargs={'id': self.pk})
   
    def get_fields(self):
        return [(field.name, getattr(self, field.name)) for field in self._meta.fields]

class Tag(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
class Review(models.Model):
    MARKS = (
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
    )
    
    marks = models.CharField(max_length=100, choices=MARKS, default='5')
    text = models.CharField(max_length=100, default="отличный фильм")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Оценка:{self.marks}-Коммент:{self.text}'
    
