from rest_framework import serializers

from accounts.models import CustomUser


class RegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'password', 'password2')
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, data):
        password = data.get('password')
        password2 = data.get('password2')

        if password != password2:
            raise serializers.ValidationError({'password': 'Passwords do not match.'})

        return data

    def create(self, validated_data):
        user = CustomUser(
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
