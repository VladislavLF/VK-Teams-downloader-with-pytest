import os
import pytest
import psutil
import time
from pywinauto import Desktop

def test_installation(install_application):
    """Проверка корректности установки приложения"""
    install_dir = install_application
    exe_path = os.path.join(install_dir, "vkteams.exe")
    assert os.path.exists(exe_path), "Основной исполняемый файл не найден"
    assert os.path.getsize(exe_path) > 1024 * 1024, "Некорректный размер исполняемого файла"

def test_app_launch(app_process):
    """Проверка запуска приложения"""
    time.sleep(3)
    process_running = any(
        "vkteams" in proc.info['name'].lower().replace(" ", "")
        for proc in psutil.process_iter(['name'])
    )
    assert process_running, "Процесс приложения не обнаружен"

    try:
        app = Desktop(backend="uia").window(title_re="VK Teams")
        assert app.exists(timeout=10), "Главное окно приложения не найдено"
        print("Приложение успешно работает")
    finally:
        for proc in psutil.process_iter(['name']):
            if "vkteams" in proc.info['name'].lower().replace(" ", ""):
                proc.kill()
        print("Приложение завершило работу")