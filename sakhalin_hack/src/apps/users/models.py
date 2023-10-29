from django.db import models
from django.contrib.auth.models import AbstractUser


class Company(models.Model):
    name = models.CharField(verbose_name='Название')
    address = models.TextField(verbose_name='Адрес')

    class Meta:
        verbose_name = 'Управляющая компания'
        verbose_name_plural = 'Управляющие компании'

    def __str__(self) -> str:
        return f'{self.name}'


class CustomUser(AbstractUser):
    photo = models.ImageField(verbose_name='Фото профиля', upload_to='./cleaners_photo/')
    company = models.ManyToManyField(Company)
    phone_number = models.CharField(verbose_name='Номер телефона', null=True)
