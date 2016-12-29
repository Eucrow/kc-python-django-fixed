from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.exceptions import ValidationError


class UserListSerializer(serializers.Serializer):
    id = serializers.ReadOnlyField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()


class UserSerializer(serializers.Serializer):
    id = serializers.ReadOnlyField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    username = serializers.CharField()
    password = serializers.CharField()
    email = serializers.EmailField()

    def create(self, validated_data):
        instance = User()
        return self.update(instance, validated_data)

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name')
        instance.last_name = validated_data.get('last_name')
        instance.username = validated_data.get('username')
        # make_password guarda la contraseña encriptada
        instance.password = make_password(validated_data.get('password'))
        instance.email = validated_data.get('email')
        instance.save()
        return instance

    # Esto no lo entiendo muy bien... ¿pero cuándo ejecuta los métodos validate_username
    # y validate_email????
    def validate_username(self, username):
        if (self.instance is None or self.instance.username != username)\
                and User.objects.filter(username=username).exists():
            raise ValidationError("El nombre de usuario {0} ya está siendo utilizado".format(username))
        return username

    def validate_email(self, email):
        if (self.instance is None or self.instance.email != email) \
                and User.objects.filter(email=email).exists():
            raise ValidationError("El email {0} ya está siendo utilizado".format(email))
        return email.lower()
