from . import views
from django.conf.urls import url
from .views import index


app_name = 'home'
urlpatterns = [
         url(r'^$', index, name='index'),
         url(r'^allnews/', views.allnews, name='allnews'),
         url(r'^tag/(?P<tag_slug>[-\w]+)/$', views.allnews,
          name='allnews_by_tag'),
         url(r'^new/(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/' \
           r'(?P<new>[-\w]+)/$',
           views.latest_detail,
           name='news'),
         url(r'^who-we-are/', views.who, name='who'),
         url(r'^get-involved/$', views.register, name='register'),
         ]


