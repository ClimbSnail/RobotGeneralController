# import tkinter as tk
import re
import tkutils as tku
#from tkinter import ttk

class Test():

    def __init__(self, root):
        self.m_tree_head_l = ["编号", "状态", "运行", "移动"] # 表头字段
        self.m_tree_head_r = ["None"]
        self.m_tree_width = [40, 40, 80, 40, 50]   # 列对应的宽度

        # 滑动条
        self.m_scrollbar_y = tk.Scrollbar(root)
        self.m_scrollbar_y.pack(side=tk.RIGHT, fill=tk.Y)
        self.m_scrollbar_x = tk.Scrollbar(root)
        self.m_scrollbar_x.pack(side=tk.BOTTOM, fill=tk.X)
        row_num = 5  # 设置表格显示多少行
        self.m_tree = ttk.Treeview(root, show="headings", height=row_num,
                                   xscrollcommand=self.m_scrollbar_x.set,
                                   yscrollcommand=self.m_scrollbar_y.set,
                                   selectmode=tk.BROWSE)
        self.m_scrollbar_y.config(command=self.m_tree.yview, orient=tk.VERTICAL)
        self.m_scrollbar_x.config(command=self.m_tree.xview, orient=tk.HORIZONTAL)
        self.m_scrollbar_y.update()
        self.m_scrollbar_x.update()
        self.m_tree["columns"] = tuple(self.m_tree_head_l + self.m_tree_head_r)
        # 以下代码设置表格的行高
        rowheight = 20
        style = ttk.Style()
        style.configure('Treeview', rowheight=rowheight)  # repace 40 with whatever you need
        self.updata_table_head(self.m_tree_head_l+self.m_tree_head_r, self.m_tree_width)

        self.m_tree.pack(side=tk.LEFT, expand = True, fill = tk.BOTH)  # 设置表格最大化
        self.updata_table_head(self.m_tree_head_l+["HA"]+self.m_tree_head_r,
                               self.m_tree_width[:2]+[100]+self.m_tree_width[2:])

    def updata_table_head(self, head_list, width_list):
        """
        设置表头属性名称
        :param head_list: 表头名称
        :param width_list: 表头名称对应列的宽度
        :return: None
        """
        head_len = len(head_list)
        # width_list[head_len-1] = self.m_width-sum( width_list[:head_len] )
        print(width_list)
        #self.m_tree.configure(columns=head_list)
        self.m_tree["columns"] = tuple(head_list)
        for col, width in zip(head_list, width_list):
            print(col, width, end=" ")
            self.m_tree.column(col, width=width, anchor="center")  # 设置列
            self.m_tree.heading(col, text=col)  # 设置显示的表头名
        print()

class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        myset = set()
        length = len(s)
        max_len = 0
        start = 0
        end = 0
        for pos in range(length):
            if pos!= 0:
                myset.remove(s[pos-1])
            while end<length and s[end] not in myset :
                myset.add(s[end])
                end += 1
            max_len = max_len if max_len>end-pos else end-pos
        return max_len

if __name__ == "__main__":

    text = Solution()
    print( text.lengthOfLongestSubstring("abcabcbb") )

    root = tk.Tk()  # 创建窗口对象的背景色
    root.title("机器人通用控制平台")           #窗口名
    root.geometry('250x650+10+10')
    root.iconbitmap("./img/favicon_64.ico")  # 窗体图标
    # root.resizable(False, False)  # 设置窗体不可改变大小
    engine = Test(root)
    tku.center_window(root)  # 将窗体移动到屏幕中央
    # 进入消息循环 父窗口进入事件循环，可以理解为保持窗口运行，否则界面不展示
    root.mainloop()

"""


if __name__ == "__main__":
    print("hello")
    pass

"""





