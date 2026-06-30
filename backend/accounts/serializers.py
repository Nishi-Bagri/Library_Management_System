from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password

from .models import (
    User,
    PasswordResetRequest,
    AccountDeactivationRequest
)


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "role",
            "is_active",
        ]


class RegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "role",
        ]

    def validate(self, value):

        if value == "ADMIN":
            raise serializers.ValidationError(
                "Admin accounts cannot be created."
            )

        return value

    def create(self, validated_data):

        user = User.objects.create(
            username=validated_data["username"],
            email=validated_data["email"],
            role=validated_data["role"],
        )

        return user


class LoginSerializer(serializers.Serializer):

    username = serializers.CharField()

    password = serializers.CharField(
        write_only=True
    )

    def validate(self, data):

        user = authenticate(
            username=data["username"],
            password=data["password"],
        )

        if not user:
            raise serializers.ValidationError(
                "Invalid Credentials"
            )

        data["user"] = user

        return data


class CreatePasswordSerializer(serializers.Serializer):

    password = serializers.CharField(
        required=True,
        write_only=True
    )


class ForgotPasswordSerializer(serializers.Serializer):

    username = serializers.CharField()


class PasswordResetRequestSerializer(serializers.ModelSerializer):

    username = serializers.CharField(
        source="user.username",
        read_only=True
    )

    class Meta:
        model = PasswordResetRequest
        fields = [
            "id",
            "username",
            "status",
            "requested_at",
            "approved_at",
            "completed_at",
        ]

class AccountDeactivationRequestSerializer(serializers.ModelSerializer):

    username = serializers.CharField(
        source="user.username",
        read_only=True
    )

    class Meta:
        model = AccountDeactivationRequest

        fields = [
            "id",
            "username",
            "reason",
            "remarks",
            "status",
            "requested_at",
            "approved_by",
            "approved_at",
            "rejected_by",
            "rejected_at",
        ]

        read_only_fields = [
            "status",
            "requested_at",
            "approved_by",
            "approved_at",
            "rejected_by",
            "rejected_at",
            "username",
        ]

class ChangePasswordSerializer(serializers.Serializer):

    current_password = serializers.CharField(write_only = True, required = True)

    new_password = serializers.CharField(write_only = True, required=True, validators=[validate_password])

    confirm_password = serializers.CharField(write_only = True, required=True)

    def validate(self, attrs):

        if attrs["new_password"] != attrs["confirm_password"]:
            raise serializers.ValidationError(
                {
                    "confirm_password":
                    "New password and new password do not match"
                }
            )
        
        return attrs