import urllib.request
import json
import csv
from urllib import parse
import smtplib
import email
import time
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart


today_time = time.strftime('%Y-%m-%d', time.localtime(time.time()))
city="石狮"
def get_weather_data():

    citycode=parse.quote(city)
    key='c84a2ac3b3b44637a37734fab64de2e8'
    url = r'https://free-api.heweather.net/s6/weather/forecast?location='+citycode+'&key='+key
    print(url)
    #爬取
    res = urllib.request.urlopen(url)
    #json转为字典
    mp=json.loads(res.read().decode('UTF-8'))

    #得到查询城市的经纬度、时区信息
    result = mp['HeWeather6'][0]['basic']
    #未来三天天气信息
    weather=mp['HeWeather6'][0]['daily_forecast']
    names = ['城市','时间','天气状况','最高温','最低温','日出','日落']
    with open('today_weather.csv', 'w', newline='')as f:
        writer = csv.writer(f)
        writer.writerow(names)
        for data in weather:
            date = data['date']
            cond = data['cond_txt_d']
            max_tmp = data['tmp_max']
            min_tmp = data['tmp_min']
            sr = data['sr']
            ss = data['ss']
            writer.writerows([(city, date, cond, max_tmp, min_tmp, sr, ss)])
    send_email(weather)

def work(weather):
    res=[]
    for data in weather:
        condd = data['cond_txt_d']
        condn = data['cond_txt_n']
        max_tmp = data['tmp_max']
        min_tmp = data['tmp_min']
        sr = data['sr']
        ss = data['ss']
        tmp="白天："+condd+"       夜晚："+condn+"\n温度："+min_tmp+"℃~"+max_tmp+"℃\n日出："+sr+ "      日落："+ss
        res.append(tmp)
    ans=""
    ans="今天:\n"+res[0]+"\n"+"明天:\n"+res[1]+"\n"+"后天:\n"+res[2]+"\n"
    return ans


def send_email(weather):
    #文本
    text="老大,今天"+city+"的天气预报到账啦，请查收:\n" +  work(weather)
    # 设置邮箱域名
    HOST = 'smtp.qq.com'
    # 设置邮件标题
    SUBJECT = '天气预报'
    # 设置发件人邮箱
    FROM = '1076452761@qq.com'
    # 收件人
    TO = '1076452761@qq.com'

    message = MIMEMultipart('related')
    # --------------------发送文本--------------
    # 发送邮件正文到对方邮箱中
    message_html = MIMEText(text, 'plain', 'utf-8')
    message.attach(message_html)

    # --------------------添加文件--------------
    # 要确定当前目录有test.csv这个文件
    message_xlsx = MIMEText(open('today_weather.csv', 'rb').read(), 'base64', 'utf-8')
    # 设置文件在附件当中的名字
    message_xlsx['Content-Disposition'] = 'attachment;filename="today_weather.csv"'
    message.attach(message_xlsx)

    # 设置邮件发件人
    message['From'] = FROM
    # 设置邮件收件人
    message['To'] = TO
    # 设置邮件标题
    message['Subject'] = SUBJECT

    # 获取简单邮件传输协议的证书
    email_client = smtplib.SMTP_SSL()
    # 设置发件人邮箱的域名和端口，端口为465
    email_client.connect(HOST, '465')
    # ---------------------------邮箱授权码------------------------------
    result = email_client.login(FROM, 'jwmdhdptvzgbieed')
    print('登录结果', result)
    email_client.sendmail(from_addr=FROM, to_addrs=TO, msg=message.as_string())
    # 关闭邮件发送客户端
    email_client.close()

get_weather_data()