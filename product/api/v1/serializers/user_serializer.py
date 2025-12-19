from django.contrib.auth import get_user_model
from djoser.serializers import UserSerializer
from rest_framework import serializers

from courses.models import Course
from users.models import Subscription

User = get_user_model()


class CustomUserSerializer(UserSerializer):
    """Сериализатор для пользователей."""

    class Meta:
        """Мета-класс сериализатора пользователей."""

        model = User
        fields = [
            'username',
            'email',
            'first_name',
            'last_name',
        ]


class SubscriptionSerializer(serializers.ModelSerializer):
    """Сериализатор подписки."""

    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )
    course = serializers.PrimaryKeyRelatedField(
        queryset=Course.objects.all()
    )
    course_title = serializers.CharField(
        source='course.title',
        read_only=True
    )
    user_full_name = serializers.CharField(
        source='user.get_full_name',
        read_only=True
    )

    class Meta:
        model = Subscription
        fields = (
            'id',
            'user',
            'user_full_name',
            'course',
            'course_title',
        )
        read_only_fields = ('created_at',)
