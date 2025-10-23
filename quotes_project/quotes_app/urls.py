from django.urls import path
from . import views

app_name = 'quotes_app'

urlpatterns = [
    path('', views.main, name='root'),
    path('page/<int:page>/', views.main, name='root_paginate'),
    path('author/<int:author_id>/', views.author_detail, name='author_detail'),
    path('tag/<str:tag_name>/', views.tag_quotes, name='tag_quotes'),
    path('add_quote/', views.add_quote, name='add_quote'),
]
