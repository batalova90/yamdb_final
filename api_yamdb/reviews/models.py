import textwrap

from categories.models import Titles
from django.db import models
from users.models import User


class Review(models.Model):
    title = models.ForeignKey(
        Titles,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Titles'
    )
    text = models.TextField()
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Author'
    )
    score = models.IntegerField('Score')
    pub_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Publication date'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'title'],
                name='unique review')
        ]
        verbose_name = 'Review'
        verbose_name_plural = 'Reviews'

    def __str__(self):
        cropped_text = textwrap.shorten(self.text,
                                        width=200,
                                        placeholder='...')
        return f'{cropped_text} {self.author} {self.pub_date}'


class Comment(models.Model):
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Review'
    )
    text = models.TextField('Text')
    author = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='Author'
    )
    pub_date = models.DateTimeField(
        'Publication date',
        auto_now_add=True,
    )

    class Meta:
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'

    def __str__(self):
        cropped_text = textwrap.shorten(self.text,
                                        width=200,
                                        placeholder='...')
        return f'{cropped_text} {self.author} {self.pub_date}'
