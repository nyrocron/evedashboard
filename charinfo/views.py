from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required

from charinfo.models import Character

@login_required
def charList(request):
    characters = request.user.character_set.all()
    return render(request, 'charinfo/charlist.html', {
        'characters': characters,
    })

@login_required
def charDetail(request, pk):
    char = get_object_or_404(Character, pk=pk)
    if char not in request.user.character_set.all():
        raise PermissionDenied
    charsheet = char.charactersheet()
    return render(request, 'charinfo/detail.html', {
        'name': charsheet.name,
        'corp': charsheet.corporationName,
        'alliance': charsheet.allianceName,
    })
