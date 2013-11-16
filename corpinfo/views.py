from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required

from eveapi.models import APIKey
from corpinfo.models import Corporation

@login_required
def corpList(request):
    corps = request.user.corporation_set.all()
    return render(request, 'corpinfo/corplist.html', {
        'corps': corps,
    })

@login_required
def corpContracts(request, pk):
    corp = get_object_or_404(Corporation, pk=pk)
    if corp.user != request.user:
        raise PermissionDenied
    contracts = corp.contracts()
    return render(request, 'corpinfo/contracts.html', {
        'contracts': contracts,
    })
