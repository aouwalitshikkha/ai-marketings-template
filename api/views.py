from rest_framework import viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from glossary.models import GlossaryTerm, GlossaryPageConfig
from .serializers import GlossaryTermSerializer, GlossaryTermListSerializer, GlossaryPageConfigSerializer


class GlossaryTermViewSet(viewsets.ModelViewSet):
    queryset = GlossaryTerm.objects.all().order_by('term')
    serializer_class = GlossaryTermSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status']
    search_fields = ['term', 'description']
    ordering_fields = ['term', 'created_at', 'updated_at']

    def get_serializer_class(self):
        if self.action == 'list':
            return GlossaryTermListSerializer
        return GlossaryTermSerializer


class GlossaryPageConfigViewSet(viewsets.ModelViewSet):
    queryset = GlossaryPageConfig.objects.all()
    serializer_class = GlossaryPageConfigSerializer
