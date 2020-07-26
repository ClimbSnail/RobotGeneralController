import configurator as cfg
import tkinter as tk
import tkutils as tku
import massagehead as mh
import WindowElement as we
from tkinter import messagebox

VERSION = "Ver1.0"

class Engine(object):
    """
    引擎
    """
    def __init__(self, root):
        """
        引擎初始化
        :param root:窗体控件
        """
        self.root = root
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.v_lang = []    # 储存语言项
        self.word_map = {}  # 储存指定语言所对应字段下的文字
        self.start()
        self.OnThreadMessage(mh.M_ENGINE, mh.M_SYSINFO, mh.A_INFO_PRINT, "System init succ.\n")

    def start(self ):
        """
        使用grid管理位置
        :return:
        """
        # 初始化系统配置信息
        self.m_sysinfo_file = cfg.SystemConfig("./init.cfg")
        self.sys_info = self.m_sysinfo_file.m_sysinfo
        # 模型文件控制对象
        self.m_model_file = cfg.ModelFile()
        # 动作组文件控制对象
        self.m_action_file = cfg.ActionFile()
        # 初始化语言控制类
        self.m_lang = cfg.Language(self.sys_info["system_init"]["language"]) # first
        self.v_lang, self.word_map = self.m_lang.api(mh.A_UPDATALANG) # 先执行一遍语言更新

        # 初始化菜单栏
        self.m_menu = we.CtrlMenu(self.root, self)

        # 初始化舵机控件管理器
        self.madel_grid_frame = tk.Frame(self.root, width=800, height=450, bg="white")
        #self.madel_grid_frame.grid(row=0, column=0)
        self.madel_grid_frame.place(x=0, y=0)
        #self.madel_grid_frame.pack()
        self.madel_grid_frame.update()
        self.m_modelManager = we.ModelManager(self.madel_grid_frame, self,
                                              width=self.madel_grid_frame.winfo_width(),
                                              height=self.madel_grid_frame.winfo_height())

        # 连接器相关控件
        # 使用LabelFrame控件 框出连接相关的控件
        self.connor_grid_frame = tk.LabelFrame(self.root, text=self.word_map["Connect"]["Connect"],
                                     labelanchor="nw", bg="white")
        #self.connor_grid_frame.place(anchor="ne", relx=1.0, rely=0.0)
        #self.connor_grid_frame.grid(row=0, column=1)
        self.connor_grid_frame.place(x=self.madel_grid_frame.winfo_width()+5, y=0)
        self.connor_grid_frame.update()
        self.m_connor = we.Connector(self.connor_grid_frame, self)

        # 日志打印类
        # 日志打印信息框
        self.m_info_out = tk.LabelFrame(self.root, text=self.word_map["SysOut"]["title"],
                                        labelanchor="nw", width=20, height=30)
        #self.m_info_out.place(anchor="ne", relx=1.0, rely=0.0)
        #self.info_grid_frame.grid(row=0, column=1)
        self.m_info_out.update()
        self.m_info_out.place(x=self.madel_grid_frame.winfo_width()+5,
                              y=self.connor_grid_frame.winfo_height()+5)
        self.m_infoOut = we.InfoOut(self.m_info_out, self)

        # 动作组可视表格
        self.action_grid_frame = tk.Frame(self.root, width=800, height=150, bg="white")
        #self.action_grid_frame.grid(row=0, column=0)
        self.action_grid_frame.place(x=0, y=self.madel_grid_frame.winfo_height())
        self.action_grid_frame.update()
        print(self.action_grid_frame.winfo_width(), self.action_grid_frame.winfo_height())
        self.m_actionTable = we.GroupActionTable(self.action_grid_frame, self,
                                              width=self.action_grid_frame.winfo_width(),
                                              height=self.action_grid_frame.winfo_height())

    def OnThreadMessage(self, fromwho, towho, action, param = None):
        """
        引擎的调度函数 控件利用此函数可间接操作或者获取其他控件的对应资源
        :param fromwho:表示调用者
        :param towho:表示请求操作的控件
        :param action:表示请求操作的操作类型
        :param param:操作请求所携带的参数(根据具体请求来指定参数类型)
        """
        print(fromwho, towho, action, param)
        #info = fromwho+" "+towho+" "+action+" "+param
        #self.OnThreadMessage(mh.M_ENGINE, mh.M_SYSINFO, mh.A_INFO_PRINT, info+"\n")

        if towho == mh.M_LANGUAGE and action == mh.A_UPDATALANG: # 语言更新请求
            self.v_lang, self.word_map = self.m_lang.api(action, param)
            self.m_menu.api(mh.A_UPDATALANG)    # 菜单栏语言更新
            self.m_infoOut.api(mh.A_UPDATALANG)
            self.m_modelManager.api(mh.A_UPDATALANG)    # 按钮语言更新
            self.updata_lang(self.word_map)

        elif towho == mh.M_SMMODEL_MANAGER: # 舵机模型控件操作请求
            self.m_modelManager.api(action, param)
        elif towho == mh.M_SYSINFO:
            self.m_infoOut.api(mh.A_INFO_PRINT, param)
        # 模型文件读写操作
        elif towho == mh.M_MODEL_FILEMANAGER:
            self.m_infoOut.api(mh.A_INFO_PRINT, action+" "+param+"\n")
            if action == mh.A_FILE_CREATE:
                model_filepath = param
                self.m_model_file.create_file(model_filepath)
                self.m_modelManager.api(mh.A_SET_MODELNAME, model_filepath.split('/')[-1])
            elif action == mh.A_FILE_OPEN:
                model_filepath = param
                model_info = self.m_model_file.read(model_filepath)
                self.m_modelManager.api(mh.A_SET_MODELINFO, model_info)
                self.m_modelManager.api(mh.A_SET_MODELNAME, model_filepath.split('/')[-1])
                self.m_actionTable.api(mh.A_SET_TABLEHEAD, model_info)
            elif action == mh.A_FILE_SAVE:
                model_info = self.m_modelManager.api(mh.A_GET_MODELINFO, None)
                self.m_model_file.save(model_info)
            elif action == mh.A_FILE_SAVEAS:
                model_filepath = param
                model_info = self.m_modelManager.api(mh.A_GET_MODELINFO, None)
                self.m_model_file.save(model_info, model_filepath)
                self.m_modelManager.api(mh.A_SET_MODELNAME, model_filepath.split('/')[-1])
        # 动作组文件读写
        elif towho == mh.M_ACTION_FILEMANAGER:
            self.m_infoOut.api(mh.A_INFO_PRINT, action+" "+param+"\n")
            if action == mh.A_FILE_CREATE:
                action_filepath = param
                self.m_action_file.create_file(action_filepath)
            elif action == mh.A_FILE_OPEN:
                action_filepath = param
                action_info = self.m_model_file.read(action_filepath)
                self.m_modelManager.api(mh.A_SET_ACTIONINFO, action_info)
            elif action == mh.A_FILE_SAVE:
                action_info = self.m_modelManager.api(mh.A_GET_ACTIONINFO, None)
                self.m_action_file.save(action_info)
            elif action == mh.A_FILE_SAVEAS:
                action_filepath = param
                action_info = self.m_modelManager.api(mh.A_GET_ACTIONINFO, None)
                self.m_action_file.save(action_info, action_filepath)
        # 模型数据呈现指定数据
        elif action == mh.A_UPDATA_ALL_MODEL_VAL:
            self.m_modelManager.api(mh.A_UPDATA_ALL_MODEL_VAL, param)
        # 表格数据呈现指定数据
        elif action == mh.A_UPDATA_TREE_SELECT_ROW:
            self.m_actionTable.api(mh.A_UPDATA_TREE_SELECT_ROW, param)

    def updata_lang(self, val_map):
        """
        更新主窗口字段语种
        :param val_map: 字段信息所对应要显示的语言
        :return: None
        """
        self.root.title(self.word_map["Windows"]["Title"]+"\t  "+VERSION)  # 窗口名
        self.connor_grid_frame["text"] = val_map["Connect"]["Connect"]
        self.m_info_out["text"] = val_map["SysOut"]["title"]

    def on_closing(self):
        """
        关闭主窗口时要触发的函数
        :return: None
        """
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.m_modelManager.__del__()
            root.destroy()

if __name__ == "__main__":
    root = tk.Tk()  # 创建窗口对象的背景色
    root.title("机器人通用控制平台"+"\t  "+VERSION)           #窗口名
    root.geometry('1000x650+10+10')
    root.iconbitmap("./img/favicon_64.ico")  # 窗体图标
    engine = Engine(root)
    tku.center_window(root)  # 将窗体移动到屏幕中央
    # 进入消息循环 父窗口进入事件循环，可以理解为保持窗口运行，否则界面不展示
    root.mainloop()