from django.contrib.sitemaps import Sitemap
from .models import Post


# Adding a sitemap
class PostSitemap(Sitemap):
    changefreq = 'daily'
    priority = 0.9


    def items(self):
        return Post.objects.all()


    def lastmod(self, obj):
        return obj.updated_at


    def location(self, obj):
        return obj.get_absolute_url()