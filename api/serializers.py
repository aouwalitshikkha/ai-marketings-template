from rest_framework import serializers
from glossary.models import GlossaryTerm, GlossaryPageConfig


class GlossaryTermSerializer(serializers.ModelSerializer):
    class Meta:
        model = GlossaryTerm
        fields = ['id', 'term', 'description', 'status', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']


class GlossaryTermListSerializer(serializers.ModelSerializer):
    class Meta:
        model = GlossaryTerm
        fields = ['id', 'term', 'status', 'created_at']


class GlossaryPageConfigSerializer(serializers.ModelSerializer):
    class Meta:
        model = GlossaryPageConfig
        fields = ['id', 'seo_title', 'seo_description', 'updated_at']
        read_only_fields = ['id', 'updated_at']
