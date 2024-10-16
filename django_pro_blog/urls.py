from django.conf import settings
from django.conf.urls.static import s
from django.contrib import admin
from django.urls import path, include
from django.contrib.sitemaps.views import sitemap
from blog.sitemaps import PostSitemap





# Adding a sitemap url
sitemaps = {
    'posts': PostSitemap
}


urlpatterns = [
    path('admin/', admin.site.urls),
    path('blog/', include('blog.urls')),
    path('users/', include('users.urls')),
    path('accounts/', include('allauth.urls')), 
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='sitemap'),
]  + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
