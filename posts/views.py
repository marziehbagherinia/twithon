from django.contrib.auth.models import User

from rest_framework import status
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from posts.models import Post
from comments.models import Comment
from posts.serializers import PostSerializer
from comments.serializers import CommentSerializer
from accounts.serializers import UserSerializer

class PostCreateView(generics.GenericAPIView):
    serializer_class = PostSerializer
    permission_classes = (IsAuthenticated, )

    def post(self, request, *args, **kwargs):
        data = request.data
        data['user'] = request.user.id
        
        serializer = self.get_serializer(data = data)
        serializer.is_valid(raise_exception = True)
        post = serializer.save()

        return Response({
            "post": PostSerializer(post, context = self.get_serializer_context()).data,
        })

class PostList(generics.GenericAPIView):
    permission_classes = (IsAuthenticated, )
    
    def get(self, request):

        try:
            posts = Post.objects.filter(user = request.user.id).order_by('created_on')
        except Post.DoesNotExist:
            data = {
                "message": "There is no Post with this user_id."
            }
            return Response(data = data, status = status.HTTP_404_NOT_FOUND)

        serializer = PostSerializer(posts, many = True)

        return Response(serializer.data)

class PostDetail(generics.GenericAPIView):
    permission_classes = (IsAuthenticated, )
    
    def get(self, request, id):

        try:
            post = Post.objects.get(id = id)
        except Post.DoesNotExist:
            data = {
                "message": "Post with this id does not exist."
            }
            return Response(data = data, status = status.HTTP_404_NOT_FOUND)

        serializer = PostSerializer(post)

        return Response(serializer.data)

    def put(self, request, id):

        try:
            post = Post.objects.get(id = id, user = request.user.id)
        except User.DoesNotExist:
            data = {
                "message": "Post with this id does not exist."
            }
            return Response(data = data, status = status.HTTP_404_NOT_FOUND)

        serializer = PostSerializer(post, data = request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):

        try:
            post = Post.objects.get(id = id, user = request.user.id)
        except User.DoesNotExist:
            data = {
                "message": "Post with this id does not exist."
            }
            return Response(data = data, status = status.HTTP_404_NOT_FOUND)

        post.delete()
        return Response(status = status.HTTP_204_NO_CONTENT)


class PostCommentList(generics.GenericAPIView):
    permission_classes = (IsAuthenticated, )
    
    def get(self, request, id):

        try:
            post = Post.objects.get(id = id)
            comments = Comment.objects.filter(user = request.user.id, post = post.id)
        except Post.DoesNotExist:
            data = {
                "message": "Post with this id does not exist."
            }
            return Response(data = data, status = status.HTTP_404_NOT_FOUND)
        except Comment.DoesNotExist:
            data = {
                "message": "There is no comment for this post"
            }
            return Response(data = data, status = status.HTTP_404_NOT_FOUND)

        serializer = CommentSerializer(comments, many = True)

        return Response(serializer.data)

class PostOperation(generics.GenericAPIView):
    permission_classes = (IsAuthenticated, )
    
    def get(self, request, id, operation):

        try:
            post = Post.objects.get(id = id)
        except Post.DoesNotExist:
            data = {
                "message": "Post with this id does not exist."
            }
            return Response(data = data, status = status.HTTP_404_NOT_FOUND)
            
        if operation == 'unlike':
            post.remove_like(request.user)
        elif operation =='like':
            post.add_like(request.user)

        return Response({
            "message" : '{operation} has done successfully.'.format(operation = operation),
            "likes"   : 'The number of likes for post {id} is equal to: {post_likes}'.format(id = id, post_likes = post.likes.count()),
        })

class PostLikeList(generics.GenericAPIView):
    permission_classes = (IsAuthenticated, )
    
    def get(self, request, id):

        try:
            post = Post.objects.get(id = id)
        except Post.DoesNotExist:
            data = {
                "message": "Post with this id does not exist."
            }
            return Response(data = data, status = status.HTTP_404_NOT_FOUND)

        serializer = UserSerializer(post.likes, many = True)

        return Response(serializer.data)
        