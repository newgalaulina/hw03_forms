from django.core.paginator import Paginator

num_posts = 10

def get_page_context(queryset, request):
    paginator = Paginator(queryset, num_posts)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return {
        'page_obj': page_obj,
    }