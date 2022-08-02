from django.contrib.sitemaps import Sitemap
from events.models import Blog
from college.models import Examination, Course, Vacancy


class BlogSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.7

    def items(self):
        return Blog.published.all()

    def lastmod(self, obj):
        return obj.publish


class VacancySitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.8

    def items(self):
        return Vacancy.objects.all()

    def lastmod(self, obj):
        return obj.date_created


