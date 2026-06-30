from django.utils import timezone
from rest_framework import serializers
from .models import IssueBook


class IssueBookSerializer(serializers.ModelSerializer):

    user_name = serializers.CharField(source='user.username', read_only=True)
    book_name = serializers.CharField(source='book.title', read_only=True)
    issued_by_name = serializers.CharField(source='issued_by.username', read_only=True)

    display_status = serializers.SerializerMethodField()
    fine_amount = serializers.SerializerMethodField()

    def get_display_status(self, obj):

        if (
            obj.status == "ISSUED"
            and obj.due_date < timezone.now().date()
        ):
            return "OVERDUE"

        return obj.status

    def get_fine_amount(self, obj):

        # Show stored fine for returned books
        if obj.status == "RETURNED":
            return obj.fine_amount

        # Calculate live fine for overdue books
        if (
            obj.status == "ISSUED"
            and obj.due_date < timezone.now().date()
        ):
            late_days = (
                timezone.now().date() - obj.due_date
            ).days

            return late_days * 10

        return 0

    class Meta:
        model = IssueBook
        fields = [
            "id",
            "user",
            "book",
            "issued_by",
            "issue_date",
            "due_date",
            "status",
            "display_status",
            "late_days",
            "fine_per_day",
            "fine_amount",
            "renewal_count",
            "user_name",
            "book_name",
            "issued_by_name",
        ]

        read_only_fields = [
            "issued_by",
            "issue_date",
            "due_date",
            "status",
            "late_days",
            "renewal_count",
            "fine_per_day",
        ]

class FineSummarySerializer(serializers.Serializer):

    user = serializers.IntegerField()
    username = serializers.CharField(source="user__username")
    books_with_fine = serializers.IntegerField()
    total_fine = serializers.DecimalField(
        max_digits=10,
        decimal_places=2
    )


class FineHistorySerializer(serializers.ModelSerializer):

    book_title = serializers.CharField(
        source="book.title",
        read_only=True
    )

    return_date = serializers.DateField(
        source="actual_return_date",
        read_only=True
    )

    class Meta:
        model = IssueBook
        fields = [
            "book_title",
            "issue_date",
            "due_date",
            "return_date",
            "late_days",
            "fine_per_day",
            "fine_amount",
        ]