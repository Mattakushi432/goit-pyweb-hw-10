from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required


def main(request, page=1):
    quotes = Quote.objects.all()
    paginator = Paginator(quotes, 10)
    quotes_on_page = paginator.page(page)
    return render(request, 'quotes_app/index.html', context={'quotes': quotes_on_page})


@login_required
def add_quote(request):
    if request.method == 'POST':
        form = QuoteForm(request.POST)
        if form.is_valid():
            return redirect(to='quotes_app:root')
    return render(request, 'quotes_app/add_quote.html', {'form': QuoteForm()})
