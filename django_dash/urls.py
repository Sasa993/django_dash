from django.conf import settings
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf.urls.static import static
from django.views.generic import RedirectView

# from news.views import scrape
from finance.views import company_article_list, ChartData, dash, dash_ajax
# from .views import home

app_name = "notes"
urlpatterns = [
	path('admin/', admin.site.urls),
	# path('notes/', include('notepad.urls')),
	# path('scrape/', scrape, name="scrape"),
	# path('home/', home, name="home"),
	path('companies/', company_article_list, name="companies"),
	path('api/chart/data/', ChartData.as_view(), name="api-chart-data"),
	re_path(r'^favicon\.ico$', RedirectView.as_view(url='/static/images/favicon.ico')),
	# path('dash/', include('finance.urls')),
	# path('dash_tutorial/', include('dash_tutorial.urls')),
	re_path('_dash-', dash_ajax),
	re_path('^$', dash),
]

# if settings.DEBUG:
# 	urlpatterns += static(settings.STATIC_URL,
# 						document_root=settings.STATIC_ROOT)
# 	urlpatterns += static(settings.MEDIA_URL,
# 						document_root=settings.MEDIA_ROOT)