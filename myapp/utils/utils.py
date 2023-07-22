from django.utils import timezone
import datetime

def get_banner(main="Our Blog", sub="Python, Django, JavaScript & Life", text=''):
    banner = {
        "main": main,
        "sub": sub,
        "text": text,
    }
    return banner

def view_count_cookie(request, pk):
    context = {
        'flag': False,
        'value':request.COOKIES.get('view_count'),
        'expires': datetime.datetime.replace(timezone.datetime.now(), hour=23, minute=59, second=0),
        }
    if context.get('value'):
        view_list = context.get('value').split('_')
        if str(pk) not in view_list:
            context['value'] += f'_{pk}'
            context['flag'] = True
    else:
        context['value'] = pk
        context['flag'] = True

    return context