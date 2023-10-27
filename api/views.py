import os

from django.conf import settings
from drf_multiple_model.viewsets import FlatMultipleModelAPIViewSet
from rest_framework import generics
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import PreloadDataItem, Category, Currency, Income, Expense, CustomUser, Story, Note
from .serializers import (
    PreloadDataItemSerializer,
    CategorySerializer,
    CurrencySerializer,
    IncomeSerializer,
    ExpenseSerializer,
    UserSerializer,
    StorySerializer,
    NoteSerializer
)
from .utils import read_from_json, generate_code, make_qs_list, get_top_news
from django.core.mail import send_mail


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
    queryset = CustomUser.objects.all()

    def retrieve(self, request, pk=None):
        user = CustomUser.objects.get(pk=pk)
        expenses = list(Expense.objects.filter(user=user).values())
        incomes = list(Income.objects.filter(user=user).values())

        expenses_copy = make_qs_list(expenses, 'expense')
        incomes_copy = make_qs_list(incomes, 'income')

        return Response(expenses_copy+incomes_copy)


class UserStatisticsViewSet(viewsets.ViewSet):
    def retrieve(self, request, pk=None):
        user = CustomUser.objects.get(pk=pk)

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


class StoryViewSet(viewsets.ModelViewSet):
    queryset = Story.objects.all()
    serializer_class = StorySerializer

    def list(self, request, *args, **kwargs):
        result = []
        for item in self.queryset:
            obj = {
                "pk": item.pk,
                "title": item.title,
                "images": [
                    img.img.url for img in item.images.all()
                ]
            }
            result.append(obj)
        return Response(result)


class NoteViewSet(viewsets.ModelViewSet):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer

    # def retrieve(self, request, *args, **kwargs):


@api_view(["GET"])
def get_news(request):
    # path = os.path.join(settings.BASE_DIR, "news.json")
    # data = read_from_json(path)

    return Response(get_top_news())


class UserAccountCreateView(generics.ListCreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer


class UserAccountUpdateView(generics.RetrieveUpdateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer

    def retrieve(self, request, *args, **kwargs):
        user = CustomUser.objects.get(pk=kwargs["pk"])
        serializer = UserSerializer(user)
        return Response(serializer.data)


@api_view(["POST"])
def login_user(request):
    data = request.data
    user = CustomUser.objects.filter(
        email=data["email"],
        password=data["password"]
    ).first()

    if user is None:
        return Response({"status": False})

    code = generate_code()
    user.code = code
    user.save()

    send_mail(
        subject="Код для подтверждения авторизации",
        message=f"Ваш код для авторизации: {code}",
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[user.email]
    )

    return Response({"status": True})


@api_view(["POST"])
def check_user_by_code(request):
    data = request.data

    user = CustomUser.objects.filter(code=data["code"]).first()

    if user is None:
        return Response({"status": False})

    serializer = UserSerializer(user)
    return Response({"status": True, **serializer.data})


@api_view(["GET"])
def get_user_notes(request, pk):
    query = request.GET.get('month')

    user = CustomUser.objects.get(pk=pk)

    if query:
        notes = Note.objects.filter(created_at__month=int(query), user=user)
    else:
        notes = Note.objects.filter(user=user)
    serializer = NoteSerializer(notes, many=True)
    return Response(serializer.data)
