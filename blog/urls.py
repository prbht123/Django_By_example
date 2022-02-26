
from django.urls import path,include,re_path
from . import views

urlpatterns = [
    path('',views.post_list,name='post_list'),
    path('postlist',views.PostListView.as_view(),name='postlist'),
    path('post/<int:year>/<int:month>/<int:day>/<str:post>',views.post_detail,name='post_list'),
    path('email/<int:post_id>',views.post_share,name='post_share'),

    
    ]