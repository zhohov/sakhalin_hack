from django.db import models
from django.urls import reverse

from apps.users.models import CustomUser


class Address(models.Model):
    city = models.CharField(verbose_name='Город', null=False)
    district = models.CharField(verbose_name='Район', null=False)
    street = models.CharField(verbose_name='Улица', null=False)
    build = models.CharField(verbose_name='Дом', null=True)

    class Meta:
        verbose_name = 'Адрес'
        verbose_name_plural = 'Адреса'

    def __str__(self):
        return f'{self.city} {self.district} {self.street}'


class Task(models.Model):
    cleaner = models.ForeignKey(CustomUser, verbose_name='Исполнитель', on_delete=models.CASCADE, related_name="task_cleaner")
    manager = models.ForeignKey(CustomUser, verbose_name='Заказчик', on_delete=models.CASCADE, related_name='task_manager')
    address = models.ManyToManyField(Address)
    date = models.DateTimeField()
    notes = models.TextField(verbose_name='Приечания', null=True, blank=True)
    is_active = models.BooleanField(verbose_name='Активная задача', default=True)

    class Meta:
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'

    def __str__(self):
        return f'id задачи: {self.id}, исполнитель: {self.cleaner.username}'

    def get_absolute_url(self):
        return reverse('tasks/task_report', kwargs={'task_id': self.id})


class CompletedTask(models.Model):
    CHOICES = [
        ('Выполнена', 'Выполнена'),
        ('Не выполнена',
            (
                ('NotCompleted', 'Не выполнена без причины'),
                ('NotCompleted', 'Не выполнена по причине плохой погоды'),
                ('NotCompleted', 'Не выполнена по причине ремонта двора'),
                ('NotCompleted', 'Не выполнена по причине ремонта двора'),
            )
         )
    ]

    photo = models.ImageField(verbose_name='Фото уборки', upload_to='./clearing_photo/%Y/%m/%d/', blank=True)
    task = models.ForeignKey(Task, verbose_name='Задача', on_delete=models.CASCADE)
    cleaner = models.ForeignKey(CustomUser, verbose_name='Исполнитель', on_delete=models.CASCADE, related_name='report_cleaner')
    manager = models.ForeignKey(CustomUser, verbose_name='заказчик', on_delete=models.CASCADE, related_name='report_manager')
    address = models.ManyToManyField(Address, verbose_name='Адрес')
    date = models.DateTimeField(verbose_name='Дата выполнения')

    coord1 = models.CharField(verbose_name='Координата 1', null=True, blank=True)
    coord2 = models.CharField(verbose_name='Координата 2', null=True, blank=True)
    marks = models.CharField(verbose_name='Работа', choices=CHOICES)
    notes = models.TextField(verbose_name='Примечания по работе', null=True)

    class Meta:
        verbose_name = 'Выполненная задача'
        verbose_name_plural = 'Выполненные задачи'

    def __str__(self) -> str:
        return f'id выполненной задачи: {self.id}, id задачи: {self.task.id}, исполнитель: {self.cleaner.username}'
