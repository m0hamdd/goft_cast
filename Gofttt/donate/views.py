from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings
from django.views import View
from django.contrib import messages
from .models import Donate
import requests

import json

# تنظیمات درگاه زرین پال
ZP_API_REQUEST = "https://sandbox.zarinpal.com/pg/rest/WebGate/PaymentRequest.json"
ZP_API_VERIFY = "https://sandbox.zarinpal.com/pg/rest/WebGate/PaymentVerification.json"
ZP_API_STARTPAY = "https://sandbox.zarinpal.com/pg/StartPay/"
description = "پرداخت کمک مالی به وب‌سایت"  # توضیحات تراکنش
CallbackURL = 'http://127.0.0.1:8000/donate/verify/'  # آدرس بازگشت پس از پرداخت

class DonateView(View):
    def get(self, request):
        return render(request, "donate/donate.html")
    
    def post(self, request):
        try: 
            amount = int(request.POST.get("amount"))
        except ValueError:
            messages.error(request, "مبلغ نامعتبر است!", 'danger')
            return redirect('donate:donate')

        if amount < 10000:
            messages.error(request, "حداقل مبلغ پرداخت باید ۱۰,۰۰۰ ریال باشد!", 'danger')
            return redirect('donate:donate')

        # ذخیره مقدار در سشن برای استفاده در تأیید پرداخت
        request.session["donation"] = {'amount': amount}

        data = {
            "MerchantID": settings.MERCHANT,
            "Amount": amount,
            "Description": description,
            "CallbackURL": CallbackURL,
        }

        data = json.dumps(data)
        headers = {'content-type': 'application/json', 'content-length': str(len(data))}

        try:
            response = requests.post(ZP_API_REQUEST, data=data, headers=headers, timeout=10)

            if response.status_code == 200:
                response = response.json()
                if response['Status'] == 100:
                    return redirect(f"{ZP_API_STARTPAY}{response['Authority']}")
                else:
                    messages.error(request, "مشکلی در اتصال به درگاه پرداخت پیش آمد.", 'danger')
                    return redirect("donate:donate")
                
            messages.error(request, "مشکلی در اتصال به درگاه پرداخت پیش آمد.", 'danger')
            return redirect("donate:donate")
        
        except requests.exceptions.Timeout:
            messages.error(request, "خطای اتصال: مدت‌زمان درخواست به پایان رسید.", 'danger')
            return redirect("donate:donate")
        except requests.exceptions.ConnectionError:
            messages.error(request, "مشکل در اتصال به اینترنت. لطفاً دوباره تلاش کنید.", 'danger')
            return redirect("donate:donate")

class DonateVerifyView(View):
    def get(self, request):
        user = request.user
        donation = request.session.get("donation")
        authority = request.GET.get('Authority')

        if not donation or not authority:
            messages.error(request, "تراکنش نامعتبر است!", 'danger')
            return redirect("donate:donate")

        data = {
            "MerchantID": settings.MERCHANT,
            "Amount": donation['amount'],
            "Authority": authority
        }

        data = json.dumps(data)
        headers = {'content-type': 'application/json', 'content-length': str(len(data))}
        response = requests.post(ZP_API_VERIFY, data=data, headers=headers)

        if response.status_code == 200:
            response = response.json()
            if response['Status'] == 100:
                # پرداخت موفق بود
                Donate.objects.create(user=user, amount=donation['amount'], currency="IRR", transaction_id=response['RefID'], status="success")
                messages.success(request, "پرداخت شما با موفقیت انجام شد!", 'success')
                del request.session['donation']
                return redirect("donate:donate")

        messages.error(request, "پرداخت ناموفق بود یا لغو شد.", 'danger')
        del request.session['donation']
        return redirect("donate:donate")
