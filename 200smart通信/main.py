import gettext
import re
import sys
import threading

import snap7
from snap7.util import *
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget,QStyleFactory,QHeaderView
from PyQt5.QtCore import QTimer,Qt
from PyQt5 import QtWidgets
from untitled import Ui_MainWindow
plc = snap7.client.Client()
plc.set_connection_type(3)  # (200专用)
class MainWindow(QMainWindow,QWidget,Ui_MainWindow):

    def __init__(self,parent=None,):
        super(MainWindow,self).__init__()
        # 使用ui文件导入定义界面类

        # 初始化界面
        self.setupUi(self)
        self.timexh()
    def timexh(self):
        t1 = QTimer(self)

        t1.timeout.connect(self.sjwrite)
        t1.start(1000)

    #向表格写数据
    def sjwrite(self):
        self.label.setText(str(11))



# 定义Plc连接
def plc_connect(ip, rack, slot):
    plc.connect(ip, rack, slot)
    if plc.get_connected():
        print("连接成功")


# PLC断开连接
def plc_disconnect():
    plc.disconnect()


def dbRead(dbnum, dblength):
    """
    DB块的读操作；如果是200smart系列的将dbnum设置为0
    :param dbnum:
    :param dblength:
    :return:
    """
    print('ks')
    data = plc.read_area(snap7.types.Areas.DB, dbnum, 100, dblength)
    print(data)
    w =[]
    ww=[]
    s=bytearray()
    '''for i in range(0,40):
        if data[i] != 0  :
            s.append(data[i])
        else:

            s.append(169)
        print(data[i])
        print(s)
        if s[i] == 169:
            a1 = str(s.decode('GBK'))
            w.append(a1[2:40])
            break'''



    a3='3000（初心） 3200\x00犛泊奇） 4000\x00犛泊奇） 2800（硬传奇） 3000（新时代） 3000（软阿诗玛） '
    a4 =b'(\x053200\x00\xa0\x000\x00\x00\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xea\x8a\xaa\xaa\xaa\xaa\xaa\xaa\xa8\xaa\x8a\xaa\xaa\xaa\xaa\xaa\xaa\xaa\xaa'
    www = '4000'
    #a5 = a4.decode('gbk')
    print(www.encode('utf-8'))



def dbWrite(dbnum, dblength):
    """
    DB块的写操作；如果是200smart系列的将dbnum设置为0
    :param dbnum: DB块的序号
    :param dblength:
    :return: 字节长度，根据需要设定
    """
    data = plc.read_area(snap7.types.Areas.DB, dbnum, 0, dblength)
    # set_int(data, 0, 20)
    # set_bool(data, 2, 0, False)
    # set_dword(data, 4, 1000)
    # set_real(data, 8, 11.3)
    # set_int(data, 12, 99)
    set_bool(data, 0, 0, False)  # 设置DBD0.DBX0.0为False
    # set_byte(data, 2, 2)
    # set_int(data, 4, 100)

    plc.write_area(snap7.types.Areas.DB, dbnum, 0, data)
    print('写入成功！！！')


def mRead1(num, bit):
    """
    M区的读操作--------bool
    :param num:
    :param bit:
    :return:
    """
    data = plc.read_area(snap7.types.Areas.MK, 0, num, 1)
    print(get_bool(data, 0, bit))


def mRead2(num):
    """
    M区的读操作--------int/word/dint/dword
    :param num:
    :return:
    """
    global cc
    data = plc.read_area(snap7.types.Areas.MK, 0, num, 2)
    #print(get_int(data, 0))  # 读取MW0值
    cc=get_int(data,0)
    #print(get_byte(data, 0))  # 读取MB0值
    #print(get_dint(data, 0))  # 读取MD0值
    mWrite2(2,cc)
    mWrite1(10,0,True)
def mWrite1(byte, bit, value):
    """
    M块的写操作---------bool
    :param byte:
    :param bit:
    :param value:
    :return:
    """
    data = plc.read_area(snap7.types.Areas.MK, 0, byte, 1)

    set_bool(data, 0, bit, value)

    plc.write_area(snap7.types.Areas.MK, 0, byte, data)


def mWrite2(byte, value):
    """
    M块的写操作---------int/word/dint/dword
    :param byte:
    :param value:
    :return:
    """

    data = plc.read_area(snap7.types.Areas.MK, 0, byte, 2)
    # set_int(data, 0, value)
    set_int(data, 0, value)

    plc.write_area(snap7.types.Areas.MK, 0, byte, data)
    #print(data)

def qRead1(byte, bit):
    """
    Q区的读操作-------------bool
    :param byte:
    :param bit:
    :return:
    """
    data = plc.read_area(snap7.types.Areas.PA, 0, byte, 1)
    print(get_bool(data, 0, bit))


def qRead2(byte):
    """
    Q区的读操作-------------byte/int/word/dint/dword
    :param byte:
    :return:
    """
    data = plc.read_area(snap7.types.Areas.PA, 0, byte, 2)
    # print(get_byte(data, 0))
    print(get_int(data, 0))
    # print(get_dint(data, 0))


def qWrite1(byte, bit, value):
    """
    Q区的写操作----------bool
    :param byte:
    :param bit:
    :param value:
    :return:
    """
    data = plc.read_area(snap7.types.Areas.PA, 0, byte, 1)  # read_area的SIZE参数，这里默认位一个字节
    set_bool(data, 0, bit, value)
    plc.write_area(snap7.types.Areas.PA, 0, byte, data)


def qWrite2(byte, value):
    """
    Q区的写操作----------int/word/dint/dword
    :param byte:
    :param value:
    :return:
    """
    data = plc.read_area(snap7.types.Areas.PA, 0, byte, 2)  # read_area的SIZE参数，int-2；dint-4
    set_int(data, 0, value)  # 读取QW0值
    # set_dint(data, 0, value)
    plc.write_area(snap7.types.Areas.PA, 0, byte, data)


def iRead1(byte, bit):
    """
    输入映象区的读操作-------bool
    :param byte:
    :param bit:
    :return:
    """
    data = plc.read_area(snap7.types.Areas.PE, 0, byte, 1)  # Size参数，这里我们定义为1个字节的长度
    print(get_bool(data, 0, bit))


def iRead2(byte):
    """
    输入映象区的读操作-------byte/int/word/dint/dword
    :param byte:
    :return:
    """
    data = plc.read_area(snap7.types.Areas.PE, 0, byte, 2)  # Size参数，这里我们定义为1个字节的长度
    # print(get_byte(data, 0))
    print(get_int(data, 0))
    # print(get_dint(data, 0))
def min():
    app = QApplication(sys.argv)
    # 对ui进行再次布局与设置
    mainw = MainWindow()
    mainw.show()
    sys.exit(app.exec_())
def tx():
    plc_connect('192.168.20.12', 0, 1)

    while 1:
        dbRead(1,40)

    plc_disconnect()
xiancheng = []
ck = threading.Thread(target=min)
xiancheng.append(ck)
xsj = threading.Thread(target=tx)
xsj.setDaemon(True)
xiancheng.append(xsj)

if __name__ == '__main__':
    for i in xiancheng:
        i.start()
