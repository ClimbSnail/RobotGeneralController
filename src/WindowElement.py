import os
import time
import tkinter as tk
import tkutils as tku
from tkinter import ttk
import massagehead as mh
import tkinter.font as tkFont
from tkinter import messagebox
from tkinter import simpledialog
from tkinter import filedialog

from PIL import Image, ImageTk	# pip3 install pillow
# 使用 ttk.Notebook 作为标签切换


class CtrlMenu(object):
    """
    菜单栏类
    """
    def __init__(self, father, engine, lock = None):
        """
        CtrlMenu初始化
        :param father:父类窗口
        :param engine:引擎对象，用于推送与其他控件的请求
        :param lock:线程锁
        :return:None
        """
        self.m_engine = engine    # 负责各个组件之间数据调度的引擎
        self.father = father    # 保存父窗口
        # 创建菜单栏
        self.menuBar = tk.Menu(father)
        # 将菜单栏放到主窗口
        self.father.config(menu=self.menuBar)
        # 添加菜单项
        self.init_modelBar(self.menuBar, )
        self.init_actionBar(self.menuBar)
        self.init_settingBar(self.menuBar)
        self.init_helpBar(self.menuBar)

    def init_modelBar(self, menuBar):
        """
        初始化模型菜单子项
        :param menuBar: 主菜单
        :return: None
        """
        self.m_model_filepath = None
        # 创建菜单项
        self.modelBar = tk.Menu(menuBar, tearoff=0)
        # 将菜单项添加到菜单栏
        menuBar.add_cascade(label=self.m_engine.word_map["Menu"]["Model"], menu=self.modelBar)
        # 在菜单项中加入子菜单
        self.modelBar.add_command(label=self.m_engine.word_map["Menu"]["Create"], command= self.click_model_create)
        self.modelBar.add_command(label=self.m_engine.word_map["Menu"]["Open"], command= self.click_model_open)
        self.modelBar.add_command(label=self.m_engine.word_map["Menu"]["Save"], command=self.click_model_save)
        self.modelBar.add_command(label=self.m_engine.word_map["Menu"]["SaveAs"], command= self.click_model_saveAs)
        # 创建分割线
        self.modelBar.add_separator()
        self.modelBar.add_command(label=self.m_engine.word_map["Menu"]["Exit"], command=self.father.destroy)

    def init_actionBar(self, menuBar):
        """
        初始化动作菜单子项
        :param menuBar: 主菜单
        :return: None
        """
        self.m_action_filepath = None
        # 创建菜单项
        self.actionBar = tk.Menu(menuBar, tearoff=0)
        # 将菜单项添加到菜单栏
        menuBar.add_cascade(label=self.m_engine.word_map["Menu"]["Action"], menu=self.actionBar)
        # 在菜单项中加入子菜单
        self.actionBar.add_command(label=self.m_engine.word_map["Menu"]["Create"], command= self.click_action_create)
        self.actionBar.add_command(label=self.m_engine.word_map["Menu"]["Open"], command= self.click_action_open)
        self.actionBar.add_command(label=self.m_engine.word_map["Menu"]["Save"], command=self.click_action_save)
        self.actionBar.add_command(label=self.m_engine.word_map["Menu"]["SaveAs"], command= self.click_action_saveAs)
        # 创建分割线
        # self.actionBar.add_separator()
        # self.actionBar.add_command(label=self.m_engine.word_map["Menu"]["Exit"], command=self.father.destroy)

    def init_settingBar(self, menuBar):
        """
        初始化设置菜单子项
        :param menuBar: 主菜单
        :return: None
        """
        # 创建一个tk回调参数变量
        vLang = tk.StringVar()
        def language_choose():
            """
            语言设置触发函数
            """
            global word_map
            print(vLang.get())
            # 更新语言文本操作请求推送到引擎
            self.m_engine.OnThreadMessage(mh.M_CTRLMENU, mh.M_LANGUAGE,
                                                      mh.A_UPDATALANG, vLang.get())

        v_fileManager = tk.IntVar()
        v_transInfo = tk.IntVar()

        def view_choose():
            """
            视图设置触发函数
            """
            print(v_fileManager.get())
            print(v_transInfo.get())

        # 创建菜单项
        self.settingBar = tk.Menu(menuBar, tearoff=0)
        # 将菜单项添加到菜单栏
        menuBar.add_cascade(label=self.m_engine.word_map["Menu"]["Setting"], menu=self.settingBar)

        self.languageBar = tk.Menu(self.settingBar, tearoff=0)
        for lang in self.m_engine.v_lang:
            self.languageBar.add_radiobutton( label=lang, command=language_choose, variable = vLang)
            # languageBar.add_separator() # 分割线
        # 在菜单项中加入子菜单
        self.settingBar.add_cascade(label=self.m_engine.word_map["Menu"]['Language'], menu=self.languageBar)

        self.viewBar = tk.Menu(self.settingBar, tearoff=0)
        self.viewBar.add_checkbutton( label=self.m_engine.word_map["Menu"]['FileManager'],
                                      command=view_choose, variable = v_fileManager)
        self.viewBar.add_checkbutton( label=self.m_engine.word_map["Menu"]['TransInfo'],
                                      command=view_choose, variable = v_transInfo)

        # 在菜单项中加入子菜单
        self.settingBar.add_cascade(label=self.m_engine.word_map["Menu"]['View'], menu=self.viewBar)

    def init_helpBar(self, menuBar):
        """
        初始化"帮助"菜单子项
        :param menuBar: 主菜单
        :return: None
        """
        # 创建菜单项
        self.helpBar = tk.Menu(menuBar, tearoff=0)
        # 将菜单项添加到菜单栏
        menuBar.add_cascade(label=self.m_engine.word_map["Menu"]["Help"], menu=self.helpBar)
        # 在菜单项中加入子菜单
        self.helpBar.add_command(label=self.m_engine.word_map["Menu"]["Registration"],
                                 command=self.click_Regist)
        self.helpBar.add_command(label=self.m_engine.word_map["Menu"]["About"],
                                 command=self.click_About)

    def click_model_create(self):
        """
        点击模型"创建"菜单项触发的函数
        :return: None
        """
        # 打开文件对话框 获取文件路径
        # defaultextension 为选取保存类型中的拓展名为文件名
        # filetypes为文件拓展名
        filepath = tk.filedialog.asksaveasfilename(
            title='选择一个模型文件',
            defaultextension =".espace",
                    filetypes = [('Model', '.mo'),('Normal', '.nor')])
        if filepath == None or filepath == "":
            return None
        self.m_model_filepath = filepath
        self.m_engine.OnThreadMessage(mh.M_CTRLMENU, mh.M_MODEL_FILEMANAGER,
                                      mh.A_FILE_CREATE, self.m_model_filepath)

    def click_model_open(self):
        """
        点击模型"打开"菜单项触发的函数
        :return:
        """
        # 打开文件对话框 获取文件路径
        # defaultextension 为选取保存类型中的拓展名为文件名
        # filetypes为文件拓展名
        filepath = tk.filedialog.askopenfilename(
            title='选择一个模型文件',
            defaultextension =".espace",
                    filetypes = [('Model', '.mo'),('Normal', '.nor')])
        if filepath == None or filepath == "":
            return None
        self.m_model_filepath = filepath
        self.m_engine.OnThreadMessage(mh.M_CTRLMENU, mh.M_MODEL_FILEMANAGER,
                                      mh.A_FILE_OPEN, self.m_model_filepath)

    def click_model_save(self):
        """
        点击模型"保存"菜单项触发的函数
        :return:
        """
        if self.m_model_filepath == None:
            tk.messagebox.showinfo("操作有误","请选择一个模型文件")
        else:
            self.m_engine.OnThreadMessage(mh.M_CTRLMENU, mh.M_MODEL_FILEMANAGER,
                                        mh.A_FILE_SAVE, self.m_model_filepath)

    def click_model_saveAs(self):
        """
        点击模型"另存为"菜单项触发的函数
        :return:
        """
        # 打开文件对话框 获取文件路径
        # defaultextension 为选取保存类型中的拓展名为文件名
        # filetypes为文件拓展名
        filepath = tk.filedialog.asksaveasfilename(
            title='',
            defaultextension =".espace",
                    filetypes = [('Model', '.mo'),('Normal', '.nor')])
        if filepath == None or filepath == "":
            return None
        self.m_model_filepath = filepath
        self.m_engine.OnThreadMessage(mh.M_CTRLMENU, mh.M_MODEL_FILEMANAGER,
                                      mh.A_FILE_SAVEAS, self.m_model_filepath)

    def click_action_create(self):
        """
        点击动作"创建"菜单项触发的函数
        :return: None
        """
        # 打开文件对话框 获取文件路径
        # defaultextension 为选取保存类型中的拓展名为文件名
        # filetypes为文件拓展名
        filepath = tk.filedialog.asksaveasfilename(
            title='选择一个动作组文件',
            defaultextension=".espace",
            filetypes=[('Action', '.act'), ('Normal', '.nor')])
        if filepath == None or filepath == "":
            return None
        self.m_action_filepath = filepath
        self.m_engine.OnThreadMessage(mh.M_CTRLMENU, mh.M_ACTION_FILEMANAGER,
                                      mh.A_FILE_CREATE, self.m_action_filepath)

    def click_action_open(self):
        """
        点击动作"打开"菜单项触发的函数
        :return:
        """
        # 打开文件对话框 获取文件路径
        # defaultextension 为选取保存类型中的拓展名为文件名
        # filetypes为文件拓展名
        filepath = tk.filedialog.askopenfilename(
            title='选择一个模型文件',
            defaultextension=".espace",
            filetypes=[('Action', '.act'), ('Normal', '.nor')])
        if filepath == None or filepath == "":
            return None
        self.m_action_filepath = filepath
        self.m_engine.OnThreadMessage(mh.M_CTRLMENU, mh.M_ACTION_FILEMANAGER,
                                      mh.A_FILE_OPEN, self.m_action_filepath)

    def click_action_save(self):
        """
        点击动作"保存"菜单项触发的函数
        :return:
        """
        if self.m_action_filepath == None:
            tk.messagebox.showinfo("操作有误", "请选择一个模型文件")
        else:
            self.m_engine.OnThreadMessage(mh.M_CTRLMENU, mh.M_ACTION_FILEMANAGER,
                                          mh.A_FILE_SAVE, self.m_action_filepath)

    def click_action_saveAs(self):
        """
        点击动作"另存为"菜单项触发的函数
        :return:
        """
        # 打开文件对话框 获取文件路径
        # defaultextension 为选取保存类型中的拓展名为文件名
        # filetypes为文件拓展名
        filepath = tk.filedialog.asksaveasfilename(
            title='',
            defaultextension=".espace",
            filetypes=[('Action', '.act'), ('Normal', '.nor')])
        if filepath == None or filepath == "":
            return None
        self.m_action_filepath = filepath
        self.m_engine.OnThreadMessage(mh.M_CTRLMENU, mh.M_ACTION_FILEMANAGER,
                                      mh.A_FILE_SAVEAS, self.m_action_filepath)

    def click_About(self):
        """
        点击"帮助"->"关于"菜单项触发的函数
        :return: None
        """
        if tk.messagebox.showinfo(self.helpBar.entrycget(1, "label"),
                                  "具体请访问 https://github.com/ClimbSnail/RobotGeneralController"):
            pass

    def click_Regist(self):
        """
        点击"注册"菜单项触发的函数
        获取字符串（标题，提示，初始值）
        :return:
        """
        result = tk.simpledialog.askstring(title=self.helpBar.entrycget(0, "label"),
                                                prompt=self.m_engine.word_map["MassageBox"]["UserCode"],
                                            initialvalue=self.m_engine.word_map["MassageBox"]["UserCodeText"])

    def updata_lang(self, word_map):
        """
        更新文字语种接口
        :param word_map: 字段map: key->value
        :return: None
        """
        self.father.title(word_map["Windows"]["Title"])  # 窗口名
        # 更新菜单栏的菜单项文字
        self.menuBar.entryconfigure(1, label=word_map["Menu"]["Model"])
        self.menuBar.entryconfigure(2, label=word_map["Menu"]["Action"])
        self.menuBar.entryconfigure(3, label=word_map["Menu"]["Setting"])
        self.menuBar.entryconfigure(4, label=word_map["Menu"]["Help"])
        # 更新菜单项下 模型的子菜单文字
        self.modelBar.entryconfigure(0, label=word_map["Menu"]["Create"])
        self.modelBar.entryconfigure(1, label=word_map["Menu"]["Open"])
        self.modelBar.entryconfigure(2, label=word_map["Menu"]["Save"])
        self.modelBar.entryconfigure(3, label=word_map["Menu"]["SaveAs"])
        self.modelBar.entryconfigure(5, label=word_map["Menu"]["Exit"])
        # 更新菜单项下 动作组的子菜单文字
        self.actionBar.entryconfigure(0, label=word_map["Menu"]["Create"])
        self.actionBar.entryconfigure(1, label=word_map["Menu"]["Open"])
        self.actionBar.entryconfigure(2, label=word_map["Menu"]["Save"])
        self.actionBar.entryconfigure(3, label=word_map["Menu"]["SaveAs"])
        # self.actionBar.entryconfigure(5, label=word_map["Menu"]["Exit"])
        # 更新菜单项下的子菜单文字
        self.settingBar.entryconfigure(0, label=word_map["Menu"]['Language'])
        self.languageBar = tk.Menu(self.settingBar, tearoff=0)
        for lang in self.m_engine.v_lang:
            self.languageBar.entryconfigure( self.m_engine.v_lang.index(lang), label=lang)
        self.settingBar.entryconfigure(1, label=word_map["Menu"]['View'])
        self.viewBar.entryconfigure( 0, label=word_map["Menu"]['FileManager'])
        self.viewBar.entryconfigure( 1, label=word_map["Menu"]['TransInfo'])
        # 帮助
        self.helpBar.entryconfigure( 0, label=word_map["Menu"]['Registration'])
        self.helpBar.entryconfigure( 1, label=word_map["Menu"]['About'])

    def api(self, action, param=None):
        """
        外界操作舵机控件管理器的api接口
        """
        if action == mh.A_UPDATALANG:  # 更新语言
            self.updata_lang(self.m_engine.word_map)

