from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from cours.models import Lesson, Payment, Subscription
from cours.models import Well
from cours.validators import LinkToVideoValidator


class SubscriptionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = ['id', 'sab_well', 'seb_user', 'sab_activ']


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = "__all__"
        validators = [LinkToVideoValidator(fields='link_to_video')]


class WellSerializer(serializers.ModelSerializer):
    class Meta:
        model = Well
        fields = "__all__"


class WellDetailSerializer(serializers.ModelSerializer):
    lesson_count = SerializerMethodField(read_only=True)
    lessons = LessonSerializer(source="lesson_set", many=True, read_only=True)
    is_subscribed = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Well
        fields = ["title", "content", "lesson_count", "lessons", "is_subscribed"]

    def get_is_subscribed(self, obj):
        user = self.context['request'].user
        return Subscription.objects.filter(sab_well=obj, seb_user=user, sab_activ=True).exists()

    def get_lesson_count(self, obj):
        return Lesson.objects.filter(well=obj).count()


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = "__all__"
