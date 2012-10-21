from hotel.models import Room, ParkingSpace, Product, Customer, Reservation, ReservationItem, ParkingItem
from django.contrib import admin


class RoomAdmin(admin.ModelAdmin):
    list_display = ('number', 'beds', 'fridge', 'tresor','balcony','price','appartment')
    search_fields = ['number', 'beds', 'fridge', 'tresor','balcony','price','appartment']
    
class ParkingSpaceAdmin(admin.ModelAdmin):
    list_display = ('position','in_garage')
    search_fields = ['position']

class ProductAdmin(admin.ModelAdmin):
    list_display = ('number','name','price','prod_type','stock','unit')
    search_fields = ['number']
    
    
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('surname', 'name', 'cust_type', 'phone','email','town','country')
    search_fields = ['surname']
    list_filter = ['registered']

class ReservationAdmin(admin.ModelAdmin):
    list_display = ('room','customer','created','reserved_from','reserved_until','checkin','checkout','status','all_inclusive')
    search_fields = ['customer','room','created','reserved_from','reserved_until']
    list_filter = ['created','checkin','checkout']



admin.site.register(Room, RoomAdmin)
admin.site.register(ParkingSpace, ParkingSpaceAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Customer, CustomerAdmin)
admin.site.register(Reservation, ReservationAdmin)



