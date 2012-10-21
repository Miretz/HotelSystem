from django import forms
from hotel.models import Reservation, Room, Customer, STATUSES, CUSTOMER_TYPE
from django.forms import ModelForm
from django.contrib.admin import widgets 

# NOW DO THE MODEL FORM


class NewResForm(forms.ModelForm):
    class Meta:
        model = Reservation

class NewCustForm(forms.ModelForm):
    class Meta:
        model = Customer

class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
