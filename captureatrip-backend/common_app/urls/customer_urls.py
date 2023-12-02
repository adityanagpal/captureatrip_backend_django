from django.urls import path
from common_app.views import customer_views

urlpatterns = [
    path('slider/', customer_views.SliderList.as_view()),
    path('slider/<int:pk>/', customer_views.SliderView.as_view()),

    path('menu/header/', customer_views.HeaderMenuList.as_view()),
    path('menu/highlighted_trips/', customer_views.HighlightedTripList.as_view()),
    
    path('testimonial/video/', customer_views.TestimonialList.as_view()),
    path('testimonial/review/', customer_views.ReviewList.as_view()),
    
    path('blog/', customer_views.BlogList.as_view()),
    path('blog/recent/', customer_views.RecentBlogsList.as_view()),
    path('blog/<str:blog_slug>/', customer_views.BlogView.as_view()),
]