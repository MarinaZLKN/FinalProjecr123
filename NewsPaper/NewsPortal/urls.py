from django.urls import path
from .views import PostList, PostDetail, create_post, PostUpdate, PostDelete, PostSearch


urlpatterns = [
   path('', PostList.as_view(), name='posts'),
   path('<int:pk>', PostDetail.as_view(), name='post_detail'),
   path('create/', create_post, name='create_post'),
   path('update/<int:pk>', PostUpdate.as_view(), name='update_post'),
   path('delete/<int:pk>', PostDelete.as_view(), name='delete_post'),
   path('search/', PostSearch.as_view(),name='post_search'),
]