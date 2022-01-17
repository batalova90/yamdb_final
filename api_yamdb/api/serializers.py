from django.shortcuts import get_object_or_404
from django.db.models import Avg
from rest_framework import serializers
from reviews.models import Comment, Review
from categories.models import Genres, Titles, Categories, TitlesGenres
from users.models import User
import datetime as dt


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('username', 'email')
        model = User
        extra_kwargs = {
            'username': {'required': True},
            'email': {'required': True}
        }

    def validate_username(self, value):
        if value.lower() == 'me':
            raise serializers.ValidationError(
                'It is forbidden to use this name as a username.'
            )
        return value


class TokenSerializer(serializers.Serializer):
    username = serializers.CharField()
    confirmation_code = serializers.CharField(max_length=128)


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role')
        extra_kwargs = {
            'username': {'required': True},
            'email': {'required': True}
        }


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genres
        fields = ('name', 'slug')


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True,
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Comment
        fields = ('id', 'text', 'author', 'pub_date')


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True,
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')

    def validate(self, data):
        if self.context['request'].method == 'PATCH':
            return data

        author = self.context['request'].user
        title_id = self.context['view'].kwargs.get('title_id')

        if Review.objects.filter(
                author=author, title=title_id).exists():
            raise serializers.ValidationError(
                'You can only leave one review '
            )
        return data

    def validate_score(self, value):
        if not 1 <= value <= 10:
            raise serializers.ValidationError(
                'enter a score from 1 to 10 '
            )
        return value


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Categories
        fields = ('name', 'slug')


class TitleSerializer(serializers.ModelSerializer):
    rating = serializers.SerializerMethodField(read_only=True, default=None)
    description = serializers.CharField(required=False)
    genre = GenreSerializer(many=True, read_only=True)
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Titles
        fields = '__all__'

    def create(self, validated_data):
        genres = self.initial_data['genre']
        category = get_object_or_404(Categories,
                                     slug=self.initial_data['category'])
        title = Titles.objects.create(**validated_data, category=category)
        for genre in genres:
            current_genre = get_object_or_404(Genres, slug=genre)
            TitlesGenres.objects.create(genre=current_genre, title=title)
        current_genre = get_object_or_404(Genres, slug=genres)
        TitlesGenres.objects.create(genre=current_genre, title=title)
        return title

    def get_rating(self, obj):
        if obj.reviews.exists():
            return int(obj.reviews.aggregate(Avg('score'))['score__avg'])
        return None

    def validate_year(self, value):
        if value <= dt.datetime.now().year:
            return value
        raise serializers.ValidationError(
            'Год выпуска не может быть больше текущего!'
        )

    def validate_category(self, value):
        if not Categories.objects.get(slug=value).exists():
            raise serializers.ValidationError(
                'Категории с таким slug не существует'
            )
        return value

    def validate_genre(self, value):
        if not Genres.objects.get(slug=value).exists():
            raise serializers.ValidationError(
                'Жанра с таким slug не существует'
            )
        return value
