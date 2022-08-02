from django import template
from home.models import Latest


def do_latest_videos(parser, token):
    return LatestNewsNode()


class LatestNewsNode(template.Node):
    def render(self, context):
        context['latest_videos'] = Latest.objects.filter(category__title__exact='Videos')[:4]
        return ''


register = template.Library()
register.tag('get_latest_videos', do_latest_videos)
