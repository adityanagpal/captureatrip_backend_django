from rest_framework import generics
from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import JSONParser
from django.contrib.sitemaps import Sitemap
from django.db.models import Q
from django.utils import timezone

from trip_app.serializers import AdminTripSerializer, AdminTripListSerializer, AdminPerkSerializer, AdminTripLocationSerializer,\
    AdminTripDurationSerializer, AdminSliderTripSerializer
from trip_app.models import TripMaster, PerkMaster, TripLocationMaster, TripDurationMaster, SliderTrips

# Create your views here.
class AdminTripListCreate(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [JSONParser]    
    
    def get_serializer_class(self):
        if self.request.method == 'POST':            
            return AdminTripSerializer
        return AdminTripListSerializer
    
    def get_queryset(self):
        category_id = self.request.query_params.get('category_id')
        trip_duration_id = self.request.query_params.get('trip_duration_id')
        
        # Optionally filter using query parameter in the URL.
        query = Q()

        if category_id:
            query &= Q(trip_category__category_id=category_id, trip_category__is_primary_category=True)
        
        if trip_duration_id:
            query &= Q(duration=trip_duration_id)
        
        queryset = TripMaster.objects.filter(query).prefetch_related('trip_category__category_id').order_by('-trip_id')
        
        return queryset

class AdminTripViewUpdate(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [JSONParser]
    queryset = TripMaster.objects.prefetch_related('trip_category__category_id')
    serializer_class = AdminTripSerializer

class AdminSliderTripListCreate(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AdminSliderTripSerializer

    def get_queryset(self):
        queryset = SliderTrips.objects.none()

        # Filter using query parameter (SliderMaster foreign key) in the URL.
        slider_id = self.request.query_params.get('slider_id')
        if slider_id:
            queryset = SliderTrips.objects.filter(slider_id=slider_id) \
                .select_related('trip_id__pickup_location', 'trip_id__drop_location', 'trip_id__duration') \
                    .prefetch_related('trip_id__trip_category__category_id') \
                        .order_by('-slider_trip_position')
                    
        return queryset

class AdminSliderTripUpdateDelete(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = AdminSliderTripSerializer
    queryset = SliderTrips.objects.all()

class AdminPerkList(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = PerkMaster.objects.all()
    serializer_class = AdminPerkSerializer

class AdminTripLocationListCreate(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = TripLocationMaster.objects.all()
    serializer_class = AdminTripLocationSerializer

class AdminTripLocationRetrieveUpdate(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = TripLocationMaster.objects.all()
    serializer_class = AdminTripLocationSerializer

class AdminTripDurationList(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = TripDurationMaster.objects.all()
    serializer_class = AdminTripDurationSerializer

class TripSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.85

    def items(self):
        return TripMaster.objects.all().order_by('-trip_id')

    def lastmod(self, obj):
        return obj.last_updated_date
        
    def location(self,obj):
        return '/trip/%s' % (obj.trip_slug)

class UpcomingTripSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.8

    def items(self):
        return [
                'all', 'February-trip', 'March-trip', 'April-trip', 'May-trip', 'June-trip', 'July-trip',
                'August-trip', 'September-trip', 'October-trip', 'November-trip', 'December-trip'
            ]
    
    def lastmod(self, _):
        return timezone.now()

    def location(self, obj):
        return '/upcoming-trips/%s' % (obj)