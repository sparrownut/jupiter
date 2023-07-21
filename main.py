import imaplib
import re
import threading
import time
import traceback
import eventlet
from email import message_from_bytes

from Global import username, password
from do.do import do, mark_all_as_read

eventlet.monkey_patch() #添加超时控制

if __name__ == '__main__':

    while True:
        try:
            # 连接到邮箱服务器
            imap = imaplib.IMAP4_SSL('imap.qq.com')
            imap.login(username, password)
            print("* login done")
            # 选择收件箱
            imap.select('INBOX')
            print("* select done")
            # 循环监听新邮件
            while True:
                print("* check")
                try:

                    # 搜索未读邮件
                    status, messages = imap.search('UNSEEN')

                    # 将消息ID列表转换为逗号分隔的字符串
                    messages = messages[0].split(b' ')
                    sender = ""
                    try:
                        with eventlet.Timeout(5, False):
                            # 循环处理每个未读邮件
                            # print(messages)
                            if messages[0] != b'':
                                for msg_id in messages:
                                    # 获取邮件内容
                                    _, msg_data = imap.fetch(msg_id, '(RFC822)')
                                    msg = message_from_bytes(msg_data[0][1])
                                    for it in str(msg_data[0]).split("\\r"):
                                        # print(it)
                                        if "From" in it:
                                            # print(it)
                                            s = re.findall("<(.*?)>", it)
                                            if len(s) > 0:
                                                # print(s[0])
                                                sender = s[0]

                                    # 获取邮件正文
                                    body = ''
                                    if msg.is_multipart():
                                        for part in msg.walk():
                                            content_type = part.get_content_type()
                                            if content_type == 'text/plain' or content_type == 'text/html':
                                                body = part.get_payload(decode=True).decode(encoding="gb18030")
                                                break
                                    else:
                                        body = msg.get_payload(decode=True).decode(encoding="gb18030")

                                    # 调用do函数并传递发件人和邮件内容参数
                                    threading.Thread(target=do, args=(sender, body,)).start()
                    except Exception as e:
                        mark_all_as_read(username, password, "imap.qq.com")
                        traceback.print_exception(e)
                        time.sleep(5)
                except Exception as e:
                    mark_all_as_read(username, password, "imap.qq.com")
                    if "FETCH" not in str(e):
                        traceback.print_exception(e)

                time.sleep(5)
                # 等待新邮件
                # imap.idle()

            # 关闭连接
            imap.close()
            imap.logout()
        except Exception as e:
            traceback.print_exception(e)
