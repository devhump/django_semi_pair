from django.shortcuts import render, redirect
from .forms import ArticleForm, CommentForm
from .models import Article

# Create your views here.


def index(request):

    articles = Article.objects.all()

    context = {
        "articles": articles,
    }

    return render(request, "articles/index.html", context)


def create(request):

    if request.method == "POST":
        article_form = ArticleForm(request.POST)
        if article_form.is_valid():
            article_ = article_form.save(commit=False)
            article_.user = request.user
            article_.save()
            return redirect("articles:index")
    else:
        article_form = ArticleForm()
    context = {
        "article_form": article_form,
    }

    return render(request, "articles/create.html", context)


def detail(request, pk):

    article = Article.objects.get(pk=pk)
    comment_form = CommentForm()
    comment = article.comment_set.order_by("-pk")

    context = {
        "article": article,
        "comment_form": comment_form,
        "comment": comment,
    }

    return render(request, "articles/detail.html", context)


def delete(request, pk):

    article = Article.objects.get(pk=pk)
    article.delete()

    return redirect("articles:index")


def update(request, pk):

    article = Article.objects.get(pk=pk)

    if request.method == "POST":
        article_form = ArticleForm(request.POST, instance=article)
        if article_form.is_valid():
            article_form.save()
            return redirect("articles:detail", pk)
    else:
        article_form = ArticleForm(instance=article)
    context = {
        "article_form": article_form,
    }

    return render(request, "articles/update.html", context)


def c_create(request, pk):

    comment_form = CommentForm(request.POST)
    article = Article.objects.get(pk=pk)

    if comment_form.is_valid():
        comment = comment_form.save(commit=False)
        comment.article = article
        comment.user = request.user
        comment.save()

    return redirect("articles:detail", pk)
