'''
用740641978@qq.com发送电子邮件到我的libin11170225@gmail.com邮箱中去
参考教程: https://blog.csdn.net/MATLAB_matlab/article/details/106240424

'''
# from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

#发送方邮箱信息
msg_from = '740641978@qq.com'
passwd = 'lndghjmddadobahi'

#接收方邮箱信息
# to = ['libin11170225@gmail.com','li@g.ecc.u-tokyo.ac.jp']
to = 'libin11170225@gmail.com'

#邮件内容
# msg = MIMEMultipart() #MIMEMultipart类可以放各种各样的格式的内容
# cont = "弃我去者，昨日之日不可留; 乱我心者，今日之日多烦忧。"
# msg.attach(MIMEText(cont,'plain','utf-8')) #MIMEText三个参数，文本内容，文本格式和编码格式

cont = "弃我去者，昨日之日不可留; 乱我心者，今日之日多烦忧。"
msg = MIMEText(cont,'plain','utf-8')

#邮件主题
msg['Subject'] = '宣州谢眺楼饯别校书叔云_李白'

#from和to信息
msg['From'] = msg_from
msg['to'] = to


try:
    #通过SSL发送，需要定义服务器地址和端口
    s = smtplib.SMTP_SSL('smtp.qq.com', 465)
    #登陆邮箱
    s.login(msg_from, passwd)
    #开始发送
    s.sendmail(msg_from,to,msg.as_string())
    print('邮件发送成功')
except smtplib.SMTPException as e:
    print(' Error: 无法发送邮件.Case:%s'%e)
