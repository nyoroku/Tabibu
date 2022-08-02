from django import template
from home.models import Display, Latest


def do_latest_displays(parser, token):
    return LatestDisplaysNode()


class LatestDisplaysNode(template.Node):
    def render(self, context):
        context['latest_displays'] = Latest.objects.order_by('-created')[:1]
        return ''


register = template.Library()
register.tag('get_latest_displays', do_latest_displays)
