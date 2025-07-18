from ronglian_sms_sdk import SmsSDK


def send_code(mobile, code):
    accId = '8a216da86c8a1a54016c9907b3e30abe'
    accToken = '0efb48b013d645edabe3ea3497c42d3b'
    appId = '8a216da86c8a1a54016c9907b4380ac5'
    sdk = SmsSDK(accId, accToken, appId)

    datas = (code, 5)
    res = sdk.sendMessage("1", mobile, datas)
    print(res)


if __name__ == '__main__':
    send_code('15049212123', '8888')
