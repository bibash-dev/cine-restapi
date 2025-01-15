from django.contrib.auth.models import User
from rest_framework import serializers


class RegistrationSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(
        write_only=True, style={"input_type": "password"}
    )

    class Meta:
        model = User
        fields = ["username", "email", "password", "confirm_password"]
        extra_kwargs = {"password": {"write_only": True}}

    def save(self, **kwargs):
        password = self.validated_data["password"]
        confirm_password = self.validated_data["confirm_password"]
        if password != confirm_password:
            raise serializers.ValidationError(
                {"error": "password and confirm password must match."}
            )
        email = self.validated_data["email"]
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError({"error": "Email already exists."})

        username = self.validated_data["username"]
        account = User(email=email, username=username)
        account.set_password(password)
        account.save()
        return account
