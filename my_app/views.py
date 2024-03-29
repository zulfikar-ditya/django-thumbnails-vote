from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.core.paginator import Paginator

from .forms import RegisterForm, PoolForm
from .models import Pool, Categories


def index(request):
    pool = Pool.objects.filter(status=True).order_by('-date_add')
    paginator = Paginator(pool, 15)
    pageNum = request.GET.get('page')
    pageObj = paginator.get_page(pageNum)
    return render(request, 'home/index.html', {
        'pool': pageObj,
        }
    )


def detail(request, pool_id):
    if request.user.is_authenticated:
        try:
            getPool = Pool.objects.get(pk=pool_id)
            if getPool.status is True:
                img1 = getPool.vote_img1.all()
                img2 = getPool.vote_img1.all()
                user_vote_status_img1 = None
                user_vote_status_img2 = None
                if getPool.vote_img1_count == 0 and getPool.vote_img2_count == 0:
                    user_vote_status_img1 = None
                    user_vote_status_img2 = None
                else:
                    for i in img1:
                        if request.user != i:
                            user_vote_status_img1 = None
                            pass
                        else:
                            user_vote_status_img1 = 'img1'
                            break
                    for i in img2:
                        if request.user != i:
                            user_vote_status_img2 = None
                            pass
                        else:
                            user_vote_status_img2 = 'img2'
                            break
                if request.method == 'POST':
                    try:
                        img = request.POST['img1']
                        getPool.vote_img1.add(request.user)
                    except (KeyError, Pool.DoesNotExist):
                        img = request.POST['img2']
                        getPool.vote_img2.add(request.user)

                    return HttpResponseRedirect(f'../../detail/{getPool.id}/')

                return render(request, 'home/detail.html', {
                    'pool': getPool,
                    'user_vote_status_img1' : user_vote_status_img1,
                    'user_vote_status_img2' : user_vote_status_img2,
                })
            else:
                return HttpResponseRedirect(reverse('home:nout_found'))
        except (KeyError, Pool.DoesNotExist):
            return HttpResponseRedirect(reverse('home:not_found'))
    else:
        return HttpResponseRedirect(reverse('home:login_status'))


def add_thumbnails(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form = PoolForm(request.POST, request.FILES)
            if form.is_valid():
                instance = form.save(commit=False)
                instance.user = request.user
                instance.save()
                return HttpResponseRedirect(reverse('home:index'))
        else:
            form = PoolForm()
        return render(request, 'home/add_thumnails.html', {
            'form' : form,
        }
        )
    else:
        return HttpResponseRedirect(reverse('home:login_status'))


def edit_thumb(request, pool_id):
    if request.user.is_authenticated:
        try:
            getPool = Pool.objects.get(pk=pool_id)
            if getPool.status is True and getPool.user == request.user:
                categories = Categories.objects.all()

                if request.method == 'POST':
                    get_title = request.POST['title']
                    get_categori = request.POST['categories']

                    # check the image will update or not
                    try:
                        # try tu update image 1
                        getPool.img_1 = request.FILES['img_1']
                    except:
                        # if the img is blnk
                        pass

                    try:
                        getPool.img_2 = request.FILES['img_2']
                    except:
                        pass
                    # update
                    getPool.title = get_title
                    getPool.categories = Categories.objects.get(pk=int(get_categori))
                    getPool.save()

                    return HttpResponseRedirect(reverse('home:my_thumbnails'))

                return render(request, 'home/edit.html', {
                    'pool': getPool,
                    'categories': categories,
                })
            else:
                return HttpResponseRedirect(reverse('home:not_found'))
        except (KeyError, Pool.DoesNotExist):
            return HttpResponseRedirect(reverse('home:not_found'))
    else:
        return HttpResponseRedirect(reverse('home:login_status'))


def my_thumbnails(request):
    if request.user.is_authenticated:
        my_thum = Pool.objects.filter(user=request.user).order_by('-date_add')
        paginator = Paginator(my_thum, 15)
        pageNum = request.GET.get('page')
        pageObj = paginator.get_page(pageNum)
        if len(my_thum) == 0:
            message = "You don't have a post yet"
        else:
            message = None
        return render(request, 'home/my.html', {
            'pool': pageObj,
            'message' : message,
        })
    else:
        return HttpResponseRedirect(reverse('home:login_status'))


def delete(request, pool_id):
    if request.user.is_authenticated:
        try:
            getPool = Pool.objects.get(pk=pool_id)
            if getPool.status == True and getPool.user == request.user:
                if request.method == 'POST':
                    getPool.deactive()
                    getPool.save()
                    return HttpResponseRedirect(reverse('home:my_thumbnails'))
                return render(request, 'home/delete_confirm.html', {
                    'getPool' : getPool,
                })
            else:
                return HttpResponseRedirect(reverse('home:not_found'))
        except (KeyError, Pool.DoesNotExist):
            return HttpResponseRedirect(reverse('home:not_found'))
    else:
        return HttpResponseRedirect(reverse('home:login_status'))


def register(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('home:login_status'))
    else:
        if request.method == 'POST':
            form = RegisterForm(request.POST)   
            if form.is_valid():
                form.save()
                return HttpResponseRedirect('../login/')
        else:
            form = RegisterForm()
        return render(request, 'registration/register.html', {'form': form,})


def login_status(request):
    if request.user.is_authenticated:
        return render(request, 'logged_in.html')
    
    else:
        return HttpResponseRedirect('../login/')


def not_found(request):
    return render(request, 'home/404.html')