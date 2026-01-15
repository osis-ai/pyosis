import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import time
import threading
import queue
import sys

class ThreadedChatInterface(threading.Thread):
    """
    线程化的聊天界面类
    可以在独立线程中运行，不阻塞主程序
    """
    
    def __init__(self, on_send_message=None, window_title="AI 设计助手"):
        super().__init__()
        self.daemon = True  # 设置为守护线程，主程序退出时自动结束
        
        # 回调函数，用于外部获取用户消息
        self.on_send_message = on_send_message
        self.window_title = window_title
        
        # 当前流式输出的消息ID
        self.current_stream_id = None
        
        # 命令队列 - 用于线程间通信
        self.command_queue = queue.Queue()
        
        # UI组件将在run方法中初始化
        self.root = None
        self.main_frame = None
        self.chat_area = None
        self.input_var = None
        self.input_entry = None
        self.send_button = None
        
        # 用于安全关闭的标志
        self._is_running = True
        
        # 启动线程
        self.start()
    
    def run(self):
        """线程主函数，运行Tkinter主循环"""
        try:
            self.root = tk.Tk()
            self.root.title(self.window_title)
            self.root.geometry("700x600+200+200")
            self.root.configure(bg='#f0f0f0')
            self.root.protocol("WM_DELETE_WINDOW", self._on_closing)
            
            # 创建主框架
            self.main_frame = ttk.Frame(self.root, padding="10")
            self.main_frame.pack(fill=tk.BOTH, expand=True)
            
            # 创建UI组件
            self._create_chat_area()
            self._create_input_area()
            
            # # 添加初始消息
            # self._add_initial_messages()
            
            # 启动命令处理循环
            self._process_commands()
            
            # 运行Tkinter主循环
            self.root.mainloop()
            
        except Exception as e:
            print(f"UI线程发生错误: {e}")
        finally:
            self._cleanup()
    
    def _create_chat_area(self):
        """创建聊天区域"""
        chat_frame = ttk.Frame(self.main_frame)
        chat_frame.pack(fill=tk.BOTH, expand=True)
        
        # 创建滚动文本框
        self.chat_area = scrolledtext.ScrolledText(
            chat_frame, 
            wrap=tk.WORD, 
            width=60, 
            height=20,
            font=("微软雅黑", 10),
            state=tk.DISABLED,
            borderwidth=0,
            highlightthickness=0,
            bg='#fafafa'
        )
        self.chat_area.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # 配置标签样式
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
        
        self.chat_area.tag_configure("user_timestamp", 
                                    foreground="gray", 
                                    font=("微软雅黑", 8),
                                    background="#e3f2fd",
                                    justify='left')
        
        self.chat_area.tag_configure("ai_timestamp", 
                                    foreground="gray", 
                                    font=("微软雅黑", 8),
                                    background="#f5f5f5",
                                    justify='left')
    
    def _create_input_area(self):
        """创建输入区域"""
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
        self.input_entry.bind("<Return>", lambda event: self._send_message())
        
        # 创建发送按钮
        self.send_button = ttk.Button(
            input_frame, 
            text="发送", 
            command=self._send_message
        )
        self.send_button.pack(side=tk.RIGHT)
    
    # def _add_initial_messages(self):
    #     """添加初始欢迎消息"""
    #     welcome_message = "您好！我是AI设计助手，请问有什么可以帮助您的？"
    #     self._add_message(welcome_message, "ai")
    
    def _send_message(self):
        """处理发送消息"""
        message = self.input_var.get().strip()
        if not message:
            return
        
        # 添加用户消息到聊天区域
        self._add_message(message, "user")
        
        # 清空输入框
        self.input_var.set("")
        
        # 如果有回调函数，则调用
        if self.on_send_message:
            # 在线程中执行回调，避免阻塞UI
            threading.Thread(
                target=self._safe_callback,
                args=(self.on_send_message, message),
                daemon=True
            ).start()
    
    def _safe_callback(self, callback, *args):
        """安全执行回调函数"""
        try:
            callback(*args)
        except Exception as e:
            print(f"回调函数执行错误: {e}")
    
    def _add_message(self, message, sender):
        """内部方法：添加消息到聊天区域"""
        if not self.root:
            return
            
        self.chat_area.config(state=tk.NORMAL)
        
        # 添加时间戳
        timestamp = time.strftime("%H:%M:%S")
        
        # 添加消息和时间戳
        if sender == "user":
            self.chat_area.insert(tk.END, f"[{timestamp}] ", "user_timestamp")
            self.chat_area.insert(tk.END, f"你: {message}\n\n", "user")
        else:
            self.chat_area.insert(tk.END, f"[{timestamp}] ", "ai_timestamp")
            self.chat_area.insert(tk.END, f"AI: {message}\n\n", "ai")
        
        self.chat_area.config(state=tk.DISABLED)
        self.chat_area.see(tk.END)
    
    def _start_ai_stream(self, stream_id=None):
        """内部方法：开始AI流式输出"""
        if not self.root:
            return None
            
        self.chat_area.config(state=tk.NORMAL)
        
        # 使用传入的stream_id或生成新的
        if stream_id is None:
            stream_id = f"stream_{int(time.time()*1000)}"
        
        self.current_stream_id = stream_id
        
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
        
        return stream_id
    
    def _update_ai_stream(self, text_chunk, stream_id=None):
        """内部方法：更新流式输出的内容"""
        if not self.root:
            return
            
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
    
    def _end_ai_stream(self, stream_id=None):
        """内部方法：结束流式输出"""
        if not self.root:
            return
            
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
    
    def _add_ai_response(self, message):
        """内部方法：添加AI回复（非流式）"""
        self._add_message(message, "ai")
    
    def _process_commands(self):
        """处理命令队列"""
        if not self.root:
            return
            
        try:
            while True:
                # 从队列获取命令
                command_data = self.command_queue.get_nowait()
                self._execute_command(command_data)
        except queue.Empty:
            pass
        finally:
            # 继续检查新命令
            if self._is_running and self.root:
                self.root.after(100, self._process_commands)
    
    def _execute_command(self, command_data):
        """执行命令"""
        if not self.root:
            return
            
        try:
            command, *args = command_data
            
            if command == "add_message":
                message, sender = args
                self._add_message(message, sender)
                
            elif command == "add_ai_response":
                message, = args
                self._add_message(message, "ai")
                
            elif command == "start_ai_stream":
                stream_id = args[0] if args else None
                result = self._start_ai_stream(stream_id)
                # 如果需要返回结果，可以放入结果队列
                
            elif command == "update_ai_stream":
                text_chunk, stream_id = args
                self._update_ai_stream(text_chunk, stream_id)
                
            elif command == "end_ai_stream":
                stream_id = args[0] if args else None
                self._end_ai_stream(stream_id)
                
            elif command == "clear_chat":
                self._clear_chat()
                
            elif command == "resize_window":
                width, height = args
                self.root.geometry(f"{width}x{height}")
                
            elif command == "set_window_position":
                x, y = args
                self.root.geometry(f"+{x}+{y}")
                
            elif command == "set_title":
                title, = args
                self.root.title(title)
                
            elif command == "focus_input":
                self.input_entry.focus_set()
                
            elif command == "show_info":
                title, message = args
                messagebox.showinfo(title, message)
                
            elif command == "show_warning":
                title, message = args
                messagebox.showwarning(title, message)
                
            elif command == "close":
                self._is_running = False
                self.root.quit()
                
        except Exception as e:
            print(f"执行命令时发生错误: {e}")
    
    def _clear_chat(self):
        """清空聊天记录"""
        if not self.root:
            return
            
        self.chat_area.config(state=tk.NORMAL)
        self.chat_area.delete(1.0, tk.END)
        self.chat_area.config(state=tk.DISABLED)
    
    def _on_closing(self):
        """窗口关闭时的处理"""
        self._is_running = False
        self.root.quit()
    
    def _cleanup(self):
        """清理资源"""
        self._is_running = False
    
    # ============ 线程安全的公共方法 ============
    # 以下方法可以从任何线程安全地调用
    
    def add_message(self, message, sender="ai"):
        """
        添加消息到聊天区域
        
        Args:
            message: 消息内容
            sender: 发送者 ("user" 或 "ai")
        """
        self.command_queue.put(("add_message", message, sender))
    
    def add_ai_response(self, message):
        """添加AI回复（非流式）"""
        self.command_queue.put(("add_ai_response", message))
    
    def start_ai_stream(self, stream_id=None):
        """
        开始AI流式输出
        
        Args:
            stream_id: 可选的流ID，如果为None则自动生成
            
        Returns:
            str: 流ID（注意：由于是异步的，可能无法立即获取返回值）
        """
        if stream_id is None:
            stream_id = f"stream_{int(time.time()*1000)}"
        
        self.command_queue.put(("start_ai_stream", stream_id))
        return stream_id
    
    def update_ai_stream(self, text_chunk, stream_id=None):
        """
        更新流式输出的内容
        
        Args:
            text_chunk: 文本块
            stream_id: 流ID，如果为None则使用当前流
        """
        if stream_id is None:
            stream_id = self.current_stream_id
            
        self.command_queue.put(("update_ai_stream", text_chunk, stream_id))
    
    def end_ai_stream(self, stream_id=None):
        """
        结束流式输出
        
        Args:
            stream_id: 流ID，如果为None则使用当前流
        """
        self.command_queue.put(("end_ai_stream", stream_id))
    
    def clear_chat(self):
        """清空聊天记录"""
        self.command_queue.put(("clear_chat",))
    
    def resize_window(self, width, height):
        """调整窗口大小"""
        self.command_queue.put(("resize_window", width, height))
    
    def set_window_position(self, x, y):
        """设置窗口位置"""
        self.command_queue.put(("set_window_position", x, y))
    
    def set_title(self, title):
        """设置窗口标题"""
        self.command_queue.put(("set_title", title))
    
    def focus_input(self):
        """聚焦到输入框"""
        self.command_queue.put(("focus_input",))
    
    def show_info(self, title, message):
        """显示信息对话框"""
        self.command_queue.put(("show_info", title, message))
    
    def show_warning(self, title, message):
        """显示警告对话框"""
        self.command_queue.put(("show_warning", title, message))
    
    def close(self):
        """安全关闭窗口"""
        self.command_queue.put(("close",))
    
    def is_alive(self):
        """检查UI线程是否还在运行"""
        return self._is_running


