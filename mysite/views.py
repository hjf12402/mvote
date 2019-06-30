#未解决ajax刷新局部代码后投票函数失效问题！！！！


from django.shortcuts import render, redirect
import datetime
from .models import PollItem, Poll, Profile, VoteCheck
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import Http404, HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .form import AddPoll, AddItem
import json

# Create your views here.
def index(request):
    time = datetime.datetime.now()
    all_polls = Poll.objects.filter(enabled=True).order_by('-created_at')
    if all_polls.count() == 0:
        messages.add_message(request, messages.INFO, '暂无投票项目')
    else:
        paginator = Paginator(all_polls, 5)
        p = request.GET.get('p')
        try:
            polls = paginator.page(p)
        except PageNotAnInteger:
            polls = paginator.page(1)
        except EmptyPage:
            polls = paginator.page(paginator.num_pages)
    return render(request, 'index.html', locals())

@login_required
def poll(request, pollid):
    try:
        poll = Poll.objects.get(id=pollid)
        pollitems = PollItem.objects.filter(poll=poll)
        if pollitems.count() == 0:
            messages.add_message(request, messages.INFO, '暂无投票项')
    except:
        raise Http404
    return render(request, 'poll.html', locals())

@login_required
def vote(request, pollid, pollitemid):
    pollitem = PollItem.objects.get(id=pollitemid)
    pollitem.vote += 1
    pollitem.save()
    url = '/poll/{}'.format(pollid)
    messages.add_message(request, messages.INFO, '投票成功')
    return redirect(url)

@login_required
def govote(request):
    if request.method == 'GET' and request.is_ajax():
        pollitemid = request.GET.get('pollitemid')
        pollid = request.GET.get('pollid')
        bypass = 0
        if VoteCheck.objects.filter(userid=request.user.id, pollid=pollid, vote_date=datetime.date.today()):
            bypass = 1
        else:
            vote_rec = VoteCheck(userid=request.user.id, pollid=pollid, vote_date=datetime.date.today())
            vote_rec.save()
        try:
            pollitem = PollItem.objects.get(id=pollitemid)
            if not bypass:
                pollitem.vote += 1
                pollitem.save()
            votes = pollitem.vote
        except:
            votes = 0
    else:
        votes = 0

    return HttpResponse(json.dumps({'votes':votes, 'bypass':bypass}))

@login_required
def delete_item(request):
    if request.method == 'GET':
        pollitemid = request.GET.get('pollitemid')
        pollitem = PollItem.objects.get(id=pollitemid)
        poll = pollitem.poll
        pollitem.delete()
    url = '/poll/{} #pollitems'.format(poll.id)
    return HttpResponse(url)

@login_required
def addpoll(request):
    if request.method == 'POST':
        newpoll = Poll(user=request.user, enabled=True)
        form = AddPoll(request.POST, instance=newpoll)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.INFO, '已增加项目')
            return redirect('/')
        else:
            messages.add_message(request, messages.INFO, '每个字段都要填写')
    else:
        form = AddPoll()
    return render(request, 'addpoll.html', locals())

def additem(request, pollid):
    poll = Poll.objects.get(id=pollid)
    if request.method == 'POST':
        newitem = PollItem(poll=poll)
        form = AddItem(request.POST, instance=newitem)
        if form.is_valid():
            form.save()
            messages.add_message(request, messages.INFO, '已增加项目')
            url = '/poll/{}'.format(poll.id)
            return redirect(url)
        else:
            messages.add_message(request, messages.INFO, '每个字段都要填写')
    else:
        form = AddItem()
    return render(request, 'additem.html', locals())