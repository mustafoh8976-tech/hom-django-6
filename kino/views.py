from django.shortcuts import get_object_or_404, redirect, render
from .models import Janore, Kino, Komentari


def home_view(request):
    kinolar = Kino.objects.prefetch_related('janore').all()
    search_name = request.GET.get('name', '').strip()
    selected_janore = request.GET.get('janore', '').strip()

    if selected_janore.isdigit():
        kinolar = kinolar.filter(janore__id=selected_janore)
    kinolar = kinolar.distinct()
    if search_name:
        search_text = search_name.casefold()
        kinolar = [kino for kino in kinolar if search_text in kino.name.casefold()]

    context = {
        'kinolar': kinolar,
        'janorelar': Janore.objects.all(),
        'search_name': search_name,
        'selected_janore': selected_janore,
    }
    return render(request, 'home.html', context=context)


def kino_detail(request, pk):
    kino = get_object_or_404(Kino.objects.prefetch_related('janore'), pk=pk)
    error = ''

    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        text = request.POST.get('text', '').strip()
        if not name or not text:
            error = 'Заполни имя и текст комментария.'
        elif len(name) > 100:
            error = 'Имя должно содержать не больше 100 символов.'
        else:
            Komentari.objects.create(kino=kino, name=name, text=text)
            return redirect('kino_detail', pk=kino.pk)

    context = {
        'kino': kino,
        'komentari': kino.komentari.all(),
        'error': error,
        'comment_name': request.POST.get('name', '') if request.method == 'POST' else '',
        'comment_text': request.POST.get('text', '') if request.method == 'POST' else '',
    }
    return render(request, 'detail.html', context=context)
