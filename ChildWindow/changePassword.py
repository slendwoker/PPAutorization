from tkinter import *
import tkinter as tk
from tkinter import messagebox
class ChangePassword:
    def __init__(self, current_password, current_login, connection):
        self.current_password = current_password
        self.login = current_login
        self.connection = connection
        self.cursor = self.connection.cursor()
        self.password_window = tk.Toplevel()
        self.password_window.title("Смена пароля")
        self.password_window.geometry("500x380+520+300")
        self.password_window.minsize(500, 380)
        self.password_window.maxsize(800, 600)
        self.password_window.resizable(True, True)
        self.password_window.attributes('-topmost', True)

        # Главный фрейм для содержимого (растягивается)
        main_frame = tk.Frame(self.password_window)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Фрейм для формы (растягивается с отступами)
        form_frame = tk.Frame(main_frame)
        form_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

        # Текущий пароль
        self.label_current_pass = tk.Label(form_frame, text="Текущий пароль", font=('Arial', 13))
        self.label_current_pass.pack(pady=5, anchor='w')
        self.edit_current_pass = tk.Entry(form_frame, font=('Arial', 13))
        self.edit_current_pass.insert(0, current_password)
        self.edit_current_pass.config(state=DISABLED)
        self.edit_current_pass.pack(fill=tk.X, pady=5, ipady=5)

        # Новый пароль
        self.label_new_pass = tk.Label(form_frame, text="Новый пароль", font=('Arial', 13))
        self.label_new_pass.pack(pady=5, anchor='w')
        self.edit_new_pass = tk.Entry(form_frame, font=('Arial', 13))
        self.edit_new_pass.pack(fill=tk.X, pady=5, ipady=5)

        # Подтверждение пароля
        self.label_proof_pass = tk.Label(form_frame, text="Подтверждение пароля", font=('Arial', 13))
        self.label_proof_pass.pack(pady=5, anchor='w')
        self.edit_proof_pass = tk.Entry(form_frame, font=('Arial', 13))
        self.edit_proof_pass.pack(fill=tk.X, pady=5, ipady=5)

        self.pass_button = tk.Button(self.password_window, font=13, text="Изменить", activebackground='#65158a', padx=20,
                                    command=self.correct_new_password)
        self.pass_button.pack(fill=tk.X, pady=20, ipady=5)
        

    def correct_new_password(self):
        new_pass = self.edit_new_pass.get()
        proof_pass = self.edit_proof_pass.get()
        if new_pass != proof_pass:
            messagebox.showerror("Ошибка", "Пароли не совпадают!")
            return
            
        if new_pass == self.current_password:
            messagebox.showerror("Ошибка", "Новый пароль такой же как старый!")
            return
            
        if len(new_pass) > 8:
            messagebox.showerror("Ошибка", "Пароль должен быть не длиннее 8 символов!")
            return
        request = "UPDATE clients SET pass_client = %s WHERE login_client = %s"
        self.cursor.execute(request,(new_pass, self.login))
        self.connection.commit()
        messagebox.showinfo("Успешно", "Пароль изменен")
        self.password_window.destroy()
