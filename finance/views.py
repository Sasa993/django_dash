from django.shortcuts import render
from django.http.response import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Company
from .as_dash import dispatcher
from .as_dash import clean_dash_content


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


def dash(request):
	dash_content = HttpResponse(dispatcher(request), content_type='application/json').getvalue()
	# clean the dash HMTL content, using clean_dash_content from as_dash.py (the content contains lots of unnecessary characters like '\n')
	dash_content = clean_dash_content(dash_content)
	context = {'dash_content': dash_content}

	return render(request, 'finance/historical_charts.html', context)


@csrf_exempt
def dash_ajax(request):
	return HttpResponse(dispatcher(request), content_type='application/json')