# 使用示例
def main_example():
    """使用示例"""
    import random
    
    def handle_user_message(message):
        """处理用户消息的回调函数"""
        print(f"收到用户消息: {message}")
        
        # 示例1：直接添加AI回复
        ui.add_ai_response(f"我收到了你的消息: {message}")
        
        # 示例2：模拟流式输出
        stream_id = ui.start_ai_stream()
        
        # 模拟AI思考过程
        responses = [
            "让我思考一下...",
            "这个问题很有趣...",
            "基于我的知识...",
            f"对于 '{message}' 我的回答是..."
        ]
        
        def simulate_streaming():
            for response in responses:
                time.sleep(0.5)
                # 添加一小段文字
                chunk = response + "\n"
                ui.update_ai_stream(chunk, stream_id)
            
            # 最终回答
            final_answer = f"这是我对 '{message}' 的完整回答。\n我认为这是一个很好的问题！"
            time.sleep(0.5)
            ui.update_ai_stream(final_answer, stream_id)
            
            # 结束流式输出
            time.sleep(0.5)
            ui.end_ai_stream(stream_id)
        
        # 在后台线程中模拟流式输出
        threading.Thread(target=simulate_streaming, daemon=True).start()
    
    # 创建线程化UI
    ui = ThreadedChatInterface(
        on_send_message=handle_user_message,
        window_title="AI助手聊天窗口"
    )
    
    print("UI已启动在主线程外运行...")
    print("主程序可以继续执行其他任务，不会被UI阻塞")
    
    # 主程序可以继续执行其他任务
    try:
        count = 0
        while ui.is_alive():
            # 模拟主程序的其他工作
            count += 1
            print(f"主程序正在工作... 循环 {count}")
            
            # # 每3秒向UI发送一个自动消息
            # if count % 3 == 0:
            #     auto_msg = f"系统通知 #{count}: 一切正常"
            #     ui.add_ai_response(auto_msg)
            
            # # 每5秒改变窗口大小（演示线程安全操作）
            # if count % 5 == 0:
            #     width = 700 + random.randint(-50, 50)
            #     height = 600 + random.randint(-50, 50)
            #     ui.resize_window(width, height)
            
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\n正在关闭...")
        ui.close()


if __name__ == "__main__":
    main_example()