from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from common_app.utils import CustomBase64ImageField
from common_app.utils import PDFBase64File

from django.db import transaction
from django.db import IntegrityError

from trip_app.models import TripMaster, PerkMaster, TripRelatedImages, TripRelatedVideos, TripLocationMaster,\
    TripDurationMaster, TripDates, SliderTrips
from category_app.serializers import AdminTripCategorySerializer
from category_app.models import TripCategory

class AdminTripRelatedImagesSerializer(serializers.ModelSerializer):
    related_image = CustomBase64ImageField()

    class Meta:
        model = TripRelatedImages
        fields = ('trip_related_image_id', 'trip_id', 'related_image')
        extra_kwargs = {
            'trip_id': {
                'required': False
            }
        }

class AdminTripRelatedImagesDeleteSerializer(serializers.ModelSerializer):
    trip_related_image_id = serializers.PrimaryKeyRelatedField(
            queryset=TripRelatedImages.objects.all()
        )

    class Meta:
        model = TripRelatedImages
        fields = ['trip_related_image_id']

class AdminTripRelatedVideosSerializer(serializers.ModelSerializer):

    class Meta:
        model = TripRelatedVideos
        fields = ('trip_related_video_id', 'trip_id', 'trip_related_video_url')
        extra_kwargs = {
            'trip_id': {
                'required': False
            }
        }

class AdminTripDatesSerializer(serializers.ModelSerializer):

    class Meta:
        model = TripDates
        fields = ['date_value']

# For Trip Create, Update and Detail
class AdminTripSerializer(serializers.ModelSerializer):
    ## nested serializer declarations (write-only)
    primary_category = AdminTripCategorySerializer(write_only=True)
    additional_categories = AdminTripCategorySerializer(many=True, write_only=True, required=False)
    trip_related_images = AdminTripRelatedImagesSerializer(many=True, write_only=True, required=False)
    trip_related_videos = AdminTripRelatedVideosSerializer(many=True, write_only=True, required=False)
    trip_dates = AdminTripDatesSerializer(many=True, write_only=True)
    ##

    ## Objects for retrieving detail (read-only)
    trip_category = AdminTripCategorySerializer(many=True, read_only=True)
    trip_related_image = AdminTripRelatedImagesSerializer(many=True, read_only=True)
    trip_related_video = AdminTripRelatedVideosSerializer(many=True, read_only=True)
    trip_date = AdminTripDatesSerializer(many=True, read_only=True)
    ##

    ## delete-only objects for deleting image records during update
    delete_trip_related_images = AdminTripRelatedImagesDeleteSerializer(many=True, write_only=True, required=False)
    ##

    cover_image = CustomBase64ImageField()
    banner_image = CustomBase64ImageField()
    trip_itinerary_pdf = PDFBase64File(required=False)
    
    trip_slug = serializers.SlugField(
        validators=[UniqueValidator(queryset=TripMaster.objects.all(), message='Trip slug already exists')]
    )

    class Meta:
        model = TripMaster
        fields = (
            "trip_id", "trip_name", "trip_slug", "cover_image", "cover_image_alt_tag", "banner_image", "banner_image_alt_tag",
            "review_video_url", "perk1", "perk2", "pickup_location", "drop_location", "starting_cost","discounted_cost" ,"duration",
            "trip_description", "trip_itinerary", "trip_itinerary_pdf", "trip_exclusion", "trip_inclusion", "multiple_costing",
            "note", "meta_title", "meta_keywords", "meta_description", "primary_category", "additional_categories", 
            "trip_related_images", "trip_related_videos", "trip_dates", "trip_category", "trip_related_image", 
            "trip_related_video", "trip_date", "delete_trip_related_images", "is_booking_closed_before_24h"
        )
    
    @transaction.atomic
    def create(self, validated_data):

        primary_category_data = validated_data.pop('primary_category')
        additional_categories_data = validated_data.pop('additional_categories', {})
        trip_dates_data = validated_data.pop('trip_dates')
        trip_related_images_data = validated_data.pop('trip_related_images', {})
        trip_related_videos_data = validated_data.pop('trip_related_videos', {})

        try:
            # Get Trip id after create
            trip_object = TripMaster.objects.create(**validated_data)        

            # Create primary category
            TripCategory.objects.create(trip_id=trip_object, is_primary_category=True, **primary_category_data)

            # Create additional categories        
            for additional_category in additional_categories_data:
                TripCategory.objects.create(trip_id=trip_object, is_primary_category=False, **additional_category)
            
            # Create Trip dates
            for trip_date in trip_dates_data:
                TripDates.objects.create(trip_id=trip_object, **trip_date)

            # Create Trip related images
            for trip_related_image in trip_related_images_data:
                TripRelatedImages.objects.create(trip_id=trip_object, **trip_related_image)

            # Create Trip related videos
            for trip_related_video in trip_related_videos_data:
                TripRelatedVideos.objects.create(trip_id=trip_object, **trip_related_video)
                
        except IntegrityError as e:
            raise serializers.ValidationError("Form contains duplicate values")

        return trip_object
    
    @transaction.atomic
    def update(self, instance, validated_data):
        trip_id = instance.trip_id
        categories_cleared = False
        
        if all (k in validated_data for k in ("primary_category", "additional_categories")):
            # Delete all existing categories for the trip (this avoids potential IntegrityError due to duplicates)
            TripCategory.objects.filter(trip_id=trip_id).delete()
            categories_cleared = True
                        
        if "primary_category" in validated_data:
            primary_category_data = validated_data.pop('primary_category')
            
            # Add/Update primary category record
            TripCategory.objects.update_or_create(
                trip_id=trip_id, is_primary_category=True,
                defaults={'trip_id': instance, 'is_primary_category': True, **primary_category_data}
            )
        
        if "additional_categories" in validated_data:
            additional_categories_data = validated_data.pop('additional_categories')
            
            # Delete existing additional category records, add updated records
            if not categories_cleared:
                TripCategory.objects.filter(trip_id=trip_id, is_primary_category=False).delete()

            for additional_category in additional_categories_data:
                TripCategory.objects.create(trip_id=instance, is_primary_category=False, **additional_category)
        
        if "trip_dates" in validated_data:
            trip_dates_data = validated_data.pop('trip_dates')
            
            # Delete existing date records, add updated records
            TripDates.objects.filter(trip_id=trip_id).delete()
            for trip_date in trip_dates_data:
                TripDates.objects.create(trip_id=instance, **trip_date)
        
        if "trip_related_images" in validated_data:
            trip_related_images_data = validated_data.pop('trip_related_images')

            # Add Trip related images
            for trip_related_image in trip_related_images_data:
                TripRelatedImages.objects.create(trip_id=instance, **trip_related_image)
        
        if "trip_related_videos" in validated_data:
            trip_related_videos_data = validated_data.pop('trip_related_videos')

            # Delete existing video records
            TripRelatedVideos.objects.filter(trip_id=trip_id).delete()
            
            # Now, add new Trip related videos
            for trip_related_video in trip_related_videos_data:
                TripRelatedVideos.objects.create(trip_id=instance, **trip_related_video)
        
        if "delete_trip_related_images" in validated_data:
            delete_trip_related_images_data = validated_data.pop('delete_trip_related_images')

            for delete_trip_related_image in delete_trip_related_images_data:
                trip_related_image_id = delete_trip_related_image['trip_related_image_id'].pk
                if trip_related_image_id:
                    TripRelatedImages.objects.filter(
                        trip_id=trip_id, trip_related_image_id=trip_related_image_id
                    ).delete()

        return super().update(instance, validated_data)

