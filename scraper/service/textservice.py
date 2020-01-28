import re
from django import template
from django.utils.html import strip_tags
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe
from django.utils.encoding import force_text
from bs4 import BeautifulSoup

register = template.Library()


@register.filter
@stringfilter
def strip_js(text):
    stripped = re.sub(r'<script(?:\s[^>]*)?(>(?:.(?!/script>))*</script>|/>)', '', force_text(text), flags=re.S)
    return mark_safe(stripped)


@register.filter
@stringfilter
def strip_css(text):
    stripped = re.sub(r'<style(?:\s[^>]*)?(>(?:.(?!/style>))*</style>|/>)', '', force_text(text), flags=re.S)
    return mark_safe(stripped)


@register.filter
@stringfilter
def strip_whitespace(text):
    stripped = re.sub(r'\n', ' ', force_text(text), flags=re.S)
    stripped = re.sub(r'\t', ' ', force_text(stripped), flags=re.S)
    stripped = re.sub(' +', ' ', force_text(stripped), flags=re.S)
    return mark_safe(stripped)


class TextService():
    @staticmethod
    def clear_text(text):
        output = text
        output = strip_js(output)
        output = strip_css(output)
        output = strip_tags(output)
        output = strip_whitespace(output)

        return output

    @staticmethod
    def get_images_from_text(text):

        soup = BeautifulSoup(text)

        images_list = []

        for img in soup.findAll('img'):
            img_src = img.get('src')

            extension = img_src.split('.')[-1]

            if extension.lower() in ['jpg', 'jpeg', 'gif', 'png']:
                images_list.append(img_src)

        return images_list
