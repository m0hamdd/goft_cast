from django.shortcuts import render
from django.views import View

# Payment View.
class PaymentView(View):
    def get(self, request):
        return render(request, 'payment/price.html')
    
    def post(self, request):
        return render(request, 'payment/price.html')
