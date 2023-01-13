from django.urls import path
from posts.views import *

app_name = 'posts'

urlpatterns = [
    path('create'               , PostCreateView.as_view()  , name = 'post-create'),
    path(''                     , PostList.as_view()        , name = 'post-list'),
    path('<int:id>'             , PostDetail.as_view()      , name = 'post-detail'),
    path('<int:id>/<operation>/', PostOperation.as_view()   , name = "post-like_unlike"),
    path('<int:id>/likes'       , PostLikeList.as_view()    , name = 'post-like-list'),
    path('<int:id>/comments'    , PostCommentList.as_view() , name = 'post-comment-list'),
]
