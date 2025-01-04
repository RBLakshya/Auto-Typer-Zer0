#!/usr/bin/env python3
import flet as ft
import keyboard
import time
import threading
import subprocess
import sys
import re
import requests
from functools import partial
from pynput.keyboard import Key, Controller

# Application version and OS
APP_VERSION = "v1.0"
#OS = "Windows"
OS = "macOS"

keyboard = Controller()

def auto_typer(text, typing_speed, super_fast):
    if super_fast:
        keyboard.type(text)
    else:
        for char in text:
            keyboard.press(char)
            keyboard.release(char)
            time.sleep(typing_speed)
            
def auto_typer_code(text, typing_speed, super_fast, OS, stop_flag):
    lines = text.splitlines()
    for line in lines:
        if stop_flag.is_set():
            break

        if super_fast:
            # Type the entire line at once in super-fast mode
            keyboard.type(line)
        else:
            for char in line:
                keyboard.press(char)
                keyboard.release(char)
                if stop_flag.is_set():
                    break
                time.sleep(typing_speed)        
        keyboard.press(Key.enter)
        keyboard.release(Key.enter)

        if OS == "Windows":
            keyboard.press(Key.space)
            keyboard.release(Key.space)
            time.sleep(0.01)
            keyboard.press(Key.ctrl)
            time.sleep(0.01)
            keyboard.press(Key.backspace)
            time.sleep(0.01)
            keyboard.release(Key.backspace)
            keyboard.release(Key.ctrl)

        elif OS == "macOS":
            keyboard.press(Key.space)
            keyboard.release(Key.space)
            time.sleep(0.01)
            keyboard.press(Key.alt)
            time.sleep(0.01)
            keyboard.press(Key.backspace)
            time.sleep(0.01)
            keyboard.release(Key.backspace)
            keyboard.release(Key.alt)

        if not super_fast:
            time.sleep(typing_speed)

def check_for_updates():
    try:
        url = "https://raw.githubusercontent.com/RBLakshya/Auto-Typer-Zer0/main/README.md"
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            print("Fetched README file successfully.")

            match = re.search(r"AutoTyper Zer0 - V?(\d+\.\d+(\.\d+)?)", response.text, re.IGNORECASE)
            if match:
                latest_version = match.group(1).strip()  # Extract and clean the latest version
                current_version = APP_VERSION.lstrip("Vv").strip()

                print(f"Current version: {current_version}, Latest version: {latest_version}\n")

                # Compare versions
                try:
                    latest_version_tuple = tuple(map(int, latest_version.split('.')))
                    current_version_tuple = tuple(map(int, current_version.split('.')))
                except ValueError as version_error:
                    return f"Error parsing version numbers: {version_error}"

                if latest_version_tuple > current_version_tuple:
                    return f"Update available: V{latest_version}. Get the latest update at GitHub."
                else:
                    return "You are using the latest version."
            else:
                return "Could not find version information in the README file."
        else:
            return f"Failed to check for updates. HTTP Status Code: {response.status_code}"
    except Exception as e:
        return f"Unable to connect to the update server. Error: {e}"

print(check_for_updates())

