from django.shortcuts import render
from django.http.response import HttpResponse

from django.views.decorators.csrf import csrf_exempt

from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Company
from .as_dash import dispatcher

from django.template.loader import get_template


def company_article_list(request):
	return render(request, "finance/plotly.html", {})


class ChartData(APIView):
	authentication_classes = []
	permission_classes = []

	def get(self, request, format=None):
		articles = dict()
		for company in Company.objects.all():
			if company.articles > 0:
				articles[company.name] = company.articles

		articles = sorted(articles.items(), key=lambda x: x[1])
		articles = dict(articles)

		data = {
			"article_labels": articles.keys(),
			"article_data": articles.values(),
		}

		return Response(data)

# Dash
# return HttpResponseRedirect(reverse('news-year-archive', args=(year,))) I PROBAJ DJANGO TAGS I PROBAJ SA KLASAMA
# **kwargs takes all other arguments that are pass in
# def dash(request, **kwargs):
# 	template_name = get_template("finance/test.html")
# 	return HttpResponse(dispatcher(request), template_name)


def dash(request):
	return HttpResponse(dispatcher(request))


@csrf_exempt
def dash_ajax(request):
	return HttpResponse(dispatcher(request), content_type='application/json')
