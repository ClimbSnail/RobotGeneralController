import tkinter as tk

root = tk.Tk()  # 创建窗口对象的背景色
root.title("机器人通用控制平台")  # 窗口名

imgBtn = tk.PhotoImage(file = "./img/running.png")
tk.Button(root, image=imgBtn).pack()

tk.mainloop()