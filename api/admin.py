from django.contrib import admin

from .models import PreloadDataItem, Category, Income, Expense, Currency

admin.site.register(PreloadDataItem)
admin.site.register(Category)
admin.site.register(Currency)
admin.site.register(Income)
admin.site.register(Expense)
