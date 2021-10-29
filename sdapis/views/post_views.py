from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.conf import settings
from sdapis.pagination import PostPagination
from sdapis.serializers import PostSerializer
from sdapis.models import Post, Author
from .node_helper import is_valid_node

HOST_NAME = settings.HOST_NAME

@api_view(['GET'])
def all_post_view(request):
    '''
    get all posts, ordered by published time
    '''
    valid = is_valid_node(request)
    if not valid:
        return Response({"message":"not a valid node"}, status=status.HTTP_403_FORBIDDEN)

    if request.method == "GET":
        # get recent posts of author (paginated)
        paginator = PostPagination()
        posts = Post.objects.all().order_by('-published')
        paginated = paginator.paginate_queryset(posts, request)
        serializer = PostSerializer(paginated, many=True)
        return paginator.get_paginated_response(serializer.data)


@api_view(['GET', 'POST'])
def post_view(request, author_id):
    '''
    get an author's all posts,
    create a post
    '''
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


@api_view(['GET','DELETE', 'PUT', 'POST'])
def post_detail_view(request, author_id, post_id):
    '''
    view a post's detail, delete a post(authenticated), forward a post, update a post(authenticated)
    '''
    valid = is_valid_node(request)
    if not valid:
        return Response({"message":"not a valid node"}, status=status.HTTP_403_FORBIDDEN)

    if request.method == "GET":
        # get post data
        post = get_object_or_404(Post, id=post_id)
        serializer = PostSerializer(post)
        return Response(serializer.data)

    elif request.method == "DELETE":
        try:
            del_post = get_object_or_404(Post, id=post_id)
        except Post.DoesNotExist:
            return Response(status = status.HTTP_404_NOT_FOUND)
        del_post.delete()
        return Response({'message': "delete successful!"}, status=status.HTTP_200_OK)

    elif request.method == "PUT":
        # create a new post with the given id
        try:
            author = Author.objects.get(author_id=author_id)
            po = Post.objects.get(id=post_id)
        except Author.DoesNotExist:
            return Response({"message":"author id not found"}, status=status.HTTP_404_NOT_FOUND)
        except Post.DoesNotExist:
            return Response({"message":"post id not found"}, status=status.HTTP_404_NOT_FOUND)
        data = request.data
        data['id'] = post_id
        data['source'] = request.build_absolute_uri()
        data['origin'] = HOST_NAME
        foward_author = data['author_id']
        
        try:
            get_object_or_404(Author, author_id=foward_author)
        except Author.DoesNotExist:
            return Response({"message": "foward author does not exist"}, status=status.HTTP_404_NOT_FOUND)

        serializer = PostSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({'message':serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "POST":
        # update the post
        new_data = request.data
        new_data['author_id'] = author_id
        new_data['post_id'] = id
        try:
            this_post = get_object_or_404(Post, id=post_id)
        except Post.DoesNotExist:
            return Response({"message":"post not found"}, status = status.HTTP_404_NOT_FOUND)
        if this_post.author_id != author_id:
            return Response({"message":"author not found"}, status = status.HTTP_401_UNAUTHORIZED)
        serializer = PostSerializer(this_post, data=new_data)
        if serializer.is_valid():
            post = serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response({'message':serializer.errors}, status=status.HTTP_400_BAD_REQUEST)