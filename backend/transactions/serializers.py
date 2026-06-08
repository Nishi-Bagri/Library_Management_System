from rest_framework import serializers
from .models import IssueBook

class IssueBookSerializer(serializers.ModelSerializer):

    user_name = serializers.CharField(source='user.username', read_only=True)
    book_name = serializers.CharField(source='book.title', read_only=True)
    issued_by_name = serializers.CharField(source='issued_by.username', read_only=True)

    class Meta:
        model = IssueBook
        fields = '__all__'
    
        read_only_fields = [
            'issued_by',
            'issue_date',
            'due_date',
            'status',
            'late_days',
            'fine_amount',
            'renewal_count'
        ]