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
def charTile(request, pk):
    char = get_object_or_404(Character, pk=pk)
    if char.user != request.user:
        raise PermissionDenied
    charsheet = char.charactersheet()
    return render(request, 'charinfo/tile.html', {
        'id': pk,
        'name': charsheet.name,
        'corptag': char.corptag(),
        'balance': float(charsheet.balance),
        'skillpoints': char.total_skillpoints(),
        'clone_skillpoints': charsheet.cloneSkillPoints,
        'skillqueue_time': char.skillqueue_time(),
        'subscribed_time': char.subscribed_time(),
        'current_skill': char.current_skill(),
        'current_skill_level': char.current_skill_level(),
        'is_training': char.is_training(),
    })

@login_required
def charDetail(request, pk):
    char = get_object_or_404(Character, pk=pk)
    if char.user != request.user:
        raise PermissionDenied
    charsheet = char.charactersheet()
    return render(request, 'charinfo/detail.html', {
        'name': charsheet.name,
        'corp': charsheet.corporationName,
        'alliance': charsheet.allianceName,
        'skillpoints': char.total_skillpoints(),
        'skillqueue': char.skillqueue(),
        'ship': char.ship(),
    })
