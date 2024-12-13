import tkinter as tk
from tkinter import messagebox, filedialog, ttk
import sqlite3
import csv

# Класс для управления базой данных
class HotelDatabase:
    def __init__(self, db_filepath='hotel_db.sqlite'):
        self.conn = sqlite3.connect(db_filepath)  #подключение к базе данных через библиотеку sqlite3
        self.create_table()

    def create_table(self):  #функция создания таблицы, если она еще не существует (с помощью sql) СЛОЖНОСТЬ: О(1)
        cursor = self.conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS rooms (
                Room_ID TEXT PRIMARY KEY,
                Room_Type TEXT,
                Price REAL,
                Room_Count INTEGER,
                Amenities TEXT,
                Status TEXT
            )
        ''')
        self.conn.commit()

    def add_record(self, record):  #функция добавления записи, тк я использовала sql-запрос и кортеж для передачи параметров в sql запрос, то такая структура позволяет добавлять номер за О(1) просто по индексу room_id в случае, если нет конфликтов
        cursor = self.conn.cursor()

        # сначала проверяем, существует ли такая комната уже в нашей таблице, если да-выдаем предупреждение, если нет-добавляем запись
        cursor.execute('''
            SELECT COUNT(*) FROM rooms WHERE Room_ID = ?
        ''', (record['Room_ID'],))

        exists = cursor.fetchone()[0] > 0

        if exists:
            return False  # запись уже существует

        # если запись не существует, добавляем новую
        cursor.execute('''
            INSERT INTO rooms (Room_ID, Room_Type, Price, Room_Count, Amenities, Status)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (record['Room_ID'], record['Room_Type'], record['Price'],
              record['Room_Count'], record['Amenities'], record['Status']))
        self.conn.commit()
        return True

    def delete_record(self, room_id):    #функция удаления комнаты по room_id, сложность O(logn) за счет функции delete
        cursor = self.conn.cursor()
        cursor.execute('DELETE FROM rooms WHERE Room_ID = ?', (room_id,))
        self.conn.commit()
        return cursor.rowcount > 0

    def search_records(self, room_id):    #поиск комнаты по room_id сложность O(1)
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM rooms WHERE Room_ID = ?', (room_id,))
        return cursor.fetchone()

    def update_record(self, record):      #функция обновления уже существующей информации по комнате, параметры передаются в кортеж
        cursor = self.conn.cursor()
        cursor.execute('''
            UPDATE rooms
            SET Room_Type = ?, Price = ?, Room_Count = ?, Amenities = ?, Status = ?
            WHERE Room_ID = ?
        ''', (record['Room_Type'], record['Price'], record['Room_Count'],
              record['Amenities'], record['Status'], record['Room_ID']))
        self.conn.commit()

    def load_rooms(self):                 #выгружаем все комнаты в GUI для удобного просмотра
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM rooms')
        return cursor.fetchall()

    def export_to_csv(self, csv_filename): #экспортируем данные в cvs-файл
        cursor = self.conn.cursor()
        cursor.execute('SELECT * FROM rooms')
        rows = cursor.fetchall()

        with open(csv_filename, 'w', newline='', encoding='utf-8') as csvfile: #открытие файла на запись с кодировкой файла в UTF-8 для поддержки символов, не входящих в стандартный ASCII.
            fieldnames = ['Room_ID', 'Room_Type', 'Price', 'Room_Count', 'Amenities', 'Status']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for row in rows:
                writer.writerow(dict(zip(fieldnames, row)))

    def import_from_csv(self, csv_filename):  #импорт данных из cvs-файла
        cursor = self.conn.cursor()
        with open(csv_filename, 'r', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                try:
                    self.add_record(row)
                except sqlite3.IntegrityError:
                    continue  #пропускаем записи с повторяющимися room_id
        self.conn.commit()

    def close(self):  #закрытие соединения с бд
        self.conn.close()

# основное приложение
class HotelDatabaseApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Hotel Database Management")
        self.db = HotelDatabase()
        self.create_widgets()

    def create_widgets(self):
        #поля ввода
        self.room_id_var = tk.StringVar()  #создание переменной StringVar для хранения значения, введенного в поле
        self.room_type_var = tk.StringVar()
        self.price_var = tk.StringVar()
        self.room_count_var = tk.StringVar()
        self.amenities_var = tk.StringVar()
        self.status_var = tk.StringVar()

        tk.Label(self.root, text="Room ID").grid(row=0, column=0)   #метка (Label) с текстом "Room ID" и размещение её на сетке 0*0
        tk.Entry(self.root, textvariable=self.room_id_var).grid(row=0, column=1) #поля ввода (Entry) для ввода значения room id, кот связано с переменной self.room_id_var

        tk.Label(self.root, text="Room Type").grid(row=1, column=0)
        tk.Entry(self.root, textvariable=self.room_type_var).grid(row=1, column=1)

        tk.Label(self.root, text="Price").grid(row=2, column=0)
        tk.Entry(self.root, textvariable=self.price_var).grid(row=2, column=1)

        tk.Label(self.root, text="Room Count").grid(row=3, column=0)
        tk.Entry(self.root, textvariable=self.room_count_var).grid(row=3, column=1)

        tk.Label(self.root, text="Amenities").grid(row=4, column=0)
        tk.Entry(self.root, textvariable=self.amenities_var).grid(row=4, column=1)

        tk.Label(self.root, text="Status").grid(row=5, column=0)
        tk.Entry(self.root, textvariable=self.status_var).grid(row=5, column=1)

        #кнопки
        tk.Button(self.root, text="Add Record", command=self.add_record).grid(row=6, column=0)
        tk.Button(self.root, text="Delete Record", command=self.delete_record).grid(row=6, column=1)
        tk.Button(self.root, text="Search Record", command=self.search_record).grid(row=7, column=0)
        tk.Button(self.root, text="Update Record", command=self.update_record).grid(row=7, column=1)
        tk.Button(self.root, text="Export to CSV", command=self.export_to_csv).grid(row=8, column=0)
        tk.Button(self.root, text="Import from CSV", command=self.import_from_csv).grid(row=8, column=1)
        tk.Button(self.root, text="Load Rooms", command=self.load_rooms).grid(row=9, column=0)

        #таблица для отображения всех комнат и дальнейшей работы с функцией load_room
        self.tree = ttk.Treeview(self.root, columns=('Room_ID', 'Room_Type', 'Price', 'Room_Count', 'Amenities', 'Status'), show='headings')
        self.tree.heading('Room_ID', text='Room ID')
        self.tree.heading('Room_Type', text='Room Type')
        self.tree.heading('Price', text='Price')
        self.tree.heading('Room_Count', text='Room Count')
        self.tree.heading('Amenities', text='Amenities')
        self.tree.heading('Status', text='Status')
        self.tree.grid(row=10, column=0, columnspan=2)

    def add_record(self):    #добавление комнаты
        record = {     #словарь
            'Room_ID': self.room_id_var.get(),
            'Room_Type': self.room_type_var.get(),
            'Price': self.price_var.get(),
            'Room_Count': self.room_count_var.get(),
            'Amenities': self.amenities_var.get(),
            'Status': self.status_var.get()
        }

        if self.db.add_record(record):
            messagebox.showinfo("Success", "Record added successfully.")
        else:
            messagebox.showwarning("Warning", "A record with this Room_ID already exists.")

        self.clear_entries()
        self.load_rooms()

    def delete_record(self):  #удаление комнаты
        room_id = self.room_id_var.get()
        if self.db.delete_record(room_id):
            messagebox.showinfo("Success", "Record deleted successfully.")
        else:
            messagebox.showwarning("Warning", "No record found with the given Room ID.")
        self.clear_entries()
        self.load_rooms()

    def search_record(self):   #поиск комнаты
        room_id = self.room_id_var.get()
        record = self.db.search_records(room_id)
        if record:
            messagebox.showinfo("Result", f"Record found: {record}")
        else:
            messagebox.showinfo("Result", "No record found with the given Room ID.")
        self.clear_entries()

    def update_record(self):  #обновление данных об уже существующей комнате
        record = {
            'Room_ID': self.room_id_var.get(),
            'Room_Type': self.room_type_var.get(),
            'Price': self.price_var.get(),
            'Room_Count': self.room_count_var.get(),
            'Amenities': self.amenities_var.get(),
            'Status': self.status_var.get()
        }
        self.db.update_record(record)
        messagebox.showinfo("Success", "Record updated successfully.")
        self.clear_entries()
        self.load_rooms()

    def load_rooms(self):  #выгрузка текущих данных в gui
        for i in self.tree.get_children():
            self.tree.delete(i)

        for record in self.db.load_rooms():
            self.tree.insert('', 'end', values=record)

    def export_to_csv(self):   #экспорт данных в csv
        csv_filename = filedialog.asksaveasfilename(title="Save CSV File", defaultextension=".csv",
                                                     filetypes=[("CSV files", "*.csv")])
        if csv_filename:
            self.db.export_to_csv(csv_filename)
            messagebox.showinfo("Success", "Database exported to CSV successfully.")

    def import_from_csv(self):   #импорт данных из csv
        csv_filename = filedialog.askopenfilename(title="Select CSV File", filetypes=[("CSV files", "*.csv")])
        if csv_filename:
            self.db.import_from_csv(csv_filename)
            messagebox.showinfo("Success", "Database imported from CSV successfully.")
            self.load_rooms()

    def clear_entries(self):   #очищает все поля ввода
        self.room_id_var.set("")
        self.room_type_var.set("")
        self.price_var.set("")
        self.room_count_var.set("")
        self.amenities_var.set("")
        self.status_var.set("")

    def on_closing(self):   #вызывается при закрытии окна приложения
        self.db.close()
        self.root.destroy()

root = tk.Tk()    #Tk-главное окно приложения
app = HotelDatabaseApp(root)  #создание нового экземпляра класса
root.protocol("WM_DELETE_WINDOW", app.on_closing)   #обработка закрытия окна
root.mainloop()   #для взаимодействия пользователя с интерфейсом
