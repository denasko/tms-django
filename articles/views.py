from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect

from .models import Article


def index(request: HttpResponse) -> str:
    articles = Article.objects.all()
    data = {
        'title': 'Main page',
        'articles': articles,
    }
    return render(request, 'articles/index.html', context=data)


def show_article(request: HttpResponse, article_id: int) -> str:
    article = get_object_or_404(Article, pk=article_id)
    data = {'article': article}
    return render(request, 'articles/article.html', context=data)


def like(request: HttpResponse, article_id: int) -> str:
    if request.method == 'POST':
        article = Article.objects.get(id=article_id)
        article.like_count += 1
        article.save()
        return redirect('articles:show_article', article_id)


def about(request: HttpResponse) -> str:
    return render(request, 'articles/about.html')


def feedback(request: HttpResponse) -> str:
    return render(request, 'articles/feedback.html')


def login(request: HttpResponse) -> str:
    return render(request, 'article/login.html')


def create_article(request: HttpResponse) -> str:
    return render(request, 'articles/create_article.html')
