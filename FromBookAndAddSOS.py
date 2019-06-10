#   实现需求：从通讯录添加手机号码，若存在旧的SOS号码，先删除再添加，若通讯录中没有号码，需先新建。

import uiautomator2 as u2
from time import sleep
import time
import random

distinct_devices =  "H6ZPKR45DAB64DJB"
device = u2.connect(distinct_devices)
package = "com.njzx.shbsetting"
path = "E:\\pycharm\\run\\UiAutomator2\\F5\\SOS\\FromBookPic\\"
path_result = "E:\\pycharm\\run\\UiAutomator2\\F5\\SOS\\result\\"
now_time = time.strftime("%Y-%m-%d-%H-%M-%S")

#   启动SOS应用
def start_app():
    device.screen_on()
    device.app_start(package)
    sleep(1)

#  从通讯录添加号码并保存
def addTel_submit():
    device(resourceId="com.njzx.shbsetting:id/layout_sos").click()
    sleep(1)
    #   判断是否存在旧的SOS号码，若存在先删除再添加
    count_elments = device(resourceId = "zte.shb.sossetting:id/number").count
    print("已有的旧的SOS号码个数为："+ str(count_elments) + "。\n稍后执行删除动作！")
    if count_elments != 0:
        for i in range(0,count_elments):
            device(resourceId="zte.shb.sossetting:id/delete").click()
            device(resourceId="zte.shb.sossetting:id/btn_set").click()
            print("删除成功！")
        getFromContactors()
        device.press("home")
    else:
        getFromContactors()
        device.press("home")


#   从通讯录选择号码：
list_name = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n"]
list_tel = ["1234","143536","5656565435","2344567","234455756","686778967","144354657",
            "562789","90909090","6725111","6764535"]
def getFromContactors():
    device(resourceId = "zte.shb.sossetting:id/add_from_contactors").click()
    sleep(1)
    #   判断有没有联系人，如果没有，返回到联系人应用先新建联系人 package = "com.android.dialer"，然后添加
    none_elements = device(text = "您还没有添加任何联系人")
    count_oldTel = device(resourceId = "com.android.contacts:id/cliv_name_textview").count
    dialer_package = "com.android.dialer"
    #   没有可选号码，需要新建5个
    if none_elements.exists:
        device.app_start(dialer_package)
        device(text = "通讯录").click()#   确保在联系人界面
        sleep(1)
        #   判断列表中：姓名列表的长度和号码列表的长度和最多能够添加多少个SOS号码（也就是5）的大小，然后新建联系人
        if len(list_name) >= 5 and len(list_tel)>=5 :
            for i in range(0,5):
                print("直接选取5个号码")
                addNameAddTel()
        elif len(list_name) < 5 and len(list_tel) <= len(list_name):
            for i in range(0,len(list_tel)):    #   len(list_tel)
                print("以list_tel的长度作为全部号码")
                addNameAddTel()
        elif len(list_tel) < 5 and len(list_name) <= len(list_tel):
            for i in range(0,len(list_name)):    #   len(list_name)
                print("以list_name的长度作为全部号码")
                addNameAddTel()
        elif len(list_name) >5 and len(list_tel)<5:
            for i in range(0,len(list_tel)):    #   len(list_tel)
                print("以list_tel的长度作全部号码")
                addNameAddTel()
        elif len(list_tel)>5 and len(list_name)<5:
            for i in range(0,len(list_name)):    #   len(list_name)
                print("以list_name的长度作为全部号码")
                addNameAddTel()
        #   重新打开SOS，选择已经新建好的号码：
        ContinueOpenSOSAndSelectTel()
    #   若存在5个联系人，直接添加为SOS：
    elif count_oldTel  == 5:
        selectTelFromContect()
        sleep(3)
        image = device.screenshot()
        image.save(path_result + now_time + '.jpg')
    #   若存在小于5个联系人，但不为0，删除全部再新建至5个：
    else:
        print("目前已有的联系人个数：" + str(count_oldTel) + "，稍后执行删除全部新增5个号码操作！")
        device.app_start(dialer_package)
        device(text = "通讯录").click()
        sleep(1)
        device(resourceId="com.android.dialer:id/zte_edit_contact").click()
        device(text = "删除联系人").click()
        device(text = "全 选").click()
        device(text = "删除").click()
        device(text = "确定").click()
        if len(list_name) >= 5 and len(list_tel)>=5 :
            for i in range(0,5):
                print("直接选取5个号码")
                addNameAddTel()
        elif len(list_name) < 5 and len(list_tel) <= len(list_name):
            for i in range(0,len(list_tel)):    #   len(list_tel)
                print("以list_tel的长度作为全部号码")
                addNameAddTel()
        elif len(list_tel) < 5 and len(list_name) <= len(list_tel):
            for i in range(0,len(list_name)):    #   len(list_name)
                print("以list_name的长度作为全部号码")
                addNameAddTel()
        elif len(list_name) >5 and len(list_tel)<5:
            for i in range(0,len(list_tel)):    #   len(list_tel)
                print("以list_tel的长度作全部号码")
                addNameAddTel()
        elif len(list_tel)>5 and len(list_name)<5:
            for i in range(0,len(list_name)):    #   len(list_name)
                print("以list_name的长度作为全部号码")
                addNameAddTel()
        #   重新打开SOS，选择已经新建好的号码：
        ContinueOpenSOSAndSelectTel()


