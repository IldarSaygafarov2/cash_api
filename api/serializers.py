from rest_framework import serializers

from .models import PreloadDataItem, Category, Currency, Income, Expense, CustomUser, Story, StoryImage


class StorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Story
        fields = ["pk", "title"]


class PreloadDataItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = PreloadDataItem
        fields = ['pk', 'text', 'img']


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['pk', 'name']


class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = ['pk', 'name', 'code']


class IncomeSerializer(serializers.ModelSerializer):
    currency = serializers.SlugRelatedField(
        queryset=Currency.objects.all(),
        read_only=False,
        slug_field='code'
    )

    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        read_only=False,
        slug_field='name'
    )

    class Meta:
        model = Income
        fields = ['pk', 'amount', 'created_at', 'currency', 'category', 'user']


class ExpenseSerializer(serializers.ModelSerializer):
    currency = serializers.SlugRelatedField(
        queryset=Currency.objects.all(),
        read_only=False,
        slug_field='code'
    )

    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        read_only=False,
        slug_field='name'
    )

    class Meta:
        model = Expense
        fields = ['pk', 'amount', 'created_at', 'currency', 'category', 'user']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ("pk", "username", "email", "password", "avatar")
