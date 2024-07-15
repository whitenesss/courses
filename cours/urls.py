from django.urls import path, include
from rest_framework.routers import DefaultRouter
from cours.views import WellViewSet, PaymentViewSet
from cours.views import LessonCreateAPIView, LessonListAPIView, LessonRetrieveAPIView, LessonUpdateAPIView, \
    LessonDestroyAPIView

from cours.apps import CoursConfig

app_name = CoursConfig.name

router = DefaultRouter()
router.register(r'', WellViewSet, basename='well')
router.register(r'payments', PaymentViewSet, basename='payment')

urlpatterns = [
    path('/', include(router.urls)),
    path('/lesson', LessonListAPIView.as_view(), name='list'),
    path('/lesson/create/', LessonCreateAPIView.as_view(), name='create'),
    path('/lesson/retrieve/<int:pk>/', LessonRetrieveAPIView.as_view(), name='retrieve'),
    path('/lesson/update/<int:pk>/', LessonUpdateAPIView.as_view(), name='update'),
    path('/lesson/destroy/<int:pk>/', LessonDestroyAPIView.as_view(), name='destroy'),
]
