from django.urls import path

from . import views

urlpatterns = [
    # 加载基本页面
    path('', views.index, name='vote_page'),
    # 添加选项
    path('vote_add_option/', views.vote_add_option, name='vote_add_option'),
    # 投票
    path('vote/', views.vote, name='vote'),
    # 添加投票人
    path('add_user/', views.add_user, name='add_user')
]
