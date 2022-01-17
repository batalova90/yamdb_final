import textwrap

from django.db import models


class Genres(models.Model):
    name = models.CharField('Name of genre', max_length=200, unique=True)
    slug = models.SlugField(max_length=50, unique=True)

    class Meta:
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'
        ordering = ['id', ]

    def __str__(self):
        return f'{self.slug}'


class Categories(models.Model):
    name = models.CharField('Name of categories', max_length=200, unique=True)
    slug = models.SlugField(max_length=50, unique=True)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['id', ]

    def __str__(self):
        return f'{self.slug}'


class Titles(models.Model):
    name = models.CharField('Name of titles', max_length=200)
    year = models.IntegerField()
    description = models.TextField()
    category = models.ForeignKey(Categories, related_name='categories',
                                 on_delete=models.SET_NULL, null=True)
    genre = models.ManyToManyField(Genres, through='TitlesGenres')
    rating = models.IntegerField(default=0)

    class Meta:
        verbose_name = 'Произведение'
        verbose_name_plural = 'Произведения'
        ordering = ['id', ]

    def __str__(self):
        cropped_text = textwrap.shorten(self.description,
                                        width=100,
                                        placeholder='...')

        return f'{self.name} {self.year} {cropped_text}'


class TitlesGenres(models.Model):
    genre = models.ForeignKey(Genres, on_delete=models.CASCADE)
    title = models.ForeignKey(Titles, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.genre.slug}'
