from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from django.db.models import Q
from rest_framework.views import APIView

from blog.models import Blog
from blog.permissions import IsAdminOrOwner
from blog.serializers import BlogSerializer, UserTokenSerializer


# View Yozish usuli
# 1. Function Based View
# 2. Class Based View

# Views Built-in Types
# View: APIView
# Generic
# ViewSet
class MyBlogListAPIView(APIView):
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [IsAuthenticated, IsAdminOrOwner]

    def get(self, request, *args, **kwargs):
        # owner
        blogs = Blog.objects.filter(author=request.user)
        # search
        title = request.query_params.get("title", None)
        desc = request.query_params.get("description", None)

        if title:
            blogs = blogs.filter(title__icontains=title)

        if desc:
            blogs = blogs.filter(description__icontains=desc)

        serializer = BlogSerializer(blogs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class BlogListCreateAPIView(APIView):
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [IsAuthenticated, IsAdminOrOwner]

    def get(self, request):
        # all
        blogs = Blog.objects.all()
        # search
        title = request.query_params.get("title", None)
        desc = request.query_params.get("description", None)

        if title:
            blogs = blogs.filter(title__icontains=title)

        if desc:
            blogs = blogs.filter(description__icontains=desc)

        serializer = BlogSerializer(blogs, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = BlogSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BlogRetriveUpdateDeleteAPIView(APIView):
    authentication_classes = [TokenAuthentication, ]
    permission_classes = [IsAuthenticated, IsAdminOrOwner]

    def get(self, request, pk):
        blog = get_object_or_404(Blog, id=pk)
        self.check_object_permissions(request, blog)
        serializer = BlogSerializer(blog)
        return Response(serializer.data)

    def put(self, request, pk):
        blog = get_object_or_404(Blog, id=pk)
        self.check_object_permissions(request, blog)
        serializer = BlogSerializer(blog, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        blog = get_object_or_404(Blog, id=pk)
        self.check_object_permissions(request, blog)
        blog.delete()
        return Response({"success": "Blog deleted"}, status=status.HTTP_204_NO_CONTENT)


class UserRegisterView(APIView):
    permission_classes = [AllowAny, ]

    def post(self, request):
        serializer = UserTokenSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, created = Token.objects.get_or_create(user=user)
            data = {
                "token": str(token),
                "user_id": user.id,
                "username": user.username,
                "email": user.email
            }
            return Response(data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