class AdminTripListSerializer(serializers.ModelSerializer):
    trip_categories = AdminTripCategorySerializer(many=True, source='trip_category')
    pickup_location = serializers.ReadOnlyField(source='pickup_location.trip_location_name')
    drop_location = serializers.ReadOnlyField(source='drop_location.trip_location_name')
    duration = serializers.ReadOnlyField(source='duration.trip_duration_name')

    class Meta:
        model = TripMaster
        fields = (
            "trip_id", "trip_name", "trip_slug", "pickup_location", "drop_location", "starting_cost", "duration", "trip_categories"
        )

class AdminSliderTripSerializer(serializers.ModelSerializer):
    trip_name = serializers.ReadOnlyField(source='trip_id.trip_name')
    trip_slug =  serializers.ReadOnlyField(source='trip_id.trip_slug')
    pickup_location = serializers.ReadOnlyField(source='trip_id.pickup_location.trip_location_name')
    drop_location = serializers.ReadOnlyField(source='trip_id.drop_location.trip_location_name')
    starting_cost = serializers.ReadOnlyField(source='trip_id.starting_cost') 
    duration = serializers.ReadOnlyField(source='trip_id.duration.trip_duration_name')
    trip_categories = AdminTripCategorySerializer(source='trip_id.trip_category', many=True, read_only=True)

    class Meta:
        model = SliderTrips
        fields = (
            'slider_trip_id', 'slider_id', 'trip_id', 'trip_name', 'trip_slug', 'pickup_location', 'drop_location',
            'starting_cost', 'duration', 'slider_trip_position', 'trip_categories'
        )
    
    def create(self, validated_data):
        try:            
            trip_object = validated_data.get('trip_id')
            slider_trip_object = SliderTrips.objects.create(**validated_data)
            return slider_trip_object
        except IntegrityError:
            raise serializers.ValidationError(detail=f'Trip - {trip_object.trip_name} ({trip_object.trip_id}) already exists')

class AdminPerkSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = PerkMaster
        fields = ('perk_id', 'perk_name', 'perk_icon')

class AdminTripLocationSerializer(serializers.ModelSerializer):
    trip_location_name = serializers.CharField(
        validators=[UniqueValidator(queryset=TripLocationMaster.objects.all(), message='Trip Location name already exists')]
    )
    
    class Meta:
        model = TripLocationMaster
        fields = ('trip_location_id', 'trip_location_name')

class AdminTripDurationSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = TripDurationMaster
        fields = ('trip_duration_id', 'trip_duration_name')