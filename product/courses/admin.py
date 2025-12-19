from django.contrib import admin
from django.utils.html import format_html

from courses.models import Course, Group, Lesson


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    """Админка для курсов."""

    list_display = (
        'title',
        'author',
        'start_date',
        'price',
        'lessons_count',
        'groups_count',
    )
    list_filter = ('author', 'start_date')
    search_fields = ('title', 'author')
    ordering = ('-start_date',)

    fieldsets = (
        ('Основная информация', {
            'fields': ('title', 'author', 'start_date', 'price')
        }),
    )

    def lessons_count(self, obj):
        return obj.lessons.count()
    lessons_count.short_description = 'Количество уроков'

    def groups_count(self, obj):
        return obj.groups.count()
    groups_count.short_description = 'Количество групп'


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    """Админка для уроков."""

    list_display = ('title', 'course', 'link_display')
    list_filter = ('course',)
    search_fields = ('title', 'course__title')
    ordering = ('course', 'id')
    list_select_related = ('course',)

    def link_display(self, obj):
        return format_html(
            '<a href="{}" target="_blank">{}</a>',
            obj.link, obj.link[:50] + '...' if len(obj.link) > 50 else obj.link
        )
    link_display.short_description = 'Ссылка'


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    """Админка для групп."""

    list_display = ('title', 'course', 'students_count')
    list_filter = ('course',)
    search_fields = ('title', 'course__title')
    ordering = ('-id',)
    list_select_related = ('course',)
    filter_horizontal = ('students',)

    fieldsets = (
        ('Основная информация', {
            'fields': ('title', 'course')
        }),
        ('Студенты', {
            'fields': ('students',)
        }),
    )

    def students_count(self, obj):
        return obj.students.count()
    students_count.short_description = 'Количество студентов'
