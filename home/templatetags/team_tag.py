from django import template
from home.models import Team


def do_latest_team(parser, token):
    return LatestTeamNode()


class LatestTeamNode(template.Node):
    def render(self, context):
        context['latest_team'] = Team.objects.all()
        return ''


register = template.Library()
register.tag('get_latest_team', do_latest_team)