class ServoMotorModel(object):
    """
    舵机控件类
    """
    def __init__(self, father, start_x = 0, start_y = 0, name = "S0", model_en=True, manager = None):
        """
        舵机控件类初始化
        :param father: 父类空间
        :param start_x: 本舵机控件起始坐标
        :param start_y: 本舵机控件起始坐标
        :param name: 本舵机控件名称
        :param manager: 引擎
        """
        self.m_father = father
        self.m_manager = manager
        self.m_name = name
        self.my_ft1 = tkFont.Font(family="微软雅黑", size=7, weight=tkFont.BOLD)   # 定义字体
        self.my_ft2 = tkFont.Font(family="微软雅黑", size=10, weight=tkFont.BOLD)   # 定义字体
        self.m_model_en = model_en    # 舵机的使能标志位
        self.m_val_min = 500    # 控件控制的数值最小值
        self.m_val_max = 2500    # 控件控制的数值最大值
        self.m_frame = tk.Frame(self.m_father, bg="LightYellow",highlightthickness = 1)
        self.create_element(self.m_frame, self.m_name)
        self.m_start_x = start_x    # 本控件相对于父容器的起点x坐标
        self.m_start_y = start_y    # 本控件相对于父容器的起点y坐标
        self.m_frame.place(x = self.m_start_x, y = self.m_start_y)
        self.m_frame.update()   # 一定要更新 才可得到winfo_width winfo_height真实值
        self.m_centerX = self.m_frame.winfo_width()/2
        self.m_centerY = self.m_frame.winfo_height()/2
        self.m_frame.bind("<B1-Motion>", self.mouseMove)    # 鼠标拖拽
        self.m_frame.bind("<Double-1>", self.mouseDoubleClick)    # 鼠标左键双击
        self.m_frame.bind("<Button-1>", self.mouseSingleClick)    # 鼠标左键单击

    def mouseMove(self, event):
        """
        鼠标移动事件
        :param event: 事件
        :return: None
        """
        # 检测模型是否可编辑
        if self.m_manager.m_model_editable == False:
            return None
        self.m_start_x = self.m_start_x +( event.x-self.m_centerX)
        self.m_start_y = self.m_start_y +( event.y-self.m_centerY)
        # 添加移动的边框横向限制条件
        if self.m_start_x > self.m_father.winfo_width()-self.m_frame.winfo_width():
            self.m_start_x = self.m_father.winfo_width()-self.m_frame.winfo_width()
        if self.m_start_x < 0:
            self.m_start_x = 0
        # 添加移动的边框纵向限制条件
        if self.m_start_y > self.m_father.winfo_height()-self.m_frame.winfo_height():
            self.m_start_y = self.m_father.winfo_height()-self.m_frame.winfo_height()
        if self.m_start_y < 0:
            self.m_start_y = 0
        # 重新设置窗口的位置
        self.m_frame.place(x=self.m_start_x, y=self.m_start_y)

    def mouseDoubleClick(self, event):
        """
        鼠标左键双击事件
        :param event: 事件
        :return: None
        """
        # 检测模型是否可编辑
        if self.m_manager.m_model_editable == False:
            return None
        self.m_manager.api(mh.A_SELECT, self.m_name)

    def mouseSingleClick(self, event):
        """
        鼠标单击触发本函数
        :param event: 事件
        :return:
        """
        self.m_manager.api(mh.A_SELECT, None)

    def create_element(self, father, name):
        """
        创建一个舵机控件
        :param father:父类窗口
        :param name: 本舵机控件的名字
        :return: None
        """
        self.m_name_label = tk.Label(father, text=name, font=self.my_ft2, bg=father['bg'])
        # 创建输入框
        self.m_val_entry = tk.Entry(father, font=self.my_ft1, width=5, highlightcolor="LightGrey")
        self.m_val_entry.insert(tk.END, '1500')
        self.m_pre_val_text = "1500"    # 保存修改前m_val_text输入框中的内容，供错误输入时使用
        self.m_val_entry.bind("<Return>", self.change_val)  # 绑定enter键的触发
        # 创建范围控件
        self.m_val = tk.StringVar()
        self.m_scale = tk.Scale(father,
                                from_=self.m_val_min,  # 设置最小值
                                to=self.m_val_max,  # 设置最大值
                                resolution=2,  # 设置步距值
                                bd = 1, # 槽的边框
                                length=100,  # 200像素
                                width = 10, # 字符宽度
                                sliderlength = 8,   # 滑块长度
                                showvalue=0,  # 是否显示当前值
                                orient=tk.HORIZONTAL,  # 设置水平方向
                                variable=self.m_val,  # 绑定变量
                                command = self.set_entry_val,  # 设置回调函数
                                bg = father['bg'], # 背景
                                troughcolor = "white", # 槽的颜色
                                # highlightbackground =  "black",
                                cursor = "arrow", # 光标样式
                                takefocus = 0,
                                relief = tk.FLAT,
                                )
        # 范围控件预设值
        self.m_scale.set( (self.m_val_min+self.m_val_max)/2 )
        self.m_scale.pack(side=tk.BOTTOM)
        self.m_name_label.pack(side=tk.LEFT, padx=10, pady=2)
        self.m_val_entry.pack(side=tk.RIGHT, padx=10)  # 将小部件放置到窗口中

    def set_entry_val(self, val):
        """
        设置文本输入框中的值
        :param val: 设置的目标值
        :return: None
        """
        self.m_val_entry.delete(0, tk.END)   # 清空文本框
        self.m_val_entry.insert(tk.END, val) # 插入新值
        self.m_pre_val_text = val

    def change_val(self, extern_val=None):
        """
        文本输入框按下Enter将触发本函数
        :param extern_val: 设置的目标值
        :return: None
        """
        m_val_entry = None
        if extern_val == None or type(extern_val) == tk.Event:  # 当控件的事件被触发extern_val为一个控件对象
            m_val_entry = self.m_val_entry.get().strip()    # 得到输入的文本
        else:
            m_val_entry = extern_val.strip()  # 得到外部传进来的文本数值
        try:
            val = int(m_val_entry)  # 得到数值
            val = val if val>=self.m_val_min and val<=self.m_val_max else int(self.m_pre_val_text)
            self.m_scale.set(val)   # 数据符合范围，即可设置范围控件(进度条)
        except Exception as err:    # 有效过滤输入的非法字符
            print(err)

        self.set_entry_val(self.m_pre_val_text) # 输入结束，将文本框更新为目标值

    def __del__(self):
        # self.m_frame.pack_forget()
        # Release resources
        self.m_frame.destroy()

