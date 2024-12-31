from django.test import TestCase
from datetime import datetime 
from .models import Booking
# Create your tests here.

class BookingModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.Booking=Booking.objects.create(first_name = 'Marie',
    )
def test_fields(self):
    self.assertIsInstance(self.Booking.first_name,str)
    
def test_timestamps(self):
    self.assertIsInstance(self.Booking_time,datetime)
def __str__(self):
    return self.first_name

def test_timestamps(self):
    self.assertIsInstance(self.Booking.booking_time,datetime)
    def __str__(self):
        return self.frst_name