from rest_framework import serializers

from .models import CustomUser, Address


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6, style={"input_type": "password"})
    class Meta:
        model = CustomUser
        fields = ["id", "email", "phone_number", "password"]

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            email=validated_data["email"],
            password=validated_data["password"],
            phone_number=validated_data.get("phone_number", "")
        )
        return user
    

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ["id", "title", "receiver_name", "receiver_phone", "city", "state", "postal_address", "postal_code"]
        read_only_fields = ["id"]