class ModelManager(object):
    """
    ServoMotorModel(舵机控件)管理器
    """
    def __init__(self, father, engine = None, width=700, height=500):
        """
        ServoMotorModel(舵机控件)管理器 初始化
        :param father:父类控件
        :param engine:引擎对象，用于推送与其他控件的请求
        :param width:本控件的宽度
        :param height:本控件的高度
        """
        self.m_engine = engine  # 保存引擎
        self.m_image_path = self.m_engine.m_sys_info["system_init"]["imagepath"]
        self.m_father = father
        self.width = width
        self.height = height
        self.m_frame = tk.Frame(father, width=self.width, height=self.height, bg="white")
        self.m_model_map = {}   # 储存舵机控件 name(key):object
        self.m_frame.pack(side = tk.LEFT)
        self.m_frame.update()
        self.m_select_name = None
        self.m_model_editable = True   # 标志模型是否可编辑(位置、删除)

        # 初始化操作按钮
        self.add_button = tk.Button(self.m_frame, text=self.m_engine.word_map["Action"]["Add"],
                               command = self.add_ServoMotorModel, width=10, height=1)
        # button['width'] = 30
        # button['height'] = 20
        width = 80
        height = 30
        self.add_button.place(x=self.m_frame.winfo_width()-width,
                              y=self.m_frame.winfo_height()-height*2)
        self.del_button = tk.Button(self.m_frame, text=self.m_engine.word_map["Action"]["Del"],
                               command = self.del_ServoMotorModel, width=10, height=1)
        self.del_button.place(x=self.m_frame.winfo_width()-width,
                              y=self.m_frame.winfo_height()-height)
        # 编辑图标按钮
        pencil_bg_image = Image.open(self.m_image_path+"pencil_16x16.ico")
        self.pencil_edit_img = ImageTk.PhotoImage(pencil_bg_image)
        pencil_bg_image = Image.open(self.m_image_path+"yes_16x16.ico")
        self.pencil_yes_img = ImageTk.PhotoImage(pencil_bg_image)
        self.pencil_button = tk.Button(self.m_frame, command = self.pencil_click,
                               image=self.pencil_yes_img)
        self.pencil_button.place(x=self.m_frame.winfo_width()-30,
                              y=self.m_frame.winfo_height()-height*3)
        # 用来显示模型名称
        self.name_label = tk.Label(self.m_frame, text="", bg=self.m_frame['bg']) # , font=self.my_ft1
        self.name_label.place(x=5, y=self.height-25)

    def add_ServoMotorModel(self):
        """
        添加一个ServoMotorModel(舵机控件)
        """
        find_num = 0    # 用来产生舵机控件的编号
        for find_num in range(1000):
            if "S"+str(find_num) not in self.m_model_map.keys():
                break
        name = "S"+str(find_num)    # "S"+编号组合成ServoMotorModel(舵机控件)的名字 当作m_model_map的key值
        self.m_model_map[name] = ServoMotorModel(
            self.m_frame, start_x = 50, start_y = 50, name = name, model_en=True, manager = self)

    def del_ServoMotorModel(self):
        if self.m_select_name != None:
            # 先释放控件对象
            self.m_model_map[self.m_select_name].__del__()
            # 删除字典
            del self.m_model_map[self.m_select_name]
            self.m_select_name = None

    def pencil_click(self):
        """
        修改按钮按下之后触发编辑状态改变
        :return:
        """
        if self.m_model_editable == False:
            self.set_model_edit_state(True)
        else:
            self.set_model_edit_state(False)

    def set_model_edit_state(self, status):
        """
        设置模型是否处于可编辑状态
        :return: None
        """
        if status == False:
            # 标志模型是否可编辑(位置、删除)
            self.m_model_editable = False
            # 编辑图标
            self.pencil_button["image"] = self.pencil_edit_img
            # 设置按键不可按
            self.add_button["state"] = tk.DISABLED
            self.del_button["state"] = tk.DISABLED
        else:
            # 标志模型是否可编辑(位置、删除)
            self.m_model_editable = True
            # 编辑图标
            self.pencil_button["image"] = self.pencil_yes_img
            # 设置按键不可按
            self.add_button["state"] = tk.NORMAL
            self.del_button["state"] = tk.NORMAL

    def updata_lang(self, val_map):
        """
        更新字段语言
        :param val_map: 字段所对应的map
        :return:
        """
        self.add_button["text"] = val_map["Add"]
        self.del_button["text"] = val_map["Del"]

    def get_all_motor_model_info(self):
        """
        获取模型控件所在的坐标位置, 使能状态, 控件上的值(值暂时用不上)
        :return: 所有舵机的列表集合
        """
        res = {}
        for name, model in self.m_model_map.items():
            res[name] = {"pos_x":model.m_start_x, "pos_y":model.m_start_y,
                         "model_en":model.m_model_en, "val":model.m_pre_val_text}
        return res

    def load_all_model(self, model_info):
        """
        通过传入的模型列表信息 生成对应的模型
        :param model_info:
        :return:
        """
        # 先清空原先的模型
        keyList = list(self.m_model_map.keys())
        for key in keyList:
            # 先释放控件对象
            self.m_model_map[key].__del__()
            # 删除字典
            del self.m_model_map[key]
            self.m_select_name = None
        # 设置模型处于不可编辑状态
        self.set_model_edit_state(False)
        # 添加指定的舵机模型控件
        for name, info in model_info.items():
            self.m_model_map[name] = ServoMotorModel(
                self.m_frame, start_x=info["pos_x"], start_y=info["pos_y"], name=name, model_en=info["model_en"], manager=self)
        return True

    def set_model_name(self, model_name):
        """
        设置模型标识的名字
        :param model_name: 模型的目标名字
        :return: None
        """
        self.name_label["text"] = model_name

    def updata_all_model_val(self, param):
        #change_val
        pass

    def api(self, action, param = None):
        """
        外界操作舵机控件管理器的api接口
        :param action: 动作类型
        :param param: 携带参数
        :return: None
        """
        if action == mh.A_CREATE_MODEL: # 创建新控件(舵机控件)
            self.add_ServoMotorModel()
        elif action == mh.A_DEL_MODEL: # 删除(被选择的)控件(舵机控件)
            self.del_ServoMotorModel()
        elif action == mh.A_SELECT: # 选择控件(舵机控件)，之后才可进行删除操作
            self.m_select_name = param
        elif action == mh.A_UPDATALANG:  # 更新语言
            self.updata_lang(self.m_engine.word_map["Action"])
        elif action == mh.A_GET_MODELINFO:
            return self.get_all_motor_model_info()
        elif action == mh.A_SET_MODELINFO:
            self.load_all_model(param)
        elif action == mh.A_SET_MODELNAME:
            self.set_model_name(param)
        elif action == mh.A_UPDATA_ALL_MODEL_VAL:
            self.updata_all_model_val(param)
        return None

    def __del__(self):
        """
        主要工作：释放舵机控件所占用的资源
        :return: None
        """
        # 释放模型控件资源
        keyList = list(self.m_model_map.keys())
        for key in keyList:
            # 先释放控件对象
            self.m_model_map[key].__del__()
            # 删除字典
            del self.m_model_map[key]
            self.m_select_name = None

