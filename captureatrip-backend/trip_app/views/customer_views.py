from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Case, Value, When
from django.db.models import IntegerField

from trip_app.serializers import TripViewSerializer, TripDurationSerializer, TripSearchSerializer,\
    TripListSerializer
from category_app.models import TripCategory
from trip_app.models import TripMaster, TripDurationMaster, SliderTrips

from django.utils import timezone
from django.db.models import Q
from django.template.loader import render_to_string

from email_app.utils import EmailSender

# Create your views here.
class TripView(generics.RetrieveAPIView):
    queryset = TripMaster.objects.all()
    serializer_class = TripViewSerializer
    lookup_field = 'trip_slug'

class TripDurationList(generics.ListAPIView):
    queryset = TripDurationMaster.objects.all()
    serializer_class = TripDurationSerializer

class RelatedTripsList(generics.ListAPIView):
    serializer_class = TripListSerializer

    def get_queryset(self):
        # Fetch primary category id which the trip is in
        primary_qs = TripCategory.objects \
                .filter(trip_id=self.kwargs.get('pk'), is_primary_category=True) \
                    .values('category_id').first()
        
        if not primary_qs:
            return TripCategory.objects.none()

        # Fetch other trips that have the same primary category id, exclude itself from trip list
        category_trip_qs = TripCategory.objects.filter(
                category_id=primary_qs.get('category_id'),
                is_primary_category=True,
            ).exclude(trip_id=self.kwargs.get('pk')) \
                .values('trip_id')
        
        # Final trip queryset, filter out past dates
        queryset = TripMaster.objects \
            .select_related('perk1', 'perk2', 'pickup_location', 'drop_location', 'duration') \
                .prefetch_related('trip_date') \
                    .filter(trip_id__in=category_trip_qs, trip_date__date_value__gte=timezone.now().today()) \
                        .distinct('trip_id')
        
        return queryset

class SliderTripsList(generics.ListAPIView):
    serializer_class = TripListSerializer
    
    def get_queryset(self):        

        # Get Trips in slider
        slider_trip_qs = SliderTrips.objects \
            .filter(slider_id=self.kwargs.get('slider_id')).values_list('trip_id', flat=True) \
                .order_by('slider_trip_position')
        
        limit = slider_trip_qs.count()
        query = Q()

        # Filter by slider trips
        query &= Q(trip_id__in=slider_trip_qs)

        # Optionally filter using query parameters in the URL.
        if self.request.query_params.get('no_of_records'):
            limit = self.request.query_params.get('no_of_records')

        if self.request.query_params.get('month'):
            query &= Q(trip_date__date_value__month=self.request.query_params.get('month'))
        
        if self.request.query_params.get('year'):
            query &= Q(trip_date__date_value__year=self.request.query_params.get('year'))
        
        if self.request.query_params.get('trip_duration_id'):
            query &= Q(duration=self.request.query_params.get('trip_duration_id'))

        # Exclude trips with past trip dates
        if self.request.query_params.get('exclude_past_trips'):
            query &= Q(trip_date__date_value__gte=timezone.now().today())

        queryset = TripMaster.objects \
            .select_related('perk1', 'perk2', 'pickup_location', 'drop_location', 'duration') \
                .prefetch_related('trip_date') \
                    .filter(query).distinct('trip_id')[:int(limit)]
                    
        # sort and return result
        slider_trip_list = list(slider_trip_qs)
        return sorted(queryset, key=lambda x: slider_trip_list.index(x.trip_id))

class TripSearchList(generics.ListAPIView):
    serializer_class = TripSearchSerializer

    def get_queryset(self):
        keyword = self.request.query_params.get('keyword')

        if keyword and len(keyword) > 1:
            trip_name_query = Q(trip_name__icontains=keyword)
            trip_itinerary_query = Q(trip_itinerary__icontains=keyword)
            
            queryset = (
                TripMaster.objects
                .filter(trip_name_query | trip_itinerary_query)
                .annotate(
                    search_order=Case(
                        When(trip_name_query, then=Value(1)),
                        When(trip_itinerary_query, then=Value(0)),
                        default=Value(-1),
                        output_field=IntegerField(),
                    )
                )
                .order_by('-search_order')
            )
            
        else:
            queryset = TripMaster.objects.none()
        
        return queryset

class TripEnquiry(generics.GenericAPIView):

    def post(self, request):
        name = request.data.get('name')
        email = request.data.get('email')
        phone = request.data.get('phone')
        destination = request.data.get('destination')
        
        # Init email object
        obj = EmailSender(email_logs=False)

        # Send email
        result = obj.send_single_email(
            subject='You have a new trip enquiry on Captureatrip',
            body=render_to_string('trip_app/email/trip-enquiry.html',
            {
                "name": name,
                "email": email,
                "phone": phone,
                "destination": destination
            }),
            receiver='info@captureatrip.com'
        )

        if result:
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class UpcomingTripList(generics.ListAPIView):
    serializer_class = TripListSerializer
    
    def get_queryset(self):
        filter_year = self.request.query_params.get('year')
        filter_month = self.request.query_params.get('month')
        trip_duration_id = self.request.query_params.get('trip_duration_id')

        # Optionally filter using query parameters in the URL.
        query = Q()

        if filter_year: query &= Q(trip_date__date_value__year=filter_year)
        if filter_month: query &= Q(trip_date__date_value__month=filter_month)
        if trip_duration_id: query &= Q(duration=trip_duration_id)
        
        # Exclude trips with past trip dates
        if not (filter_year and filter_month):
            query &= Q(trip_date__date_value__gte=timezone.now().today())

        queryset = TripMaster.objects \
            .select_related('perk1', 'perk2', 'pickup_location', 'drop_location', 'duration') \
                .prefetch_related('trip_date') \
                    .filter(query).distinct('trip_id')
        return queryset

class TripBookingEnquiry(generics.GenericAPIView):

    def post(self, request):
        name = request.data.get('name')
        email = request.data.get('email')
        phone = request.data.get('phone')
        number_of_pax = request.data.get('number_of_pax')
        trip_name = request.data.get('trip_name')
        trip_page = request.data.get('trip_page')
        trip_date = request.data.get('trip_date')

        if not all([name, email, phone, number_of_pax, trip_name, trip_page, trip_date]):
            return Response({"error": "Some parameter is missing"}, status=status.HTTP_400_BAD_REQUEST)
        
        # Init email object
        obj = EmailSender(email_logs=False)

        # Send email
        result = obj.send_single_email(
            subject='Enquiry for booking a trip',
            body=render_to_string('trip_app/email/trip-booking-enquiry.html',
            {
                "name": name,
                "email": email,
                "phone": phone,
                "number_of_pax": number_of_pax,
                "trip_name": trip_name,
                "trip_page": trip_page,
                "trip_date": trip_date
            }),
            receiver='info@captureatrip.com'
        )

        if result:
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)