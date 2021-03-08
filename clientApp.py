import tkinter as tk
from client import Client


class ClientApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        for F in (StartPage, PageMain):
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
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.client = Client
        tk.Label(self, text="Messagerie config:").grid(row=0, column=0)
        tk.Label(self, text="username:").grid(row=1, column=0)
        tk.Label(self, text="server:").grid(row=2, column=0)
        tk.Label(self, text="port:").grid(row=3, column=0)

        self.entryUsername = tk.Entry(self)
        self.entryUsername.grid(row=1, column=1)
        self.entryServer = tk.Entry(self)
        self.entryServer.grid(row=2, column=1)
        self.entryPort = tk.Entry(self)
        self.entryPort.grid(row=3, column=1)
        button = tk.Button(self, text="valider", command=lambda: self.validateConfig({
            'username': self.entryUsername.get(),
            'server': self.entryServer.get(),
            'port': int(self.entryPort.get())
        }))
        button.grid(row=4, column=0, columnspan=2)

    def validateConfig(self, data):
        self.client.receive_data(data)
        self.controller.show_frame("PageMain")


class PageMain(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        self.controller = controller
        self.client = Client
        messages = tk.Text(self, width=50)
        messages.grid(row=0, column=0, padx=10, pady=10)

        self.entryMessage = tk.Entry(self, width=50)
        self.entryMessage.insert(0, "Votre message")
        self.entryMessage.grid(row=1, column=0, padx=10, pady=10)

        def send_message(data):
            clientMessage = data['msg']
            messages.insert('1.0', "\n" + "You: " + clientMessage)
            self.client.receive_message(data, clientMessage)

        btnSendMessage = tk.Button(self, text="Send", width=20, command=lambda: send_message({
            'msg': self.entryMessage.get()
        }))
        btnSendMessage.grid(row=1, column=1, padx=10, pady=10)


if __name__ == '__main__':
    ClientApp().mainloop()
