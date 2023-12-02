from django.urls import path
from trip_app.views import customer_views

urlpatterns = [    
    path('duration/', customer_views.TripDurationList.as_view()),
    path('search/', customer_views.TripSearchList.as_view()),
    path('enquiry/', customer_views.TripEnquiry.as_view()),
    path('book/enquiry/', customer_views.TripBookingEnquiry.as_view()),
    path('upcoming/', customer_views.UpcomingTripList.as_view()),
    path('slider/<int:slider_id>/', customer_views.SliderTripsList.as_view()),
    path('<str:trip_slug>/', customer_views.TripView.as_view()),
    path('related/<int:pk>/', customer_views.RelatedTripsList.as_view()),
]