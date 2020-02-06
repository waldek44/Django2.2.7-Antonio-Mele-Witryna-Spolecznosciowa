from django.contrib.auth import authenticate, login
from django.http import HttpResponse
from django.shortcuts import render
from .forms import LoginForm
from django.contrib.auth.decorators import login_required


'''
1) pobiera formularz z forms.py i przypisuje go do zmiennej form,
    która tworzy nowy egzemplarz formularza logowania wraz z wysłanymi danymi i wyświetli go w szablonie account/login
    
2) is_valid() - waliduje czy wszystkie pola formularza są poprawne

3) metoda authenticate() - jeżeli pola formularza są poprawne to za pomocą metody authenticate uwierzytelniam 
   użytkownika na podstawie informacji przechowywanych w db metoda authenticate pobiera username i password a zwraca 
   obiekt user jeśli użytkownik zostanie uwierzytelniony lub None wraz z odpowiednim komunikatem
   
4) is_active - atrybut modelu User - sprawdza czy konto użytkownika jest aktywne

5) metoda login() - jeśli konto aktywne to loguje i rozpoczyna sesję (umieszcza użytkownika w sesji)
'''


# widok logowania użytkownika
def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'],
                                password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse('Uwierzytelnienie zakończyło się sukcesem.')
                else:
                    return HttpResponse('Konto jest zablokowane.')
            else:
                return HttpResponse('Nieprawidłowe dane uwierzytelniające.')
    else:
        form = LoginForm()
    return render(request, 'account/login.html', {'form': form})


@login_required
def dashboard(request):
    return render(request, 'account/dashboard.html', {'section': 'dashboard'})
