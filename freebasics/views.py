import json
import requests
from django.views.generic import TemplateView
from django.conf import settings
from django.utils import translation


url = settings.CONTENTREPO_URL
class HomeView(TemplateView):
    template_name = "core/main.html"

    def get_context_data(self, **kwargs):
        language_code = self.request.GET.get("language_code")
        if not language_code:
            language_code = 'en'
        translation.activate(language_code)
        settings.LANGUAGE_CODE = language_code
        languages = requests.get(url + "/api/v2/custom/languages/").json()
        footers = requests.get(url + "/api/v2/pages/?include_in_footer=True&locale=" + language_code).json()["results"]
        sections = requests.get(url + "/api/v2/indexes/?locale=" + language_code).json()["results"]
        context = super().get_context_data(**kwargs)
        context["footers"] = footers
        context["sections"] = sections
        context["languages"] = languages
        return context

class ArticleView(TemplateView):
    template_name = "core/article_page.html"

    def get_context_data(self, **kwargs):
        id = self.request.path[1:-1]
        article = requests.get(url + "/api/v2/pages/" + id).json()
        context = super().get_context_data(**kwargs)
        context["article"] = article
        context["contentrepo_url"] = url
        return context


class SectionView(TemplateView):
    template_name = "core/section_page.html"

    def get_context_data(self, **kwargs):
        id = self.request.path.split("/")[2]
        section = requests.get(url + "/api/v2/indexes/" + id).json()
        children_articles = requests.get(url + "/api/v2/pages/?parent=" + id + "&type=home.ContentPage&fields=subtitle,feed_image_thumbnail&locale=" + settings.LANGUAGE_CODE).json()["results"]
        context = super().get_context_data(**kwargs)
        context["section"] = section
        context["children_articles"] = children_articles
        context["contentrepo_url"] = url
        return context


class SearchResultsView(TemplateView):
    template_name = "search/search_results.html"

    def get_context_data(self, **kwargs):
        search_query = self.request.GET.get("q")
        search_results = requests.get(url + "/api/v2/pages/?fields=subtitle,feed_image_thumbnail&type=home.ContentPage&search=" + search_query + "&locale=" + settings.LANGUAGE_CODE).json()["results"]
        context = super().get_context_data(**kwargs)
        context["search_results"] = search_results
        context["search_query"] = search_query
        context["contentrepo_url"] = url
        return context
