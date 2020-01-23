from django.contrib import admin
from django.urls import path, re_path
from django.conf.urls import url,include
from accounts import views as accounts_views
from scraper import views as scraper_views
from rest_framework_simplejwt import views as jwt_views
from rest_framework.routers import DefaultRouter

urlpatterns = [
    path('admin/', admin.site.urls),
]

urlpatterns += [
    url(r'^$',accounts_views.index,name='index'),
    url(r'^accounts/',include('accounts.urls')),
]

urlpatterns += [
    re_path(r'scraper/api/download/(?P<identifier>.+)/(?P<type>.+)/(?P<filename>.+)', scraper_views.ScraperViews.as_view({'get': 'download'}), name='download')
]

router = DefaultRouter()
router.register(r'scraper/api', scraper_views.ScraperViews, basename='scraper')
urlpatterns += router.urls

