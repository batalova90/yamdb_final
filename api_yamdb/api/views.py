from categories.models import Categories, Genres, Titles
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import (AllowAny, IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from reviews.models import Review
from users.models import User

from .permissions import (AdminAddInfoClasses, IsAdmin, IsAuthorOrReadOnly,
                          IsModerator)
from .serializers import (CategorySerializer, CommentSerializer,
                          GenreSerializer, RegisterSerializer,
                          ReviewSerializer, TitleSerializer, TokenSerializer,
                          UserSerializer)


class RegisterViewSet(viewsets.ViewSet):
    permission_classes = (AllowAny,)

    def create(self, request):
        username = request.data.get('username')
        email = request.data.get('email')
        user = User.objects.filter(username=username, email=email).first()

        if user is not None:
            confirmation_code = default_token_generator.make_token(user)
            send_mail(subject='Confirmation code',
                      message=confirmation_code,
                      from_email='api_yamdb@yamdb.com',
                      recipient_list=[email])

            return Response({'username': username, 'email': email},
                            status=status.HTTP_200_OK)

        serializer = RegisterSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            user = get_object_or_404(User, username=username)
            confirmation_code = default_token_generator.make_token(user)

            send_mail(subject='Confirmation code',
                      message=confirmation_code,
                      from_email='api_yamdb@yamdb.com',
                      recipient_list=[email])

            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TokenViewSet(viewsets.ViewSet):
    permission_classes = (AllowAny, )

    def create(self, request):
        serializer = TokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = get_object_or_404(
            User,
            username=serializer.validated_data.get('username')
        )

        confirmation_code = serializer.validated_data.get('confirmation_code')

        if default_token_generator.check_token(user, confirmation_code):
            refresh = RefreshToken.for_user(user)

            return Response(
                {'token': str(refresh.access_token)},
                status=status.HTTP_200_OK
            )
        return Response(
            {'confirmation_code': 'Incorrect code'},
            status=status.HTTP_400_BAD_REQUEST
        )


class UsersViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdmin,)
    filter_backends = (filters.SearchFilter, )
    search_fields = ('username',)
    lookup_field = 'username'

    @action(detail=False, methods=['GET', 'PATCH'],
            url_path='me', permission_classes=[IsAuthenticated])
    def get_or_update_user_profile(self, request):
        if request.method == 'GET':
            serializer = UserSerializer(request.user)
            return Response(serializer.data)

        serializer = UserSerializer(request.user,
                                    data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save(role=request.user.role)

        return Response(serializer.data)


class MixinViewSet(mixins.CreateModelMixin, mixins.ListModelMixin,
                   mixins.DestroyModelMixin):
    pass


class GenreViewSet(MixinViewSet, viewsets.GenericViewSet):
    queryset = Genres.objects.all()
    serializer_class = GenreSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,
                          AdminAddInfoClasses, )
    filter_backends = (filters.SearchFilter, )
    search_fields = ('name', )
    lookup_field = 'slug'


class CategoryViewSet(MixinViewSet, viewsets.GenericViewSet):
    queryset = Categories.objects.all()
    serializer_class = CategorySerializer
    permission_classes = (IsAuthenticatedOrReadOnly,
                          AdminAddInfoClasses, )
    filter_backends = (filters.SearchFilter, )
    search_fields = ('name', )
    lookup_field = 'slug'


class ReviewsPagination(PageNumberPagination):
    page_size = 10


class ReviewViewSet(viewsets.ModelViewSet):

    serializer_class = ReviewSerializer
    pagination_class = ReviewsPagination
    permission_classes = (
        IsAdmin | IsModerator | IsAuthorOrReadOnly,
    )

    def get_queryset(self):
        title = get_object_or_404(Titles, id=self.kwargs.get('title_id'))
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Titles, id=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)


class CommentPagination(PageNumberPagination):
    page_size = 10


class CommentViewSet(viewsets.ModelViewSet):

    serializer_class = CommentSerializer
    pagination_class = CommentPagination
    permission_classes = (
        IsAdmin | IsModerator | IsAuthorOrReadOnly,
    )

    def get_queryset(self):
        review = get_object_or_404(Review, id=self.kwargs.get('review_id'))
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(Review, id=self.kwargs.get('review_id'))
        serializer.save(author=self.request.user, review=review)


class TitleViewSet(viewsets.GenericViewSet, MixinViewSet,
                   mixins.RetrieveModelMixin, mixins.UpdateModelMixin):
    queryset = Titles.objects.all()
    serializer_class = TitleSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,
                          AdminAddInfoClasses, )
    filter_backends = (DjangoFilterBackend, filters.SearchFilter, )
    search_fields = ('name', )
    filterset_fields = ('category', 'genre', 'name', 'year')
