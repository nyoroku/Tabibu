from django import template
from home.models import Testimonial


def do_latest_testimonials(parser, token):
    return LatestTestimonialsNode()


class LatestTestimonialsNode(template.Node):
    def render(self, context):
        context['latest_testimonials'] = Testimonial.objects.all()
        return ''


register = template.Library()
register.tag('get_latest_testimonials', do_latest_testimonials)

