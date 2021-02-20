from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
#tworzy gotowy form z django
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth import login, logout, authenticate
from .forms import ToDoForm
from .models import ToDo
from .forms import CustomUserCreationForm
from django.core.paginator import Paginator





#LISTA 3 OGLOSZEN NA STRONIE GLOWNEJ
def main(request):
    ToDos=ToDo.objects.filter(Akceptacja='TAK').order_by('-created')[:3]
    pagecount = ToDo.objects.filter(Akceptacja='TAK')
    pagecountfound = ToDo.objects.filter(Kategoria='ZNALEZIONO')
    pagecountsearch = ToDo.objects.filter(Kategoria='SZUKAM')
    pagecountend = ToDo.objects.filter(Kategoria='ZAKOŃCZONE')
    pagecountothers = ToDo.objects.filter(Kategoria='INNE')
    if request.user.is_authenticated:
        usercount = ToDo.objects.filter(user=request.user)
        usercountfound = ToDo.objects.filter(user=request.user).filter(Kategoria='ZNALEZIONO')
        usercountsearch = ToDo.objects.filter(user=request.user).filter(Kategoria='SZUKAM')
        usercountend = ToDo.objects.filter(user=request.user).filter(Kategoria='ZAKOŃCZONE')
        usercountothers = ToDo.objects.filter(user=request.user).filter(Kategoria='INNE')
        return render(request,'index/index.html', {'ToDos':ToDos,'pagecount':pagecount, 'pagecountfound':pagecountfound, 'pagecountsearch':pagecountsearch,
        'pagecountend':pagecountend, 'pagecountothers':pagecountothers, 'usercount':usercount,'usercountfound':usercountfound, 'usercountsearch':usercountsearch,
        'usercountend':usercountend, 'usercountothers':usercountothers,})
    return render(request,'index/index.html', {'ToDos':ToDos,'pagecount':pagecount, 'pagecountfound':pagecountfound, 'pagecountsearch':pagecountsearch,
    'pagecountend':pagecountend, 'pagecountothers':pagecountothers})

#REJESTRACJA UZYTKOWNIKA
def signupuser(request):
    if request.method == 'GET':
        return render(request,'index/signupuser.html',{'form':CustomUserCreationForm()})
    else:
        if request.POST['password1'] == request.POST['password2']:
            try:
            #Tworzenie uzytkownika
                user = User.objects.create_user(request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                return redirect ('index')
            except IntegrityError:
                return render(request,'index/signupuser.html',{'form':UserCreationForm(), 'error':'Podany login jest już zajęty'})
        else:
            #Powiedz uzytkownikowi, ze hasla nie sa te same
            return render(request,'index/signupuser.html',{'form':UserCreationForm(), 'error':'Podane hasla nie są takie same'})



#LISTA OGLOSZEN
def currents(request):
    TODOS = ToDo.objects.filter(Akceptacja='TAK').order_by('-created')
    search_query = request.GET.get('search', '')
    if search_query:
        TODOS = ToDo.objects.filter(Miasto__icontains=search_query)
    else:
        TODOS = ToDo.objects.all()
    paginator = Paginator(TODOS, 3)
    page = request.GET.get('page')
    TODOS = paginator.get_page(page)
    return render(request,'index/currents.html', {'TODOS':TODOS})

#Lista ogloszen zakonczonych
def currentsdone(request):
    TODOS = ToDo.objects.filter(Kategoria='ZAKOŃCZONE', Akceptacja='TAK').order_by('-created')
    paginator = Paginator(TODOS, 3)
    page = request.GET.get('page')
    TODOS = paginator.get_page(page)
    return render(request,'index/currentsdone.html', {'TODOS':TODOS})

#Lista ogloszen innych
def currentsother(request):
    TODOS = ToDo.objects.filter(Kategoria='INNE', Akceptacja='TAK').order_by('-created')
    paginator = Paginator(TODOS, 3)
    page = request.GET.get('page')
    TODOS = paginator.get_page(page)
    return render(request,'index/currentsother.html', {'TODOS':TODOS})

#LISTA OGLOSZEN ZNALEZIONE
def currentsfound(request):
    TODOS = ToDo.objects.filter(Kategoria='ZNALEZIONO', Akceptacja='TAK').order_by('-created')
    paginator = Paginator(TODOS, 3)
    page = request.GET.get('page')
    TODOS = paginator.get_page(page)
    return render(request,'index/currentsfound.html', {'TODOS':TODOS})

#Lista ogloszen szukajacych
def currentslost(request):
    TODOS = ToDo.objects.filter(Kategoria='SZUKAM', Akceptacja='TAK').order_by('-created')
    paginator = Paginator(TODOS, 3)
    page = request.GET.get('page')
    TODOS = paginator.get_page(page)
    return render(request,'index/currentslost.html', {'TODOS':TODOS})

#Lista ogloszen uzytkownika
def UserTodo(request):
    if request.user.is_authenticated:
        TODOS=ToDo.objects.all().order_by('-created')
        usercount = ToDo.objects.filter(user=request.user)
        usercountfound = ToDo.objects.filter(user=request.user).filter(Kategoria='ZNALEZIONO')
        usercountsearch = ToDo.objects.filter(user=request.user).filter(Kategoria='SZUKAM')
        usercountend = ToDo.objects.filter(user=request.user).filter(Kategoria='ZAKOŃCZONE')
        usercountothers = ToDo.objects.filter(user=request.user).filter(Kategoria='INNE')
        return render(request,'index/usertodo.html', {'TODOS':TODOS, 'usercount':usercount,'usercountfound':usercountfound, 'usercountsearch':usercountsearch,
        'usercountend':usercountend, 'usercountothers':usercountothers,})
    else:
        return render(request,'index/usertodo.html')


#WYLOGOWANIE UZYTKOWNIKA
def logoutuser(request):
    if request.method == 'POST':
        logout(request)
        return redirect ('index')

#LOGOWANIE UZYTKOWNIKA
def loginuser(request):
    if request.method == 'GET':
        return render(request,'index/login.html',{'form':AuthenticationForm()})
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request,'index/login.html',{'form':AuthenticationForm(), 'error':'Podano błędne dane'})
        else:
            login(request, user)
            return redirect ('index')

#EDYTOWANIE POSTOW
def detail(request, ToDo_id):
    TODO = get_object_or_404(ToDo, pk=ToDo_id)
    if request.method == 'GET':
        form = ToDoForm(instance=TODO)
        return render(request, 'index/detail.html', {'ToDo':TODO, 'form':form})
    else:
        try:
            form = ToDoForm(request.POST, request.FILES, instance=TODO)
            newtodo = form.save(commit=False)
            newtodo.user = request.user
            newtodo.save()
            return redirect('currents')
        except ValueError:
            return render(request, 'index/detail.html', {'ToDo':TODO, 'form':form, 'error':'Niepoprawne dane'})

#TWORZENIE OGLOSZENIA
def createtodo(request):
    if request.method == 'GET':
        return render(request, 'index/usercreate.html', {'form':ToDoForm()})
    else:
        try:
            form = ToDoForm(request.POST, request.FILES)
            newtodo = form.save(commit=False)
            newtodo.user = request.user
            newtodo.save()
            return redirect('UserTodo')
        except ValueError:
            return render(request, 'index/usercreate.html', {'form':ToDoForm(), 'error':'Niepoprawne dane'})


#USUWANIE OGŁOSZENIA
def deletetodo(request, ToDo_id):
    TODO = get_object_or_404(ToDo, pk=ToDo_id)
    if request.method == 'POST':
        TODO.delete()
        return redirect('currents')
