import requests
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from django.core import signing
from django.utils import timezone
from django.core.files.base import ContentFile
from django.core.validators import validate_email
from django.template.loader import render_to_string
from django.core.files.storage import default_storage

from email_app.utils import EmailSender
from django.contrib.sitemaps import Sitemap

from common_app.serializers import AdminSliderSerializer, AdminHeaderMenuSerializer, AdminHighlightedTripSerializer,\
    AdminTestimonialSerializer, AdminReviewSerializer, AdminBlogListSerializer, AdminBlogSerializer

from common_app.models import AdminUser, SliderMaster, HeaderMenu, HighlightedTrips, TestimonialMaster, ReviewMaster, BlogMaster
from django.contrib.auth.models import User

# Create your views here.

# Token salt
token_salt = "2Je!@nH27#4G"

class AdminForgotPassword(generics.GenericAPIView):

    def post(self, request):
        admin_email = request.data.get('admin_email').lower()
        password_reset_uri = request.data.get('password_reset_uri')
        admin_object = AdminUser.objects.filter(user__username=admin_email, is_active=True).first()
        
        if admin_object:
            # Generate Reset Link
            try:
                validate_email(admin_email)
            except Exception as e:
                return Response({"error": "Email format invalid"}, status=status.HTTP_400_BAD_REQUEST)
        
            signer = signing.TimestampSigner(salt=token_salt)
            token = signer.sign_object(admin_email)

            # Init email object
            obj = EmailSender(email_logs=False)
            # Send email
            result = obj.send_single_email(
                subject='Admin Password Reset - Captureatrip.com',
                body = render_to_string('common_app/email/forgot-password.html',
                {
                    "first_name": admin_object.user.first_name,
                    "reset_link":  password_reset_uri + '?token=' + token
                }),
                receiver=admin_email
            )
            
            if result:
                return Response(status=status.HTTP_204_NO_CONTENT)
            else:
                return Response(status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response({"error": "Email not found"}, status=status.HTTP_404_NOT_FOUND)

class AdminResetPassword(generics.GenericAPIView):
    def post(self, request):
        new_password = request.data.get('new_password')
        token = request.data.get('token')

        try:
            signer = signing.TimestampSigner(salt=token_salt)
            admin_email = signer.unsign_object(token, max_age=1800)
            if admin_email:
                u = User.objects.get(username=admin_email)
                u.set_password(new_password)
                u.save()
                return Response({"message": "Password updated successfully"}, status=status.HTTP_200_OK)

        except signing.BadSignature:
            return Response({"error": "Reset link is invalid"}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({"error": "Some error occured, please try again"}, status=status.HTTP_400_BAD_REQUEST)

class AdminSliderViewUpdate(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = SliderMaster.objects.all()
    serializer_class = AdminSliderSerializer

class AdminHeaderMenuList(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = HeaderMenu.objects.all()
    serializer_class = AdminHeaderMenuSerializer

class AdminHeaderMenuViewUpdate(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = HeaderMenu.objects.all()
    serializer_class = AdminHeaderMenuSerializer

class AdminHighlightedTripList(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    queryset = HighlightedTrips.objects.all().order_by('position')
    serializer_class = AdminHighlightedTripSerializer

class AdminHighlightedTripViewUpdate(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = HighlightedTrips.objects.all()
    serializer_class = AdminHighlightedTripSerializer

class AdminTestimonialListCreate(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = TestimonialMaster.objects.all()
    serializer_class = AdminTestimonialSerializer

class AdminTestimonialViewUpdate(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = TestimonialMaster.objects.all()
    serializer_class = AdminTestimonialSerializer

class AdminReviewListCreate(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = ReviewMaster.objects.all()
    serializer_class = AdminReviewSerializer

class AdminReviewViewUpdate(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = ReviewMaster.objects.all()
    serializer_class = AdminReviewSerializer

class AdminBlogListCreate(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    queryset = BlogMaster.objects.all()
    
    def get_serializer_class(self):
        if self.request.method == 'POST':            
            return AdminBlogSerializer
        return AdminBlogListSerializer

class AdminBlogViewUpdate(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = BlogMaster.objects.all()
    serializer_class = AdminBlogSerializer

class CKEditorFileUpload(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):        

        image = request.data.get('upload') # file
        if not image:
            return Response({"uploaded": 0, "error": {"message": "File is missing from request"}}, status=status.HTTP_400_BAD_REQUEST)

        limit = 4 * 1024 * 1024   # 3 MiB file limit

        if(image.size > limit):
            return Response(
                {"uploaded": 0, "error": {"message": "File size should not exceed 4 MB"}}, status=status.HTTP_400_BAD_REQUEST
            )

        try:
            path = default_storage.save(f'uploads/ckeditor/images/{image.name}', image)
            final_uri = default_storage.url(path) # Builds URI with settings.MEDIA_URL
            return Response({"uploaded": 1, "fileName": image.name, "url": final_uri}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {"uploaded": 0, "error": {"message": "File could not be uploaded: "+ str(e)}}, status=status.HTTP_400_BAD_REQUEST
            )

class UploadSitemap(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            url = request.build_absolute_uri("/admin/sitemap/generate/")
            response = requests.request("GET", url)
            sitemap_xml = ContentFile(bytes(response.text, encoding='utf-8'))

            # Delete existing sitemap if exists
            sitemap_path_in_bucket = 'generated/sitemaps/sitemap.xml'
            if default_storage.exists(sitemap_path_in_bucket):
                default_storage.delete(sitemap_path_in_bucket)

            default_storage.save(sitemap_path_in_bucket, sitemap_xml)
            return Response(status=status.HTTP_204_NO_CONTENT)

        except Exception as e:
            return Response(
                {"error": "File could not be uploaded: "+ str(e)}, status=status.HTTP_400_BAD_REQUEST
            )

## Sitemap classes
class BlogSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.6

    def items(self):
        return BlogMaster.objects.all().order_by('-blog_id')

    def lastmod(self, obj):
        return obj.last_updated_date
        
    def location(self, obj):
        return '/blog/%s' % (obj.blog_slug)

class StaticSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.5

    def items(self):
        return ['privacy-policy', 'cancellation', 'terms-and-conditions', 'disclaimer']
    
    def lastmod(self, _):
        return timezone.now()

    def location(self, obj):
        return '/%s' % (obj)

class HomeSitemap(StaticSitemap):
    priority = 1.0

    def items(self):
        return ['']
##