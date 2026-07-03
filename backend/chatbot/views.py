from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .services import AIService


class ChatBotAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        message = request.data.get("message", "").strip()

        if not message:
            return Response(
                {"reply": "Please enter a message."},
                status=400,
            )

        ai = AIService()
        reply = ai.chat(
            message=message,
            user=request.user,
        )

        return Response({"reply": reply})