from django.db import models

from courses.constants import (MAX_AUTHOR_LENGHT, MAX_LINK_LENGHT,
                               MAX_TITLE_LENGHT)


class Course(models.Model):
    """Модель продукта - курса."""

    author = models.CharField(
        max_length=MAX_AUTHOR_LENGHT,
        verbose_name='Автор',
    )
    title = models.CharField(
        max_length=MAX_TITLE_LENGHT,
        verbose_name='Название',
    )
    start_date = models.DateTimeField(
        auto_now=False,
        auto_now_add=False,
        verbose_name='Дата и время начала курса'
    )
    price = models.PositiveIntegerField(
        verbose_name='Стоимость',
    )

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'
        ordering = ('-id',)

    def __str__(self):
        return self.title


class Lesson(models.Model):
    """Модель урока."""

    title = models.CharField(
        max_length=MAX_TITLE_LENGHT,
        verbose_name='Название',
    )
    link = models.URLField(
        max_length=MAX_LINK_LENGHT,
        verbose_name='Ссылка',
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='%(class)ss',
        verbose_name='Курс'
    )

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'
        ordering = ('id',)

    def __str__(self):
        return self.title


class Group(models.Model):
    """Модель группы."""

    title = models.CharField(
        max_length=MAX_TITLE_LENGHT,
        verbose_name='Название',
    )
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name='%(class)ss',
        verbose_name='Курс'
    )
    students = models.ManyToManyField(
        'users.CustomUser',
        related_name='student_groups',
        verbose_name='Студенты',
        blank=True
    )

    class Meta:
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'
        ordering = ('-id',)

    def __str__(self):
        return f'{self.title} ({self.course.title})'