def main(page: ft.Page):
    global text_field
    if OS == "macOS":
        page.window_width = 500
        page.window_height = 635
    elif OS == "Windows":
        page.window_width = 520
        page.window_height = 665

    page.window_resizable = False
    page.window_maximizable = False
    page.title = f"Auto Typer Zer0 {APP_VERSION} - {OS}"
    page.window_icon = "AT0Icon.ico"
    page.padding = 10
    page.bgcolor = "#1e1e1e"
    page.theme = ft.Theme(font_family="Consolas")

    # Settings window
    expanded_states = [False] * 5

    def open_settings(e):
        update_status = check_for_updates()
        sections = [
            {
                "group_title": "Update Features",
                "items": [
                    {"title": "Release log", "details": "Official Release!\n - Super Speed mode with zero delay\n - Typing modes for Codeing and Codetantra\n - 'Remove Comments' and 'Remove Indentation' added to the code Auto Typing modes."},
                ],
            },
            {
                "group_title": "Tips",
                "items": [
                    {"title": "Codetantra", "details": "Select the coding language required for Codetantra before starting. Click on 'Remove comments' and 'Remove Indentation' once to ensure it works correctly"},
                    {"title": "Random '.' while typing on MacOS", "details": "To Resolve this issue, Open settings, Kryboard>Advanced, and disable double space for full stop/period insertion."},
                ],
            },
        ]

        def toggle_visibility(index):
            for i in range(len(expanded_states)):
                expanded_states[i] = False
            expanded_states[index] = True
            rebuild_content()

        def rebuild_content():
            content_widgets = [
                ft.Text(f"App Version: {APP_VERSION}", width=360, color="#339dfa", size=24),
                ft.Text(update_status, width=360, color="{up_colour}"),
            ]
            section_index = 0
            for group in sections:
                content_widgets.append(ft.Text(group["group_title"], size=16, weight="bold", width=360))

                for item in group["items"]:
                    current_index = section_index
                    content_widgets.append(
                        ft.Column(
                            [
                                ft.Row(
                                    [
                                        ft.Text(item["title"], weight="bold", expand=True),
                                        ft.IconButton(
                                            icon=ft.icons.EXPAND_MORE if not expanded_states[current_index] else ft.icons.EXPAND_LESS,
                                            on_click=lambda e, i=current_index: toggle_visibility(i),
                                        ),
                                    ],
                                    alignment="spaceBetween",
                                ),
                                ft.Text(
                                    item["details"],
                                    visible=expanded_states[current_index],
                                    color="#c1c1c1",
                                    width=360,
                                ),
                            ],
                            spacing=5,
                        )
                    )
                    section_index += 1

            content_widgets.append(
                ft.Row(
                    [
                        ft.TextButton(
                            "GitHub",
                            on_click=lambda _: page.launch_url("https://github.com/RBLakshya/Auto-Typer-Zer0"),
                            style=ft.ButtonStyle(color="#007bff"),
                        )
                    ],
                    alignment="end",
                )
            )

            settings_window.content = ft.Column(content_widgets, spacing=10, scroll="auto")  # Add scroll here
            page.update()

        settings_window = ft.AlertDialog(
            title=ft.Text("Menu"),
            content=ft.Container(
                content=ft.Column([], spacing=10),
                width=400,
            ),
            actions=[
                ft.TextButton(
                    "Close",
                    on_click=lambda _: setattr(settings_window, "open", False) or page.update(),
                )
            ],
        )

        rebuild_content()

        page.dialog = settings_window
        settings_window.open = True
        page.update()


    stop_flag = threading.Event()
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

        # Disable the start button
        start_button.disabled = True
        start_button.style = ft.ButtonStyle(
            color="#030303",
            bgcolor="#aaaaaa",
            shape=ft.RoundedRectangleBorder(radius=8),
        )
        page.update()
        stop_flag.clear()

        def countdown_task():
            for i in range(delay, 0, -1):
                if stop_flag.is_set():
                    break
                print(f"Starting in {i} seconds...")
                time.sleep(1)

            if not stop_flag.is_set():
                if language_dropdown.value in ["Python", "C/C++", "Java"]:
                    auto_typer_code(text, typing_speed, super_fast_check.value, OS, stop_flag)
                else:
                    auto_typer(text, typing_speed, super_fast_check.value)

            start_button.disabled = False
            start_button.style = ft.ButtonStyle(
                color="#030303",
                bgcolor="#50fa7b",
                shape=ft.RoundedRectangleBorder(radius=8),
            )
            page.update()

        threading.Thread(target=countdown_task, daemon=True).start()


    def stop_typing(e):
        stop_flag.set()

    def update_ui_for_language(e):
        lang = language_dropdown.value
        remove_comments_button.visible = lang in ["Python", "Java", "C/C++"]
        remove_indent_button.visible = lang in ["Java", "C/C++"]
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
        "    @RBLakshya - AutoTyperZer0",
        font_family="Consolas",
        color="#6200ff",
        size=18,
        weight="bold",  
        expand=True,
        #text_align="left",
    )
    #page.add(header)

    text_field = ft.TextField(
        multiline=True,
        expand=False,
        height=200,
        width=500,
        bgcolor="#282a36",
        color="#f8f8f2",
        border_radius=8,
        border_color="#6272a4",
        text_style=ft.TextStyle(font_family="Consolas"),
        helper_text="Enter the text/code in one or multiple lines."
    )
    def clear_text():
        text_field.value = ""
        page.update()
        
    delay_field = ft.TextField(
        #icon=ft.icons.TIMER_SHARP,
        label="Start Delay:",
        value="5",
        width=150,
        bgcolor="#282a36",
        color="#f8f8f2",
        border_radius=4,
        border_color="#6272a4",
    )
    speed_field = ft.TextField(
        label="Typing Speed (seconds/char):",
        value="0.01",
        width=150,
        bgcolor="#282a36",
        color="#f8f8f2",
        border_radius=8,
        border_color="#6272a4",
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
        border_color="#c1bfc5",
        color="#f8f8f2",
        border_radius=8,
        on_change=update_ui_for_language,
    )

    super_fast_check = ft.Checkbox(
        label="Super Fast Mode",
        value=False,
        fill_color="#81b2b7",
        check_color="#6200ff",
    )

    remove_comments_button = ft.ElevatedButton(
        text="Remove Comments",
        on_click=remove_comments,
        visible=False,
        width=190,
        style=ft.ButtonStyle(
            color="#110825", bgcolor="#006fbf",
        ),
    )
    remove_indent_button = ft.ElevatedButton(
        text="Remove Indentation",
        on_click=remove_indentation,
        visible=False,
        width=190,
        style=ft.ButtonStyle(
            color="#110825", bgcolor="#006fbf",
        ),
    )
    clear_button = ft.OutlinedButton(
        text="Clear Text",
        width=150,
        on_click=lambda e: clear_text(),
        style=ft.ButtonStyle(
            color="#ff5555", shape=ft.RoundedRectangleBorder(radius=8)
        ),
    )
    copy_button = ft.OutlinedButton(
        text="Copy Text",
        width=150,
        on_click=lambda e: page.set_clipboard(text_field.value),
        style=ft.ButtonStyle(
            color="#50defa", shape=ft.RoundedRectangleBorder(radius=8)
        ),
    )
    start_button = ft.ElevatedButton(
        text="Start Typing",
        on_click=on_start_click,
        width=190,
        style=ft.ButtonStyle(
            color="#030303", bgcolor="#50fa7b", shape=ft.RoundedRectangleBorder(radius=8),
        ),
    )
    stop_button = ft.ElevatedButton(
        text="Stop Typing",
        on_click=stop_typing,
        width=190,
        style=ft.ButtonStyle(
            color="#000000", bgcolor="#ff5555", shape=ft.RoundedRectangleBorder(radius=8)
        ),
    )

    settings_icon = ft.IconButton(
        icon=ft.icons.MENU,
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
