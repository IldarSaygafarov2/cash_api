from django.contrib import admin
from django.contrib.admin import ModelAdmin


from .models import PreloadDataItem, Category, Income, Expense, Currency, CustomUser, Story,StoryImage


class StoryImageInline(admin.TabularInline):
    model = StoryImage
    extra = 1


class StoryImageAdmin(admin.ModelAdmin):
    inlines = [StoryImageInline]


admin.site.register(CustomUser, ModelAdmin)
admin.site.register(PreloadDataItem)
admin.site.register(Category)
admin.site.register(Currency)
admin.site.register(Income)
admin.site.register(Expense)
admin.site.register(Story, StoryImageAdmin)
