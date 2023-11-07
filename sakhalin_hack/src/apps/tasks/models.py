from django.db import models

from apps.users.models import CustomUser, Address


class Task(models.Model):
    cleaner = models.ForeignKey(CustomUser,
                                verbose_name='Исполнитель',
                                on_delete=models.CASCADE,
                                related_name="task_cleaner"
                                )
    manager = models.ForeignKey(CustomUser,
                                verbose_name='Заказчик',
                                on_delete=models.CASCADE,
                                related_name='task_manager'
                                )
    address = models.ManyToManyField(Address)
    date = models.DateTimeField(verbose_name='Дата и время')
    notes = models.TextField(verbose_name='Примечания по работе', null=True, blank=True)

    is_active = models.BooleanField(verbose_name='Активная задача', default=True)
    quality_assessment = models.BooleanField(verbose_name='Контроль качества', default=False)

    class Meta:
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'
        ordering = ('-date', )

    def __str__(self):
        return f'id задачи: {self.id}, исполнитель: {self.cleaner.__str__}'


class CompletedTask(models.Model):
    CHOICES = [
        ('Выполнена', 'Выполнена'),
        ('Не выполнена',
            (
                ('Не выполнена без причины', 'Не выполнена без причины'),
                ('Не выполнена по причине плохой погоды', 'Не выполнена по причине плохой погоды'),
                ('Не выполнена по причине ремонта двора', 'Не выполнена по причине ремонта двора'),
                ('Не выполнена по причине ремонта двора', 'Не выполнена по причине ремонта двора'),
            )
         )
    ]

    photo = models.FileField(verbose_name='Фото уборки', upload_to='./clearing_photo/%Y/%m/%d/', blank=True)
    photo2 = models.FileField(verbose_name='Фото уборки', upload_to='./clearing_photo/%Y/%m/%d/', blank=True)
    photo3 = models.FileField(verbose_name='Фото уборки', upload_to='./clearing_photo/%Y/%m/%d/', blank=True)
    photo4 = models.FileField(verbose_name='Фото уборки', upload_to='./clearing_photo/%Y/%m/%d/', blank=True)
    photo5 = models.FileField(verbose_name='Фото уборки', upload_to='./clearing_photo/%Y/%m/%d/', blank=True)
    task = models.ForeignKey(Task, verbose_name='Задача', on_delete=models.CASCADE)

    cleaner = models.ForeignKey(CustomUser,
                                verbose_name='Исполнитель',
                                on_delete=models.CASCADE,
                                related_name='report_cleaner'
                                )
    manager = models.ForeignKey(CustomUser,
                                verbose_name='заказчик',
                                on_delete=models.CASCADE,
                                related_name='report_manager'
                                )

    address = models.ForeignKey(Address, verbose_name='Адрес проверки', on_delete=models.CASCADE)
    date = models.DateTimeField(verbose_name='Дата выполнения')

    coord1 = models.CharField(verbose_name='Координата 1', null=True, blank=True)
    coord2 = models.CharField(verbose_name='Координата 2', null=True, blank=True)
    marks = models.CharField(verbose_name='Работа', choices=CHOICES)
    notes = models.TextField(verbose_name='Примечания по работе', blank=True, null=True)

    verified_address = models.BooleanField(verbose_name='Проверка адреса', default=False)

    class Meta:
        verbose_name = 'Выполненная задача'
        verbose_name_plural = 'Выполненные задачи'

    def __str__(self) -> str:
        return f'id выполненной задачи: {self.id}, id задачи: {self.task.id}, исполнитель: {self.cleaner.username}'


class QualityAssessment(models.Model):
    CHOICES = [
        ('Работа не выполнена', 'Работа не выполнена'),
        ('Работа выполнена',
            (
                ('1', '1'),
                ('2', '2'),
                ('3', '4'),
                ('4', '4'),
                ('5', '5'),
            )
         )
    ]

    cleaner = models.ForeignKey(CustomUser,
                                verbose_name='Исполнитель',
                                on_delete=models.CASCADE,
                                related_name="quality_assessment_cleaner"
                                )
    manager = models.ForeignKey(CustomUser,
                                verbose_name='Проверяющий',
                                on_delete=models.CASCADE,
                                related_name='quality_assessment_manager'
                                )

    task = models.ForeignKey(Task, verbose_name='Задача', on_delete=models.CASCADE)
    task_report = models.ForeignKey(CompletedTask, verbose_name='Отчет по задаче', on_delete=models.CASCADE)

    text = models.TextField(verbose_name='Комментарий к выполненной работе', blank=True, null=True)
    mark = models.CharField(verbose_name='Оценка', choices=CHOICES)

    address = models.ForeignKey(Address, verbose_name='Адрес проверки', on_delete=models.CASCADE)
    date = models.DateTimeField(verbose_name='Дата проверки')

    photo1 = models.FileField(
        verbose_name='Фото выездной проверки (обязательное при проведении)',
        upload_to='./quality_assessment/%Y/%m/%d/',
        blank=True, null=True
    )
    photo2 = models.FileField(
        verbose_name='Фото выездной проверки (необязательное)',
        upload_to='./quality_assessment/%Y/%m/%d/',
        blank=True, null=True
    )
    photo3 = models.FileField(
        verbose_name='Фото выездной проверки (необязательное)',
        upload_to='./quality_assessment/%Y/%m/%d/',
        blank=True, null=True
    )

    class Meta:
        verbose_name = 'Оценка качества'
        verbose_name_plural = 'Оценки качества'

    def __str__(self) -> str:
        return f'id проверки: {self.id}, id задачи: {self.task.id}, проверяющий: {self.cleaner.username}'

