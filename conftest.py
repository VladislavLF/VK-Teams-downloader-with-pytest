import pytest
import os
import subprocess
import time
import requests
from pywinauto import Desktop
import keyboard

@pytest.fixture(scope="session")
def download_installer():
    """Скачивает установщик приложения с проверкой целостности"""
    url = "https://vkteams-www.hb.bizmrg.com/win/x64/vkteamssetup.exe"
    installer_path = os.path.join(os.getcwd(), "vkteamssetup.exe")

    if not os.path.exists(installer_path):
        print("Скачивание установщика...")
        response = requests.get(url, stream=True)
        response.raise_for_status()

        with open(installer_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

        print("Установщик поставлен успешно")

    if os.path.getsize(installer_path) < 1024 * 1024:
        os.remove(installer_path)
        pytest.fail("Установочный файл слишком мал или поврежден")

    return installer_path


@pytest.fixture(scope="session")
def install_application(download_installer, request):
    """Устанавливает приложение и возвращает путь установки"""
    installer_path = download_installer
    install_dir = fr"C:\Users\{os.getenv('username')}\AppData\Local\Programs\VK Teams"

    if os.path.exists(install_dir):
        print("Приложение уже установлено, пропускаем установку")
        return install_dir

    print("Запуск установки...")
    try:
        process = subprocess.Popen(
            [installer_path, '/SILENT', '/NORESTART', '/ALLUSERS'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=True
        )
        time.sleep(3)
        keyboard.press_and_release("enter")
        timeout = 300
        try:
            process.wait(timeout=timeout)
        except subprocess.TimeoutExpired:
            process.kill()
            pytest.fail(f"Установка не завершилась за {timeout} секунд")

        if process.returncode != 0:
            pytest.fail(f"Установка завершилась с кодом {process.returncode}")

        exe_path = os.path.join(install_dir, "vkteams.exe")
        wait_time = 60
        start_time = time.time()
        while not os.path.exists(exe_path):
            if time.time() - start_time > wait_time:
                pytest.fail(f"Файлы приложения не появились за {wait_time} секунд")
            time.sleep(3)

    except Exception as e:
        pytest.fail(f"Ошибка при установке: {str(e)}")

    print("Приложение установлено")

    return install_dir


@pytest.fixture
def app_process(install_application):
    """Запускает приложение и возвращает процесс"""
    install_dir = install_application
    exe_path = os.path.join(install_dir, "vkteams.exe")

    try:
        process = subprocess.Popen(exe_path)
        time.sleep(30)
        print("Приложение запущено")
        return process
    except Exception as e:
        pytest.fail(f"Не удалось запустить приложение: {str(e)}")