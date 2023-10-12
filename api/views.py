from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .utils import get_top_news
from .models import PreloadDataItem, Category, Currency, Income, Expense, User
from .serializers import (
    PreloadDataItemSerializer,
    CategorySerializer,
    CurrencySerializer,
    IncomeSerializer,
    ExpenseSerializer,
    UserSerializer
)

from drf_multiple_model.viewsets import FlatMultipleModelAPIViewSet



class PreloadDataItemViewSet(viewsets.ModelViewSet):
    """
    API для получения данных о слайдере на главной странице
    """
    queryset = PreloadDataItem.objects.all()
    serializer_class = PreloadDataItemSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    """
    API для получения данных о категориях
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CurrencyViewSet(viewsets.ModelViewSet):
    """
    API для получения данных о валютах
    """
    queryset = Currency.objects.all()
    serializer_class = CurrencySerializer


class IncomeViewSet(viewsets.ModelViewSet):
    """
    API для получения данных о приходах
    """
    queryset = Income.objects.all()
    serializer_class = IncomeSerializer


class ExpenseViewSet(viewsets.ModelViewSet):
    """
    API для получения данных о расходах
    """
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer


class HistoryViewSet(FlatMultipleModelAPIViewSet):
    """
    API для получения данных о истории расходов и доходов пользователя
    """

    sorting_fields = ['-created_at']

    querylist = [
        {
            'queryset': Income.objects.all().order_by('-created_at'),
            'serializer_class': IncomeSerializer
        },
        {
            'queryset': Expense.objects.all().order_by('-created_at'),
            'serializer_class': ExpenseSerializer
        },
    ]


class UserDataViewSet(viewsets.ViewSet):
    queryset = User.objects.all()
    def retrieve(self, request, pk=None):
        user = User.objects.get(pk=pk)
        expenses = Expense.objects.filter(user=user)
        incomes = Income.objects.filter(user=user)

        expense_serializer = ExpenseSerializer(expenses, many=True)
        income_serializer = IncomeSerializer(incomes, many=True)

        data = expense_serializer.data + income_serializer.data
        return Response(data)


class UserStatisticsViewSet(viewsets.ViewSet):
    def retrieve(self, request, pk=None):
        user = User.objects.get(pk=pk)

        expenses = Expense.objects.filter(user=user)
        incomes = Income.objects.filter(user=user)

        expenses_total = sum([i.amount for i in expenses])
        incomes_total = sum([i.amount for i in incomes])

        balance = incomes_total - expenses_total

        data = {
            "expenses_total": expenses_total,
            "incomes_total": incomes_total,
            "balance": balance
        }

        return Response(data)


@api_view(["GET"])
def get_news(request):
    return Response(get_top_news())
