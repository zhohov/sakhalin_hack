from django.db import models
from django.contrib.auth.models import AbstractUser


class Address(models.Model):
    city = models.CharField(verbose_name='Город', null=False)
    street = models.CharField(verbose_name='Улица', null=False)
    build = models.CharField(verbose_name='Дом', null=True)

    class Meta:
        verbose_name = 'Адрес'
        verbose_name_plural = 'Адреса'

    def __str__(self):
        return f'{self.city}, {self.street}, {self.build}'


class Company(models.Model):
    name = models.CharField(verbose_name='Название')
    address = models.ManyToManyField(Address, verbose_name='Адреса', blank=True)

    class Meta:
        verbose_name = 'Управляющая компания'
        verbose_name_plural = 'Управляющие компании'

    def __str__(self) -> str:
        return f'{self.name}'


class CustomUser(AbstractUser):
    photo = models.ImageField(verbose_name='Фото профиля', upload_to='./cleaners_photo/', blank=True)
    company = models.ManyToManyField(Company, blank=True)
    phone_number = models.CharField(verbose_name='Номер телефона', unique=True, null=True, blank=True, max_length=11)
    email = models.EmailField(unique=True)

    phone_code = models.CharField(verbose_name='Код для входа по телефону', null=True, blank=True,)
    middle_name = models.CharField(verbose_name='Отчество', null=True, blank=True)

    REQUIRED_FIELDS = ['email', 'password']

    def __str__(self) -> str:
        return f'{self.last_name} {self.first_name} {self.middle_name}'

