from tkinter import *
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from database.connect_db import *
class EditWindow:
    def __init__(self, connection, table, parent):
        self.connection = connection
        self.table = table  # Таблица из родительского окна
        self.parent = parent  # Ссылка на родительское окно
        self.cursor = self.connection.cursor()
    def correct_edit_window(self):
        self.connection = connection
        self.cursor = self.connection.cursor()
        select_row = self.table.focus()
        if not select_row:
            messagebox.showerror("Ошибка", "Запись не выбрана")
            return
        client_data = self.table.item(select_row)['values']
        self.connection = connection
        self.cursor = self.connection.cursor()
        self.add_clients = tk.Toplevel()
        self.add_clients.geometry("600x580+100+10")
        self.add_clients.minsize(650, 580)
        self.add_clients.maxsize(1200, 1040)
        self.add_clients.resizable(True, True)
        self.add_clients.attributes('-topmost', True)

         # Главный фрейм для содержимого (растягивается)
        main_frame = tk.Frame(self.add_clients)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Фрейм для формы (растягивается с отступами)
        form_frame = tk.Frame(main_frame)
        form_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Создаем все виджеты с возможностью растяжения
        self.last_name_label = tk.Label(form_frame, text="Фамилия", font=('Arial', 13))
        self.last_name_label.pack(pady=5, anchor='w')
        self.last_name_entry = tk.Entry(form_frame, font=('Arial', 13))
        self.last_name_entry.insert(0, client_data[1])
        self.last_name_entry.pack(fill=tk.X, pady=5, ipady=5)

        self.firt_name_label = tk.Label(form_frame, text="Имя", font=('Arial', 13))
        self.firt_name_label.pack(pady=5, anchor='w')
        self.first_name_entry = tk.Entry(form_frame, font=('Arial', 13))
        self.first_name_entry.insert(0, client_data[2])
        self.first_name_entry.pack(fill=tk.X, pady=5, ipady=5)

        self.father_name_label = tk.Label(form_frame, text="Отчество", font=('Arial', 13))
        self.father_name_label.pack(pady=5, anchor='w')
        self.father_name_entry = tk.Entry(form_frame, font=('Arial', 13))
        self.father_name_entry.insert(0, client_data[3])
        self.father_name_entry.pack(fill=tk.X, pady=5, ipady=5)

        self.number_phone_label = tk.Label(form_frame, text="Номер телефона", font=('Arial', 13))
        self.number_phone_label.pack(pady=5, anchor='w')
        self.number_phone_entry = tk.Entry(form_frame, font=('Arial', 13))
        self.number_phone_entry.insert(0, client_data[4])
        self.number_phone_entry.pack(fill=tk.X, pady=5, ipady=5)
        def validate_phone(new_text):
            allowed_chars = '+0123456789'
            for char in new_text:
                if char not in allowed_chars:
                    return False
            return True
        
        vcmd = (self.add_clients.register(validate_phone), '%P')
        self.number_phone_entry.config(validate='key', validatecommand=vcmd)
        self.number_phone_entry.insert(0, '+')
        

        self.login_label = tk.Label(form_frame, text="Логин", font=('Arial', 13))
        self.login_label.pack(pady=5, anchor='w')
        self.login_entry = tk.Entry(form_frame, font=('Arial', 13))
        self.login_entry.insert(0, client_data[5])
        self.login_entry.pack(fill=tk.X, pady=5, ipady=5)
        self.login_entry.config(state=tk.DISABLED)

        self.password_label = tk.Label(form_frame, text="Пароль", font=('Arial', 13))
        self.password_label.pack(pady=5, anchor='w')
        self.password_entry = tk.Entry(form_frame, font=('Arial', 13))
        self.password_entry.insert(0, client_data[6])
        self.password_entry.pack(fill=tk.X, pady=5, ipady=5)
        self.password_entry.config(state=tk.DISABLED)
        self.confrim_button = tk.Button(form_frame, text="Изменить", font=('Arial', 13), 
        command=self.correct_edit_client)
        self.confrim_button.pack(fill=tk.X, pady=20, ipady=10)
    def correct_edit_client(self):
        last_name = self.last_name_entry.get()
        first_name = self.first_name_entry.get()
        father_name = self.father_name_entry.get()
        phone_number = self.number_phone_entry.get()
        login = self.login_entry.get()
        password = self.password_entry.get()
        if len(last_name) >20 or len(first_name) >20 or len(father_name) > 20:
            messagebox.showerror("Ошибка", "Данные о пользователе не должны превышать 20 символов")
            return
        if not all([last_name, first_name, father_name, phone_number, login, password]):
            messagebox.showerror("Ошибка", "Все поля должны быть заполнены")
            return
        if len(phone_number) != 12:
            messagebox.showerror("Ошибка", "Номер телефона должен содержать только цифры или не полностью указан номер телефона")
            return            
        request = "UPDATE clients SET lastname= %s, firstname= %s, fathername= %s, phonenumber= %s, pass_client =%s WHERE login_client= %s"
        data = (last_name, first_name, father_name, phone_number, password, login)
        self.cursor.execute(request, data)
        self.connection.commit()
        self.add_clients.destroy()
        self.parent.update_table()
        messagebox.showinfo("Успешно", "Запись о клиенте изменена")