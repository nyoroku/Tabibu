from django.conf.urls import url
from . import views


app_name = 'appointments'
urlpatterns = [


    url(r'^mine/$', views.ManageAppointmentListView.as_view(), name='my_list'),
    url(r'^(?P<pk>\d+)/appointment/$', views.AppointmentCreateView.as_view(), name='appointment_add'),
    url(r'^(?P<pk>\d+)/edit/$', views.AppointmentUpdateView.as_view(), name='appointment_edit'),
    url(r'^(?P<pk>\d+)/delete/$', views.AppointmentDeleteView.as_view(), name='delete'),
    url(r'^today/$', views.today_appointments, name='today_appointments'),
    url(r'^tomorrow/$', views.tomorrow_appointments, name='tomorrow_appointments'),
]