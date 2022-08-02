from django import template
from home.models import Latest


def do_latest_politics(parser, token):
    return LatestNewsNode()


class LatestNewsNode(template.Node):
    def render(self, context):
        context['politics_news'] = Latest.objects.filter(category__title__exact='Politics')[:4]
        return ''


register = template.Library()
register.tag('get_politics_news', do_latest_politics)
