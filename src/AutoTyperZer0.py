#!/usr/bin/env python3
import flet as ft
import keyboard
import time
import threading
import subprocess
import sys
import re

APP_VERSION = "v1.0 Beta 2"


def auto_typer(text, typing_speed, super_fast):
    if super_fast:
        keyboard.write(text)
    else:
        for char in text:
            keyboard.write(char)
            time.sleep(typing_speed)

def main(page: ft.Page):
    page.window_width = 500
    page.window_height = 635
    page.window_resizable = False
    page.title = "Auto Typer Zer0"
    page.padding = 10
    page.bgcolor = "#1e1e1e"
    page.theme = ft.Theme(font_family="Consolas")

    def open_settings(e):
        settings_window = ft.AlertDialog(
            title=ft.Text("Settings"),
            content=ft.Text(f"App Version: {APP_VERSION}"),
            actions=[
                ft.TextButton(
                    "Close",
                    on_click=lambda _: setattr(settings_window, "open", False) or page.update(),
                )
            ],
        )
        page.dialog = settings_window
        settings_window.open = True
        page.update()


    # Start typing
    def on_start_click(e):
        text = text_field.value.strip()
        if not text:
            page.snack_bar = ft.SnackBar(ft.Text("Please enter some text to auto-type!"))
            page.snack_bar.open = True
            page.update()
            return
        
        try:
            delay = int(delay_field.value)
            typing_speed = float(speed_field.value)
        except ValueError:
            page.snack_bar = ft.SnackBar(ft.Text("Invalid delay or speed values!"))
            page.snack_bar.open = True
            page.update()
            return

        def countdown_task():
            for i in range(delay, 0, -1):
                print(f"Starting in {i} seconds...")
                time.sleep(1)
            auto_typer(text, typing_speed, super_fast_check.value)

        threading.Thread(target=countdown_task, daemon=True).start()

    def update_ui_for_language(e):
        lang = language_dropdown.value
        remove_comments_button.visible = lang in ["Python", "Java", "C/C++"]
        remove_indent_button.visible = lang != "Text"
        page.update()

    def remove_comments(e):
        lang = language_dropdown.value
        text = text_field.value

        if lang == "Python":
            cleaned_text = re.sub(r'(?<!print\()[ \t]*#.*$', '', text, flags=re.MULTILINE)
        elif lang == "Java":
            cleaned_text = re.sub(r'(?<!System\.out\.print\()[ \t]*//.*$', '', text, flags=re.MULTILINE)
            cleaned_text = re.sub(r'(?<!System\.out\.print\()[ \t]*/\*.*?\*/', '', cleaned_text, flags=re.DOTALL)
        elif lang == "C/C++":
            cleaned_text = re.sub(r'(?<!cout\()[ \t]*//.*$', '', text, flags=re.MULTILINE)
            cleaned_text = re.sub(r'(?<!cout\()[ \t]*/\*.*?\*/', '', cleaned_text, flags=re.DOTALL)
        else:
            cleaned_text = text
        
        text_field.value = cleaned_text
        page.update()

    def remove_indentation(e):
        text = text_field.value
        unindented_text = "\n".join(line.lstrip() for line in text.splitlines())
        text_field.value = unindented_text
        page.update()

    # Layouts and UI elements
    header = ft.Text(
        "@RBLakshya - AutoTyperZer0",
        color="#ff79c6",
        size=18,
        weight="bold",
        expand=True,
        text_align="left",
    )
    page.add(header)

    text_field = ft.TextField(
        multiline=True,
        expand=False,
        height=200,
        width=480,
        bgcolor="#282a36",
        color="#f8f8f2",
        border_radius=8,
        border_color="#6272a4",
        text_style=ft.TextStyle(font_family="Consolas"),
    )

    delay_field = ft.TextField(
        label="Start Delay (seconds):",
        value="5",
        width=200,
        bgcolor="#44475a",
        color="#f8f8f2",
        border_radius=8,
    )
    speed_field = ft.TextField(
        label="Typing Speed:",
        value="0.01",
        width=200,
        bgcolor="#44475a",
        color="#f8f8f2",
        border_radius=8,
    )
    language_dropdown = ft.Dropdown(
        label="Select Mode:",
        options=[
            ft.dropdown.Option("Text"),
            ft.dropdown.Option("Python"),
            ft.dropdown.Option("Java"),
            ft.dropdown.Option("C/C++"),
        ],
        bgcolor="#44475a",
        color="#f8f8f2",
        border_radius=8,
        on_change=update_ui_for_language,
    )

    super_fast_check = ft.Checkbox(
        label="Super Fast Mode",
        value=False,
        fill_color="#ff79c6",
        check_color="#282a36",
    )

    remove_comments_button = ft.ElevatedButton(
        text="Remove Comments", on_click=remove_comments, visible=False
    )
    remove_indent_button = ft.ElevatedButton(
        text="Remove Indentation", on_click=remove_indentation, visible=False
    )

    clear_button = ft.OutlinedButton(
        text="Clear Text",
        on_click=lambda e: setattr(text_field, "value", ""),
        style=ft.ButtonStyle(
            color="#ff5555", shape=ft.RoundedRectangleBorder(radius=8)
        ),
    )
    copy_button = ft.OutlinedButton(
        text="Copy Text",
        on_click=lambda e: page.set_clipboard(text_field.value),
        style=ft.ButtonStyle(
            color="#50fa7b", shape=ft.RoundedRectangleBorder(radius=8)
        ),
    )
    start_button = ft.ElevatedButton(
        text="Start Typing",
        on_click=on_start_click,
        style=ft.ButtonStyle(
            color="#f8f8f2", bgcolor="#50fa7b", shape=ft.RoundedRectangleBorder(radius=8)
        ),
    )
    stop_button = ft.ElevatedButton(
        text="Stop Typing",
        on_click=lambda e: keyboard.unhook_all(),
        style=ft.ButtonStyle(
            color="#f8f8f2", bgcolor="#ff5555", shape=ft.RoundedRectangleBorder(radius=8)
        ),
    )

    # Settings Icon
    settings_icon = ft.IconButton(
        icon=ft.icons.SETTINGS,
        on_click=open_settings,
        tooltip="Settings",
        icon_color="#f8f8f2",
    )

    page.add(
        ft.Row(
            [
                ft.Container(width=450, alignment=ft.alignment.center, content=header),
                settings_icon,
            ],
            alignment="spaceBetween",
        ),
        text_field,
        ft.Row([clear_button, copy_button], alignment="center", spacing=10),
        ft.Row([delay_field, speed_field], alignment="center", spacing=10),
        ft.Row([super_fast_check], alignment="center"),
        ft.Row(
            [
                ft.Column([remove_comments_button, remove_indent_button], spacing=5),
                ft.Column([start_button, stop_button], spacing=5),
            ],
            alignment="center",
        ),
        language_dropdown,
    )

ft.app(target=main)
