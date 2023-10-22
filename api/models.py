from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    # username = models.CharField(max_length=255, blank=True, null=True)
    avatar = models.ImageField(verbose_name="Аватар", upload_to="users/avatars/", null=True, blank=True)
    code = models.CharField(verbose_name="Код авторизации", max_length=6, default="", null=True, blank=True)

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


class PreloadDataItem(models.Model):
    text = models.TextField(verbose_name="Текст")
    img = models.ImageField(verbose_name="Фото", upload_to="photos/preload/")

    def __str__(self):
        return f'{self.pk} слайд'

    class Meta:
        verbose_name = "Слайд"
        verbose_name_plural = "Слайды"


class Category(models.Model):
    name = models.CharField(verbose_name="Категория", max_length=155, unique=True)
    icon = models.FileField(verbose_name="Иконка", upload_to="categories/icons/", null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class Currency(models.Model):
    name = models.CharField(verbose_name="Полное название валюты", max_length=155, unique=True)
    code = models.CharField(verbose_name="Код валюты", max_length=10, unique=True)

    def __str__(self):
        return f'{self.name}: {self.code}'

    class Meta:
        verbose_name = 'Валюта'
        verbose_name_plural = 'Валюты'


class Income(models.Model):
    created_at = models.DateTimeField(verbose_name="Время добавления", auto_now_add=True)
    amount = models.IntegerField(verbose_name="Сумма дохода", default=0)
    currency = models.ForeignKey(verbose_name="Валюта", to=Currency, on_delete=models.PROTECT)
    category = models.ForeignKey(verbose_name="Категория", to=Category, on_delete=models.PROTECT)
    user = models.ForeignKey(verbose_name="Пользователь", to=CustomUser, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f'Доход({self.category}: {self.amount})'

    class Meta:
        verbose_name = "Приход"
        verbose_name_plural = "Приходы"


class Expense(models.Model):
    created_at = models.DateTimeField(verbose_name="Время добавления", auto_now_add=True)
    amount = models.IntegerField(verbose_name="Сумма расхода", default=0)
    currency = models.ForeignKey(verbose_name="Валюта", to=Currency, on_delete=models.PROTECT)
    category = models.ForeignKey(verbose_name="Категория", to=Category, on_delete=models.PROTECT)
    user = models.ForeignKey(verbose_name="Пользователь", to=CustomUser, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return f'Расход({self.category}: {self.amount})'

    class Meta:
        verbose_name = "Расход"
        verbose_name_plural = "Расходы"


class Story(models.Model):
    title = models.CharField(verbose_name="Название", max_length=155, blank=True, null=True)


    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "История"
        verbose_name_plural = "Истории"


class StoryImage(models.Model):
    story = models.ForeignKey(Story, on_delete=models.CASCADE, verbose_name='История', related_name="images")
    img = models.ImageField(verbose_name="Фото", upload_to="photos/stories/", blank=True, null=True)

    def __str__(self):
        return self.story.title

    class Meta:
        verbose_name = "Фотка истории"
        verbose_name_plural = "Фотки истории"


class Note(models.Model):
    title = models.CharField(verbose_name="Заголовок", max_length=255)
    body = models.TextField(verbose_name="Описание")
    created_at = models.DateTimeField(verbose_name="Дата создания", auto_now_add=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name="notes", verbose_name="Пользователь")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Заметка"
        verbose_name_plural = "Заметки"
