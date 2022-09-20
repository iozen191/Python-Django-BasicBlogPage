from multiprocessing import context
from django.shortcuts import render,HttpResponse,redirect,get_object_or_404,reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import ArticleForm
from .models import Article,Comment



# Create your views here.

def articles(request):
    keyword = request.GET.get('keyword')
    if keyword:
        articles = Article.objects.filter(title__contains=keyword)
        context = {
            "articles": articles
        }
        return render(request,"articles.html",context)
    articles = Article.objects.all()
    context = {
        "articles": articles
    }
    return render(request,"articles.html",context)



def index(request):
    context = {
        "txt":["MGT Gaming","Banzerino"]   
    }
    return render(request,"index.html",context)

def about(request):
    return render(request,"about.html")
    
@login_required(login_url = "user:login")
def dashboard(request):
    articles = Article.objects.filter(author=request.user)
    context = {
        "articles": articles
    }
    return render(request,"dashboard.html",context)

@login_required(login_url = "user:login")
def addArticle(request):
    form = ArticleForm(request.POST or None,request.FILES or None)
    if form.is_valid():
        article = form.save(commit=False)
        article.author = request.user
        article.save()
        messages.success(request,"Makale Başarıyla Oluşturuldu...")
        return redirect("article:dashboard")
    context = {
        "form": form
    }
    return render(request,"addarticle.html",context)
    
def details(request,id):
    #article = Article.objects.filter(id=id).first()
    article = get_object_or_404(Article, id=id)
    comments = article.comments.all()

    context = {
        "article":article,
        "comments":comments
    }
    return render(request,"details.html",context)

@login_required(login_url = "user:login")
def update(request,id):
    article = get_object_or_404(Article, id=id)
    form = ArticleForm(request.POST or None, request.FILES or None,instance=article)
    if form.is_valid():
        article = form.save(commit=False)
        article.author = request.user
        article.save()
        messages.success(request,"Makale Başarıyla Güncellendi...")
        return redirect("article:dashboard")
    context = { 
        "form":form 
        }
    return render(request,"update.html",context)


@login_required(login_url = "user:login")
def deleteArticle(request,id):
    article = get_object_or_404(Article, id=id)
    article.delete()
    messages.success(request,"Makale Başarıyla Silindi...")
    return redirect("article:dashboard")


def addComments(request,id):
    article = get_object_or_404(Article, id=id)
    if request.method == "POST":
        comment_author = request.POST.get("comment_author")
        comment_content = request.POST.get("comment_content")
        newComment = Comment(comment_author=comment_author,comment_content=comment_content)
        newComment.article = article
        newComment.save()    
    return redirect(reverse("article:details",kwargs = {"id":id}))