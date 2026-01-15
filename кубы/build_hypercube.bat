@echo off
chcp 65001 >nul
echo ╔════════════════════════════════════════════════════════════╗
echo ║     СБОРКА ПРИЛОЖЕНИЯ СИМУЛЯЦИИ СЕТИ ГИПЕРКУБОВ           ║
echo ╚════════════════════════════════════════════════════════════╝
echo.

echo [1/4] Установка зависимостей...
pip install -r requirements.txt
echo.

echo [2/4] Проверка установки PyInstaller...
pip show pyinstaller >nul 2>&1
if errorlevel 1 (
    echo PyInstaller не найден. Устанавливаю...
    pip install pyinstaller
) else (
    echo ✓ PyInstaller уже установлен
)
echo.

echo [3/4] Сборка исполняемого файла...
pyinstaller --onefile --windowed --name="HypercubeSimulator" --icon=NONE --hidden-import=matplotlib --hidden-import=networkx hypercube_gui.py
echo.

echo [4/4] Проверка результата...
if exist "dist\HypercubeSimulator.exe" (
    echo.
    echo ╔════════════════════════════════════════════════════════════╗
    echo ║                  СБОРКА ЗАВЕРШЕНА!                         ║
    echo ╚════════════════════════════════════════════════════════════╝
    echo.
    echo Исполняемый файл: dist\HypercubeSimulator.exe
    echo.
    echo Вы можете запустить приложение из папки dist
) else (
    echo.
    echo ✗ Ошибка при сборке. Проверьте логи выше.
)

echo.
pause
