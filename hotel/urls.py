from django.conf.urls import patterns, include, url
from django.views.generic import DetailView, ListView

urlpatterns = patterns('',
    url(r'^$','hotel.views.index'),
    url(r'^(?P<reservation_id>\d+)/$','hotel.views.reservation'),
    url(r'^rooms/$','hotel.views.rooms'),
    url(r'^new/$','hotel.views.newres'),
    url(r'^new/(?P<room_id>\d+)/$','hotel.views.newres_room'),
    url(r'^rooms/(?P<room_id>\d+)/$','hotel.views.oneroom'),
    url(r'^newcust/$','hotel.views.newcust'),
    url(r'^editcust/(?P<id_cust>\d+)/$','hotel.views.editcust'),
    url(r'^editcust/$','hotel.views.rooms'),
    url(r'^oneroom/$','hotel.views.oneroom'),
)
