from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer
from django.contrib.auth.decorators import login_required
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import status

# Post ViewSet (for CRUD operations with authentication)
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]  # Require authentication for CRUD operations

    def perform_create(self, serializer):
        # Automatically set the author to the logged-in user
        serializer.save(author=self.request.user)

    # Optional: Custom action (e.g., for liking a post, etc.)
    @action(detail=True, methods=['post'])
    def like(self, request, pk=None):
        post = self.get_object()
        # Handle liking a post (this is just an example)
        post.likes += 1
        post.save()
        return Response({'status': 'Post liked'})

# Comment ViewSet (for CRUD operations with authentication)
class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]  # Require authentication for CRUD operations

    def perform_create(self, serializer):
        # Automatically set the author to the logged-in user
        post = serializer.validated_data['post']
        serializer.save(author=self.request.user)

