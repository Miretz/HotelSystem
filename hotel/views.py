from django.shortcuts import render, get_object_or_404, render_to_response
from django.template import Context, loader
from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.template import RequestContext
from hotel.models import Reservation, Room
from django.utils import timezone
from django.shortcuts import redirect
import random
from django.http import Http404
from hotel.forms import NewResForm, NewCustForm, RoomForm
from hotel.models import Customer
#from django.views.generic.simple import direct_to_template
#from django.views.generic import TemplateView

'''
INDEX
'''
def index(request):
    res_list = Reservation.objects.all().order_by('created').reverse()
    c = RequestContext(request, {'res_list': res_list})
    return render_to_response('hotel/Index.html', c)

'''
ROOMS
'''
def rooms(request):
    room_list = Room.objects.all().order_by('number')
    res_list = Reservation.objects.all().order_by('created')
    c = RequestContext(request, {'room_list': room_list,'res_list': res_list})
    return render_to_response('hotel/Rooms.html', c)
    

'''
OPEN ONE ROOM
'''
def oneroom(request, room_id):
    instance = get_object_or_404(Room, number=room_id)
    form = RoomForm(request.POST or None, instance=instance)
    if form.is_valid():
        form.save()
        return HttpResponseRedirect('/hotel/rooms/')
    return render(request, 'hotel/Room.html', {'form': form})

'''
RESERVATION
'''
def reservation(request, reservation_id):
    instance = get_object_or_404(Reservation, id=reservation_id)
    form = NewResForm(request.POST or None, instance=instance)
    if form.is_valid():
        form.save()
        return HttpResponseRedirect('/hotel/rooms/')
    return render(request, 'hotel/NewRes.html', {'form': form})


'''
NEW RESERVATION
'''
def newres(request): 
    if request.method == 'POST':
        form = NewResForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/hotel/rooms/')
    else:
        form = NewResForm(initial={'created': timezone.now() })
    return render(request, 'hotel/NewRes.html', {'form': form})


def newres_room(request, room_id):
    try:
        p = Room.objects.get(number=room_id)
    except Room.DoesNotExist:
        raise Http404
    
    if request.method == 'POST':
        form = NewResForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/hotel/rooms/')
    else:
        form = NewResForm(initial={'created': timezone.now() })
    return render(request, 'hotel/NewRes.html', {'form': form,'room': p,})


'''
NEW CUSTOMER
'''

def newcust(request):
    if request.method == 'POST':
        form = NewCustForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/hotel/rooms/')
    else:
        form = NewCustForm(initial={'registered': timezone.now() })
    return render(request, 'hotel/NewCust.html', {'form': form})


'''
EDIT CUSTOMER
'''

def editcust(request,id_cust):
    instance = get_object_or_404(Customer, id=id_cust)
    form = NewCustForm(request.POST or None, instance=instance)
    if form.is_valid():
        form.save()
        return HttpResponseRedirect('/hotel/rooms/')
    return render(request, 'hotel/NewCust.html', {'form': form})





