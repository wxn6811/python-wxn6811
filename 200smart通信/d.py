import snap7
from snap7.util import *

plc = snap7.client.Client()
plc.set_connection_type(3)  # (200专用)


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
    data = plc.read_area(snap7.types.Areas.DB, dbnum, 0, dblength)
    print(get_int(data, 0))
    print(get_bool(data, 2, 0))
    print(get_dword(data, 4))
    print(get_real(data, 8))
    print(get_bool(data, 0, 0))
    print(get_byte(data, 2))


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
    data = plc.read_area(snap7.types.Areas.MK, 0, num, 2)
    print(get_int(data, 0))  # 读取MW0值
    print(get_byte(data, 0))  # 读取MB0值
    print(get_dint(data, 0))  # 读取MD0值


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
    data = plc.read_area(snap7.types.Areas.MK, 0, byte, 4)
    # set_int(data, 0, value)
    set_dint(data, 0, value)
    plc.write_area(snap7.types.Areas.MK, 0, byte, data)


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


if __name__ == '__main__':
    plc_connect('192.168.1.10', 0, 1)
    dbRead(1, 4)
    dbWrite(1, 4)
    mRead1(20, 2)
    mRead2(100)
    mWrite1(20, 6, True)
    mWrite2(22, 100)
    qRead1(100, 5)
    qRead2(200)
    qWrite1(100, 5)
    iRead1(99, 7)
    iRead2(122)
    plc_disconnect()
# 功能：间接调用ui文件（将ui文件转化为py文件）
from PySide2.QtCore import Qt, QUrl, QRect, QSize
from PySide2.QtWebEngineWidgets import QWebEngineView
from PySide2.QtWidgets import QApplication, QMainWindow, QScrollArea

from ui import Ui_Form


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        # 使用ui文件导入定义界面类
        self.ui = Ui_Form()
        # 初始化界面
        self.ui.setupUi(self)


# 实例化
app = QApplication([])
# 对ui进行再次布局与设置
mainw = MainWindow()
mainw.show()
app.exec_()