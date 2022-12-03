"""Context processors"""
import datetime


def today_year(request):
    """Add 'year' variable to all templates"""
    return {
        'year': datetime.date.today().year
    }


def get_links(request):
    links = {
        'clients': ('Клиенты', 'clients'),
        'teachers': ('Тренеры', 'teachers'),
        'managers': ('Менеджеры', 'managers'),
        'courses': ('Курсы', 'courses:list')
    }
    result = {
        'links': []
    }
    if request.user.is_anonymous:
        return result
    if request.user.role in ('C', 'T'):
        result['links'] = [links.get('courses')]
    elif request.user.role == 'M':
        result['links'] = [v for k, v in links.items() if k != 'managers']
    else:
        result['links'] = [v for v in links.values()]

    return result
