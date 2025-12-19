from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from api.v1.permissions import IsStudentOrIsAdmin, ReadOnlyOrIsAdmin
from api.v1.serializers.course_serializer import (CourseSerializer,
                                                  CreateCourseSerializer,
                                                  CreateGroupSerializer,
                                                  CreateLessonSerializer,
                                                  GroupSerializer,
                                                  LessonSerializer)
from api.v1.serializers.user_serializer import SubscriptionSerializer
from courses.models import Course
from users.models import Balance, Subscription


class LessonViewSet(viewsets.ModelViewSet):
    """Уроки."""

    permission_classes = (IsStudentOrIsAdmin,)

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return LessonSerializer
        return CreateLessonSerializer

    def get_сourse(self):
        """Получает курс по ID."""
        return get_object_or_404(Course, id=self.kwargs.get('course_id'))

    def perform_create(self, serializer):
        serializer.save(course=self.get_сourse())

    def get_queryset(self):
        return self.get_сourse().lessons.all()


class GroupViewSet(viewsets.ModelViewSet):
    """Группы."""

    permission_classes = (permissions.IsAdminUser,)

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return GroupSerializer
        return CreateGroupSerializer

    def get_сourse(self):
        """Получает курс по ID."""
        return get_object_or_404(Course, id=self.kwargs.get('course_id'))

    def perform_create(self, serializer):
        serializer.save(course=self.get_сourse())

    def get_queryset(self):
        return self.get_сourse().groups.all()


class CourseViewSet(viewsets.ModelViewSet):
    """Курсы."""

    queryset = Course.objects.all()
    permission_classes = (ReadOnlyOrIsAdmin,)

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return CourseSerializer
        elif self.action == 'pay':
            return SubscriptionSerializer
        return CreateCourseSerializer

    @action(
        methods=['post'],
        detail=True,
        permission_classes=[IsStudentOrIsAdmin]
    )
    def pay(self, request, pk):
        """Покупка доступа к курсу (подписка на курс)."""
        try:
            course = self.get_object()
        except Course.DoesNotExist:
            return Response(
                {'error': 'Курс не найден'},
                status=status.HTTP_404_NOT_FOUND
            )
        user = request.user
        if Subscription.objects.filter(user=user, course=course).exists():
            return Response(
                {'error': 'Вы уже подписаны на этот курс'},
                status=status.HTTP_400_BAD_REQUEST
            )
        balance, created = Balance.objects.get_or_create(
            user=user,
            defaults={'bonuses': 0}
        )
        if balance.bonuses < course.price:
            return Response(
                {
                    'error': 'Недостаточно бонусов',
                    'current_balance': balance.bonuses,
                    'required': course.price,
                    'deficit': course.price - balance.bonuses
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        subscription_data = {
            'user': user.id,
            'course': course.id
        }
        subscription_serializer = SubscriptionSerializer(
            data=subscription_data,
            context={'request': request}
        )
        if not subscription_serializer.is_valid():
            return Response(
                subscription_serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
        with transaction.atomic():
            previous_balance = balance.bonuses
            balance.bonuses -= course.price
            balance.save()
            subscription = subscription_serializer.save()
        response_serializer = SubscriptionSerializer(subscription)
        data = {
            'message': 'Курс успешно оплачен',
            'subscription': response_serializer.data,
            'payment_details': {
                'amount': course.price,
                'previous_balance': previous_balance,
                'remaining_balance': balance.bonuses
            }
        }
        return Response(data, status=status.HTTP_201_CREATED)
