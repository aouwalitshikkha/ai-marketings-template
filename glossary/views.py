from django.shortcuts import render
from .models import GlossaryTerm

LETTER_RANGES = [
    ('group-a-e', 'A–E', 'ABCDE'),
    ('group-f-j', 'F–J', 'FGHIJ'),
    ('group-k-o', 'K–O', 'KLMNO'),
    ('group-p-t', 'P–T', 'PQRST'),
    ('group-u-z', 'U–Z', 'UVWXYZ'),
]


def index(request):
    terms = GlossaryTerm.objects.filter(status=GlossaryTerm.Status.PUBLISHED).order_by('term')

    groups = []
    for group_id, label, letters in LETTER_RANGES:
        filtered = [t for t in terms if t.term[0].upper() in letters]
        groups.append({
            'id': group_id,
            'label': label,
            'terms': filtered,
            'count': len(filtered),
        })

    context = {
        'groups': groups,
    }
    return render(request, 'glossary/index.html', context)
