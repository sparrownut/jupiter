# 邮箱账号密码

CDLA = False  # companyDoingLockerActived
username = '2155185732@qq.com'
password = 'ryezqcfcorhheaef'
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
