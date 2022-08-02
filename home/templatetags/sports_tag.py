from django import template
from home.models import Latest


def do_latest_sports(parser, token):
    return LatestNewsNode()


class LatestNewsNode(template.Node):
    def render(self, context):
        context['sports_news'] = Latest.objects.filter(category__title__exact='Sports')[:4]
        return ''


register = template.Library()
register.tag('get_sports_news', do_latest_sports)
