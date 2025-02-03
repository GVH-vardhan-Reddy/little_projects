import tkinter as tk
from tkinter import font as tkfont
import socket
import threading
import queue

class BlueTalksServerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("BlueTalks Server")
        self.geometry("800x600")
        self.configure(bg='black')
        
        self.title_font = tkfont.Font(family='Helvetica', size=36, weight="bold")
        self.subtitle_font = tkfont.Font(family='Helvetica', size=24, weight="normal")
        self.button_font = tkfont.Font(family='Helvetica', size=14, weight="bold")
        self.custom_font = tkfont.Font(family='Helvetica', size=18, weight="normal")
        
        self.server = None
        self.client_socket = None
        self.server_address = "40:1A:58:6B:D5:5E"
        self.server_port = 4
        
        self.frames = {}
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        
        for F in (StartPage, ChatPage):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        
        self.show_frame("StartPage")
    
    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

    def start_server(self):
        try:
            self.server = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
            self.server.bind((self.server_address, self.server_port))
            self.server.listen(1)
            print("Waiting for connection...")
            self.client_socket, client_address = self.server.accept()
            print(f"Accepted connection from {client_address}")
            self.show_frame("ChatPage")
            self.receive_messages()
        except Exception as e:
            print(f"Error starting server: {e}")

    def receive_messages(self):
        self.message_queue = queue.Queue()
        threading.Thread(target=self._receive_messages).start()
        self.after(100, self.process_messages)

    def _receive_messages(self):
        try:
            while True:
                data = self.client_socket.recv(1024)
                if not data:
                    break
                message = data.decode('utf-8')
                self.message_queue.put((message, "Client"))
        except Exception as e:
            print(f"An error occurred: {e}")

    def process_messages(self):
        try:
            while not self.message_queue.empty():
                message, sender = self.message_queue.get()
                self.frames["ChatPage"].display_message(sender, message)
            self.after(100, self.process_messages)
        except Exception as e:
            print(f"Error processing messages: {e}")

class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(bg='black')

        title_label = tk.Label(self, text="BlueTalks Server", font=controller.title_font, fg='white', bg='black')
        title_label.place(x=50, y=50)

        subtitle_label = tk.Label(self, text="A Bluetooth Chat Server", font=controller.subtitle_font, fg='white', bg='black')
        subtitle_label.place(x=55, y=120)

        start_server_button = tk.Button(self, text="START SERVER", font=controller.button_font, fg='black', bg='yellow', command=controller.start_server)
        start_server_button.place(x=55, y=180)

class ChatPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(bg="#000000")

        header = tk.Frame(self, bg="#000000")
        header.pack(fill=tk.X)

        logo = tk.Label(header, text="BlueTalks Server", fg="#FFFFFF", bg="#000000", font=("Helvetica", 16, "bold"))
        logo.pack(side=tk.LEFT, padx=10, pady=10)

        logout_button = tk.Button(header, text="Logout", command=self.logout, bg="#000000", fg="#FFFFFF")
        logout_button.pack(side=tk.RIGHT, padx=10, pady=10)

        self.received_label = tk.Label(self, text="", bg="#FAF6D4", font=("Helvetica", 12), wraplength=500)
        self.received_label.pack(fill=tk.X, padx=10, pady=10)

        entry_frame = tk.Frame(self, bg="#FAF6D4")
        entry_frame.pack(fill=tk.X, padx=10, pady=10)

        self.entry = tk.Entry(entry_frame, font=("Helvetica", 12), width=50)
        self.entry.pack(side=tk.LEFT, padx=5, pady=5)

        send_button= tk.Button(entry_frame, text="Send", font=("Helvetica", 12), bg="#000000", fg="#FFFFFF", command=self.send_message)
        send_button.pack(side=tk.RIGHT, padx=5, pady=5)

    def send_message(self):
        message = self.entry.get().strip()
        if message:
            try:
                self.controller.client_socket.send(message.encode("utf-8"))
                self.entry.delete(0, tk.END)
                self.display_message("Server", message)
            except Exception as e:
                print(f"Error sending message: {e}")
        else:
            print("Please enter a message to send.")

    def display_message(self, sender, message):
        current_messages = self.received_label.cget("text")
        new_message = f"{sender}: {message}\n"
        updated_message = current_messages + new_message
        self.received_label.config(text=updated_message)

    def logout(self):
        print("Logging out...")
        if self.controller.client_socket:
            self.controller.client_socket.close()
        if self.controller.server:
            self.controller.server.close()
        self.controller.show_frame("StartPage")

if __name__ == "__main__":
    app = BlueTalksServerApp()
    app.mainloop()