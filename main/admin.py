from django.contrib import admin
from .models import AdvUser
from .models import Card
from .models import Module
from .models import Test
from .models import Answer, Question


class CardInline(admin.TabularInline):
    model = Card


class ModuleAdmin(admin.ModelAdmin):
    inlines = [CardInline]


class QuestionInline(admin.TabularInline):
    model = Answer
    extra = 4


@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    inlines = [QuestionInline]


admin.site.register(Test)
admin.site.register(AdvUser)
admin.site.register(Card)
admin.site.register(Module, ModuleAdmin)
