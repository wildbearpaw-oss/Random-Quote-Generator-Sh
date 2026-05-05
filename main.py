import tkinter as tk
from tkinter import messagebox, ttk
import random
import json
import os

# Список цитат: каждая цитата — это словарь с текстом, автором и темой
quotes = [
    {"text": "Знание — сила", "author": "Фрэнсис Бэкон", "topic": "Философия"},
    {"text": "Быть или не быть — вот в чём вопрос", "author": "Уильям Шекспир", "topic": "Литература"},
    {"text": "Жизнь — это то, что происходит с тобой, пока ты строишь другие планы", "author": "Джон Леннон", "topic": "Жизнь"},
    {"text": "Успех — это способность идти от неудачи к неудаче, не теряя энтузиазма", "author": "Уинстон Черчилль", "topic": "Мотивация"}
]

# Файл для сохранения истории
HISTORY_FILE = "history.json"

class QuoteGenerator:
    def __init__(self, root):
        self.root = root
        self.root.title("Генератор случайных цитат")
        self.history = []  # Здесь будем хранить историю цитат
        self.load_history()  # Загружаем историю при запуске

        # Создаём элементы интерфейса
        self.create_widgets()

    def create_widgets(self):
        # Кнопка для генерации цитаты
        self.generate_btn = tk.Button(self.root, text="Сгенерировать цитату", command=self.generate_quote)
        self.generate_btn.pack(pady=10)

        # Поле для отображения цитаты
        self.quote_label = tk.Label(self.root, text="", wraplength=400, justify="left")
        self.quote_label.pack(pady=10)

        # Поле для ввода фильтра по автору
        tk.Label(self.root, text="Фильтр по автору:").pack()
        self.author_entry = tk.Entry(self.root)
        self.author_entry.pack(pady=5)

        # Поле для ввода фильтра по теме
        tk.Label(self.root, text="Фильтр по теме:").pack()
        self.topic_entry = tk.Entry(self.root)
        self.topic_entry.pack(pady=5)

        # Кнопка для применения фильтров
        self.filter_btn = tk.Button(self.root, text="Применить фильтры", command=self.apply_filters)
        self.filter_btn.pack(pady=5)

        # Список для отображения истории
        self.history_listbox = tk.Listbox(self.root, width=60, height=10)
        self.history_listbox.pack(pady=10)

        # Обновляем список истории
        self.update_history_display()

    def generate_quote(self):
        # Выбираем случайную цитату из списка
        quote = random.choice(quotes)
        # Сохраняем её в историю
        self.history.append(quote)
        # Сохраняем историю в файл
        self.save_history()
        # Показываем цитату на экране
        self.show_quote(quote)
        # Обновляем список истории
        self.update_history_display()

    def show_quote(self, quote):
        # Форматируем текст цитаты для отображения
        text = f'"{quote["text"]}"\n— {quote["author"]}\nТема: {quote["topic"]}'
        self.quote_label.config(text=text)

    def save_history(self):
        # Сохраняем историю в JSON-файл
        with open(HISTORY_FILE, 'w', encoding='utf-8') as f:
            json.dump(self.history, f, ensure_ascii=False, indent=4)

    def load_history(self):
        # Загружаем историю из файла, если он существует
        if os.path.exists(HISTORY_FILE):
            with open(HISTORY_FILE, 'r', encoding='utf-8') as f:
                self.history = json.load(f)

    def update_history_display(self):
        # Очищаем список истории
        self.history_listbox.delete(0, tk.END)
        # Добавляем все цитаты из истории в список
        for quote in self.history:
            self.history_listbox.insert(tk.END, f'{quote["text"]} — {quote["author"]}')

    def apply_filters(self):
        # Получаем значения фильтров и убираем лишние пробелы
        author_filter = self.author_entry.get().strip()
        topic_filter = self.topic_entry.get().strip()

        # Проверяем, что хотя бы одно поле заполнено
        if not author_filter and not topic_filter:
            messagebox.showwarning("Внимание", "Введите автора или тему для фильтрации")
            return

        # Если поля заполнены, но содержат только пробелы — тоже ошибка
        if (author_filter == "" and topic_filter != "") or (author_filter != "" and topic_filter == ""):
            # В этом случае хотя бы одно поле непустое, но нужно проверить на пробелы
            if author_filter == " " * len(author_filter) or topic_filter == " " * len(topic_filter):
                messagebox.showwarning("Внимание", "Поля не должны содержать только пробелы")
                return

        # Фильтруем цитаты: ищем совпадения без учёта регистра
        filtered_quotes = []
        for quote in self.history:
            # Проверяем совпадение по автору (если поле заполнено)
            if author_filter and author_filter.lower() in quote["author"].lower():
                filtered_quotes.append(quote)
            # Проверяем совпадение по теме (если поле заполнено и цитата ещё не добавлена)
            elif topic_filter and topic_filter.lower() in quote["topic"].lower() and quote not in filtered_quotes:
                filtered_quotes.append(quote)

        # Очищаем и обновляем список истории с фильтрами
        self.history_listbox.delete(0, tk.END)
        if filtered_quotes:
            for quote in filtered_quotes:
                self.history_listbox.insert(tk.END, f'{quote["text"]} — {quote["author"]}')
        else:
            self.history_listbox.insert(tk.END, "По вашему запросу ничего не найдено")

# Запускаем приложение
if __name__ == "__main__":
    root = tk.Tk()
    app = QuoteGenerator(root)
    root.mainloop()