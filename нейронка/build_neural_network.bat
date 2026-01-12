@echo off
chcp 65001 >nul
echo ================================================
echo   Сборка приложения "Нейронная сеть"
echo ================================================
echo.

REM Проверка наличия Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python не найден! Установите Python и повторите попытку.
    pause
    exit /b 1
)

echo ✅ Python найден
echo.

REM Установка зависимостей
echo 📦 Установка зависимостей...
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m pip install pyinstaller
echo.

REM Сборка EXE
echo 🔨 Сборка исполняемого файла...
pyinstaller --noconfirm --onefile --windowed ^
    --name "NeuralNetwork" ^
    --add-data "neural_network.py;." ^
    --hidden-import "numpy" ^
    --hidden-import "matplotlib" ^
    --hidden-import "tkinter" ^
    --collect-all matplotlib ^
    neural_network_gui.py

if errorlevel 1 (
    echo.
    echo ❌ Ошибка при сборке!
    pause
    exit /b 1
)

echo.
echo ================================================
echo   ✅ Сборка завершена успешно!
echo ================================================
echo.
echo 📁 Исполняемый файл находится в папке: dist\NeuralNetwork.exe
echo.
pause
