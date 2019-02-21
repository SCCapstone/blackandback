#from django.contrib.auth import login, authenticate
#from django.shortcuts import render, redirect
#from forms import SignUpForm

#def signup(request):
#    if request.method == 'POST':
#        form = SignUpForm(request.POST)
#        if form.is_valid():
#            form.save()
#            username = form.cleaned_data.get('username')
#            raw_password = form.cleaned_data.get('password')
#            user = authenticate(username=username, password=raw_password)
#            login(request, user)
#            return redirect('home')
#    else:
#        form = SignUpForm()
#    return render(request, 'signup.html', {'form': form})
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic

class SignUp(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'

