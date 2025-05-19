import flet as ft
import database_creatorplus as dc
import pandas as pd
import os

# Создание/подключение к базе
db = dc.Database("DB")

# Создание таблицы Partners, если её нет
db.Table.create(
    db, "Partners",
    ["id", "Name", "Family", "Number"],
    ["INTEGER PRIMARY KEY AUTOINCREMENT", "TEXT", "TEXT", "TEXT"]
)

# Импорт данных из Excel, если таблица пуста
def import_data(path_table, name_table):
    df = pd.read_excel(path_table)
    for i in df.values:
        db.Table.write(db, name_table, *i)

if not db.Table.get(db, "Partners"):
    import_data("C:/Users/andre/Desktop/СПОР/Partners.xlsx", "Partners")

# Заголовки таблицы
def get_cols(data):
    return [ft.DataColumn(ft.Text(i)) for i in data]

# Строки таблицы
def get_rows(data):
    return [ft.DataRow([ft.DataCell(ft.Text(str(j))) for j in i]) for i in data]

# Главная функция
def main(page: ft.Page):
    page.fonts = {"Segoe UI": "C:/Windows/Fonts/segoeui.ttf"}
    page.title = "Окно"
    page.window.icon = "C:/Users/andre/Desktop/СПОР/icon.ico"
    page.window.maximized = True
    page.window.resizable = False
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    img = ft.Image(
        width=300,
        height=300,
        fit=ft.ImageFit.CONTAIN,
        src="C:/Users/andre/Desktop/СПОР/app_icon.ico"
    )

    def route_change(route):
        page.views.clear()

        if page.route == "/main":
            page.views.append(
                ft.View(
                    route="/main",
                    controls=[
                        img,
                        ft.ElevatedButton("Продукты", on_click=lambda e: page.go("/Partners"))
                    ],
                    vertical_alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER
                )
            )

        elif page.route == "/Partners":
            error_text = ft.Text("", color="red")

            fields=[ft.TextField(width=100) for i in range(1,len(db.Info.getColumns(db, "Partners")))]
            # Поля ввода
            

            # Таблица — объявляем сначала как пустую, потом наполняем
            Create_teble = ft.DataTable(
                columns=get_cols(db.Info.getColumns(db, "Partners")),
                rows=get_rows(db.Table.get(db, "Partners"))
            )
            # Обновление таблицы
            def update_table():
                Create_teble.columns = get_cols(db.Info.getColumns(db, "Partners"))
                Create_teble.rows = get_rows(db.Table.get(db, "Partners"))
                page.update()

            # Сохранение записи
            def save_data(e):
                args=[field.value for field in fields]
                correct_input=True
                for field in fields:
                    if not field.value:
                        correct_input=False
                if correct_input:
                    db.Table.write(db, "Partners", *args)
                    for field in fields:
                        field.value=""
                    update_table()
                else:
                    error_text.value = "Все поля должны быть заполнены!"
                    page.update()

            # Отображение экрана
            page.views.append(
                ft.View(
                    route="/Partners",
                    controls=[
                        Create_teble,
                        ft.Row(fields),
                        error_text,
                        ft.ElevatedButton("Добавить", on_click=save_data),
                        ft.ElevatedButton("Вернуться на главную", on_click=lambda e: page.go("/main"))
                    ],
                    
                )
            )

        page.update()

    page.on_route_change = route_change
    page.go("/main")

ft.app(main)
    
    

        
       
    
        
        

    
