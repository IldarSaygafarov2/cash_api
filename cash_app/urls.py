from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from api import views

router = routers.DefaultRouter()
router.register(r'preloader', views.PreloadDataItemViewSet)
router.register(r'categories', views.CategoryViewSet)
router.register(r'currencies', views.CurrencyViewSet)
router.register(r'incomes', views.IncomeViewSet)
router.register(r'expenses', views.ExpenseViewSet)
router.register(r'history', views.HistoryViewSet, basename='histories')
router.register(r'stories', views.StoryViewSet, basename='stories')
# router.register(r'users/accounts', views.UserAccountView, basename='accounts')
router.register(r'users/data', views.UserDataViewSet, basename='users')
router.register(r'users/statistics', views.UserStatisticsViewSet, basename='users')

router.urls.append(path("news/", views.get_news))
router.urls.append(path("users/list/", views.UserAccountCreateView.as_view()))
router.urls.append(path("users/list/update/<str:pk>/", views.UserAccountUpdateView.as_view()))
router.urls.append(path("users/check/", views.check_user_by_code))
router.urls.append(path("users/login/", views.login_user))

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include(router.urls)),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
