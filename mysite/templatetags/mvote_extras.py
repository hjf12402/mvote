from django import template
from mysite import models

register = template.Library()

def show_items(value):
    try:
        poll = models.Poll.objects.get(id=int(value))
        items = models.PollItem.objects.filter(poll=poll).count()
    except:
        items = 5
    return items
register.filter('show_items', show_items)

def show_votes(value):
    try:
        poll = models.Poll.objects.get(id=int(value))
        votes = 0
        pollitems = models.PollItem.objects.filter(poll=poll)
        for pollitem in pollitems:
            votes += pollitem.vote
    except:
        votes = 0
    return votes
register.filter('show_votes', show_votes)