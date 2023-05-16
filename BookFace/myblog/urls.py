from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, re_path

from myblog import views

app_name = 'myblog'
urlpatterns = [
    re_path(
        r'about/$', 
        views.AboutView.as_view(), 
        name='about'),
    re_path(
        r'$', 
        views.AllPost.as_view(), 
        name='post_list'),
    re_path(
        r'post/(?P<pk>\d+)/$', 
        views.PostDetail.as_view(), 
        name='post_detail'
    ),
    re_path(
        r'post/new/$', 
        views.CreatePostView.as_view(), 
        name='post_new'),
    re_path(
        r'post/(?P<pk>\d+)/edit/$',
        views.PostUpdateView.as_view(),
        name='post_edit',
    ),
    re_path(
        r'post/(?P<pk>\d+)/remove/$',
        views.DeletePostView.as_view(),
        name='post_remove',
    ),
    re_path(
        r'drafts/$', 
        views.PostDraftList.as_view(), 
        name='post_draft_list'
    ),
    re_path(
        r'post/(?P<pk>\d+)/comment/$',
        views.CreateCommentView.as_view(),
        name='add_comment_to_post',
    ),
    # re_path(r'comment/(?P<pk>\d+)/approve/$', views.comment_approve , name='comment_approve'),
    # re_path(r'comment/(?P<pk>\d+)/remove/$', views.comment_remove , name='comment_remove'),
    re_path(
        r'post/(?P<pk>\d+)/publish/$', 
        views.post_publish, 
        name='post_publish'
    ),
    re_path(
            r'wall/$', 
            views.Wall.as_view(), 
            name='wall'),
    re_path(
            r'accounts/login/$', 
            views.user_login, 
            name='user_login'),
    re_path(
        r'accounts/registration/$', 
        views.registration, 
        name='registration'
    ),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
