from django.db import models
import datetime
from datetime import date
import calendar
from django.utils import timezone 

# Constants
CUSTOMER_TYPE = (
    ('SIR','Senior'),
    ('DIS','Disabled'),
    ('FAM','Family'),
    ('YOU','Young'))

PRODUCT_TYPE = (
    ('SER','Service'),
    ('FOO','Food'),
    ('DRI','Drink'),
    ('OTH','Other'))

STATUSES = (
    ('RES','Reserved'),
    ('CIN','Checked in'),
    ('COU','Checked out'),
    ('CLO','Closed'))

FREE_ROOM = "Free Room"
EMPTY = "Empty"

'''
PHYSICAL PARTS OF HOTEL
'''
# Hotel ROOMS
class Room(models.Model):
    number = models.IntegerField()
    position = models.CharField(max_length=200,null=True, blank=True)
    description = models.TextField()
    beds = models.IntegerField()
    fridge = models.IntegerField()
    tresor = models.IntegerField()
    disabledppl = models.BooleanField()
    balcony = models.IntegerField()
    accessories = models.TextField(null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    appartment = models.BooleanField()
    
    def __unicode__(self):
        return str(self.number)
    def get_text(self):
        return str(self.number)
    def get_floor(self):
        return str(self.number/100)

    #LIST OF ALL ROOMS
    @staticmethod
    def list_rooms():
        allrooms = Room.objects.all().order_by('number')
        thelist = []
        for r in allrooms:
            thelist.append((str(r.number),str(r.number)))
        return thelist


    # GET CHECKED IN RESERVATION
    def resact(self):
        resall = Reservation.objects.filter(room=self).order_by('created').reverse()
        for res in resall:
            if res.status == "CIN":
                return res
        return None
    
    # IS THE ROOM OCCUPIED
    def is_occupied(self):
        if self.resact():
            return True
        return False

    # THE ROOM IS OCCUPIED --- OVERDUE
    def is_overdue(self):
        res = self.resact()
        now = timezone.now()
        if res:
            if res.reserved_until < now:
                return True
            return False
        return False

    # IS LAST DAY OCCUPIED
    def is_last_day(self):
        res = self.resact()
        now = timezone.now()
        if res:
            if not self.is_overdue():
                if res.reserved_until.date() == now.date():
                    return True
                return False
            return False
        return False

    # GET THE CUSTOMER
    def res_name(self):
        res = self.resact()
        if res:
            return res.customer
        if self.is_reserved():
            return self.get_reserved().customer
        return str(FREE_ROOM)
    
    # GET STATUS OF RESERVATION
    def restat(self):
        res = self.resact()
        if res:
            return res.get_status()
        if self.is_reserved():
            return self.get_reserved().get_status()
        return str(EMPTY)

    # GET RESERVATION DAYS
    def period_from(self):
        res = self.resact()
        if res:
            return res.reserved_from
        if self.is_reserved():
            return self.get_reserved().reserved_from
        return str("")
    def period_until(self):
        res = self.resact()
        if res:
            return res.reserved_until
        if self.is_reserved():
            return self.get_reserved().reserved_until
        return str("")

    # IF THE ROOM WAS RESERVED BUT NOT CHECKED IN
    def get_reserved(self):
        resall = Reservation.objects.filter(room=self).order_by('created').reverse()
        now = timezone.now()
        if not self.is_occupied():
            for res in resall:
                if res.status == "RES":
                    if now.date() >= res.reserved_from.date() and now.date() < res.reserved_until.date():
                        return res
        return None

    def is_reserved(self):
        res = self.get_reserved()
        if res:
            return True
        return False
        
    #get ALL RESERVATIONS
    def allres(self):
        return Reservation.objects.filter(room=self).order_by('created')







        
#Parking spaces
class ParkingSpace(models.Model):
    position = models.CharField(max_length=200)
    in_garage = models.BooleanField()
    description = models.TextField(null=True, blank=True)

#Products and services that are sold in the hotel
class Product(models.Model):
    number = models.IntegerField()
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10,decimal_places=2)
    unit = models.CharField(max_length=200,null=True, blank=True)
    size = models.DecimalField(max_digits=10,decimal_places=2,null=True, blank=True)
    stock = models.DecimalField(max_digits=10,decimal_places=2,null=True, blank=True)
    prod_type = models.CharField(max_length=20,choices=PRODUCT_TYPE)

'''
RESERVATION TABLES
'''
# Customers
class Customer(models.Model):
    registered = models.DateTimeField()
    name = models.CharField(max_length=200)
    surname = models.CharField(max_length=200)
    phone = models.CharField(max_length=200)
    email = models.EmailField(null=True, blank=True)
    address = models.TextField()
    town = models.CharField(max_length=200)
    state = models.CharField(max_length=200,null=True, blank=True)
    country = models.CharField(max_length=200)
    zipcode = models.CharField(max_length=200)
    passnumber = models.CharField(max_length=200)
    bank = models.CharField(max_length=200,null=True,blank=True)
    account = models.CharField(max_length=200,null=True, blank=True)
    notes = models.TextField(null=True, blank=True)
    cust_type = models.CharField(max_length=20,choices=CUSTOMER_TYPE)
    def __unicode__(self):
        return self.surname + ", " + self.name 
    def get_text(self):
        return self.surname + ", " + self.name
    def get_type(self):
        for index, item in enumerate(CUSTOMER_TYPE):
            if item[0] == self.cust_type:
                return item[1]
    
    #LIST OF ALL CUSTOMERS
    @staticmethod
    def list_customers():
        allcust = Customer.objects.all().order_by('surname')
        thelist = []
        a = 0
        for r in allcust:
            thelist.append((a,str(r.surname + ", " + r.name)))
            a = a+1
        return thelist

#Reservations
class Reservation(models.Model):
    customer = models.ForeignKey(Customer)
    room = models.ForeignKey(Room)
    all_inclusive = models.BooleanField()
    created = models.DateTimeField()
    reserved_from = models.DateTimeField(null=True, blank=True)
    reserved_until = models.DateTimeField(null=True, blank=True)
    checkin = models.DateTimeField(null=True, blank=True)
    checkout = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20,choices=STATUSES)
    def get_status(self):
        for index, item in enumerate(STATUSES):
            if item[0] == self.status:
                return item[1]
    def get_formated_date_from(self):
        return self.reserved_from.strftime("%d.%m.%Y")
    def get_formated_date_until(self):
        return self.reserved_until.strftime("%d.%m.%Y")


#Reservation items
class ReservationItem(models.Model):
    reservation = models.ForeignKey(Reservation)
    product = models.ForeignKey(Product)
    quantity = models.DecimalField(max_digits=10,decimal_places=2,null=True, blank=True)
    delivered_to_room = models.BooleanField()
    details = models.TextField()

#separate table for parking multiple cars
class ParkingItem(models.Model):
    reservation = models.ForeignKey(Reservation)
    space = models.ForeignKey(ParkingSpace)











