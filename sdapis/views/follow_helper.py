from sdapis.models import Author, Follow
from sdapis.serializers import *

def get_followings(author_id):
    follow = Follow.objects.filter(author2=author_id)
    follow_serializer = FollowSerializer(follow, many=True)
    followings = []
    remote = []
    for author in follow_serializer.data:
        following_id = author['author1']
        try:
            following_author = Author.objects.get(author_id=following_id)
            author_serializer = AuthorSerializer(following_author)
            followings.append(author_serializer.data)
        # used to connect remote nodes' authors
        except not follow.exists():
            if following_id in remote: 
                followings.append(following_author)
    return followings

def get_followers(author_id):
    follow = Follow.objects.filter(author1=author_id)
    serializer = FollowSerializer(follow, many=True)
    followers = []
    remote = []
    for author in serializer.data:
        follower_id = author['author2']
        try:
            follower = Author.objects.get(author_id=follower_id)
            serializer = AuthorSerializer(follower)
            followers.append(serializer.data)
        # used to connect remote nodes' authors
        except not follow.exists():
            if follower_id in remote:
                followers.append(follower)
    return followers