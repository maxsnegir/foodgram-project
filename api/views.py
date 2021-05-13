from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated

from recipes.models import Ingredient
from rest_framework.views import APIView
from rest_framework.response import Response
from django_filters import rest_framework as filters
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from api.filters import IngredientFilter
from api.serializers import IngredientSerializer
from users.models import Follow

User = get_user_model()


class IngredientListView(generics.ListAPIView, viewsets.ViewSet):
    serializer_class = IngredientSerializer
    queryset = Ingredient.objects.filter(draft=False)
    http_method_names = ['get', ]
    permission_classes = [IsAuthenticated, ]
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = IngredientFilter


class SubscriptionView(APIView):
    permission_classes = [IsAuthenticated, ]

    def delete(self, request, *args, **kwargs):
        author_id = self.kwargs.get('pk')
        relation = Follow.objects.filter(user=self.request.user,
                                         author=author_id)
        relation.delete()
        return Response({'success': True})

    def post(self, request):
        author_id = request.data.get('id')
        author = get_object_or_404(User, id=author_id)

        if self.request.user != author:
            Follow.objects.get_or_create(user=request.user, author=author)
        return Response({'success': True})
