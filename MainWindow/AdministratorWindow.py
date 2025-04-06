from tkinter import *
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from ChildWindow.add_client_window import *
from ChildWindow.correct_edit_window import *
class AdministratorWindow:
    def __init__(self, connection):
        self.connection = connection
        self.cursor = self.connection.cursor()

        self.admin_window = tk.Tk()
        self.admin_window.title("Работа с клиентами")
        self.admin_window.state('zoomed')
        self.admin_window.resizable(False, False)

        self.title_label = tk.Label(self.admin_window, text="Гости", font=('Arial', 15, 'bold'))
        self.title_label.pack(pady=3)

        scrollbar = ttk.Scrollbar(self.admin_window)
        scrollbar.pack(side='right', fill='y')

        request = "SELECT * FROM clients"
        self.cursor.execute(request)
        result = self.cursor.fetchall()

        column_names = [desc[0] for desc in self.cursor.description]
        table = ttk.Treeview(self.admin_window, columns=column_names, show="headings", yscrollcommand=scrollbar.set, height=25)
        scrollbar.config(command=table.yview)
        for colums in column_names:
            table.heading(colums, text=colums)
            table.column(colums, width=100)
        for row in result:
            table.insert('', tk.END, values=row)
        table.pack(expand=True, fill='both')
        self.table = table
        button_frame = tk.Frame(self.admin_window)
        button_frame.pack(side='top', pady=10) 
        
        self.add_button = tk.Button(button_frame, text="Добавить", font=('Arial', 15), command=self.open_add_window)
        self.add_button.pack(side='left', padx=10)
        
        self.unblock_button = tk.Button(button_frame, font=13, text="Снять блокировку", 
                                     activebackground='#65158a', command=self.unblock_client)
        self.unblock_button.pack(side='left', padx=10)
        
        self.edit_button = tk.Button(button_frame, font=13, text="Изменить запись", 
                                  activebackground='#65158a', command=self.open_edit_window)
        self.edit_button.pack(side='left', padx=10)
        
        button_frame.pack_configure(anchor='center')

    
    def update_table(self):
        for item in self.table.get_children():
            self.table.delete(item)
        
        request = "SELECT * FROM clients"
        self.cursor.execute(request)
        result = self.cursor.fetchall()
        
        for row in result:
            self.table.insert('', tk.END, values=row)
        
    def unblock_client(self):
        select_row = self.table.focus()
        client_data = self.table.item(select_row)['values']
        client_id = client_data[0]
        requst = "UPDATE clients SET status_block = False WHERE idclient = %s"
        self.cursor.execute(requst, (client_id,))
        self.connection.commit()
        self.update_table()
        messagebox.showinfo("Успех", "Клиент разблокирован")
    def open_add_window(self):
        add_window = AddclientWindow(self.connection, self)
        add_window.add_client_window()

    def open_edit_window(self):
        edit_window = EditWindow(self.connection, self.table, self)
        edit_window.correct_edit_window()