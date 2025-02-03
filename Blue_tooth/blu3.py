import tkinter as tk
from tkinter import font as tkfont
import socket

class BlueTalksApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("BlueTalks")
        self.geometry("800x600")
        self.configure(bg='black')
        
        self.title_font = tkfont.Font(family='Helvetica', size=36, weight="bold")
        self.subtitle_font = tkfont.Font(family='Helvetica', size=24, weight="normal")
        self.button_font = tkfont.Font(family='Helvetica', size=14, weight="bold")
        self.custom_font = tkfont.Font(family='Helvetica', size=18, weight="normal")
        
        self.client_name = ""  # Initialize client_name attribute
        self.client = None  # Initialize client socket attribute
        
        self.frames = {}
        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)
        
        for F in (StartPage, NamePage, DiscoverPage, ChatPage):
            page_name = F.__name__
            frame = F(parent=container, controller=self)
            self.frames[page_name] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        
        self.show_frame("StartPage")
    
    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()

class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(bg='black')

        title_label = tk.Label(self, text="BlueTalks", font=controller.title_font, fg='white', bg='black')
        title_label.place(x=50, y=50)

        subtitle_label = tk.Label(self, text="A Bluetooth Chat Application", font=controller.subtitle_font, fg='white', bg='black')
        subtitle_label.place(x=55, y=120)

        get_started_button = tk.Button(self, text="GET STARTED", font=controller.button_font, fg='black', bg='yellow', command=lambda: controller.show_frame("NamePage"))
        get_started_button.place(x=55, y=180)

class NamePage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(bg='black')

        logo = tk.Label(self, text="BlueTalks", fg="white", bg="black", font=controller.custom_font)
        logo.place(x=20, y=20)

        name_label = tk.Label(self, text="Enter your Name", fg="white", bg="black", font=controller.custom_font)
        name_label.place(x=20, y=200)

        self.name_entry = tk.Entry(self, font=controller.custom_font)
        self.name_entry.place(x=20, y=250, width=400, height=50)

        next_button = tk.Button(self, text="NEXT", command=self.on_next, bg="yellow", font=controller.custom_font)
        next_button.place(x=20, y=320, width=150, height=50)

    def on_next(self):
        name = self.name_entry.get().strip()
        if name:
            self.controller.client_name = name  # Save the name in the controller
            print(f"Name entered: {name}")
            self.controller.show_frame("DiscoverPage")
        else:
            print("Please enter a valid name.")

class DiscoverPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(bg='black')

        logo = tk.Label(self, text="BlueTalks", fg="white", bg="black", font=controller.custom_font)
        logo.place(x=20, y=20)

        discover_label = tk.Label(self, text="DISCOVER NEARBY DEVICES", fg="white", bg="black", font=controller.custom_font)
        discover_label.place(x=20, y=200)

        self.server_ip_entry = tk.Entry(self, font=controller.custom_font)
        self.server_ip_entry.place(x=20, y=250, width=400, height=50)

        search_button = tk.Button(self, text="CONNECT TO SERVER", command=self.connect_to_server, bg="black", fg="white", highlightbackground="yellow", font=controller.custom_font)
        search_button.place(x=20, y=320, width=300, height=50)

        next_button = tk.Button(self, text="NEXT", command=lambda: controller.show_frame("ChatPage"), bg="yellow", font=controller.custom_font)
        next_button.place(x=20, y=380, width=150, height=50)

    def connect_to_server(self):
        server_ip = self.server_ip_entry.get().strip()
        if server_ip:
            self.controller.server_ip = server_ip
            print(f"Attempting to connect to server at IP: {server_ip}")
            try:
                self.controller.client = socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM)
                self.controller.client.connect((server_ip, 4))  # Adjust the port number if needed
                self.controller.client.setblocking(False)  # Set the socket to non-blocking mode
                print("Connected to server:", server_ip)
                self.controller.show_frame("ChatPage")
                self.controller.frames["ChatPage"].check_for_messages()  # Start checking for messages
            except Exception as e:
                print("Error connecting to server:", e)
        else:
            print("Please enter a valid server IP address.")

class ChatPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.configure(bg="#000000")

        header = tk.Frame(self, bg="#000000")
        header.pack(fill=tk.X)

        logo = tk.Label(header, text="BlueTalks", fg="#FFFFFF", bg="#000000", font=("Helvetica", 16, "bold"))
        logo.pack(side=tk.LEFT, padx=10, pady=10)

        logout_button = tk.Button(header, text="Logout", command=self.logout, bg="#000000", fg="#FFFFFF")
        logout_button.pack(side=tk.RIGHT, padx=10, pady=10)

        client_frame = tk.Frame(self, bg="#776E6E")
        client_frame.pack(fill=tk.X)

        self.received_label = tk.Label(self, text="", bg="#FAF6D4", font=("Helvetica", 12), wraplength=500)
        self.received_label.pack(fill=tk.X, padx=10, pady=10)

        entry_frame = tk.Frame(self, bg="#FAF6D4")
        entry_frame.pack(fill=tk.X, padx=10, pady=10)

        self.entry = tk.Entry(entry_frame, font=("Helvetica", 12), width=50)
        self.entry.pack(side=tk.LEFT, padx=5, pady=5)

        send_button = tk.Button(entry_frame, text="Send", font=("Helvetica", 12), bg="#000000", fg="#FFFFFF", command=self.send_message)
        send_button.pack(side=tk.RIGHT, padx=5, pady=5)
        receive_button = tk.Button(entry_frame, text="Send", font=("Helvetica", 12), bg="#000000", fg="#FFFFFF", command=self.check_for_messages)
        receive_button.pack(side=tk.RIGHT, padx=10, pady=5)
        self.client_name_label = tk.Label(client_frame, text=self.controller.client_name, bg="#776E6E", fg="#FFFFFF", font=("Helvetica", 12))
        self.client_name_label.pack(side=tk.LEFT, padx=10, pady=10)

    def send_message(self):
        message = self.entry.get().strip()
        if message:
            try:
                self.controller.client.send(message.encode("utf-8"))
                self.entry.delete(0, tk.END)
                self.display_message("You", message)
            except Exception as e:
                print(f"Error sending message: {e}")
        else:
            print("Please enter a message to send.")

    def check_for_messages(self):
        if self.controller.client:
            try:
                data = self.controller.client.recv(1024)
                if data:
                    message = data.decode("utf-8")
                    self.display_message("Server", message)
            except BlockingIOError:
                pass  # No data received
            except Exception as e:
                print(f"Error receiving message: {e}")

        self.after(4000, self.check_for_messages)  # Schedule this method to be called again after 1 second

    def display_message(self, sender, message):
        current_messages = self.received_label.cget("text")
        new_message = f"{sender}: {message}\n"
        updated_message = current_messages + new_message
        self.received_label.config(text=updated_message)

    def logout(self):
        print("Logging out...")
        if self.controller.client:
            self.controller.client.close()
        self.controller.show_frame("StartPage")

if __name__ == "__main__":
    app = BlueTalksApp()
    app.mainloop()
