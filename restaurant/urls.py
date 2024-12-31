from django.urls import path
from . import views
from .views import BookingView


urlpatterns = [
    path('', views.home, name="home"),
    path('about/', views.about, name="about"),
    path('api/book/', views.book_api, name="book"),
    path('menu/', views.menu, name="menu"),
    path('api/bookings/', views.bookings, name="bookings"),
    path('menu_item/<int:pk>/', views.display_menu_item, name="menu_item"),  
]

# from django.urls import path
# from rest_framework_simplejwt.views import (
#     TokenObtainPairView,
#     TokenRefreshView,
# )

# urlpatterns = [
#     path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
#     path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
# ]
