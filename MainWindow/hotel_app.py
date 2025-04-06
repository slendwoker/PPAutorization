from tkinter import *
import tkinter as tk
from tkinter import messagebox
from database.connect_db import *
from MainWindow.AdministratorWindow import *
from ChildWindow.changePassword import *

class AuthorizationApp:
    def __init__(self):
        self.connection = connection
        if self.connection:
            print("Connected")
        self.cursor = self.connection.cursor()
        self.fail_chance ={}
        self.autorization_window = tk.Tk()
        self.autorization_window.title('Авторизация в системе отеля')
        self.autorization_window.state('zoomed')
        self.autorization_window.resizable(False, False)
        # Создаем основной фрейм для центрирования
        main_frame = tk.Frame(self.autorization_window)
        main_frame.pack(expand=True, fill='both')

        label_autorization = tk.Label(main_frame, text="Авторизация",
                                    font=('Arial', 20, 'bold'))
        label_autorization.pack(pady=(50, 20))

        label_login = tk.Label(main_frame, text="Логин",
                                    font=('Arial', 15, 'bold'))
        label_login.pack(pady=(0, 5))
        
        self.edit_login = tk.Entry(main_frame, width=30, font=("Arial", 15))
        self.edit_login.pack(pady=(0, 20))
        
        label_password = tk.Label(main_frame, text="Пароль",
                                    font=('Arial', 15, 'bold'))
        label_password.pack(pady=(0, 5))
        
        self.edit_password = tk.Entry(main_frame, width=30, font=("Arial", 15))
        self.edit_password.pack(pady=(0, 30))

        log_in_button = tk.Button(main_frame, text="Войти", font=13, 
                                 activebackground='#65158a', padx=20, command=self.on_click_btn_login)
        log_in_button.pack()

        self.autorization_window.mainloop()

    def correct_autorization(self, login, password):   
        request = "SELECT pass_client, status_block FROM clients WHERE login_client = %s"
        self.cursor.execute(request, (login,))
        result = self.cursor.fetchone()
        if result is None:
            return False
        password_store, status_block = result
        if status_block:
            return False
        return password == password_store
    
    def correct_autorization_admin(self, login, password):
        request = "SELECT password FROM staffing WHERE login = %s"
        self.cursor.execute(request,(login,))
        result = self.cursor.fetchone()
        if result is None:
            return False
        password_store = result[0]
        return password == password_store



    def on_click_btn_login(self):
        login = self.edit_login.get()
        password = self.edit_password.get()
        self.current_password = password
        self.current_login = login
        
        if not login or not password:
            messagebox.showerror("Ошибка", "Все поля должны быть заполнены")
            return
        if len(login) > 20:
            messagebox.showerror("Ошибка", "Логин не должнен превышать 20 символов")
            return
        if len(password) >8:
            messagebox.showerror("Ошибка", "Пароль не должен превышать 8 символов")
            return
        self.fail_chance[login] = self.fail_chance.get(login, 0) + 1
        
        if self.fail_chance[login] >= 3:
            self.cursor.execute("UPDATE clients SET status_block = TRUE WHERE login_client = %s", (login,))
            self.connection.commit()
            messagebox.showerror("Ошибка", "Учетная запись заблокирована обратитесь к администратору")
            return 
        if self.correct_autorization(login, password):
            messagebox.showinfo("Корректно", "Вы успешно авторизовались")
            ChangePassword(self.current_password, self.current_login, self.connection)
            return

        if self.correct_autorization_admin(login, password):
            messagebox.showinfo("Корректно", "Вы успешно авторизовались")
            self.autorization_window.destroy()
            AdministratorWindow(self.connection)
            return
        messagebox.showerror("Ошибка", "Вы ввели неверный логин или пароль. Пожалуйста проверьте ещё раз введенные данные")
    