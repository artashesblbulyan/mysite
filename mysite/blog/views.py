from django.shortcuts import render, HttpResponse, redirect
from blog.forms import ArticleForm, ArticleModelForm
from blog.models import Article
from django.contrib.auth.decorators import login_required
from django.contrib import messages

def create_article(request):
    form = ArticleModelForm()
    if request.method == "POST":
        form = ArticleModelForm(request.POST)
        if form.is_valid():
            article = form.save(commit=False)
            article.user = request.user
            article.save()
            messages.success(request, f"{article.heading} has been created successfuly")

            return redirect("blog_view", article_id=article.id)
        messages.error(request, "something went wrong")
    context = {"form": form}

    return render(request, "article/article_create.html", context)
