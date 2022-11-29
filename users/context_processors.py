"""Context processors"""
import datetime


def today_year(request):
    """Add 'year' variable to all templates"""
    return {
        'year': datetime.date.today().year
    }
