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
    sections = requests.get(url + "/api/v2/indexes/?locale=" + settings.LANGUAGE_CODE).json()["results"]
    for section in sections:
        item = {}
        item["section"] = section
        item["articles"] = requests.get(url + "/api/v2/pages/?fields=subtitle,feed_image_thumbnail&type=home.ContentPage&parent=" + str(section["id"]) + "&locale=" + settings.LANGUAGE_CODE).json()["results"]
        section_listing.append(item)
    return {"sections": section_listing, "contentrepo_url": url}

@register.inclusion_tag(
    'core/tags/breadcrumbs.html',
    takes_context=True
)
def breadcrumbs(context):
    id = context["request"].path.split("/")[-2]
    ancestors = requests.get(url + "/api/v2/pages/?ancestor_of=" + id).json()["results"]
    return {"ancestors": ancestors}
