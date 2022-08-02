from django.shortcuts import render, get_object_or_404
from taggit.models import Tag
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Count, When, Value, Case, PositiveSmallIntegerField
from django.core.urlresolvers import reverse_lazy, reverse
from django.contrib.auth import authenticate, login
from django.views.generic.list import ListView
from django.views.generic.edit import UpdateView, DeleteView, CreateView
from braces.views import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import redirect, get_object_or_404
from django.views.generic.base import TemplateResponseMixin, View
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models import Q
from django.utils.decorators import method_decorator
from taggit.models import Tag
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django_ajax.decorators import ajax
from datetime import datetime, date, timedelta
from .models import Appointment
from .forms import AppointmentForm


class AppointmentListView(ListView):
    model = Appointment
    template_name = 'appointment/list.html'

    def get_queryset(self):
        qs = super(AppointmentListView, self).get_queryset()
        return qs.filter(provider=self.request.user)


class ProviderMixin(object):
    def get_queryset(self):
        qs = super(ProviderMixin, self).get_queryset()
        return qs.filter(provider=self.request.user)


class ProviderEditMixin(object):
    def form_valid(self, form):
        form.instance.provider = self.request.user
        return super(ProviderMixin, form).form_valid(form)


class ProviderAppointmentMixin(ProviderMixin, LoginRequiredMixin):
    model = Appointment

    success_url = reverse_lazy('appointments:my_list')


class SellerVehicleEditMixin(ProviderAppointmentMixin, ProviderEditMixin):

    template_name = 'appointment/create.html'


class ManageAppointmentListView(ProviderAppointmentMixin, ListView):
    template_name = 'appointment/list.html'
    model = Appointment
    context_object_name = 'appointments'
    paginate_by = 12
    queryset = Appointment.objects.all()


@method_decorator(login_required, name='dispatch')
class AppointmentCreateView(SuccessMessageMixin, ProviderAppointmentMixin, CreateView, PermissionRequiredMixin):
    model = Appointment
    fields = ['date', 'start_time', 'end_time']

    template_name = 'appointment/create.html'
    success_message = 'Successfully Created.'

    def form_valid(self, form):
        form.instance.provider = self.request.user
        form.instance.visit_id = self.kwargs.get('pk')
        return super(AppointmentCreateView, self).form_valid(form)


@method_decorator(login_required, name='dispatch')
class AppointmentUpdateView(SuccessMessageMixin, ProviderAppointmentMixin, UpdateView, PermissionRequiredMixin):
    template_name = 'appointment/create.html'
    form_class = AppointmentForm
    success_url = reverse_lazy('appointments:my_list')
    success_message = 'Successfully Updated'


@method_decorator(login_required, name='dispatch')
class AppointmentDeleteView(SuccessMessageMixin, ProviderAppointmentMixin, DeleteView, PermissionRequiredMixin):
    template_name = 'appointment/delete.html'
    success_url = reverse_lazy('appointments:my_list')

    success_message = '%Successfully Deleted'


def today_appointments(request):
    today = datetime.now().date()
    appointments = Appointment.objects.filter(date=today)
    total_appointments = appointments.count()
    paginator = Paginator(appointments, 12)
    page = request.GET.get('page')
    try:
        appointments = paginator.page(page)
    except PageNotAnInteger:
        appointments = paginator.page(1)
    except EmptyPage:
        appointments = paginator.page(paginator.num_pages)
    return render(request, 'appointment/today_appointments.html', {'appointments': appointments, 'page': page, 'total_appointments': total_appointments})


def tomorrow_appointments(request):
    today = datetime.now().date()
    tomorrow = today + timedelta(1)
    appointments = Appointment.objects.filter(date=tomorrow)
    total_appointments = appointments.count()
    paginator = Paginator(appointments, 12)
    page = request.GET.get('page')
    try:
        appointments = paginator.page(page)
    except PageNotAnInteger:
        appointments = paginator.page(1)
    except EmptyPage:
        appointments = paginator.page(paginator.num_pages)
    return render(request, 'appointment/tomorrow_appointments.html', {'appointments': appointments, 'page': page, 'total_appointments': total_appointments})




