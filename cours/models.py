from django.db import models

from users.models import User

NULLABLE = {'blank': True, 'null': True}


class Well(models.Model):
    title = models.CharField(max_length=150, verbose_name='название')
    image = models.ImageField(upload_to="blog", verbose_name='изображение', **NULLABLE)
    content = models.TextField(verbose_name='содержание', **NULLABLE)

    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='well_owner', **NULLABLE)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'выпускной блок'
        verbose_name_plural = 'выпускные блоки'


# Create your models here.
class Lesson(models.Model):
    title = models.CharField(max_length=200, verbose_name='название')
    description = models.TextField(verbose_name='описание')
    image = models.ImageField(upload_to="blog", verbose_name='изображение', **NULLABLE)
    link_to_video = models.TextField(verbose_name='ссылка на видео', **NULLABLE)
    well = models.ForeignKey(Well, on_delete=models.CASCADE, verbose_name='курс', **NULLABLE)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='lesson_owner', **NULLABLE)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'
