from apps.artwork.models import Art, Author
from apps.artwork.serializers import ArtSerializer, AuthorSerializer
from apps.base_view import CustomViewBase


class ArtViewSet(CustomViewBase):
    queryset = Art.logic_objects.all()
    serializer_class = ArtSerializer


class AuthorViewSet(CustomViewBase):
    queryset = Author.logic_objects.all()
    serializer_class = AuthorSerializer
