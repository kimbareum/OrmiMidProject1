from django import template

register = template.Library()

@register.filter
def prev_page(value):
    return max(int(value)-10, 1)

@register.filter
def next_page(value, max_page):
    return min(int(value)+10, max_page)

@register.filter
def get_page_range(current_page, max_page):
    right_index = min(max(current_page - 5, 1) + 9, max_page)
    left_index  = max(right_index - 10 + 1, 1)
    page_range = range(left_index, right_index + 1)
    return page_range
