# coding:utf-8
import urllib
import urllib2
import json
import smtplib
from email.mime.text import MIMEText
import time
import sys
from log import Logger
import httplib
import datetime
import userConfig

mailto_list = ["akuma_cool@163.com"]
mail_host = "smtp.163.com"
mail_user = userConfig.setting["mail_user"]
mail_pass = userConfig.setting["mail_pass"]
mail_postfix = "XXX.com"
logger = Logger(logName='log.txt', logLevel="INFO", logger="getRegData.py").getlog()
json_str = ""


def timer(n):
    while True:
        logger.info("start");
        begin_date = "";
        reg_date = userConfig.setting["reg_date"]
        main(begin_date, reg_date)

        current_date = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        current_hour = int(time.strftime('%H', time.localtime(time.time())))
        begin_date=generate_begin_date(current_date,reg_date)
        time_range = [22, 23, 00, 01]
        if current_hour in time_range or (current_date >= begin_date):
            d = 15
        else:
            d = 3600
        time.sleep(d)


def generate_begin_date(current_date, reg_date):
    begin_date = ""
    for each_date in reg_date:
        if current_date<=each_date:
            begin_date = datetime.datetime.strptime(each_date, "%Y-%m-%d") - datetime.timedelta(days=14)
            return begin_date.strftime('%Y-%m-%d')

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


def main(desire_date, reg_date):
    try:
        global json_str
        json_str = ""
        posturl = "http://wx.zhicall.cn/dragon-wechat/yuyueGuahao/schedule/findExpertSchedules"
        data = userConfig.setting["doctors_list"]
        for data_single in data:

            hjson = json.loads(post(posturl, data_single))

            json_str = json.dumps(hjson, ensure_ascii=False, indent=2)

            for regSchedulelist in hjson["data"]["regScheduleVOList"]:
                for time in regSchedulelist["times"]:
                    if time["leftNum"] >0:
                        #and regSchedulelist["regDate"] in reg_date:
                        send_mail(mailto_list,
                              hjson["data"]["name"]+"-"+hjson["data"]["speciality"]+"-NewHua Hospital RegTime -" + regSchedulelist["regDate"] + time[
                                  "timeline"],
                              "Total" + str(time["totalNum"]) + "left:" + str(time["leftNum"]))
                    # print hjson["data"]["regScheduleVOList"][0]["time"]

    except httplib.IncompleteRead, e:
        logger.info(e.partial)
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
