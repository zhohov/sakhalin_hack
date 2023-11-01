from django.db import models
from apps.users.models import CustomUser


class Appeal(models.Model):
    theme = models.CharField(verbose_name='Тема обращения', null=False)
    text = models.TextField(verbose_name='Текст обращения', null=False)

    sender = models.ForeignKey(CustomUser,
                               verbose_name='Отправитель',
                               on_delete=models.CASCADE,
                               related_name='appeal_sender'
                               )
    recipient = models.ForeignKey(CustomUser,
                                  verbose_name='Получатель',
                                  on_delete=models.CASCADE,
                                  related_name='appeal_recipient'
                                  )

    date = models.DateTimeField(verbose_name='Дата и время')

    class Meta:
        verbose_name = 'Обращение'
        verbose_name_plural = 'Обращения'

    def __str__(self) -> str:
        return f'Тема: {self.theme}, от: {self.sender}'


class AppealAnswer(models.Model):
    theme = models.CharField(verbose_name='Тема обращения', null=False)
    text = models.TextField(verbose_name='Текст обращения', null=False)

    sender = models.ForeignKey(CustomUser,
                               verbose_name='Отправитель',
                               on_delete=models.CASCADE,
                               related_name='appeal_answer_sender'
                               )
    recipient = models.ForeignKey(CustomUser,
                                  verbose_name='Получатель',
                                  on_delete=models.CASCADE,
                                  related_name='appeal_answer_recipient'
                                  )
    date = models.DateTimeField(verbose_name='Дата и время')

    class Meta:
        verbose_name = 'Обращение'
        verbose_name_plural = 'Обращения'

    def __str__(self) -> str:
        return f'Тема: {self.theme}, от: {self.sender}'
