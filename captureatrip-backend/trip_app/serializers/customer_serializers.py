from rest_framework import serializers
from trip_app.models import TripMaster, TripRelatedImages, TripRelatedVideos, TripDates, PerkMaster, TripDurationMaster, SliderTrips

class PerkSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = PerkMaster
        fields = ('perk_name', 'perk_icon')

class TripRelatedImagesSerializer(serializers.ModelSerializer):

    class Meta:
        model = TripRelatedImages
        fields = ('trip_related_image_id', 'related_image')

class TripRelatedVideosSerializer(serializers.ModelSerializer):

    class Meta:
        model = TripRelatedVideos
        fields = ('trip_related_video_id', 'trip_related_video_url')

class TripDatesSerializer(serializers.ModelSerializer):

    class Meta:
        model = TripDates
        fields = ['date_value']

class TripViewSerializer(serializers.ModelSerializer):
    trip_related_image = TripRelatedImagesSerializer(many=True)
    trip_related_video = TripRelatedVideosSerializer(many=True)
    trip_date = TripDatesSerializer(many=True)

    pickup_location = serializers.ReadOnlyField(source='pickup_location.trip_location_name')
    drop_location = serializers.ReadOnlyField(source='drop_location.trip_location_name')
    duration = serializers.ReadOnlyField(source='duration.trip_duration_name')

    class Meta:
        model = TripMaster
        fields = (
                "trip_id", "trip_name", "banner_image", "banner_image_alt_tag", "review_video_url", "pickup_location", 
                "drop_location", "trip_date", "starting_cost", "duration", "trip_description", "trip_itinerary", 
                "trip_itinerary_pdf", "trip_exclusion", "trip_inclusion", "multiple_costing", "note", "meta_title", 
                "meta_keywords", "meta_description", "trip_related_image", "trip_related_video", "is_booking_closed_before_24h"
            )

class TripListSerializer(serializers.ModelSerializer):
    perk1 = PerkSerializer()
    perk2 = PerkSerializer()
    pickup_location = serializers.ReadOnlyField(source='pickup_location.trip_location_name')
    drop_location = serializers.ReadOnlyField(source='drop_location.trip_location_name')
    duration = serializers.ReadOnlyField(source='duration.trip_duration_name')
    trip_date = TripDatesSerializer(many=True)

    class Meta:
        model = TripMaster
        fields = (
            'trip_id', 'trip_name', 'trip_slug', 'cover_image', 'cover_image_alt_tag', 'pickup_location', 
            'drop_location', 'starting_cost', 'duration', 'perk1', 'perk2', 'trip_date'
        )

class TripDurationSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = TripDurationMaster
        fields = ('trip_duration_id', 'trip_duration_name')

class TripSearchSerializer(serializers.ModelSerializer):

    class Meta:
        model = TripMaster
        fields = ('trip_id', 'trip_name', 'trip_slug')