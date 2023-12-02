from django.db import models
from common_app.models import CommonModel

# Create your models here.
class TripLocationMaster(CommonModel):
    trip_location_id = models.AutoField(primary_key=True)
    trip_location_name = models.CharField(max_length=255, unique=True)

class TripDurationMaster(CommonModel):
    trip_duration_id = models.AutoField(primary_key=True)
    trip_duration_name = models.CharField(max_length=50)

class PerkMaster(CommonModel):
    perk_id = models.AutoField(primary_key=True)
    perk_name = models.CharField(max_length=255)
    perk_icon = models.ImageField(upload_to='uploads/trip/images/perk')

class TripMaster(CommonModel):
    trip_id = models.AutoField(primary_key=True)
    trip_name = models.CharField(max_length=255)
    trip_slug = models.SlugField(max_length=255, unique=True)
    cover_image = models.ImageField(upload_to='uploads/trip/images/cover')
    cover_image_alt_tag = models.CharField(max_length=128, null=True, blank=True)
    banner_image = models.ImageField(upload_to='uploads/trip/images/banner')
    banner_image_alt_tag = models.CharField(max_length=128, null=True, blank=True)
    review_video_url = models.URLField(max_length=1024)
    perk1 = models.ForeignKey(PerkMaster, related_name="trip_perk1", on_delete=models.SET_NULL, null=True, blank=True)
    perk2 = models.ForeignKey(PerkMaster, related_name="trip_perk2", on_delete=models.SET_NULL, null=True, blank=True)
    pickup_location = models.ForeignKey(TripLocationMaster, related_name="trip_pickup_location", on_delete=models.CASCADE)
    drop_location = models.ForeignKey(TripLocationMaster, related_name="trip_drop_location", on_delete=models.CASCADE)
    starting_cost = models.PositiveIntegerField(default=0) # in INR
    discounted_cost = models.PositiveIntegerField(default=0) # in INR
    duration = models.ForeignKey(TripDurationMaster, on_delete=models.CASCADE)
    trip_description = models.TextField()
    trip_itinerary = models.TextField()
    trip_itinerary_pdf = models.FileField(upload_to='uploads/trip/files/itinerary', null=True, blank=True)
    trip_exclusion = models.TextField()
    trip_inclusion = models.TextField()
    multiple_costing = models.TextField()
    is_booking_closed_before_24h = models.BooleanField(default=False)
    note = models.TextField(null=True, blank=True)
    meta_title = models.CharField(max_length=255, null=True, blank=True)
    meta_keywords = models.TextField(null=True, blank=True)
    meta_description = models.TextField(null=True, blank=True)

    class Meta:
        indexes = [
            models.Index(fields=['trip_slug'])
        ]

        constraints = [
            models.UniqueConstraint(fields=['trip_id', 'perk1'], name="unique_trip_perk1"),
            models.UniqueConstraint(fields=['trip_id', 'perk2'], name="unique_trip_perk2")
        ]

class SliderTrips(CommonModel):
    slider_trip_id = models.AutoField(primary_key=True)
    slider_id = models.ForeignKey('common_app.SliderMaster', on_delete=models.CASCADE, related_name='slider_trips')
    trip_id = models.ForeignKey(TripMaster, on_delete=models.CASCADE)
    slider_trip_position = models.PositiveIntegerField(null=True, blank=True)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['trip_id', 'slider_id'], name="unique_slider_trip"),
        ]

class TripRelatedImages(CommonModel):
    trip_related_image_id = models.AutoField(primary_key=True)
    trip_id = models.ForeignKey(TripMaster, on_delete=models.CASCADE, related_name='trip_related_image')
    related_image = models.ImageField(upload_to='uploads/trip/images/related')

class TripRelatedVideos(CommonModel):
    trip_related_video_id = models.AutoField(primary_key=True)
    trip_id = models.ForeignKey(TripMaster, on_delete=models.CASCADE, related_name='trip_related_video')
    trip_related_video_url = models.URLField(max_length=1024)

class TripDates(CommonModel):
    trip_date_id = models.AutoField(primary_key=True)
    trip_id = models.ForeignKey(TripMaster, on_delete=models.CASCADE, related_name='trip_date')
    date_value = models.DateField()

    class Meta:
        indexes = [
            models.Index(fields=['date_value'])
        ]