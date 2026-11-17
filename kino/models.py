from django.db import models


class Janore(models.Model):
    name = models.CharField(max_length=100, unique=True, verbose_name='Название жанра')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'
        ordering = ['name']


class Kino(models.Model):
    name = models.CharField(max_length=200, verbose_name='Название фильма')
    description = models.TextField(verbose_name='Описание')
    year = models.PositiveSmallIntegerField(verbose_name='Год выпуска')
    country = models.CharField(max_length=100, verbose_name='Страна')
    janore = models.ManyToManyField(Janore, related_name='kino', verbose_name='Жанры')
    poster = models.ImageField(upload_to='posters/', blank=True, null=True, verbose_name='Постер')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Фильм'
        verbose_name_plural = 'Фильмы'
        ordering = ['name']


class Komentari(models.Model):
    kino = models.ForeignKey(Kino, on_delete=models.CASCADE, related_name='komentari', verbose_name='Фильм')
    name = models.CharField(max_length=100, verbose_name='Ваше имя')
    text = models.TextField(verbose_name='Комментарий')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')

    def __str__(self):
        return f'{self.name} — {self.kino.name}'

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['-created_at']
