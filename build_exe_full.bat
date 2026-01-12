@echo off
chcp 65001 >nul
echo ========================================
echo Сборка ПОЛНОЙ версии EXE
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

echo [3/4] Сборка ПОЛНОЙ версии EXE...
echo Это может занять несколько минут...
echo.

REM Удаляем старые файлы сборки
if exist "build" rmdir /s /q build
if exist "dist\StonePartition_Full.exe" del /q "dist\StonePartition_Full.exe"
if exist "StonePartition_Full.spec" del /q StonePartition_Full.spec

REM Собираем с дополнительными параметрами для matplotlib
pyinstaller --onefile ^
    --windowed ^
    --name="StonePartition_Full" ^
    --hidden-import=matplotlib ^
    --hidden-import=matplotlib.backends.backend_tkagg ^
    --hidden-import=PIL ^
    --hidden-import=PIL._tkinter_finder ^
    --collect-data matplotlib ^
    --noconsole ^
    app_full.py

echo.

echo [4/4] Проверка результата...
if exist "dist\StonePartition_Full.exe" (
    echo.
    echo ========================================
    echo ✓ Сборка ПОЛНОЙ версии завершена!
    echo ========================================
    echo.
    echo EXE файл: dist\StonePartition_Full.exe
    echo Размер файла:
    dir "dist\StonePartition_Full.exe" | find "StonePartition_Full.exe"
    echo.
    echo Эта версия использует полный алгоритм (30-60 секунд)
    echo Подходит для демонстрации преподавателю
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
