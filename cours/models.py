from django.db import models

from users.models import User

NULLABLE = {"blank": True, "null": True}


class Well(models.Model):
    title = models.CharField(max_length=150, verbose_name="название")
    image = models.ImageField(upload_to="blog", verbose_name="изображение", **NULLABLE)
    content = models.TextField(verbose_name="содержание", **NULLABLE)

    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="well_owner", **NULLABLE
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "выпускной блок"
        verbose_name_plural = "выпускные блоки"


# Create your models here.
class Lesson(models.Model):
    title = models.CharField(max_length=200, verbose_name="название")
    description = models.TextField(verbose_name="описание")
    image = models.ImageField(upload_to="blog", verbose_name="изображение", **NULLABLE)
    link_to_video = models.TextField(verbose_name="ссылка на видео", **NULLABLE)
    well = models.ForeignKey(
        Well, on_delete=models.CASCADE, verbose_name="курс", **NULLABLE
    )
    owner = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="lesson_owner", **NULLABLE
    )

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Урок"
        verbose_name_plural = "Уроки"


class Payment(models.Model):
    PAYMENT_METHODS = (("cash", "Наличные"), ("transfer", "Перевод на счёт"))
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="payments", **NULLABLE
    )
    payment_date = models.DateTimeField(auto_now_add=True)
    paid_course = models.ForeignKey(
        Well, on_delete=models.CASCADE, related_name="payments", blank=True, null=True
    )
    paid_lesson = models.ForeignKey(
        Lesson, on_delete=models.CASCADE, related_name="payments", blank=True, null=True
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS)

    class Meta:
        verbose_name = "Платеж"
        verbose_name_plural = "Платежи"

    def __str__(self):
        return f"Payment of {self.amount} by {self.user}"


class Subscription(models.Model):
    sab_well = models.ForeignKey(Well, on_delete=models.CASCADE, **NULLABLE, verbose_name='подписка на курс')
    seb_user = models.ForeignKey(User, on_delete=models.CASCADE, **NULLABLE, verbose_name='кто подписан на курс')
    sab_activ = models.BooleanField(default=True, verbose_name='подписан не подписан')

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'

    def __str__(self):
        return f'{self.seb_user.email} подписан на {self.sab_well.title}'
