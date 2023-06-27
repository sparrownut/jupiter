# 邮箱账号密码

CDLA = False  # companyDoingLockerActived
username = '2928109164@qq.com'
password = 'xkjwcmoppfxqdgea'
AuthedUserList = []



def AddToAuthedUserList(user):
    AuthedUserList.append(user)


def IsInAuthedUserList(user):
    if user in AuthedUserList:
        return True
    else:
        return False


def RemoveWithAuthedUserList(user):
    AuthedUserList.remove(user)
