from django.db.models import Count
from django.db.models.signals import post_save
from django.dispatch import receiver

from courses.models import Group
from users.models import Balance, CustomUser, Subscription


@receiver(post_save, sender=CustomUser)
def create_user_balance(sender, instance, created, **kwargs):
    """Создать баланс при создании нового пользователя."""
    if created:
        Balance.objects.create(user=instance)


@receiver(post_save, sender=Subscription)
def post_save_subscription(sender, instance: Subscription, created, **kwargs):
    """Распределение пользователя в группу после создания подписки."""
    if created:
        user = instance.user
        course = instance.course
        groups_count = Group.objects.filter(course=course).count()
        if groups_count < 10:
            for i in range(groups_count, 10):
                Group.objects.create(
                    title=f'Группа {i+1} курса "{course.title}"',
                    course=course
                )
        group = Group.objects.filter(
            course=course
        ).annotate(
            students_count=Count('students')
        ).order_by(
            'students_count'
        ).first()
        if group:
            group.students.add(user)
