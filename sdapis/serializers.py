from rest_framework import serializers
from django.utils import timezone
from tzlocal import get_localzone
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

class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        # author2 follows author1
        fields = ['author1', 'author2']

class NodeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Node
        fields = ['host']

class InboxSerializer(serializers.ModelSerializer):
    type = serializers.CharField(source='get_type', required=False)
    author = serializers.CharField(source='get_author')

    class Meta:
        model = Inbox
        fields = ['type', 'author', 'items']

class PostSerializer(serializers.ModelSerializer):
    post_id = serializers.CharField(source='get_post_id', required=False)
    type = serializers.CharField(source='get_type', required=False)
    category = serializers.CharField(required=True)
    #comments = serializers.URLField(source='get_comments_url', required=False)
    
    def get_local_now():
        local_tz = get_localzone()
        timezone.activate(local_tz)
        now = timezone.localtime(timezone.now())
        return now

    publushed = get_local_now()
    
    def to_representation(self, instance):
        response = super(PostSerializer, self).to_representation(instance)
        author = Author.objects.get(author_id=instance.author_id)
        author_serializer = AuthorSerializer(author)
        response['author'] = author_serializer.data # add author data
        #response['comment_list'] = instance.comment_list[:5]
        return response

    class Meta:
        model = Post
        #comments will be added later
        fields = ['type', 'title', 'description', 'content','post_id', 
        'author_id', 'contentType', 'count','published', 'visibility', 'category', 'unlisted']