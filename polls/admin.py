"""The admin models for polls application."""
from django.contrib import admin

from .models import Question, Choice


class ChoiceInline(admin.TabularInline):
    """The choice of admin models."""

    model = Choice
    extra = 3


class QuestionAdmin(admin.ModelAdmin):
    """The question of admin models."""

    fieldsets = [
        (None, {'fields': ['question_text']}),
        (
            'Date Information',
            {'fields': ['pub_date', 'end_date'], 'classes': ['collapse']}
        )
    ]
    inlines = [ChoiceInline]
    list_display = (
        'question_text',
        'pub_date',
        'was_published_recently',
        'is_published',
        'can_vote'
    )
    list_filter = ['pub_date']
    search_fields = ['question_text']


admin.site.register(Question, QuestionAdmin)
