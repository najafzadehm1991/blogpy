from django.shortcuts import render
from django.views.generic import TemplateView
from .models import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from . import serializers

class IndexPage(TemplateView):

    def get(self, request, **kwargs):

        article_data = []
        all_articles = Article.objects.all().order_by('-created_at')[:2]

        for article in all_articles:
            article_data.append({
                'title': article.title,
                'cover': article.cover.url,
                'category': article.category.title,
                'created_at': article.created_at,
            })

        promote_data = []
        all_promote_articles = Article.objects.filter(promote = True)
        for promote_article in all_promote_articles:
            promote_data.append({
                'category': promote_article.category.title,
                'title': promote_article.title,
                'author': promote_article.author.user.first_name + " " + promote_article.author.user.last_name,
                'avatar': promote_article.author.avatar.url if promote_article.author.avatar else None,
                'cover': promote_article.cover.url if promote_article.cover else None,
                'created_at': promote_article.created_at,
            })



        context = {
            'article_data': article_data,
            'promote_article_data': promote_data,
        }

        return render(request, 'index.html', context)


class ContactPage(TemplateView):
    template_name = "page-contact.html"


#api

class AllArticleAPIView(APIView):

    def get(self, request, format=None): #The format parameter is used to determine the content type of the response to be returned by the API view, such as JSON or XML. If the format parameter is not specified in the URL request, Django REST Framework will use the default format specified in the DEFAULT_RENDERER_CLASSES setting.
        try:
            all_article = Article.objects.all().order_by('-created_at')[:2]
            data = []

            for article in all_article:
                data.append({
                    "title": article.title,
                    "cover": article.cover.url if article.cover else None,
                    "content": article.content,
                    "created_at": article.created_at,
                    "category": article.category.title,
                    "author": article.author.user.first_name + " " + article.author.user.last_name,
                    "promote": article.promote,

                })

            return Response({'data': data}, status=status.HTTP_200_OK)
        except:
            return Response({'status': "internal Server Error, We'll Check It Later"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class SingleArticleAPIView(APIView):

    def get(self, request, format=None):
        #try:
            article_title = request.GET['article_title']
            article = Article.objects.filter(title=article_title) # "filter" is queryset, if use Article.objects.get(title=article_title) and know have single object you should use "many=False" in next line
            serializer_data = serializers.SingleArticleSerializer(article, many=True) # the many argument is used to indicate whether the serializer should treat the input data as a single object or a list of objects
            data = serializer_data.data  # by using above code did not need for loop or data.append() method

            return Response({'data': data}, status=status.HTTP_200_OK)
       # except:
            return Response({'status': "Internal Server Error, We'll Check It Later"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class SearchArticleAPIView(APIView):

    def get(self, reqest, format=None):
        try:
            from django.db.models import Q

            query = reqest.GET['query']
            articles = Article.objects.filter(Q(content__icontains=query))
            data = []

            for article in articles:
                data.append({
                    "title": article.title,
                    "cover": article.cover.url if article.cover else None,
                    "content": article.content,
                    "created_at": article.created_at,
                    "category": article.category.title,
                    "author": article.author.user.first_name + ' ' + article.author.user.last_name,
                    "promote": article.promote,
                })

            return Response({'data':data}, status=status.HTTP_200_OK)
        except:
            return Response({'status': "Internal Server Error, We'll Check It Later"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class SubmitArticleAPIView(APIView):

    def post(self, request, format=None):

        try:
            serializer = serializers.SubmitArticleSerializer(data=request.data)
            if serializer.is_valid():
                title = serializer.data.get('title')
                cover = request.FILES['cover']
                content = serializer.data.get('content')
                category_id = serializer.data.get('category_id')
                author_id = serializer.data.get('author_id')
                promote = serializer.data.get('promote')
            else:
                return Response({'status':'Bad Request.'}, status=status.HTTP_400_BAD_REQUEST)

            user = User.objects.get(id=author_id)
            author = UserProfile.objects.get(user=user)
            category = Category.objects.get(id=category_id)

            article = Article()
            article.title = title
            article.cover = cover
            article.content = content
            article.category = category
            article.author = author
            article.promote = promote
            article.save()

            return Response({'status': 'OK'}, status=status.HTTP_200_OK)

        except:
            return Response({'status': "Internal Server Error, We'll Check It Later"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class UpdateArticleAPIView(APIView):

    def post(self, request, format=None):
        try:
            serializer = serializers.UpdateArticleCoverSerializer(data=request.data)

            if serializer.is_valid():
                article_id = serializer.data.get('article_id')
                cover = request.FILES['cover']
            else:
                return Response({'status': 'Bad Request.'}, status=status.HTTP_400_BAD_REQUEST)

            Article.objects.filter(id=article_id).update(cover=cover)

            return Response({'status':'OK'}, status=status.HTTP_200_OK)

        except:
            return Response({'status': "Internal Server Error, We'll Check It Later"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class DeleteArticleAPIView(APIView):

    def post(self, request, format=None):
        try:
            serializer = serializers.DeleteArticleSerializer(data=request.data)

            if serializer.is_valid():
                article_id = serializer.data.get('article_id')
            else:
                return Response({'status': 'Bad Request.'}, status=status.HTTP_400_BAD_REQUEST)

            Article.objects.filter(id=article_id).delete()

            return Response({'status':'OK'}, status=status.HTTP_200_OK)

        except:
            return Response({'status': "Internal Server Error, We'll Check It Later"},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)