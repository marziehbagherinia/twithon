from rest_framework import status
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from comments.models import Comment
from comments.serializers import CommentSerializer

class CommentCreateView(generics.GenericAPIView):
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticated, )

    def post(self, request, *args, **kwargs):
        data = request.data
        data['user'] = request.user.id
        
        serializer = self.get_serializer(data = data)
        serializer.is_valid(raise_exception = True)
        comment = serializer.save()

        return Response({
            "comment": CommentSerializer(comment, context = self.get_serializer_context()).data,
        })

class CommentList(generics.GenericAPIView):
    permission_classes = (IsAuthenticated, )
    
    def get(self, request):

        try:
            comments = Comment.objects.filter(user = request.user.id).order_by('created_on')
        except Comment.DoesNotExist:
            data = {
                "message": "There is no Comment with this user_id."
            }
            return Response(data = data, status = status.HTTP_404_NOT_FOUND)

        serializer = CommentSerializer(comments, many = True)

        return Response(serializer.data)

class CommentDetail(generics.GenericAPIView):
    permission_classes = (IsAuthenticated, )
    
    def get(self, request, id):

        try:
            comment = Comment.objects.get(id = id)
        except Comment.DoesNotExist:
            data = {
                "message": "Comment with this id does not exist."
            }
            return Response(data = data, status = status.HTTP_404_NOT_FOUND)

        serializer = CommentSerializer(comment)

        return Response(serializer.data)

    def put(self, request, id):

        try:
            comment = Comment.objects.get(id = id, user = request.user.id)
        except Comment.DoesNotExist:
            data = {
                "message": "Comment with this id does not exist."
            }
            return Response(data = data, status = status.HTTP_404_NOT_FOUND)

        serializer = CommentSerializer(comment, data = request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):

        try:
            comment = Comment.objects.get(id = id, user = request.user.id)
        except Comment.DoesNotExist:
            data = {
                "message": "Comment with this id does not exist."
            }
            return Response(data = data, status = status.HTTP_404_NOT_FOUND)

        comment.delete()
        return Response(status = status.HTTP_204_NO_CONTENT)