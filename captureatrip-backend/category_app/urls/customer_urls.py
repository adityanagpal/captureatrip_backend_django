from django.urls import path
from category_app.views import customer_views

urlpatterns = [
    path('', customer_views.CategoryList.as_view()),
    path('<str:category_slug>/', customer_views.CategoryView.as_view()),
    path('trips/<str:category_slug>/', customer_views.TripCategoryList.as_view()),
]