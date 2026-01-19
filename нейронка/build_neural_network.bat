@echo off
chcp 65001 >nul
echo ================================================
echo   Сборка приложения "Нейронная сеть"
echo ================================================
echo.

REM Удаляем старые файлы сборки
if exist build rmdir /s /q build
if exist dist rmdir /s /q dist
if exist NeuralNetwork.spec del /q NeuralNetwork.spec

echo 🔨 Сборка исполняемого файла...
echo.

pyinstaller --noconfirm ^
    --onefile ^
    --windowed ^
    --name "NeuralNetwork" ^
    --icon=NONE ^
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
echo 📁 Исполняемый файл: dist\NeuralNetwork.exe
echo.
pause
