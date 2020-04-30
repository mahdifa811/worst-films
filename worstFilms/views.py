from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from .models import Film, Comment, Like
from .forms import FilmForm, CommentForm, ReplyForm
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib import messages

def home(request):
    return redirect('worstFilms:home')

def home_page(request):
    film = Film.objects.all().order_by('-published_date')
    query = request.GET.get('q')
    if query:
        film= film.filter(
            Q(title__icontains=query)|
            Q(director__icontains=query)|
            Q(country__icontains=query)|
            Q(release_year__icontains=query)|
            Q(review__icontains=query)
            #Q(author__icontains=query)
        ).distinct()
    context = {
        'film' : film
    }
    return render(request , 'worst/home.html', context)

@login_required
def create_worst(request):
    if request.method == 'GET':
        form = FilmForm()
        context = {
            'form': form
        }
        return render(request , 'worst/create.html' , context)
    else:
        form = FilmForm(request.POST, request.FILES)
        if form.is_valid():
            film= form.save(commit= False)
            film.author = request.user
            film= form.save()

            return redirect('worstFilms:home')
        else:       
            form = FilmForm()
            context = {
                'form': form , 
                'error': 'bad info'
            }
            return render(request , 'worst/create.html' , context)

@login_required
def edit_worst(request , id):
    film = get_object_or_404(Film , pk=id)
    if request.method == 'GET':
        form = FilmForm(instance = film)
        return render(request, 'worst/edit.html', {'form':form, 'film':film})
    else:
        form = FilmForm(request.POST, instance= film)
        if form.is_valid():
            form.save()
            return redirect('worstFilms:home')
        else:
            form = FilmForm(instance= film)
            return render(request, 'worst/edit.html', {'form': form , 'error':'bad info'})


    

def detail_worst(request , id):
    wfilm = get_object_or_404(Film, pk = id)
    comments= Comment.objects.filter(film=wfilm, is_reply= False)
    reply_form = ReplyForm()
    can_like = False
    if request.user.is_authenticated:
        if wfilm.user_can_like(request.user):
            can_like = True
    if request.method == 'POST':
        form= CommentForm(request.POST)
        if form.is_valid():
            new_comment= form.save(commit=False)
            new_comment.user= request.user
            new_comment.film= wfilm
            new_comment.save()
            messages.success(request, 'your comment submitted successfully!', 'success')
    else:
        form= CommentForm()

    context ={
        'wfilm': wfilm,
        'comments': comments,
        'form':form,
        'reply_form': reply_form,
        'can_like': can_like
        }
    return render(request, 'worst/detail.html', context)
@login_required
def reply_worst(request, film_id, comment_id):
    film = get_object_or_404(Film, id=film_id)
    comment= get_object_or_404(Comment, pk=comment_id)
    if request.method == 'POST':
        form = ReplyForm(request.POST)
        if form.is_valid():
            reply_valid= form.save(commit=False)
            reply_valid.user= request.user
            reply_valid.film = film
            reply_valid.reply = comment
            reply_valid.is_reply = True
            reply_valid.save()
            messages.success(request, 'your reply sent successfully!', 'success')
    return redirect('worstFilms:detail', film.id)


def delete_worst(request, id):
    film= get_object_or_404(Film, pk=id)
    film.delete()
    
    return redirect('worstFilms:home')

def like_film(request, film_id):
    film= get_object_or_404(Film, id=film_id)
    like= Like(post=film, user=request.user)
    like.save()
    messages.success(request, 'You liked successfully', 'success')
    return redirect('worstFilms:detail', film.id)





    