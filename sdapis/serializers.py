from rest_framework import serializers
from .models import *

class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['email', 'username', 'password', 'github']

    def save(self):
        author = Author(
            email=self.validated_data['email'],
            username=self.validated_data['username'],
            github=self.validated_data['github']
        )
        password = self.validated_data['password']
        author.set_password(password)
        author.save()
        return author

class AuthorSerializer(serializers.ModelSerializer):
    type = serializers.CharField(source='get_type', required=False)
    id = serializers.CharField(source='get_id', required=False)
    url = serializers.CharField(source='get_id', required=False)
    host = serializers.CharField(source='get_host', required=False)
    displayName = serializers.CharField(source='username', required=False)

    class Meta:
        model = Author
        fields = ['type', 'id', 'url', 'host', 'displayName', 'github', 'profile_image']

class NodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Node
        fields = ['host']