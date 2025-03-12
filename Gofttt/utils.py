from kavenegar import *


def send_otp_code(phone_number, code):
    try:
        api = KavenegarAPI('647A31627A356E726773715371397431756875734D703469516A6335314D716F4B796B687034566939676B3D')
        params = {
            'sender': '',
            'receptor': phone_number,
            'message': f'{code} کد تایید شما'
        }
        response = api.sms_send(params)
        print(response)
    except APIException as e:
        print(e)
    except HTTPException as e:
        print(e)