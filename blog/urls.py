from django.urls import path
from . import views

urlpatterns = [
    path('', views.IndexPage.as_view(), name='index'),
    path('contact/', views.ContactPage.as_view(), name='contact'), # name='contact' use in <li><a href="{% url 'contact' %}" title="">تماس</a></li>

    #api
    path('article/all/',views.AllArticleAPIView.as_view(), name='all_article'),
    path('article/', views.SingleArticleAPIView.as_view(), name='singel_article'),
    path('article/search/',views.SearchArticleAPIView.as_view(), name='search_article'),
    path('article/submit/',views.SubmitArticleAPIView.as_view(), name='submit_article'),
    path('article/update-cover/', views.UpdateArticleAPIView.as_view(), name='update_article'),
    path('article/delete/', views.DeleteArticleAPIView.as_view(), name='delete_article'),
    ]