import tkinter as tk
from tkinter import ttk, scrolledtext
import time
import threading
import queue

class ChatInterface:
    def __init__(self, root, on_send_message=None):
        self.root = root
        self.root.title("AI 设计助手")
        self.root.geometry("700x600+200+200")
        self.root.configure(bg='#f0f0f0')
        
        # 回调函数，用于外部获取用户消息
        self.on_send_message = on_send_message
        
        # 当前流式输出的消息ID
        self.current_stream_id = None
        
        # 窗口命令队列 - 用于接收来自其他线程的窗口操作命令
        self.window_command_queue = queue.Queue()
        
        # 创建主框架
        #self.root.overrideredirect(True)

        # 创建一个框架作为窗口的内容区域，并填充整个窗口
        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # 移除了标题标签
        
        # 创建聊天区域
        self.create_chat_area()
        
        # 创建输入区域
        self.create_input_area()
        
        # 添加初始消息
        self.add_initial_messages()
        
        # 启动窗口命令处理循环
        self.root.after(100, self.process_window_commands)

        # self.root = root
        # self.root.title("AI 设计助手")
        # self.root.geometry("700x600")  # 修改窗口大小
        # self.root.configure(bg='#f0f0f0')
        
        # # 回调函数，用于外部获取用户消息
        # self.on_send_message = on_send_message
        
        # # 当前流式输出的消息ID
        # self.current_stream_id = None
        
        # # 创建主框架
        # self.main_frame = ttk.Frame(root, padding="10")
        # self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # # 移除了标题标签
        
        # # 创建聊天区域
        # self.create_chat_area()
        
        # # 创建输入区域
        # self.create_input_area()
        
        # # 添加初始消息
        # self.add_initial_messages()
    
    def create_chat_area(self):
        # 创建聊天框架
        chat_frame = ttk.Frame(self.main_frame)
        chat_frame.pack(fill=tk.BOTH, expand=True)
        
        # 创建滚动文本框 - 去掉边框
        self.chat_area = scrolledtext.ScrolledText(
            chat_frame, 
            wrap=tk.WORD, 
            width=60, 
            height=20,
            font=("微软雅黑", 10),
            state=tk.DISABLED,
            borderwidth=0,  # 去掉边框
            highlightthickness=0,  # 去掉高亮边框
            bg='#fafafa'  # 设置背景色
        )
        self.chat_area.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # 配置标签样式
        # 用户消息 - 靠左显示，蓝色背景
        self.chat_area.tag_configure("user", 
                                    background="#e3f2fd", 
                                    relief="flat", 
                                    borderwidth=0,
                                    justify='left',
                                    lmargin1=10,
                                    lmargin2=10,
                                    rmargin=10,
                                    spacing1=5,
                                    spacing3=5)
        
        # AI消息 - 靠左显示，灰色背景
        self.chat_area.tag_configure("ai", 
                                    background="#f5f5f5", 
                                    relief="flat", 
                                    borderwidth=0,
                                    justify='left',
                                    lmargin1=10,
                                    lmargin2=10,
                                    rmargin=10,
                                    spacing1=5,
                                    spacing3=5)
        
        # 流式AI消息 - 用于实时显示AI回复
        self.chat_area.tag_configure("ai_streaming", 
                                    background="#f5f5f5", 
                                    relief="flat", 
                                    borderwidth=0,
                                    justify='left',
                                    lmargin1=10,
                                    lmargin2=10,
                                    rmargin=10,
                                    spacing1=5,
                                    spacing3=5)
        
        # 时间戳 - 与消息背景一致
        self.chat_area.tag_configure("user_timestamp", 
                                    foreground="gray", 
                                    font=("微软雅黑", 8),
                                    background="#e3f2fd",  # 与用户消息背景一致
                                    justify='left')
        
        self.chat_area.tag_configure("ai_timestamp", 
                                    foreground="gray", 
                                    font=("微软雅黑", 8),
                                    background="#f5f5f5",  # 与AI消息背景一致
                                    justify='left')
    
    def create_input_area(self):
        # 创建输入框架
        input_frame = ttk.Frame(self.main_frame)
        input_frame.pack(fill=tk.X, pady=10)
        
        # 创建输入框
        self.input_var = tk.StringVar()
        self.input_entry = ttk.Entry(
            input_frame, 
            textvariable=self.input_var,
            font=("微软雅黑", 10)
        )
        self.input_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        
        # 绑定回车键发送消息
        self.input_entry.bind("<Return>", lambda event: self.send_message())
        
        # 创建发送按钮
        self.send_button = ttk.Button(
            input_frame, 
            text="发送", 
            command=self.send_message
        )
        self.send_button.pack(side=tk.RIGHT)
    
    def add_initial_messages(self):
        # 添加欢迎消息
        welcome_message = "您好！我是AI设计助手，请问有什么可以帮助您的？"
        self.add_message(welcome_message, "ai")
    
    def send_message(self):
        message = self.input_var.get().strip()
        if not message:
            return
        
        # 添加用户消息到聊天区域
        self.add_message(message, "user")
        
        # 清空输入框
        self.input_var.set("")
        
        # 如果有回调函数，则调用
        if self.on_send_message:
            self.on_send_message(message)
    
    def add_message(self, message, sender):
        self.chat_area.config(state=tk.NORMAL)
        
        # 添加时间戳
        timestamp = time.strftime("%H:%M:%S")
        
        # 添加消息和时间戳
        if sender == "user":
            # 用户消息靠左显示
            self.chat_area.insert(tk.END, f"[{timestamp}] ", "user_timestamp")
            self.chat_area.insert(tk.END, f"你: {message}\n\n", "user")
        else:
            # AI消息靠左显示
            self.chat_area.insert(tk.END, f"[{timestamp}] ", "ai_timestamp")
            self.chat_area.insert(tk.END, f"AI: {message}\n\n", "ai")
        
        self.chat_area.config(state=tk.DISABLED)
        self.chat_area.see(tk.END)
    
    def start_ai_stream(self):
        """开始AI流式输出，返回一个消息ID用于后续更新"""
        self.chat_area.config(state=tk.NORMAL)
        
        # 生成唯一消息ID
        self.current_stream_id = f"stream_{int(time.time()*1000)}"
        
        # 添加时间戳和AI前缀
        timestamp = time.strftime("%H:%M:%S")
        self.chat_area.insert(tk.END, f"[{timestamp}] ", "ai_timestamp")
        self.chat_area.insert(tk.END, "AI: ", "ai_streaming")
        
        # 标记流式输出的开始位置
        stream_start = self.chat_area.index(tk.END)
        self.chat_area.mark_set(self.current_stream_id, stream_start)
        self.chat_area.mark_gravity(self.current_stream_id, tk.LEFT)
        
        self.chat_area.config(state=tk.DISABLED)
        self.chat_area.see(tk.END)
        
        return self.current_stream_id
    
    def update_ai_stream(self, text_chunk, stream_id=None):
        """更新流式输出的内容"""
        if stream_id is None:
            stream_id = self.current_stream_id
            
        if stream_id is None:
            return
            
        self.chat_area.config(state=tk.NORMAL)
        
        # 在流式输出位置插入新的文本块
        current_pos = self.chat_area.index(stream_id)
        self.chat_area.insert(current_pos, text_chunk, "ai_streaming")
        
        # 更新标记位置
        self.chat_area.mark_set(stream_id, self.chat_area.index(tk.END))
        
        self.chat_area.config(state=tk.DISABLED)
        self.chat_area.see(tk.END)
    
    def end_ai_stream(self, stream_id=None):
        """结束流式输出，添加换行并清理标记"""
        if stream_id is None:
            stream_id = self.current_stream_id
            
        if stream_id is None:
            return
            
        self.chat_area.config(state=tk.NORMAL)
        
        # 添加换行
        current_pos = self.chat_area.index(stream_id)
        self.chat_area.insert(current_pos, "\n\n", "ai_streaming")
        
        # 删除标记
        self.chat_area.mark_unset(stream_id)
        self.current_stream_id = None
        
        self.chat_area.config(state=tk.DISABLED)
        self.chat_area.see(tk.END)
    
    def add_ai_response(self, message):
        """外部调用此方法添加AI回复（非流式）"""
        self.add_message(message, "ai")

    # ============ 新增方法：窗口命令处理 ============
    
    def process_window_commands(self):
        """处理来自其他线程的窗口命令"""
        try:
            while True:
                # 从队列获取命令
                command, *args = self.window_command_queue.get_nowait()
                
                if command == "resize_window":
                    # 修改窗口大小
                    width, height = args
                    self.root.geometry(f"{width}x{height}")
                    print(f"窗口大小已修改为: {width}x{height}")

                elif command == "set_window_position":
                    # 修改窗口位置
                    x, y = args
                    self.root.geometry(f"+{x}+{y}")
                    print(f"窗口位置已修改为: x={x}, y={y}")
            
                elif command == "close_window":
                    # 关闭窗口
                    self.root.quit()
                    print("窗口关闭命令已接收")

                # elif command == "id":
                #     # 返回窗口ID
                #     window_id = str(self.root.winfo_id())
                #     print(f"窗口ID: {window_id}")
                #     return window_id
                
        except queue.Empty:
            # 队列为空，继续等待
            pass
        finally:
            # 继续检查新命令
            self.root.after(100, self.process_window_commands)
    
    # ============ 线程安全的方法 ============
    
    def queue_window_command(self, command, *args):
        """
        线程安全的方法：将窗口命令放入队列
        这个方法可以从任何线程安全地调用
        """
        self.window_command_queue.put((command, *args))
        return True
    
    def resize_window(self, width, height):
        """
        线程安全的方法：修改窗口大小
        从其他线程调用此方法
        """
        return self.queue_window_command("resize_window", width, height)

    def set_window_position(self, x, y):
        """
        线程安全的方法：设置窗口位置
        从其他线程调用此方法
        """
        return self.queue_window_command("set_window_position", x, y)
 
    def close_window(self):
        """
        线程安全的方法：关闭窗口
        从其他线程调用此方法
        """
        return self.queue_window_command("close_window")

# 示例使用
if __name__ == "__main__":
    def handle_user_message(message):
        # 模拟流式输出
        stream_id = chat_interface.start_ai_stream()
        
        # 模拟AI回复的文本
        ai_response = "AI思考中..."
        
        # 在单独的线程中模拟流式输出
        def stream_response():
            lines = ai_response.split('\n')
            for line in lines:
                # 模拟处理延迟
                time.sleep(0.5)
                # 在主线程中更新UI
                root.after(0, lambda: chat_interface.update_ai_stream(line + '\n', stream_id))
            
            # 流式输出结束
            root.after(0, lambda: chat_interface.end_ai_stream(stream_id))
        
        # 启动流式输出线程
        threading.Thread(target=stream_response, daemon=True).start()
    
    root = tk.Tk()
    chat_interface = ChatInterface(root, on_send_message=handle_user_message)
    root.mainloop()