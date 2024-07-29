from django_filters import OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework import generics
from rest_framework.exceptions import NotFound
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK

from cours.models import Well, Payment, Subscription
from cours.paginators import LessonListPagination, WellListPagination
from cours.serliazers import WellSerializer, WellDetailSerializer, PaymentSerializer, SubscriptionSerializer

from cours.models import Lesson
from cours.serliazers import LessonSerializer
from cours.services import create_stripe_price, crate_stripe_session
from users.permissions import IsModer, NotModer, IsOwner


class WellViewSet(viewsets.ModelViewSet):
    queryset = Well.objects.all()
    serializer_class = WellSerializer
    pagination_class = WellListPagination

    def get_serializer_class(self):
        if self.action == "retrieve":
            return WellDetailSerializer
        return WellSerializer

    def perform_create(self, serializer):
        well = serializer.save()
        well.owner = self.request.user
        well.save()

    def get_permissions(self):
        if self.action in ["create"]:
            self.permission_classes = (NotModer,)
        elif self.action in ["update", "retrieve"]:
            self.permission_classes = (IsModer | IsOwner,)
        elif self.action in ["destroy"]:
            self.permission_classes = (NotModer, IsOwner,)
        return super().get_permissions()


class SubscriptionCreateAPIView(generics.CreateAPIView):
    queryset = Subscription.objects.all()
    serializer_class = SubscriptionSerializer
    permission_classes = [IsAuthenticated]

    def post(self, *args, **kwargs):
        user = self.request.user
        well_id = self.request.data.get('well_id')
        well = get_object_or_404(Well, id=well_id)

        subscription = Subscription.objects.filter(seb_user=user, sab_well=well)

        if subscription.exists():
            subscription.delete()
            message = 'Подписка удалена'
        else:
            Subscription.objects.create(seb_user=user, sab_well=well, sab_activ=True)
            message = 'Подписка добавлена'

        return Response({"message": message})


# Create your views here.
class LessonCreateAPIView(generics.CreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (NotModer, IsAuthenticated)

    def perform_create(self, serializer):
        lesson = serializer.save()
        lesson.owner = self.request.user
        lesson.save()
# [AllowAny]

class LessonListAPIView(generics.ListAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    pagination_class = LessonListPagination


class LessonRetrieveAPIView(generics.RetrieveAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (IsAuthenticated, IsModer | IsOwner,)


class LessonUpdateAPIView(generics.UpdateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (IsAuthenticated, IsModer | IsOwner,)


class LessonDestroyAPIView(generics.DestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = (NotModer, IsAuthenticated, IsOwner,)


class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filters_fields = ['paid_course', 'paid_lesson', 'payment_method']
    ordering_fields = ['payment_date']
    ordering = ['payment_date']


class PaymentCreateAPIView(generics.CreateAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

    def perform_create(self, serializer):
        payment = serializer.save(user=self.request.user)

        price = create_stripe_price(payment.amount)
        session_id, payment_link = crate_stripe_session(price)
        payment.session_id = session_id
        payment.link = payment_link
        payment.save()

