from django.urls import path
from comments.views import *

app_name = 'comments'

urlpatterns = [
    path('create'  , CommentCreateView.as_view(), name = 'comment-create'),
    path(''        , CommentList.as_view()      , name = 'comment-list'),
    path('<int:id>', CommentDetail.as_view()    , name = 'comment-detail'),
]
