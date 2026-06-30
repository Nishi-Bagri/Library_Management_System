from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from .models import Activity
from .serializers import ActivitySerializer


class RecentActivityAPIView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        if request.user.role not in ["ADMIN", "LIBRARIAN"]:
            return Response(
                {
                    "error": "Permission denied."
                },
                status=status.HTTP_403_FORBIDDEN
            )

        activities = (
            Activity.objects
            .select_related("performed_by")
            .order_by("-created_at")[:10]
        )

        serializer = ActivitySerializer(
            activities,
            many=True
        )

        return Response(serializer.data)