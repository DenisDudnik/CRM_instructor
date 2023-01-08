"""Context processors"""
import datetime

from users.models import UserMessage


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


def get_back_url(request):
    return {
        'back': request.META.get('HTTP_REFERER')
    }


def get_contacts(request):
    if request.user.is_anonymous:
        return {'contacts': []}
    result = {'contacts': []}
    added = set()
    queryset = [request.user.in_messages, request.user.out_messages]
    for x in queryset:
        for item in x.filter(kind='msg').all():
            if item.from_user == request.user:
                obj = {
                    'id': item.to_user.id,
                    'name': item.to_user.get_full_name()
                }
            else:
                obj = {
                    'id': item.from_user.id,
                    'name': item.from_user.get_full_name()
                }
            if obj['id'] not in added:
                result['contacts'].append(obj)
            added.add(obj['id'])
    return result


def get_notification(request):
    if request.user.is_anonymous:
        return {'user_notifications': []}

    message = UserMessage.objects.filter(
        to_user=request.user, kind='notify'
    ).all()
    return {'user_notifications': message}
