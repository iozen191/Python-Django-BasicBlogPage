from django.contrib import admin
from django.urls import path
from . import views

app_name = "article"

urlpatterns = [
    path('dashboard/',views.dashboard,name ="dashboard"),
    path('addarticle/',views.addArticle,name ="addarticle"),
    path('article/<int:id>',views.details,name ="details"),
    path('update/<int:id>',views.update,name ="update"),
    path('delete/<int:id>',views.deleteArticle,name ="delete"),
    path('',views.articles,name ="articles"),
    path('comments/<int:id>',views.addComments,name ="comments"),
]
