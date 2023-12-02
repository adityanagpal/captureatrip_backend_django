from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from category_app.models import CategoryMaster, TripCategory

class AdminCategorySerializer(serializers.ModelSerializer):
    trip_count = serializers.ReadOnlyField(source='category_in_trip.count')
    category_name = serializers.CharField(
        validators=[UniqueValidator(queryset=CategoryMaster.objects.all(), message='Category name already exists')]
    )
    category_slug = serializers.SlugField(
        validators=[UniqueValidator(queryset=CategoryMaster.objects.all(), message='Category slug already exists')]
    )

    class Meta:
        model = CategoryMaster
        fields = (
            "category_id", "category_name", "category_slug", "curated_category_position", "customized_category_position",
             "cover_image", "cover_image_alt_tag",  "banner_image", "banner_image_alt_tag", "icon_image","category_description",
             "icon_image_alt_tag", "meta_title", "meta_keywords", "meta_description", "trip_count","category_description_heading"
        )

class AdminTripCategorySerializer(serializers.ModelSerializer):
    category_name = serializers.ReadOnlyField(source='category_id.category_name')
    
    class Meta:
        model = TripCategory
        fields = ('trip_category_id', 'trip_id', 'category_id', 'is_primary_category', 'position', 'category_name')
        extra_kwargs = {
            'trip_id': {
                'required': False
            }
        }