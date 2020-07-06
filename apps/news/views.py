from django.shortcuts import render
from django.http import HttpResponse
from .models import News,NewsCategory,Comment,Banner
from django.conf import settings
from .serializers import NewsSerializers,CommentSerizlizer
from utils import restful
from django.http import Http404
from .forms import PublicCommentForm
from apps.xfzauth.decorators import xfz_login_required
from django.db.models import Q
# Create your views here.

def index(request):
    count = settings.ONE_PAGE_NEWS_COUNT
    context = {
        'newses' : News.objects.select_related('category','author').all()[0:count],
        'categories' : NewsCategory.objects.all(),
        'banners':Banner.objects.all()

    }
    return render(request,'news/index.html',context=context)

def news_list(request):
    page = int(request.GET.get('p',2))
    category_id = int(request.GET.get('category_id',0))
    print('category_id:',category_id)
    start = (page-1)*settings.ONE_PAGE_NEWS_COUNT
    end = start+settings.ONE_PAGE_NEWS_COUNT
    if category_id == 0:
        newses = News.objects.select_related('category','author').all()[start:end]
    else:
        newses = News.objects.select_related('category','author').filter(category_id=category_id)[start:end]
    serializers = NewsSerializers(newses,many=True)
    data = serializers.data
    return restful.result(data=data)

def news_detail(request,news_id):
    try:
        news = News.objects.select_related('category','author').prefetch_related('comments__author').get(pk=news_id)
    except News.DoesNotExist:
        raise Http404
    context = {
        'news':news
    }
    return render(request,'news/news_detail.html',context=context)

@xfz_login_required
def public_comment(request):
    form = PublicCommentForm(request.POST)
    if form.is_valid():
        news_id = form.cleaned_data.get('news_id')
        content = form.cleaned_data.get('content')
        try:
            news = News.objects.get(pk=news_id)
        except:
            print('出错')
            raise Http404

        comment = Comment.objects.create(content=content,news=news,author=request.user)
        serializers = CommentSerizlizer(comment)
        return restful.result(data=serializers.data)
    else:
        print('验证错误')
        return restful.params_error(message=form.get_errors())

def search(request):
    q = request.GET.get('q')
    context = {}
    if q:
        news = News.objects.filter(Q(title__icontains=q)|Q(content__contains=q))
        context['news'] = news
    return render(request,'search/search.html',context=context)
