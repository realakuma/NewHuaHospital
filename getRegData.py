# coding:utf-8
import urllib
import urllib2
import json
import smtplib
from email.mime.text import MIMEText
import time
import sys
from log import Logger;

mailto_list = ["realakuma@163.com"]
mail_host = "smtp.163.com"
mail_user = "realakuma@163.com"
mail_pass = "8B9zqr@123"
mail_postfix = "XXX.com"
logger = Logger(logName='log.txt', logLevel="INFO", logger="getRegData.py").getlog()
json_str = ""


def timer(n):
    while True:
        logger.info("start");

        main()
        current_hour = int(time.strftime('%H', time.localtime(time.time())))
        time_range = [22,23,00, 01]
        if current_hour in time_range:
            d = 15
        else:
            d = 3600
        time.sleep(d)


def send_mail(to_list, sub, content):
    me = "hello" + "<" + mail_user + "@" + mail_postfix + ">"
    msg = MIMEText(content, _subtype='plain', _charset='UTF-8')
    msg['Subject'] = sub
    msg['From'] = me
    msg['To'] = ";".join(to_list)
    try:
        server = smtplib.SMTP()
        server.connect(mail_host)
        server.login(mail_user, mail_pass)
        server.sendmail(me, to_list, msg.as_string())
        server.close()
        return True
    except Exception, e:
        print str(e)
        return False


def post(url, data):
    req = urllib2.Request(url)
    data = urllib.urlencode(data)
    # enable cookie
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor())
    response = opener.open(req, data)
    return response.read()


def main():
    try:
        global json_str
        posturl = "http://wx.zhicall.cn/dragon-wechat/yuyueGuahao/schedule/findExpertSchedules"
        data = {'hospitalId': '10012', 'deptId': '12305', 'expertId': '12146'}

        hjson = json.loads(post(posturl, data))

        json_str = json.dumps(hjson, ensure_ascii=False, indent=2)

        for time in hjson["data"]["regScheduleVOList"][0]["times"]:
            if time["leftNum"] > 0:
                send_mail(mailto_list,
                          "NewHua Hospital RegTime -" + hjson["data"]["regScheduleVOList"][0]["regDate"] + time[
                              "timeline"],
                          "Total" + str(time["totalNum"]) + "left:" + str(time["leftNum"]))
                # print hjson["data"]["regScheduleVOList"][0]["time"]
    except:
        # get detail from sys.exc_info() method
        error_type, error_value, trace_back = sys.exc_info()
        logger.info(error_value)
        logger.info(json_str)
        send_mail(mailto_list,
                  "NewHua Hospital Reg Error",
                  json_str + str(error_value))


if __name__ == '__main__':
    timer(10);