class Connector(object):
    """
    连接器类：管理各个连接相关的按钮
    """
    def __init__(self, father, engine = None):
        """
        ServoMotorModel(舵机控件)管理器 初始化
        :param father:父类控件
        :param engine:引擎对象，用于推送与其他控件的请求
        """
        self.m_father = father
        self.m_engine = engine
        # 单选按钮
        self.m_radio_val = tk.IntVar()  # IntVar
        radio_frame = tk.Frame(self.m_father, bg="DimGray")
        tk.Radiobutton(radio_frame, variable=self.m_radio_val, value=0,
                       text="COM", width=5, bg="DimGray",
                       command=self.radio_select).pack(side=tk.LEFT, pady=5)

        tk.Radiobutton(radio_frame, variable=self.m_radio_val, value=1,
                       text="TCP", width=5, bg="DimGray",
                       command=self.radio_select).pack(side=tk.LEFT)
        self.m_radio_val.set(0)
        radio_frame.pack(side=tk.TOP, padx=5, fill="x")

        # 连接的信息框 根据单选按钮来选择显示的内容
        self.link_param_frame = tk.Frame(self.m_father, bg=self.m_father["bg"])
        self.link_param_frame.pack(side=tk.TOP, pady=5)
        # 串口窗口
        self.uart_param_frame = tk.Frame(self.link_param_frame, bg=self.m_father["bg"])
        self.uart_param_frame.pack(side=tk.TOP, pady=5)
        self.create_com(self.uart_param_frame)
        # self.link_param_frame.pack_forget()
        # TCP窗口
        self.tcp_param_frame = tk.Frame(self.link_param_frame, bg=self.m_father["bg"])
        self.tcp_param_frame.pack(side=tk.TOP, pady=5)
        self.create_tcp(self.tcp_param_frame)
        # 先将其隐藏
        self.tcp_param_frame.pack_forget()

        # 连接按钮
        self.m_connect = tk.Button(self.m_father, text=self.m_engine.word_map["Connect"]["Connect"],
                               command = self.connect, width=15, height=1)
        self.m_connect.pack(side = tk.TOP, fill=tk.X, padx=5)

    def create_com(self, father):
        """
        创建Comm相关控件
        :param father: 父类窗口
        :return: None
        """
        # 窗口
        com_frame = tk.Frame(father, bg=self.m_father["bg"])
        self.m_com_label = tk.Label(com_frame, text=self.m_engine.word_map["Connect"]["UartNo"],
                              #font=self.my_ft1,
                              bg=self.m_father['bg'])
        self.m_com_label.pack(side=tk.LEFT, padx=10)
        self.com_combo = ttk.Combobox(com_frame, width=8)
        self.com_combo["value"] = ('COM0','COM1')
        # 设置默认值，即默认下拉框中的内容
        self.com_combo.current(0)
        self.com_combo.pack(side=tk.RIGHT, padx=10)
        com_frame.pack(side=tk.TOP, pady=5)

        baud_frame = tk.Frame(father, bg=self.m_father["bg"])
        self.m_baud_label = tk.Label(baud_frame, text=self.m_engine.word_map["Connect"]["BaudRate"],
                              #font=self.my_ft1,
                              bg=self.m_father['bg'])
        self.m_baud_label.pack(side=tk.LEFT, padx=10)
        self.m_baud_select = ttk.Combobox(baud_frame, width=8)
        self.m_baud_select["value"] = ('9600','115200')
        # 设置默认值，即默认下拉框中的内容
        self.m_baud_select.current(0)
        self.m_baud_select.pack(side=tk.RIGHT, padx=10)
        baud_frame.pack(side=tk.TOP, pady=5)

    def create_tcp(self, father):
        """
        创建TCP相关控件
        :param father: 父类窗口
        :return: None
        """
        # 窗口
        ip_frame = tk.Frame(father, bg=self.m_father["bg"])
        self.m_ip_label = tk.Label(ip_frame, text=self.m_engine.word_map["Connect"]["IpAddr"],
                              #font=self.my_ft1,
                              bg=self.m_father['bg'])
        self.m_ip_label.pack(side=tk.LEFT, padx=5)
        self.m_ip_entry = tk.Entry(ip_frame,
                                    # font=self.my_ft1,
                                    width=15, highlightcolor="LightGrey")
        self.m_ip_entry.insert(tk.END, '192.168.1.1')
        self.m_ip_entry.pack(side=tk.RIGHT, padx=5)
        ip_frame.pack(side=tk.TOP, pady=5)

        port_frame = tk.Frame(father, bg=self.m_father["bg"])
        self.m_port_label = tk.Label(port_frame, text=self.m_engine.word_map["Connect"]["Port"],
                              #font=self.my_ft1,
                              bg=self.m_father['bg'])
        self.m_port_label.pack(side=tk.LEFT, padx=5)
        self.m_port_entry = tk.Entry(port_frame,
                                    # font=self.my_ft1,
                                    width=5, highlightcolor="LightGrey")
        self.m_port_entry.insert(tk.END, '8080')
        self.m_port_entry.pack(side=tk.RIGHT, padx=5)
        port_frame.pack(side=tk.TOP, pady=5)

    def radio_select(self):
        """
        选择触发的函数
        :return:
        """
        if self.m_radio_val.get() == 0:
            self.tcp_param_frame.pack_forget()
            self.uart_param_frame.pack()
        elif self.m_radio_val.get() == 1:
            self.uart_param_frame.pack_forget()
            self.tcp_param_frame.pack()
        print("Radio select: ", self.m_radio_val.get())

    def connect(self):
        """
        创建连接按钮
        :return:
        """
        if self.m_connect["text"] == self.m_engine.word_map["Connect"]["Connect"]:
            # 连接请求推送到引擎
            self.m_engine.OnThreadMessage(mh.M_CONNECTOR, mh.M_SOCKET_MAIN, mh.A_CONNECT)
            self.m_connect["text"] = self.m_engine.word_map["Connect"]["DisConnect"]
        else:
            self.m_connect["text"] = self.m_engine.word_map["Connect"]["Connect"]
            # 断开请求推送到引擎
            self.m_engine.OnThreadMessage(mh.M_CONNECTOR, mh.M_SOCKET_MAIN, mh.A_DISCONNECT)

    def api(self, action, param = None):
        """
        连接器类向外提供的操作api
        :param action: 动作类型
        :param param: 携带参数
        :return: None
        """
        pass

    def updata_lang(self):
        """
        更新字段语言
        :return: None
        """
        pass

    def __del__(self):
        pass

