from django import template
from django.conf import settings
import json
import requests

register = template.Library()
url = settings.CONTENTREPO_URL

@register.inclusion_tag(
    'core/tags/section_listing_homepage.html',
    takes_context=True
)
def section_listing_homepage(context):
    section_listing = []
    sections = requests.get(url + "/api/v2/indexes/").json()["results"]
    for section in sections:
        item = {}
        item["section"] = section
        item["articles"] = requests.get(url + "/api/v2/pages/?parent=" + str(section["id"]) + "&type=home.ContentPage&fields=subtitle").json()["results"]
        section_listing.append(item)
    return {"sections": section_listing}

@register.inclusion_tag(
    'core/tags/breadcrumbs.html',
    takes_context=True
)
def breadcrumbs(context):
    id = context["request"].path.split("/")[-2]
    print(context["request"].path.split("/"))
    print(id, "is the id")
    ancestors = requests.get(url + "/api/v2/pages/?ancestor_of=" + id).json()["results"]
    print(ancestors)
    return {"ancestors": ancestors}