#   向联系人中新建号码
def addNameAddTel():
    device(resourceId="com.android.dialer:id/zte_edit_contact").click()
    device(text="添加联系人").click()
    sleep(1)
    # 随机选取一个姓名
    select_name = random.choice(list_name)
    list_name.remove(select_name)  # 姓名不重复
    print("本次随机选择的姓名是：" + select_name + "。\n稍后删除" + select_name + "，打印出剩余姓名！")
    print(list_name)
    device(text="姓名").click()
    device(text="姓名").send_keys(select_name)
    # 随机选取一个号码
    select_tel = random.choice(list_tel)
    list_tel.remove(select_tel)  # 号码不重复
    print("本次随机选择的号码是：" + select_tel + "。\n稍后删除" + select_tel + ",打印出剩余号码！")
    print(list_tel)
    device(text="电话").click()
    device(text="电话").send_keys(select_tel)
    device(text="完成").click()
    sleep(1)
    device.press("back")
    sleep(1)


#   重新打开SOS应用，选择已经新建好的号码：
def ContinueOpenSOSAndSelectTel():
    start_app()
    device(resourceId="com.njzx.shbsetting:id/layout_sos").click()
    sleep(1)
    device(resourceId="zte.shb.sossetting:id/add_from_contactors").click()
    sleep(1)
    image = device.screenshot()
    image.save(path + now_time + '.jpg')
    sleep(1)
    #   从联系人中随机选择SOS号码并添加
    selectTelFromContect()
    sleep(3)
    image = device.screenshot()
    image.save(path_result + now_time + '.jpg')


#   从联系人中随机选择SOS号码并添加
sostel1 = device(resourceId = "com.android.contacts:id/cliv_name_textview",instance=0)
sostel2 = device(resourceId = "com.android.contacts:id/cliv_name_textview",instance=1)
sostel3 = device(resourceId = "com.android.contacts:id/cliv_name_textview",instance=2)
sostel4 = device(resourceId = "com.android.contacts:id/cliv_name_textview",instance=3)
sostel5 = device(resourceId = "com.android.contacts:id/cliv_name_textview",instance=4)
list_sosTel = [sostel1,sostel2,sostel3,sostel4,sostel5]
def selectTelFromContect():
    count_sosTel = device(resourceId = "com.android.contacts:id/cliv_name_textview").count
    print("可选择作为SOS的号码个数：" + str(count_sosTel))
    for i in range(0,count_sosTel):
        selectFromsosTel = random.choice(list_sosTel)
        selectFromsosTel.click()
        list_sosTel.remove(selectFromsosTel)
        print(list_sosTel)
        device(text = "添加").click()
        device(text = "从通讯录中添加").click()



if __name__ == '__main__':
    start_app()
    addTel_submit()