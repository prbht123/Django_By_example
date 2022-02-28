
from django.urls import path,include,re_path
from . import views

from .feeds import LatestPostsFeed


urlpatterns = [
    path('',views.post_list,name='post_list'),
    path('postlist',views.PostListView.as_view(),name='postlist'),
    path('post/<int:year>/<int:month>/<int:day>/<str:post>',views.post_detail,name='post_listt'),

    path('email/<int:post_id>',views.post_share_template,name='post_share'),
    path('posttemplate/<int:year>/<int:month>/<int:day>/<str:post>',views.post_detail_template,name='post_list_template'),
    path('postcomment/<int:year>/<int:month>/<int:day>/<str:post>',views.post_detail_comment,name='post_Detail_comment'),
    
    path('tags',views.post_list_tag,name='post_list_tag'),
    path('tagslug/<str:tag_slug>',views.post_list_tag_slug,name='post_list_tagslug'),
    path('tagfilter/<int:pk>',views.post_retrived,name='post_retrived'),

    path('feed/',LatestPostsFeed(), name='post_feed')
    
    
    ]