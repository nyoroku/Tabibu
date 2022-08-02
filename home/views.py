from django.shortcuts import render, get_object_or_404
from models import Latest
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from taggit.models import Tag
from django.db.models import Count
from .forms import RegistrationForm


def index(request):
    news = Latest.objects.order_by('-created')[:4]
    paginator = Paginator(news, 4)
    page = request.GET.get('page')
    try:
        news = paginator.page(page)
    except PageNotAnInteger:
        news = paginator.page(1)
    except EmptyPage:
        news = paginator.page(paginator.num_pages)
    return render(request, 'home/index.html', {'news': news, 'page': page})


def allnews(request, tag_slug=None):
    news = Latest.objects.order_by('-created')
    tag = None
    if tag_slug:
        tag = get_object_or_404(Tag, slug=tag_slug)
        news = news.filter(tags__in=[tag])

    paginator = Paginator(news, 1)
    page = request.GET.get('page')
    try:
        news = paginator.page(page)
    except PageNotAnInteger:
        news = paginator.page(1)
    except EmptyPage:
        news = paginator.page(paginator.num_pages)
    return render(request, 'home/allnews.html', {'news': news, 'page': page, 'tag' : tag})


def latest_detail(request, year, month, day, new):
    new = get_object_or_404(Latest, slug=new)
    new_tag_ids = new.tags.values_list('id', flat=True)
    similar_news = Latest.objects.filter(tags__in=new_tag_ids).exclude(id=new.id)
    similar_news = similar_news.annotate(same_tags=Count('tags')).order_by('-same_tags', '-created')[:3]
    return render(request, 'home/news.html', {'new': new, 'similar_news': similar_news})


def who(request):
    return render(request, 'home/who.html')


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            registration = form.save()
            return render(request, 'application/applied.html', {'registration': registration})

    else:
        form = RegistrationForm
    return render(request, 'application/applycourse.html', {'form': form})


