from kavenegar import KavenegarAPI


class SMSUtil:
    def __init__(self, api_key):
        self.api = KavenegarAPI(api_key)

    def send_sms(self, sender, receptor, message):
        params = {'sender': sender, 'receptor': receptor, 'message': message}
        return self.api.sms_send(params)
