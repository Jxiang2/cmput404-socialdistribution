from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework import status
from sdapis.models import Author, Follow
from sdapis.serializers import AuthorSerializer, FollowSerializer
from sdapis.permissions import AccessPermission, CustomAuthentication
from .helper import is_valid_node

def get_remote_authors():
    pass

def find_remote_author():
    pass

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


@api_view(['GET'])
@authentication_classes([CustomAuthentication])
@permission_classes([AccessPermission])
def follower_list(request, author_id): # GET: get a list of authors who are their followers
    valid = is_valid_node(request)
    if not valid:
        return Response({"message":"not a valid node"}, status=status.HTTP_403_FORBIDDEN)

    followers = get_followers(author_id)
    data ={"type": "followers", "items":followers}
    return Response(data, status=status.HTTP_200_OK)


@api_view(['GET', 'DELETE', 'PUT'])
@authentication_classes([CustomAuthentication])
@permission_classes([AccessPermission])
def follower(request, author_id, author_id2):
    '''
    author_id2 follows author_id,
    author_id1 view followers, 
    author_id1 remove author_id2 as a follower,
    '''
    valid = is_valid_node(request)
    # ckeck if a valid node
    if not valid:
        return Response({"message":"not a valid node"}, status=status.HTTP_403_FORBIDDEN)

    # Add a follower
    elif request.method == "PUT": 
        if Follow.objects.filter(author1=author_id, author2=author_id2).exists():
            # already a follower
            return Response({"message":"already a follower"}, status=status.HTTP_200_OK)
        else:
            follow = Follow(author1=author_id, author2=author_id2)
            follow.save()
            return Response({"message":"success add"}, status=status.HTTP_200_OK)

    # check if follower
    if request.method == "GET":
        if Follow.objects.filter(author1=author_id, author2=author_id2).exists():
            return Response({"message":"indeed a follower"}, status=status.HTTP_200_OK)
        else:
            return Response({"message":"not a follower"}, status=status.HTTP_200_OK)

    # remove an existing follower
    elif request.method == "DELETE":
        try:
            follow = Follow.objects.get(author1=author_id, author2=author_id2)
        except Follow.DoesNotExist:
            # not a follower
            return Response({"message":"not a follower"}, status=status.HTTP_200_OK)
        follow.delete()
        return Response({"message":"success remove"}, status=status.HTTP_200_OK)

@api_view(['GET'])
@authentication_classes([CustomAuthentication])
@permission_classes([AccessPermission])
def following_list(request, author_id):
    valid = is_valid_node(request)
    if not valid:
        return Response({"message" : "not a valid node"}, status=status.HTTP_403_FORBIDDEN)

    followings = get_followings(author_id)
    return Response({"type" : "followings" , "items" : followings}, status=status.HTTP_200_OK)