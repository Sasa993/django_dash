# from django.conf.urls import url, include
# from django.contrib import admin

# from finance.views import company_article_list, ChartData, dash, dash_ajax

# urlpatterns = [
#     url(r'^admin/', admin.site.urls),
#     url(r'^companies/', company_article_list, name='companies'),
#     url(r'^api/chart/data/$', ChartData.as_view(), name='api-chart-data'),
#     url(r'^dash/', dash),
#     url(r'^_dash/', dash_ajax),
# ]
from django.conf import settings
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf.urls.static import static

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
	path('dash/', include('finance.urls')),
	# path('dash_tutorial/', include('dash_tutorial.urls')),
	# re_path('^_dash-', dash_ajax),
	# re_path('^', dash),
]

# if settings.DEBUG:
# 	urlpatterns += static(settings.STATIC_URL,
# 						document_root=settings.STATIC_ROOT)
# 	urlpatterns += static(settings.MEDIA_URL,
# 						document_root=settings.MEDIA_ROOT)