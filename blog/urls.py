from django.urls import path
from . import views

urlpatterns = [
    path('', views.IndexPage.as_view(), name='index'),
    path('xxxx/', views.ContactPage.as_view(), name='contact'), # name='contact' use in <li><a href="{% url 'contact' %}" title="">تماس</a></li>

    #api
    path('article/all/',views.AllArticleAPIView.as_view(), name='all_article')
    ]