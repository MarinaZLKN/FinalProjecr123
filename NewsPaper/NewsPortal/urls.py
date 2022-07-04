from django.urls import path
from .views import PostList, PostDetail, PostCreate, PostUpdate, PostDelete, PostSearch



urlpatterns = [
   path('', PostList.as_view(), name='posts'),
   path('<int:pk>', PostDetail.as_view(), name='post_detail'),
   path('create/', PostCreate.as_view(), name='create_post'),
   path('update/<int:pk>', PostUpdate.as_view(), name='update_post'),
   path('delete/<int:pk>', PostDelete.as_view(), name='delete_post'),
   path('search/', PostSearch.as_view(), name='post_search'),
]