from django.contrib import admin
from django.contrib.admin import ModelAdmin


from .models import PreloadDataItem, Category, Income, Expense, Currency, CustomUser


admin.site.register(CustomUser, ModelAdmin)
admin.site.register(PreloadDataItem)
admin.site.register(Category)
admin.site.register(Currency)
admin.site.register(Income)
admin.site.register(Expense)
