from django.shortcuts import render
from finances.models import Transaction

# Create your views here.

def dashboard_view(request):
    return render(request, 'dashboard.html')

def transaction_view(request):
    transactions = Transaction.objects.all()
    
    return render(request, 'transaction.html', {'transactions': transactions})