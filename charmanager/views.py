from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse

from charinfo.models import Character
from charmanager.forms import CharacterForm

@login_required
def charList(request):
    characters = request.user.character_set.all()
    return render(request, 'charmanager/charlist.html', {
        'characters': characters,
    })

@login_required
def charAdd(request):
    if request.method == 'POST':
        form = CharacterForm(request.POST)
        if form.is_valid():
            # TODO(nyro): process data
            return HttpResponseRedirect(reverse(charList)) # url somehow?

    else:
        character = Character(user=request.user)
        form = CharacterForm(instance=character)

    return render(request, 'charmanager/add.html', {
        'form': form,
    })

@login_required
def charDelete(request, pk):
    character = get_object_or_404(Character, pk=pk)
    if character.user != request.user:
        raise PermissionDenied
    character.delete()
    return HttpResponseRedirect('/charmanager')

#@login_required
#def charEdit(request, pk):
#    if request.method == 'POST':
#        form = CharacterForm(request.POST)
#        if form.is_valid():
#            # process data here
#            return HttpResponseRedirect('')
#    else:
#        character = get_object_or_404(Character, pk=pk)
#        form = CharacterForm(instance=character)
#
#    return render(request, 'charmanager/edit.html', {
#        #'character': character,
#        'form': form,
#    })
