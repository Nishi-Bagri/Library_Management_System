from rest_framework import serializers
from .models import Activity


class ActivitySerializer(serializers.ModelSerializer):

    performed_by = serializers.SerializerMethodField()

    def get_performed_by(self, obj):
        return obj.performed_by.username if obj.performed_by else "System"

    class Meta:
        model = Activity
        fields = [
            "id",
            "action",
            "description",
            "performed_by",
            "created_at",
        ]
        