from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from .models import Quote, Author, Tag
from .forms import QuoteForm


def main(request, page=1):
    quotes = Quote.objects.select_related('author').prefetch_related('tags').all()
    paginator = Paginator(quotes, 10)
    quotes_on_page = paginator.page(page)
    return render(request, 'quotes_app/index.html', context={'quotes': quotes_on_page})


def author_detail(request, author_id: int):
    author = get_object_or_404(Author, id=author_id)
    quotes = Quote.objects.filter(author=author).prefetch_related('tags')
    return render(request, 'quotes_app/author_detail.html', {'author': author, 'quotes': quotes})


def tag_quotes(request, tag_name: str):
    tag = get_object_or_404(Tag, name=tag_name)
    quotes = Quote.objects.filter(tags=tag).select_related('author').prefetch_related('tags')
    return render(request, 'quotes_app/tag_quotes.html', {'tag': tag, 'quotes': quotes})


@login_required
def add_quote(request):
    if request.method == 'POST':
        form = QuoteForm(request.POST)
        if form.is_valid():
            # Save placeholder: depends on form implementation; skip saving for now
            return redirect(to='quotes_app:root')
    else:
        form = QuoteForm()
    return render(request, 'quotes_app/add_quote.html', {'form': form})
