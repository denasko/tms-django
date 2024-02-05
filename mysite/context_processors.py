from django.shortcuts import HttpResponse


def base_template_context_processor(request: HttpResponse):
    if 'next' not in request.GET:
        return {}
    next = request.GET['next']
    if next.startswith('/polls'):
        base_template = 'polls/base.html'
    elif next.startswith('/articles'):
        base_template = 'articles/base.html'
    elif next.startswith('/shop'):
        base_template = 'shop/base.html'
    else:
        base_template = None
    return {'base_template': base_template}

