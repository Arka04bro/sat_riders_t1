import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import sqlite3
from PIL import Image, ImageTk
import io

# Подключение к БД
conn = sqlite3.connect("space_people.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS crew (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    iin TEXT,
    first_name TEXT,
    last_name TEXT,
    middle_name TEXT,
    gender TEXT,
    date_of_birth TEXT,
    age INTEGER,
    nationality TEXT,
    language_skills TEXT,
    education TEXT,
    military_rank TEXT,
    role TEXT,
    experience_years INTEGER,
    mission_name TEXT,
    mission_start TEXT,
    mission_end TEXT,
    status_in_mission TEXT,
    photo BLOB
)
""")
conn.commit()

# Сохранение фото в BLOB
def image_to_blob(path):
    with open(path, 'rb') as f:
        return f.read()

# Функция для добавления участника
def add_person():
    def save_data():
        data = [e.get() for e in entries]
        if not all(data[:3]):
            messagebox.showerror("Ошибка", "Введите минимум ИИН, имя и фамилию")
            return
        blob = None
        if photo_path.get():
            blob = image_to_blob(photo_path.get())
        cursor.execute("""
            INSERT INTO crew (iin, first_name, last_name, middle_name, gender, date_of_birth,
                              age, nationality, language_skills, education, military_rank,
                              role, experience_years, mission_name, mission_start, mission_end,
                              status_in_mission, photo)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (*data, blob))
        conn.commit()
        messagebox.showinfo("Успех", "Участник добавлен!")
        add_win.destroy()

    add_win = tk.Toplevel(root)
    add_win.title("Добавить участника")
    add_win.geometry("500x800")
    add_win.configure(bg="#0c0c1e")

    fields = ["ИИН", "Имя", "Фамилия", "Отчество", "Пол", "Дата рождения",
              "Возраст", "Гражданство", "Языки", "Образование", "Звание",
              "Роль", "Опыт (лет)", "Миссия", "Начало миссии", "Конец миссии", "Статус"]
    entries = []
    for i, f in enumerate(fields):
        tk.Label(add_win, text=f, bg="#0c0c1e", fg="white").grid(row=i, column=0, pady=3, sticky="w")
        e = tk.Entry(add_win, width=40)
        e.grid(row=i, column=1, pady=3)
        entries.append(e)

    photo_path = tk.StringVar()
    def upload_photo():
        path = filedialog.askopenfilename(filetypes=[("Images", "*.jpg;*.png")])
        if path:
            photo_path.set(path)
            img = Image.open(path).resize((100, 100))
            img_tk = ImageTk.PhotoImage(img)
            photo_label.config(image=img_tk)
            photo_label.image = img_tk

    tk.Button(add_win, text="📸 Загрузить фото", command=upload_photo, bg="#1e1e3f", fg="white").grid(row=len(fields), column=0, pady=5)
    photo_label = tk.Label(add_win, bg="#0c0c1e")
    photo_label.grid(row=len(fields), column=1)

    tk.Button(add_win, text="💾 Сохранить", command=save_data, bg="#2e2e5f", fg="white").grid(row=len(fields)+1, column=0, columnspan=2, pady=10)

# Функция для просмотра участника
def view_person():
    def search():
        iin_value = entry_iin.get()
        cursor.execute("SELECT * FROM crew WHERE iin=?", (iin_value,))
        person = cursor.fetchone()
        if not person:
            messagebox.showerror("Ошибка", "Участник не найден")
            return
        info_text.delete("1.0", tk.END)
        for i, d in enumerate(person[:-1]):
            info_text.insert(tk.END, f"{cursor.description[i][0]}: {d}\n")

        if person[-1]:
            image_data = io.BytesIO(person[-1])
            img = Image.open(image_data).resize((150, 150))
            img_tk = ImageTk.PhotoImage(img)
            photo_label.config(image=img_tk)
            photo_label.image = img_tk

    view_win = tk.Toplevel(root)
    view_win.title("Просмотр участника")
    view_win.geometry("500x700")
    view_win.configure(bg="#0c0c1e")

    tk.Label(view_win, text="Введите ИИН:", bg="#0c0c1e", fg="white").pack(pady=5)
    entry_iin = tk.Entry(view_win, width=30)
    entry_iin.pack(pady=5)
    tk.Button(view_win, text="🔍 Найти", command=search, bg="#1e1e3f", fg="white").pack(pady=5)

    info_text = tk.Text(view_win, height=20, width=55, bg="#1a1a3f", fg="white")
    info_text.pack(pady=5)

    photo_label = tk.Label(view_win, bg="#0c0c1e")
    photo_label.pack(pady=10)

# Главное окно
root = tk.Tk()
root.title("🌌 Space Crew Database")
root.geometry("800x600")

# Фон
bg_image = Image.open(r"C:\Users\Arkats\Downloads\Zvezdnoe-nebo.jpg").resize((800, 600))
bg_photo = ImageTk.PhotoImage(bg_image)
bg_label = tk.Label(root, image=bg_photo)
bg_label.place(x=0, y=0, relwidth=1, relheight=1)

frame = tk.Frame(root, bg="#0c0c1e", bd=10)
frame.place(relx=0.5, rely=0.5, anchor="center")

tk.Label(frame, text="🛰 База данных экипажа", font=("Arial", 18, "bold"), bg="#0c0c1e", fg="white").pack(pady=20)
tk.Button(frame, text="➕ Добавить участника", command=add_person, width=25, bg="#1e1e3f", fg="white").pack(pady=10)
tk.Button(frame, text="🔎 Просмотреть участника", command=view_person, width=25, bg="#1e1e3f", fg="white").pack(pady=10)

root.mainloop()
