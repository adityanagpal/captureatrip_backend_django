from rest_framework.generics import ListAPIView, RetrieveAPIView
from django.utils import timezone
from django.db.models import Q
from category_app.serializers import CategoryListSerializer, CategoryDetailSerializer, TripCategorySerializer
from category_app.models import CategoryMaster, TripCategory

# Create your views here.
class CategoryList(ListAPIView):
    queryset = CategoryMaster.objects.\
        filter(Q(curated_category_position__gt=0) | Q(customized_category_position__gt=0)) \
            .order_by('curated_category_position')
    serializer_class = CategoryListSerializer

class CategoryView(RetrieveAPIView):
    serializer_class = CategoryDetailSerializer
    lookup_field = 'category_slug'
    queryset = CategoryMaster.objects.all()

class TripCategoryList(ListAPIView):
    serializer_class = TripCategorySerializer
    
    def get_queryset(self):
        filter_year = self.request.query_params.get('year')
        filter_month = self.request.query_params.get('month')
        trip_duration_id = self.request.query_params.get('trip_duration_id')
        
        query = Q()

        query &= Q(category_id__category_slug=self.kwargs.get('category_slug'))
        
        # Optionally filter using query parameters in the URL.
        if filter_year: query &= Q(trip_id__trip_date__date_value__year=filter_year)        
        if filter_month: query &= Q(trip_id__trip_date__date_value__month=filter_month)        
        if trip_duration_id: query &= Q(trip_id__duration=trip_duration_id)

        queryset = TripCategory.objects \
            .select_related(
                'trip_id', 'trip_id__perk1', 'trip_id__perk2', 'trip_id__pickup_location',
                'trip_id__drop_location', 'trip_id__duration'                
            ).prefetch_related('trip_id__trip_date') \
                .filter(query).distinct('trip_id')
        return queryset