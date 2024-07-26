from django.contrib import admin

from cours.models import Well, Payment


# Register your models here.

@admin.register(Well)
class Well(admin.ModelAdmin):
    list_display = ('id', 'title', 'content')


@admin.register(Payment)
class Payment(admin.ModelAdmin):
    list_display = ('id', 'user', 'payment_date', 'paid_course', 'paid_lesson', 'amount', 'payment_method')
    list_filter = ('user', 'paid_course', 'payment_method')

