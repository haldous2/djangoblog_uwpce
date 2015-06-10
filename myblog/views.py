from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template import RequestContext, loader
from myblog.models import Post, Category

## /
def list_view(request):
    published = Post.objects.exclude(published_date__exact=None)
    posts = published.order_by('-published_date')
    context = {'posts': posts}
    return render(request, 'list.html', context)

## /posts/1/
def detail_view(request, post_id):
    published = Post.objects.exclude(published_date__exact=None)
    try:
        post = published.get(pk=post_id)
    except Post.DoesNotExist:
        raise Http404
    context = {'post': post}
    return render(request, 'detail.html', context)

## /categories/
def categories_view(request):
    categories = Category.objects.all()
    context = {'categories': categories}
    return render(request, 'catlist.html', context)

## /category/1/
def category_view(request, category_id):
    categories = Category.objects
    try:
        category = categories.get(pk=category_id)
    except Post.DoesNotExist:
        raise Http404
    context = {'category': category}
    return render(request, 'catdetail.html', context)
