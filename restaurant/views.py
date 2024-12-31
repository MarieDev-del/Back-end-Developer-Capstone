from django.http import HttpResponse
from django.shortcuts import render
from .models import Menu
from django.core import serializers
from .models import Booking
from datetime import datetime
import json
from django.views.decorators.csrf import csrf_exempt
from .forms import BookingForm


# Create your views here

def home(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')


# def book(request):
#     if request.method == 'POST':
#         form = BookingForm(request.POST)
#         if form.is_valid():
#             form.save()
#             # Redirect or display a success message
#     else:
#         form = BookingForm()

#     select_time = [
#         ('10', '10 AM'),
#         ('11', '11 AM'),
#     ]

#     context = {
#         'form': form,
#         'select_time': select_time,
#     }

    # return render(request, 'book.html', context)



@csrf_exempt
def bookings(request):
    if request.method == 'POST':
        data = json.load(request)
        exist = Booking.objects.filter(reservation_date=data['reservation_date']).filter(
            reservation_slot=data['reservation_slot']).exists()
        if exist==False:
            booking = Booking(
                first_name=data['first_name'],
                reservation_date=data['reservation_date'],
                reservation_slot=data['reservation_slot'],
            )
            booking.save()
        else:
            return HttpResponse("{'error':1}", content_type='application/json')
    
    date = request.GET.get('date',datetime.today().date())

    bookings = Booking.objects.all().filter(reservation_date=date)
    booking_json = serializers.serialize('json', bookings)

    return HttpResponse(booking_json, content_type='application/json')


#Add code for the bookings() view
def bookings(request):
    date = request.GET.get('date',datetime.today().date())
    bookings = Booking.objects.all()
    booking_json = serializers.serialize('json', bookings)
    return render(request, 'bookings.html',{"bookings":booking_json})


def menu(request):
    menu_data = Menu.objects.all()
    main_data = {"menu": menu_data}
    return render(request, 'menu.html', {"menu": main_data})


def display_menu_item(request, pk=None): 
    if pk: 
        menu_item = Menu.objects.get(pk=pk) 
    else: 
        menu_item = "" 
    return render(request, 'menu_item.html', {"menu_item": menu_item}) 


# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework.permissions import IsAuthenticated

# class BookingView(APIView):
#     permission_classes = [IsAuthenticated]  # Require authentication

#     def post(self, request):
#         name = request.data.get('name')
#         date = request.data.get('date')
#         time = request.data.get('time')

#         if not all([name, date, time]):
#             return Response({'error': 'All fields are required.'}, status=400)

#         # Process reservation (e.g., save to database)
#         # Example:
#         # Reservation.objects.create(name=name, date=date, time=time)

#         return Response({'message': 'Reservation successful!'}, status=200)
    
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

class BookingView(APIView):
    permission_classes = [IsAuthenticated]  # Require authentication

    def post(self, request):
        name = request.data.get('name')
        date = request.data.get('date')
        time = request.data.get('time')

        if not all([name, date, time]):
            if request.headers.get('Accept', '').lower() == 'text/html':
                return render(request, 'bookings.html', {'error': 'All fields are required.'})
            return Response({'error': 'All fields are required.'}, status=400)

        # Process reservation (e.g., save to database)
        # Reservation.objects.create(name=name, date=date, time=time)

        if request.headers.get('Accept', '').lower() == 'text/html':
            return render(request, 'bookings.html', {'message': 'Reservation successful!'})

        return Response({'message': 'Reservation successful!'}, status=200)

    def get(self, request):
        # Render HTML form for making a reservation
        if request.headers.get('Accept', '').lower() == 'text/html':
            return render(request, 'bookings.html', {})

        # Return JSON response for API clients
        available_slots = [
            {'time': '10:00 AM', 'slot': 1},
            {'time': '11:00 AM', 'slot': 2},
        ]
        return Response({'available_slots': available_slots}, status=200)
   
    
from django.http import JsonResponse
from django.shortcuts import render
from .forms import BookingForm

def book_api(request):
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save()
            if request.headers.get('Accept', '').lower() == 'application/json':
                return JsonResponse({'success': True, 'message': 'Booking successful!', 'booking_id': booking.id}, status=201)
            return render(request, 'book.html', {'form': BookingForm(), 'message': 'Booking successful!'})

        # For HTML responses, include error messages
        if request.headers.get('Accept', '').lower() == 'application/json':
            return JsonResponse({'success': False, 'errors': form.errors}, status=400)
        return render(request, 'book.html', {'form': form, 'message': 'Please correct the errors below.'})

    if request.method == 'GET':
        form = BookingForm()
        select_time = [
            {'value': '10', '10 AM': '10 AM'},
            {'value': '11', '11 AM': '11 AM'},
        ]

        # Check if the request expects JSON
        if request.headers.get('Accept', '').lower() == 'application/json':
            return JsonResponse({'success': True, 'select_time': select_time}, status=200)
        
        # Render the HTML template
        return render(request, 'book.html', {'form': form, 'select_time': select_time})

    # Unsupported method
    return JsonResponse({'success': False, 'message': 'Method not allowed'}, status=405)
