from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from apps.sitemaps import BlogSitemap, VacancySitemap
from tour.views import travel
from home.views import index


from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

#from educa.views import CourseListView
from django.contrib.staticfiles import views

sitemaps = {
  'blogs': BlogSitemap,
  'vacancy': VacancySitemap
}

urlpatterns = [
    url(r'^$', index, name='index'),
    url(r'^home/', include('home.urls')),
    url(r'^billing/', include('billing.urls')),
    url(r'^college/', include('college.urls')),
    url(r'^inpatient/', include('inpatient.urls')),
    #url(r'^$', CourseListView.as_view(), name='course_list'),
    url(r'^admin/', admin.site.urls),
    url(r'^accounts/login/$', auth_views.login, name='login'),
    url(r'^accounts/logout/$', auth_views.logout, name='logout'),
    #url(r'^educa/', include('educa.urls')),
    url(r'^events/', include('events.urls')),
    url(r'^inventory/', include('inventory.urls')),
    url(r'^tour/', include('tour.urls')),
    url(r'^student/', include('student.urls')),
    url(r'^TabibuNet/', include('TabibuNet.urls')),
    url(r'^appointments/', include('appointments.urls')),
    url(r'^coupons/', include('coupons.urls')),
    url(r'^sitemap\.xml$', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),







]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


