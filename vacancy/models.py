from django.db import models
from django.urls import reverse
# Create your models here.

class Product(models.Model):
    title = models.TextField(
        max_length=255,
        verbose_name='title',
    )
    company = models.TextField(
        max_length=255,
        verbose_name='company',
    )
    date = models.DateField(
        verbose_name='date',

    )
    link = models.URLField(
        max_length=255,
        verbose_name='link',
        unique=True,
    )

    def __str__(self):
        return f'{self.id} {self.title} {self.company} {self.date} {self.link}'

    def get_absolute_url(self):
        return reverse('vacancy:vacancy_details',
                       args=[self.id])