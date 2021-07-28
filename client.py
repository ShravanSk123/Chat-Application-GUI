import socket
import threading
import tkinter
import tkinter.scrolledtext
from tkinter import simpledialog

HOST = 'localhost'
PORT = 9090


class Client:

    def __init__(self, host, port):

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((host, port))

        msg = tkinter.Tk()
        msg.withdraw()

        self.username = simpledialog.askstring("username", "Please enter an username", parent=msg)

        self.gui_done = False

        self.running = True

        gui_thread = threading.Thread(target=self.gui_loop)
        receive_thread = threading.Thread(target=self.receive)

        gui_thread.start()
        receive_thread.start()

    def gui_loop(self):  # GUI functionality only
        self.window = tkinter.Tk()
        self.window.configure(bg="lightgray")

        self.chat_label = tkinter.Label(self.window, text="Chat:", bg="lightgray")
        self.chat_label.config(font=("Arial", 14))
        self.chat_label.pack(padx=20, pady=5)

        self.text_area = tkinter.scrolledtext.ScrolledText(self.window)
        self.text_area.pack(padx=20, pady=5)
        self.text_area.config(state='disabled')  # user should not modify history

        self.msg_label = tkinter.Label(self.window, text="Message:", bg="lightgray")
        self.msg_label.config(font=("Arial", 14))
        self.msg_label.pack(padx=20, pady=5)

        self.input_area = tkinter.Text(self.window, height=3)
        self.input_area.pack(padx=20, pady=5)

        self.send_button = tkinter.Button(self.window, text="Send", command=self.write)
        self.send_button.config(font=("Arial", 14))
        self.send_button.pack(padx=20, pady=5)

        self.gui_done = True

        self.window.protocol("WM_DELETE_WINDOW", self.stop)

        self.window.mainloop()

    def write(self):
        message = f"{self.username}: {self.input_area.get('1.0', 'end')}"
        self.sock.send(message.encode('utf-8'))
        self.input_area.delete('1.0', 'end')

    def stop(self):
        self.running = False
        self.window.destroy()
        self.sock.close()
        exit(0)

    def receive(self):
        while self.running:
            try:
                message = self.sock.recv(1024).decode('utf-8')
                if message == "USER":
                    self.sock.send(self.username.encode('utf-8'))
                else:
                    if self.gui_done:
                        self.text_area.config(state='normal')
                        self.text_area.insert('end', message)
                        self.text_area.yview('end')
                        self.text_area.config(state='disabled')
            except ConnectionAbortedError:
                break
            except:
                print("An error occured...")
                self.sock.close()
                break


client = Client(HOST, PORT)
