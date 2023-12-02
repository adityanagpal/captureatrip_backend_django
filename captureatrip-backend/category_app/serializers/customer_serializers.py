from rest_framework import serializers
from category_app.models import CategoryMaster, TripCategory
from trip_app.serializers import PerkSerializer, TripDatesSerializer

class CategoryListSerializer(serializers.ModelSerializer):

    class Meta:
        model = CategoryMaster
        fields = (
            "category_id", "category_name", "category_slug", "curated_category_position", "customized_category_position",
            "cover_image", "cover_image_alt_tag", "icon_image", "icon_image_alt_tag"
        )

class CategoryDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = CategoryMaster
        fields = (
            "category_id", "category_name", "banner_image", "banner_image_alt_tag", 
            "meta_title", "meta_keywords", "meta_description"
        )

class TripCategorySerializer(serializers.ModelSerializer):
    trip_name = serializers.ReadOnlyField(source='trip_id.trip_name')
    trip_slug = serializers.ReadOnlyField(source='trip_id.trip_slug')
    perk1 = PerkSerializer(source='trip_id.perk1')
    perk2 = PerkSerializer(source='trip_id.perk2')
    cover_image = serializers.ImageField(source='trip_id.cover_image')
    cover_image_alt_tag = serializers.ReadOnlyField(source='trip_id.cover_image_alt_tag')
    pickup_location = serializers.ReadOnlyField(source='trip_id.pickup_location.trip_location_name')
    drop_location = serializers.ReadOnlyField(source='trip_id.drop_location.trip_location_name')
    trip_duration_name = serializers.ReadOnlyField(source='trip_id.duration.trip_duration_name')
    starting_cost = serializers.ReadOnlyField(source='trip_id.starting_cost')
    trip_date = TripDatesSerializer(source='trip_id.trip_date', many=True)
    
    class Meta:
        model = TripCategory
        fields = (
            "trip_category_id", "trip_id", "trip_name", "trip_slug", "perk1", "perk2", "cover_image", "cover_image_alt_tag",
            "is_primary_category", "position", "pickup_location", "drop_location", "trip_duration_name",
            "starting_cost", "trip_date"
        )