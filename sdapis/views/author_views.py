from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
from django.db.models import Q
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from sdapis.models import Author
from sdapis.serializers import RegistrationSerializer, AuthorSerializer
from sdapis.pagination import AuthorPagination
from .node_helper import is_valid_node


@api_view(['POST'])
def register(request):
    '''
    author registration; parameters: username, email, password, github
    '''
    valid = is_valid_node(request)
    if not valid:
        return Response({"message" : "not a valid node"}, status=status.HTTP_403_FORBIDDEN)

    # register an account
    if Author.objects.filter(email=request.data["email"]).exists():
        return Response({'message' : "email already exists"}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
    serializer = RegistrationSerializer(data=request.data)
    if serializer.is_valid(): # make sure data match the model
        author = serializer.save()
        return Response({"message" : "success, please login"}, status=status.HTTP_201_CREATED)
    else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def author_list(request):
    '''
    get the list of authors
    '''
    valid = is_valid_node(request)
    if not valid:
        return Response({"message" : "not a valid node"}, status=status.HTTP_403_FORBIDDEN)

    if request.method == "GET":
        # get all authors sort by display name
        paginator = AuthorPagination()
        authors = Author.objects.filter(~Q(email="c404t21@admin.com")).order_by('username')
        paginated = paginator.paginate_queryset(authors, request)
        serializer = AuthorSerializer(paginated, many=True)
        return paginator.get_paginated_response(serializer.data)

@api_view(['GET', 'POST'])
def author_detail(request, author_id):
    '''
    view an author detail;
    modify user detail
    '''
    valid = is_valid_node(request)
    if not valid:
        return Response({"message":"node not allowed"}, status=status.HTTP_403_FORBIDDEN)

    if request.method == "GET":
        # get author data
        author = get_object_or_404(Author, author_id=author_id)
        serializer = AuthorSerializer(author)
        return Response(serializer.data)

    elif request.method == "POST":
        data = request.data
        author = get_object_or_404(Author, author_id=author_id)
        serializer = AuthorSerializer(author, data=data)
        if serializer.is_valid():
            if "password" in data and "username" in data and "email" in data:
                author.set_password(data["password"])
                author.username = data["username"]
                author.github = data["github"]
                new_email = data["email"].lower()
                # check new email doesn't already exists
                if author.email != new_email and Author.objects.filter(email=new_email).exists():
                    return Response({"message" : "email already exists"}, status=status.HTTP_422_UNPROCESSABLE_ENTITY)
                author.email = new_email
            author.save()
            serializer.save()
            return Response({"message" : "successful post"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#login
#need to be refined!
@api_view(['POST'])
def login_view(request):
    '''
    author login, return the authors' id
    '''
    author = authenticate(request, email=request.data['email'], password=request.data['password'])
    print(author)
    if author is not None:
        return Response({'authorID':author.author_id}, status=status.HTTP_200_OK)
    else:
        return Response({'message':"incorrect email or password"}, status=status.HTTP_401_UNAUTHORIZED)