from django.conf import settings
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf.urls.static import static
from django.views.generic import RedirectView

from finance.views import company_article_list, ChartData, dash, dash_ajax


app_name = "notes"
urlpatterns = [
	path('admin/', admin.site.urls),
	path('companies/', company_article_list, name="companies"),
	path('api/chart/data/', ChartData.as_view(), name="api-chart-data"),
	re_path(r'^favicon\.ico$', RedirectView.as_view(url='/static/images/favicon.ico')),
	re_path('_dash-', dash_ajax),
	re_path('^$', dash),
]

# if settings.DEBUG:
# 	urlpatterns += static(settings.STATIC_URL,
# 						document_root=settings.STATIC_ROOT)
# 	urlpatterns += static(settings.MEDIA_URL,
# 						document_root=settings.MEDIA_ROOT)