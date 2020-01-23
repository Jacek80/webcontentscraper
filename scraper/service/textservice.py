import re
from django import template
from django.utils.html import strip_tags
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe
from django.utils.encoding import force_text


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
        images_list_a = re.findall(r'<img src=\"([^\"]*?\.(?:jpg|jpeg|gif|png))\"', text, flags=re.IGNORECASE)
        images_list_b = re.findall(r'<img src=\'([^\']*?\.(?:jpg|jpeg|gif|png))\'', text, flags=re.IGNORECASE)

        return images_list_a + images_list_b
