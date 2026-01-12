@echo off
chcp 65001 >nul
echo ========================================
echo Сборка приложения "Поиск клик в графе"
echo ========================================
echo.

REM Проверка наличия Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ОШИБКА: Python не найден!
    echo Установите Python с https://www.python.org/
    pause
    exit /b 1
)

echo [1/4] Установка зависимостей...
python -m pip install --upgrade pip
python -m pip install matplotlib numpy pyinstaller

echo.
echo [2/4] Проверка файлов...
if not exist "clique_finder.py" (
    echo ОШИБКА: Файл clique_finder.py не найден!
    pause
    exit /b 1
)
if not exist "clique_gui.py" (
    echo ОШИБКА: Файл clique_gui.py не найден!
    pause
    exit /b 1
)

echo.
echo [3/4] Сборка приложения с PyInstaller...
echo Это может занять несколько минут...
pyinstaller --onefile --windowed --name="CliqueFinderGUI" --icon=NONE ^
    --add-data "clique_finder.py;." ^
    --hidden-import=matplotlib ^
    --hidden-import=numpy ^
    --hidden-import=tkinter ^
    clique_gui.py

if errorlevel 1 (
    echo.
    echo ОШИБКА при сборке!
    pause
    exit /b 1
)

echo.
echo [4/4] Проверка результата...
if exist "dist\CliqueFinderGUI.exe" (
    echo.
    echo ========================================
    echo ✓ УСПЕШНО!
    echo ========================================
    echo.
    echo Приложение собрано: dist\CliqueFinderGUI.exe
    echo.
    echo Вы можете скопировать этот файл на любой компьютер
    echo с Windows и запустить без установки Python.
    echo.
) else (
    echo.
    echo ОШИБКА: Файл CliqueFinderGUI.exe не создан!
)

pause
