from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework import status
from sdapis.models import Author, Follow, Inbox, Post
from .follow_helper import get_followers
from .node_helper import is_valid_node
from sdapis.serializers import *
from sdapis.permissions import CustomAuthentication, AccessPermission



@api_view(['GET', 'POST', 'DELETE'])
@authentication_classes([CustomAuthentication])
@permission_classes([AccessPermission])

def inbox_detail(request, author_id):
    '''
    check, update and clear an author's inbox
    '''
    valid = is_valid_node(request)
    if not valid:
        return Response({"message":"not a valid node"}, status=status.HTTP_403_FORBIDDEN)

    # get inbox objs
    if request.method == 'GET':
        try:
            Author.objects.get(author_id=author_id)
        except Author.DoesNotExist:
            return Response({"message":"author id not found"}, status=status.HTTP_404_NOT_FOUND)
        inbox, created = Inbox.objects.get_or_create(author_id=author_id)
        serializer = InboxSerializer(inbox)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # clear inbox
    elif request.method == 'DELETE':
        inbox, created = Inbox.objects.get_or_create(author_id=author_id)
        if not created:
            inbox.delete()
        return Response({'message':'inbox cleared'}, status=status.HTTP_200_OK)

    # send to others' inbox
    elif request.method == 'POST':
        type = request.data['type']

        # friend requests
        if type == 'follow':
            new_follower_id = request.data['new_follower_id']
            try:
                new_follower = Author.objects.get(author_id=new_follower_id)
            except Author.DoesNotExist:
                return Response({"message":"author id not found"}, status=status.HTTP_404_NOT_FOUND)
            
            #follow before send friend request
            if not Follow.objects.filter(author1=author_id, author2=new_follower_id).exists():
                follow = Follow(author1=author_id, author2=new_follower_id)
                follow.save()
            
            author = get_object_or_404(Author, author_id=author_id)
            summary = new_follower.username + " wants to follow " + author.username
            new_follower_serialized = AuthorSerializer(new_follower).data
            author_serialized = AuthorSerializer(author).data
            inbox, _ = Inbox.objects.get_or_create(author_id=author_id)
            #add newst friend request at front
            inbox.items.insert(0, {"type": "Follow",
            "summary":summary,
            "actor":new_follower_serialized,
            "object":author_serialized}
            )
            inbox.save()
            return Response({"message":"friend request sent"}, status=status.HTTP_200_OK)

        # others' posts
        elif type == "post":
            post_id = request.data['post_id']
            post = Post.objects.get(id=post_id)
            item_serializer = PostSerializer(post)
            data = item_serializer.data

            try:
                Author.objects.get(author_id=author_id)
                inbox, _ = Inbox.objects.get_or_create(author_id=author_id)
                #add newst post at the front
                inbox.items.insert(0, data)
                inbox.save()
                return Response({"message":"post sent"}, status=status.HTTP_200_OK)
            except Author.DoesNotExist:
                return Response({"message": "the author does not exist"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@authentication_classes([CustomAuthentication])
@permission_classes([AccessPermission])
def friend(request, author_id):
    '''
    get the list of friends of an author
    '''
    valid = is_valid_node(request)
    if not valid:
        return Response({"message":"not a valid node"}, status=status.HTTP_403_FORBIDDEN)

    followers = get_followers(author_id)
    friends = []
    for f in followers:
        follower_id = f['id'].split("/")[-1]
        if Follow.objects.filter(author1=follower_id, author2=author_id).exists():
            # check if mutually followed, if ture, friend
            friends.append(f)
    return Response({"type": "friends","items":friends}, status=status.HTTP_200_OK)
            