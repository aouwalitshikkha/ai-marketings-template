import html2text
from django.core.cache import cache
from django.views.generic import TemplateView
from .models import GlossaryPageConfig, GlossaryTerm

_md_converter = html2text.HTML2Text()
_md_converter.body_width = 0
_md_converter.ignore_links = False
_md_converter.ignore_images = False

CACHE_KEY = 'glossary_groups'
CACHE_TTL = 3600

LETTER_RANGES = [
    ('group-a-e', 'A–E', 'ABCDE'),
    ('group-f-j', 'F–J', 'FGHIJ'),
    ('group-k-o', 'K–O', 'KLMNO'),
    ('group-p-t', 'P–T', 'PQRST'),
    ('group-u-z', 'U–Z', 'UVWXYZ'),
]


def build_groups():
    terms = GlossaryTerm.objects.filter(
        status=GlossaryTerm.Status.PUBLISHED
    ).order_by('term')

    groups = []
    for group_id, label, letters in LETTER_RANGES:
        filtered = [t for t in terms if t.term[0].upper() in letters]
        groups.append({
            'id': group_id,
            'label': label,
            'terms': filtered,
            'count': len(filtered),
        })
    return groups


class GlossaryIndexView(TemplateView):
    template_name = 'glossary/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        groups = cache.get(CACHE_KEY)
        if groups is None:
            groups = build_groups()
            cache.set(CACHE_KEY, groups, CACHE_TTL)
        context['groups'] = groups

        config = GlossaryPageConfig.objects.first()
        if config and config.seo_title:
            context['page_title'] = config.seo_title
            context['page_description'] = config.seo_description
        return context


class GlossaryMarkdownView(TemplateView):
    template_name = 'glossary/glossary.md'
    content_type = 'text/markdown; charset=utf-8'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        groups = cache.get(CACHE_KEY)
        if groups is None:
            groups = build_groups()
            cache.set(CACHE_KEY, groups, CACHE_TTL)

        md_groups = []
        for group in groups:
            md_terms = []
            for term in group['terms']:
                md_desc = _md_converter.handle(term.description) if term.description else ''
                md_terms.append({'term': term.term, 'description': md_desc})
            md_groups.append({'id': group['id'], 'label': group['label'], 'terms': md_terms})

        context['groups'] = md_groups

        config = GlossaryPageConfig.objects.first()
        if config and config.seo_title:
            context['page_title'] = config.seo_title
            context['page_description'] = config.seo_description
        return context
