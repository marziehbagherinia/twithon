from django.urls import path
from .views import *

app_name = 'accounts'

urlpatterns = [
    path('', UserDetail.as_view(), name = 'login'),
    path('login', LoginAPI.as_view(), name = 'login'),
    path('register', RegisterAPI.as_view(), name = 'register'),

    # path('create'         , create_user   , name ='create'     ),
    # path('show/<int:id>'  , show_user     , name ='show'       ),
    # path('update/<int:id>', update_user   , name ='update'     ),
    # path('delete/<int:id>', delete_user   , name ='delete'     ),
    # path('login', LoginView.as_view(), name='login'),
]
