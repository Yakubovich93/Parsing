from django.db import models

# Create your models here.

class Product(models.Model):
    title = models.TextField(
        verbose_name='title',
    )
    company = models.TextField(
        verbose_name='company',
    )
    date = models.DateField(
        verbose_name='date',

    )
    link = models.URLField(
        verbose_name='link',
        unique=True,
    )

    def __str__(self):
        return f'{self.id} {self.title} {self.company} {self.date} {self.link}'
