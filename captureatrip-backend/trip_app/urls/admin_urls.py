from django.urls import path
from trip_app.views import admin_views

urlpatterns = [
    path('', admin_views.AdminTripListCreate.as_view()),
    path('<int:pk>/', admin_views.AdminTripViewUpdate.as_view()),
    path('slider/', admin_views.AdminSliderTripListCreate.as_view()),
    path('slider/<int:pk>/', admin_views.AdminSliderTripUpdateDelete.as_view()),
    path('perk/', admin_views.AdminPerkList.as_view()),
    path('location/', admin_views.AdminTripLocationListCreate.as_view()),
    path('location/<int:pk>/', admin_views.AdminTripLocationRetrieveUpdate.as_view()),
    path('duration/', admin_views.AdminTripDurationList.as_view()),
]