from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseNotFound, Http404
from django.shortcuts import get_object_or_404

from .models import Candidate, Poll, Choice

import datetime
from django.db.models import Sum

def index(request):
    candidates = Candidate.objects.all() # Candidate 모델의 모든 object를 가져옴
    context = {'candidates':candidates}
    return render(request, 'elections/index.html', context)

def candidates(request, name):
    candidate = get_object_or_404(Candidate, name = name) # 아래 주석처리된 부분과 같은 기능을 한다.
    # try:
    #     candidate = Candidate.object.get(name = name)
    # except:
    #     raise Http404
    return HttpResponse(candidate.name)

def areas(request, area):
    today = datetime.datetime.now()
    try:
        poll = Poll.objects.get(area = area, start_date__lte = today, end_date__gte = today) # start_date__let = today : start_date <= today , end_date__gte=today : today <= end_date
        candidates = Candidate.objects.filter(area = area) # 앞부분 area는 Candidate 모델의 area를 의미, 뒷 부분의 area는 매개변수의 area를 의미함.
    except:
        poll = None
        candidates = None
    context = {'candidates':candidates, 'area':area, 'poll':poll}
    return render(request, 'elections/area.html', context)

def polls(request, poll_id):
    poll = Poll.objects.get(pk = poll_id)
    selection = request.POST['choice']

    try:
        choice = Choice.objects.get(poll_id = poll.id, candidate_id = selection)
        choice.votes += 1
        choice.save()
    except:
        #최초로 투표하는 경우, DB에 저장된 Choice객체가 없기 때문에 Choice를 새로 생성합니다
        choice = Choice(poll_id = poll.id, candidate_id = selection, votes = 1)
        choice.save()

    return HttpResponseRedirect("/areas/{}/results".format(poll.area))

def results(request, area):
    candidates = Candidate.objects.filter(area = area)
    context = {'candidates':candidates, 'area':area}
    polls = Poll.objects.filter(area = area)
    poll_results = []
    for poll in polls:
        result = {}
        result['start_date'] = poll.start_date
        result['end_date'] = poll.end_date
        total_votes = Choice.objects.filter(poll_id = poll.id).aggregate(Sum('votes'))
        #print(total_votes)
        result['total_votes'] = total_votes['votes__sum']
        rates = [] #지지율
        for candidate in candidates:
            try:
                choice = Choice.objects.get(poll = poll, candidate = candidate)
                rates.append(round(choice.votes * 100 / result['total_votes'], 1))
            except :
                rates.append(0)
        result['rates'] = rates
        poll_results.append(result)

    context = {'candidates':candidates, 'area':area, 'poll_results' : poll_results}
    return render(request, 'elections/result.html', context)
