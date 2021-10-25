from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework import status
from sdapis.models import Follow
from sdapis.permissions import AccessPermission, CustomAuthentication
from .follow_helper import get_followers, get_followings
from .node_helper import is_valid_node


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