from django.conf.urls import patterns, url


## Note in regex - the 'P' before the <defined> is a Parameter

urlpatterns = patterns(

    'myblog.views',

    url(r'^$',
        'list_view',
        name="blog_index"),
    url(r'^posts/(?P<post_id>\d+)/$',
        'detail_view',
        name="blog_detail"),

    url(r'^categories/$',
        'categories_view',
        name="blog_categories"),
    url(r'^category/(?P<category_id>\d+)/$',
        'category_view',
        name="blog_category"),

)