class InfoOut(object):
    """
    日志打印类
    """
    def __init__(self, father, engine = None):
        """
        日志打印类初始化
        :param father: 父类空间
        :param engine: 引擎
        """
        self.m_father = father
        self.m_engine = engine
        self.m_father.update()
        self.info_width = self.m_father.winfo_width()
        self.info_height = self.m_father.winfo_height()/2
        # 滑动条
        self.m_scrollbar = tk.Scrollbar(self.m_father, width=12)
        # 信息文本框
        self.m_msg = tk.Text(self.m_father, width = self.info_width, height = self.info_height, yscrollcommand=self.m_scrollbar.set, state=tk.DISABLED)
        # 两个控件关联
        self.m_scrollbar.config(command=self.m_msg.yview)
        self.m_msg.pack(side=tk.LEFT, fill=tk.Y, padx=3, pady=3)

        # 清空按键
        self.m_clear = tk.Button(self.m_father, text="X", command = self.msg_clear, width=1, height=1, font=('Helvetica', '4'))
        self.m_clear.pack(side=tk.BOTTOM, fill=tk.X, pady=1)

        self.m_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def updata_lang(self, val_map):
        # self.m_info_out["text"] = val_map["title"]
        pass

    def print(self, info):
        """
        消息打印(打印到消息文本框中)
        :param info: 要打印的内容
        :return:
        """
        if info == None or info == "":
            return False
        self.m_msg.config(state=tk.NORMAL)
        self.m_msg.insert(tk.END, info)
        self.m_msg.config(state=tk.DISABLED)
        return True

    def msg_clear(self):
        """
        清空日志按钮
        :return: None
        """
        self.m_msg.config(state=tk.NORMAL)
        self.m_msg.delete(1.0, tk.END)
        self.m_msg.config(state=tk.DISABLED)

    def api(self, action, param = None):
        if action == mh.A_INFO_PRINT:
            self.print(param)
        elif action == mh.A_UPDATALANG:
            self.updata_lang(self.m_engine.word_map["SysOut"])

    def __del__(self):
        pass

