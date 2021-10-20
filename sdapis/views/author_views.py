from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
from django.db.models import Q
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework import status
from sdapis.models import Author
from sdapis.serializers import RegistrationSerializer, AuthorSerializer
from sdapis.permissions import AccessPermission, CustomAuthentication
from sdapis.views.helper import is_valid_node


@api_view(['POST'])
@authentication_classes([CustomAuthentication])
@permission_classes([AccessPermission])
def register(request):
    valid = is_valid_node(request)
    if not valid:
        return Response({"message" : "not a valid node"}, status=status.HTTP_403_FORBIDDEN)

    else:
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
@authentication_classes([CustomAuthentication])
@permission_classes([AccessPermission])
def author_list(request):
    valid = is_valid_node(request)
    if not valid:
        return Response({"message" : "not a valid node"}, status=status.HTTP_403_FORBIDDEN)

    if request.method == "GET":
        # get all authors sort by display name
        authors = Author.objects.filter(~Q(email="c404t21@admin.com")).order_by('username')
        serializer = AuthorSerializer(authors, many=True)
        custom_data = {
            "type": "authors",
            "items": serializer.data
        }
        return Response(custom_data)

@api_view(['GET', 'POST'])
@authentication_classes([CustomAuthentication])
@permission_classes([AccessPermission])
def author_detail(request, author_id):
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

#login/out can be added later if needed
@api_view(['POST'])
@authentication_classes([CustomAuthentication])
@permission_classes([AccessPermission])
def login_view(request):
    user = authenticate(request, email=request.data['email'], password=request.data['password'])
    print(user)
    if user is not None:
        return Response({'authorID':user.author_id}, status=status.HTTP_200_OK)
    else:
        return Response({'message':"incorrect email or password"}, status=status.HTTP_401_UNAUTHORIZED)