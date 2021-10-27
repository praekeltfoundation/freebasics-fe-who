import json
import requests
from django.views.generic import TemplateView
from django.conf import settings

url = settings.CONTENTREPO_URL
class HomeView(TemplateView):
    template_name = "core/main.html"

    def get_context_data(self, **kwargs):
        languages = requests.get(url + "/api/v2/custom/languages/").json()
        footers = requests.get(url + "/api/v2/pages/?include_in_footer=True").json()["results"]
        sections = requests.get(url + "/api/v2/indexes/").json()["results"]
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
        return context


class SectionView(TemplateView):
    template_name = "core/section_page.html"

    def get_context_data(self, **kwargs):
        id = self.request.path.split("/")[2]
        section = requests.get(url + "/api/v2/indexes/" + id).json()
        children_articles = requests.get(url + "/api/v2/pages/?parent=" + id + "&type=home.ContentPage&fields=subtitle").json()["results"]
        context = super().get_context_data(**kwargs)
        context["section"] = section
        context["children_articles"] = children_articles
        return context
