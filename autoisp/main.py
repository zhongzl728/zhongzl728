# -----ISP自动打卡 by 钟子龙-----2022/1/24#
import time
import smtplib
from email.mime.text import MIMEText
from selenium.webdriver.chrome.options import Options
from selenium import webdriver

# 随机等待
# sleep(random.randint(6,10))
# 模拟浏览器打开网站,并获取验证码
# 打开浏览器
chrome_options = Options()
# 设置chrome浏览器无界面模式
chrome_options.add_argument('--headless')
browser = webdriver.Chrome(chrome_options=chrome_options)
browser.get('https://xsswzx.cdu.edu.cn/ispstu2/com_user/weblogin.asp')

# 定位元素获取验证码并除去空格
qgg = browser.find_element_by_xpath("/html/body/div[1]/div/div/font/div/div/div[2]/form/div[3]")
a = qgg.text

# 找到学号和密码输入框的xpath,并在对应的位置送入账号密码
uid = "202120323119"
pwd = "Zzl19980728.."
browser.find_element_by_xpath('/html/body/div[1]/div/div/font/div/div/div[2]/form/div[1]/input').send_keys(uid)
browser.find_element_by_xpath('/html/body/div[1]/div/div/font/div/div/div[2]/form/div[2]/input').send_keys(pwd)
browser.find_element_by_xpath('/html/body/div[1]/div/div/font/div/div/div[2]/form/div[3]/input').send_keys(a.lstrip())
time.sleep(1)

# 登录
browser.find_element_by_xpath('/html/body/div[1]/div/div/font/div/div/div[2]/form/font/font/button').click()
time.sleep(1)

# 跳转疫情信息登记网页
form = "https://xsswzx.cdu.edu.cn/ispstu2/com_user/project.asp?id=74e945c0269400fc92ec8714dd4240646238cad22e96"
browser.get(form)
time.sleep(1)

# 【一键登记：无变化】
browser.find_element_by_xpath('//input[@value="【一键登记：无变化】"]').click()  # 点击某按钮后显示弹窗
time.sleep(3)  # 这里要一定做等待操作，因为等弹窗弹出后才能下一步操作，所有弹窗后操作均同此
# 获取弹窗内容
alert = browser.switch_to.alert  # 创建弹窗对象
value = alert.text
# print("弹窗的内容为：",value)   ## 可对该内容做断言处理。
# 退出浏览器
browser.quit()

# 发送邮件
mailserver = "smtp.qq.com"  # 邮箱服务器地址
username_send = '1107812770@qq.com'  # 邮箱用户名
password = 'ggrpkecfxxoxhegb'  # 邮箱密码：需要使用授权码
username_recv = '923172051@qq.com'  # 收件人，多个收件人用逗号隔开
mail = MIMEText(value)
mail['Subject'] = 'ISP每日签到情况'
mail['From'] = username_send  # 发件人
mail['To'] = username_recv  # 收件人；[]里的三个是固定写法，别问为什么，我只是代码的搬运工
smtp = smtplib.SMTP_SSL('smtp.qq.com', port=465)  # QQ邮箱的服务器和端口号
smtp.login(username_send, password)  # 登录邮箱
smtp.sendmail(username_send, username_recv, mail.as_string())
# 参数分别是发送者，接收者，第三个是把上面的发送邮件的内容变成字符串
smtp.quit()  # 发送完毕后退出smtp
# print ('success')
