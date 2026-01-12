@echo off
chcp 65001 >nul
echo ========================================
echo Сборка БЫСТРОЙ версии EXE
echo ========================================
echo.

echo [1/4] Проверка установки PyInstaller...
pip show pyinstaller >nul 2>&1
if errorlevel 1 (
    echo PyInstaller не установлен. Устанавливаем...
    pip install pyinstaller
) else (
    echo ✓ PyInstaller уже установлен
)
echo.

echo [2/4] Проверка зависимостей...
pip install -r requirements.txt
echo.

echo [3/4] Сборка БЫСТРОЙ версии EXE...
echo Это может занять несколько минут...
echo.

REM Удаляем старые файлы сборки
if exist "build" rmdir /s /q build
if exist "dist" rmdir /s /q dist
if exist "StonePartition_Fast.spec" del /q StonePartition_Fast.spec

REM Собираем с дополнительными параметрами для matplotlib
pyinstaller --onefile ^
    --windowed ^
    --name="StonePartition_Fast" ^
    --hidden-import=matplotlib ^
    --hidden-import=matplotlib.backends.backend_tkagg ^
    --hidden-import=PIL ^
    --hidden-import=PIL._tkinter_finder ^
    --collect-data matplotlib ^
    --noconsole ^
    app.py

echo.

echo [4/4] Проверка результата...
if exist "dist\StonePartition_Fast.exe" (
    echo.
    echo ========================================
    echo ✓ Сборка БЫСТРОЙ версии завершена!
    echo ========================================
    echo.
    echo EXE файл: dist\StonePartition_Fast.exe
    echo Размер файла:
    dir "dist\StonePartition_Fast.exe" | find "StonePartition_Fast.exe"
    echo.
    echo Эта версия использует быстрый алгоритм (5-10 секунд)
    echo Подходит для демонстрации и проверки работы
    echo.
) else (
    echo.
    echo ========================================
    echo ✗ Ошибка при сборке
    echo ========================================
    echo.
    echo Проверьте вывод выше для деталей ошибки.
    echo.
)

pause
