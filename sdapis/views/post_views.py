from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework import status
from sdapis.models import Post
from sdapis.serializers import PostSerializer
from sdapis.pagination import PostPagination
from sdapis.permissions import AccessPermission, CustomAuthentication
from .helper import is_valid_node



@api_view(['GET', 'POST'])
@authentication_classes([CustomAuthentication])
@permission_classes([AccessPermission])
def post_view(request, author_id):
    valid = is_valid_node(request)
    if not valid:
        return Response({"message":"not a valid node"}, status=status.HTTP_403_FORBIDDEN)

    if request.method == "GET":
        # get recent posts of author (paginated)
        paginator = PostPagination()
        posts = Post.objects.filter(author_id=author_id, unlisted=False).order_by('-published')
        paginated = paginator.paginate_queryset(posts, request)
        serializer = PostSerializer(paginated, many=True)
        return paginator.get_paginated_response(serializer.data)

    elif request.method == "POST":
        # create a new post
        data = request.data
        data['author_id'] = author_id
        serializer = PostSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({'message':serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'DELETE'])
@authentication_classes([CustomAuthentication])
@permission_classes([AccessPermission])
def post_detail_view(request, author_id, post_id):
    valid = is_valid_node(request)
    if not valid:
        return Response({"message":"Node not allowed"}, status=status.HTTP_403_FORBIDDEN)

    if request.method == "GET":
        # get post data
        post = get_object_or_404(Post, post_id=post_id)
        serializer = PostSerializer(post)
        return Response(serializer.data)

    elif request.method == "DELETE":
        try:
            del_post = get_object_or_404(Post, post_id=post_id)
        except Post.DoesNotExist:
            return Response(status = status.HTTP_404_NOT_FOUND)
        operation = del_post.delete()
        if operation:
            return Response({'message': "delete successful!"}, status=status.HTTP_200_OK)
        else:
            return Response({'message':"delete was unsuccessful"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)