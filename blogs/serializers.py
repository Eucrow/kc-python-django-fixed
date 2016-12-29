from django.contrib.auth.models import User
from rest_framework import serializers

class BlogSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = '__all__' #it's mandatory especify 'fields'

