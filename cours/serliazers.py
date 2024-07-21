from rest_framework import serializers
from rest_framework.fields import SerializerMethodField

from cours.models import Lesson, Payment
from cours.models import Well


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = "__all__"


class WellSerializer(serializers.ModelSerializer):
    class Meta:
        model = Well
        fields = "__all__"


class WellDetailSerializer(serializers.ModelSerializer):
    lesson_count = SerializerMethodField()
    lessons = LessonSerializer(source="lesson_set", many=True, read_only=True)

    class Meta:
        model = Well
        fields = ["title", "content", "lesson_count", "lessons"]

    def get_lesson_count(self, obj):
        return Lesson.objects.filter(well=obj).count()


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = "__all__"
