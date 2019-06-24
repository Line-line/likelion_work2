from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('<int:blog_id>', views.detail, name="detail"),
    path('new/', views.new, name="new"),
    path('create', views.create, name="create"),      # path만들었다고 html만 부르는것뿐만이 아니라 함수를 불러 줄 수 있다.
    path('edit/<int:blog_id>', views.edit, name="edit"),
    path('delete/<int:blog_id>', views.delete, name="delete"),

    # 댓글
    path('comment_add/<int:blog_id>', views.comment_add, name='comment_add'),
    path('comment_edit/<int:comment_id>', views.comment_edit, name='comment_edit'),
    path('comment_delete/<int:comment_id>', views.comment_delete, name='comment_delete'),
]