from django.db import models
from django.contrib.auth.models import AbstractUser


class Company(models.Model):
    name = models.CharField(verbose_name='Название')

    class Meta:
        verbose_name = 'Управляющая компания'
        verbose_name_plural = 'Управляющие компании'

    def __str__(self) -> str:
        return f'{self.name}'


class CustomUser(AbstractUser):
    photo = models.ImageField(verbose_name='Фото профиля', upload_to='./cleaners_photo/', blank=True)
    company = models.ManyToManyField(Company, blank=True)
    phone_number = models.CharField(verbose_name='Номер телефона', null=True, blank=True)

    def __str__(self) -> str:
        return f'{self.last_name} {self.first_name}'

