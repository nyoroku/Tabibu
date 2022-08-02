from django import template
from home.models import Latest


def do_latest_opinions(parser, token):
    return LatestNewsNode()


class LatestNewsNode(template.Node):
    def render(self, context):
        context['opinions_news'] = Latest.objects.filter(category__title__exact='Opinions')[:4]
        return ''


register = template.Library()
register.tag('get_opinions_news', do_latest_opinions)
