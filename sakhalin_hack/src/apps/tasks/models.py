from django.db import models
from django.urls import reverse

from apps.users.models import CustomUser


class Address(models.Model):
    city = models.CharField(verbose_name='Город', null=False)
    district = models.CharField(verbose_name='Район', null=False)
    street = models.CharField(verbose_name='Улица', null=False)

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

    class Meta:
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'

    def __str__(self):
        return f'id задачи: {self.id}, исполнитель: {self.cleaner.username}'

    def get_absolute_url(self):
        return reverse('tasks/task_report', kwargs={'task_id': self.id})


class CompletedTask(models.Model):
    CHOICES = [
        ('Completed', 'Выполнена'),
        ('Не выполнена',
            (
                ('NotCompleted', 'Не выполнена без причины'),
                ('NotCompleted', 'Не выполнена по причине плохой погоды'),
                ('NotCompleted', 'Не выполнена по причине ремонта двора'),
                ('NotCompleted', 'Не выполнена по причине ремонта двора'),
            )
         )
    ]

    photo = models.ImageField(verbose_name='Фото уборки', upload_to='./clearing_photo/', blank=True)
    task = models.ForeignKey(Task, verbose_name='Задача', on_delete=models.CASCADE)
    cleaner = models.ForeignKey(CustomUser, verbose_name='Исполнитель', on_delete=models.CASCADE)
    address = models.ManyToManyField(Address, verbose_name='Адрес')
    date = models.DateTimeField(verbose_name='Дата выполнения')

    marks = models.CharField(verbose_name='Работа', choices=CHOICES)
    notes = models.TextField(verbose_name='Примечания по работе', null=True)

    class Meta:
        verbose_name = 'Выполненная задача'
        verbose_name_plural = 'Выполненные задачи'

    def __str__(self) -> str:
        return f'id выполненной задачи: {self.id}, id задачи: {self.task.id}, исполнитель: {self.cleaner.username}'