class GroupActionTable(object):
    """
    动作组管理器
    """
    def __init__(self, father, engine = None, width=700, height=200):
        """
        栋动作组管理器 初始化
        :param father:父类控件
        :param engine:引擎对象，用于推送与其他控件的请求
        """
        self.m_father = father
        self.m_engine = engine
        self.m_image_path = self.m_engine.m_sys_info["system_init"]["imagepath"]
        self.m_width = width
        self.m_height = height
        self.m_tree_head_l = ["编号", "状态", "运行", "移动"] # 表头字段
        self.m_tree_head_r = []
        self.m_tree_width = [40, 40, 40, 40]   # 列对应的宽度
        self.ui_init()
        self.m_single_select_row = None    # 标记当前动作组表格单击选中的行
        self.m_double_select_row = None    # 标记当前动作组表格双击选中的行



    def ui_init(self):
        """
        创建动作组表格
        :return: None
        """
        self.m_frame = tk.Frame(self.m_father, bg = "LightGrey")
        self.m_frame.pack(padx=5, pady=5)
        # 滑动条
        self.m_scrollbar_y = tk.Scrollbar(self.m_frame)
        self.m_scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
        self.m_scrollbar_x = tk.Scrollbar(self.m_frame)
        self.m_scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)
        self.init_button_list(self.m_frame)
        # 两个控件关联
        row_num = 5 # 设置表格显示多少行
        self.m_tree = ttk.Treeview(self.m_frame, show = "headings", height = row_num,
                                 xscrollcommand=self.m_scrollbar_x.set,
                                 yscrollcommand=self.m_scrollbar_y.set,
                                selectmode = tk.BROWSE,
                                #selectmode = tk.EXTENDED
                                   )

        # height为显示多少行数据 headings为只显示表头
        self.m_scrollbar_y.config(command=self.m_tree.yview, orient=tk.VERTICAL)
        self.m_scrollbar_x.config(command=self.m_tree.xview, orient=tk.HORIZONTAL)
        self.m_scrollbar_y.update()
        self.m_scrollbar_x.update()

        # 以下代码设置表格的行高
        rowheight = (self.m_height-self.m_scrollbar_x.winfo_height())//row_num
        style = ttk.Style()
        style.configure('Treeview', rowheight=rowheight)  # repace 40 with whatever you need
        self.updata_table_head(self.m_tree_head_l+self.m_tree_head_r, self.m_tree_width.copy())

        self.m_tree.pack(side=tk.LEFT, expand = False)  # 设置表格最大化
        # 鼠标事件注册
        self.m_tree.bind('<Double-1>', self.double_click_row)    # 左键双击
        self.m_tree.bind('<Button-1>', self.single_click_row)    # 左键单击
        # self.m_tree.bind('<<TreeviewSelect>>', selectTree)

    def init_button_list(self, father):
        # 表格的运行、增、删操作按钮
        self.m_button_frame = tk.Frame(father)

        # 运行按钮
        self.run_table_img = ImageTk.PhotoImage( Image.open(self.m_image_path+"running_16x16.ico") )
        # self.run_all_im = tk.PhotoImage(file=self.m_image_path+"running.ico")
        self.m_run_table_button = tk.Button(self.m_button_frame, text="X", image=self.run_table_img,
                                          command = self.run_all_action )
        self.m_run_table_button.pack(side=tk.TOP, fill=tk.X, pady=1)

        # 添加加
        self.add_table_img = ImageTk.PhotoImage( Image.open(self.m_image_path+"+_16x16.ico") )
        self.m_add_table_button = tk.Button(self.m_button_frame, text="X", image=self.add_table_img,
                                          command = self.add_table )
        self.m_add_table_button.pack(side=tk.TOP, fill=tk.X, pady=1)

        # 添加减 (初始化因为没选中行 所以默认按钮关闭使能)
        self.del_table_img = ImageTk.PhotoImage( Image.open(self.m_image_path+"-_16x16.ico") )
        self.m_del_table_button = tk.Button(self.m_button_frame, text="X", image=self.del_table_img,
                                          command = self.del_table, state=tk.DISABLED )
        self.m_del_table_button.pack(side=tk.TOP, fill=tk.X, pady=1)

        # 添加设置
        self.set_table_img = ImageTk.PhotoImage( Image.open(self.m_image_path+"setting_16x16.ico") )
        self.m_set_table_button = tk.Button(self.m_button_frame, text="X", image=self.set_table_img,
                                          command = self.set_table )
        self.m_set_table_button.pack(side=tk.TOP, fill=tk.X, pady=1)

        self.m_button_frame.pack(side=tk.RIGHT, fill=tk.Y)

    def run_all_action(self):
        """
        将要执行的内容数据交给引擎，调度引擎将数据发送出去
        :return:
        """
        # 遍历Treeview中所有的行
        for item in self.m_tree.get_children():
            pass
            #self.m_tree.set(item, column=self.task_status_ind, value="已关闭")

    def add_table(self):
        if self.m_double_select_row != None:
            self.m_tree.insert('', int(self.m_double_select_row[1:])-1, values=[500])
        else:
            self.updata_select_row()

    def del_table(self):
        """
        删除双击选中的行
        :return: None
        """
        if None != self.m_double_select_row:
            self.m_tree.delete(self.m_double_select_row)  # 删除双击选中的行
        self.m_double_select_row = None
        self.m_del_table_button["state"] = tk.DISABLED  # 设置删除按钮不可按

    def set_table(self):
        pass

    def run_one_action(self):
        """
        将要执行的内容数据交给引擎，让其调度将数据发送出去
        :return:
        """
        pass

    def single_click_row(self, event):
        """
        单选表格行的时候
        :param event: 单击事件
        :return: None
        """
        x, y, widget = event.x, event.y, event.widget
        item = widget.item(widget.focus())
        itemText = item['text']
        itemValues = item['values']
        iid = widget.identify_row(y)
        column = event.widget.identify_column(x)
        print ('\n&&&&&&&& def selectItem(self, event):')
        print ('item = ', item)
        print('itemValues = ',itemValues)

        for item in self.m_tree.selection():
            item_text = self.m_tree.item(item, "values")
            print(item_text)
            # if "已关闭" in self.m_tree.item(item, "values")[self.task_status_ind]:
            #     self.m_tree.set(item, column=self.task_status_ind, value="运行中")

        # 将要更新进各个模型控件的数值交给引擎
        self.m_engine.OnThreadMessage(mh.M_TREETABLE, mh.M_SMMODEL_MANAGER, mh.A_UPDATA_ALL_MODEL_VAL, None)

        self.m_single_select_row = None
        self.m_double_select_row = None

    def double_click_row(self, event):
        """
        双击行之后调用本函数
        :return: None
        """
        select_row = self.m_tree.selection()
        self.m_double_select_row = select_row[0] if len(select_row) != 0 else None
        self.m_del_table_button["state"] = tk.NORMAL  # 设置删除按钮不可按
        self.m_single_select_row = None

    def updata_select_row(self, param=None):
        """
        将param携带的数据一一对应更新到当前选中的行
        :return: 执行的结果
        """
        param = ["1500", "1600", "1700", "1800", "1900", "2000", "2100", "2200"]
        param.insert(0, len(self.m_tree.get_children())+1)
        field_info = param
        taskkey = param[0]
        self.m_tree.insert("", tk.END, text=taskkey, values=field_info)  # 给第末行添加数据，索引值可重复

    def updata_table_head(self, head_list, width_list):
        """
        设置表头属性名称
        :param head_list: 表头名称
        :param width_list: 表头名称对应列的宽度
        :return: None
        """
        remainder = 750-sum( width_list )
        if remainder>0: # 宽度不足时 填充
            width_list.append(remainder)
            head_list.append("None")
        self.m_tree["columns"] = tuple(head_list)
        for col, width in zip(head_list, width_list):
            print(col, width, end=" ")
            self.m_tree.column(col, width=width, anchor=tk.CENTER, stretch=tk.NO)  # 设置列
            self.m_tree.heading(col, text=col)  # 设置显示的表头名

        self.m_tree.update()
        print(self.m_tree.winfo_width())
        print()

    def api(self, action, param = None):
        # 显示从模型管理器那同步过来的数据
        if action == mh.A_UPDATA_TREE_SELECT_ROW:
            self.updata_select_row(param)
        elif action == mh.A_SET_TABLEHEAD:
            print(param)
            num = len(param.items())
            new_tree_width = self.m_tree_width+[50 for cnt in range(num)]
            # 以下记得浅拷贝
            head_list = self.m_tree_head_l.copy()
            for name, model in param.items():
                head_list.append(name)
            self.updata_table_head(head_list+self.m_tree_head_r, new_tree_width)
            print()

    def __del__(self):
        pass
