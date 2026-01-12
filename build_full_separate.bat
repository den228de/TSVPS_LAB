@echo off
chcp 65001 >nul
echo ========================================
echo Сборка ПОЛНОЙ версии в папку full
echo ========================================
echo.

REM Создаем папку full если её нет
if not exist "full" mkdir full

echo [1/5] Копирование файлов...
copy stone_partition.py full\ >nul
copy app_full.py full\ >nul
copy requirements.txt full\ >nul
echo ✓ Файлы скопированы
echo.

echo [2/5] Проверка PyInstaller...
pip show pyinstaller >nul 2>&1
if errorlevel 1 (
    echo PyInstaller не установлен. Устанавливаем...
    pip install pyinstaller
) else (
    echo ✓ PyInstaller установлен
)
echo.

echo [3/5] Проверка зависимостей...
pip install -r requirements.txt >nul
echo ✓ Зависимости установлены
echo.

echo [4/5] Сборка EXE файла...
echo Это займет 3-5 минут...
echo.

cd full

REM Удаляем старые файлы сборки
if exist "build" rmdir /s /q build
if exist "dist" rmdir /s /q dist
if exist "StonePartition_Full.spec" del /q StonePartition_Full.spec

REM Собираем EXE
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

REM Очищаем временные файлы
if exist "build" rmdir /s /q build
if exist "StonePartition_Full.spec" del /q StonePartition_Full.spec

cd ..

echo [5/5] Проверка результата...
if exist "full\dist\StonePartition_Full.exe" (
    echo.
    echo ========================================
    echo ✓ ПОЛНАЯ версия успешно собрана!
    echo ========================================
    echo.
    echo 📁 Папка: full\dist\
    echo 📦 Файл: StonePartition_Full.exe
    echo.
    dir "full\dist\StonePartition_Full.exe" | find "StonePartition_Full.exe"
    echo.
    echo ⏱️  Время выполнения: 30-60 секунд
    echo 🔬 Полное тестирование (10×10×3 = 300 тестов)
    echo 👨‍🏫 Для демонстрации преподавателю
    echo.
    echo Запустите: full\dist\StonePartition_Full.exe
    echo.
) else (
    echo.
    echo ========================================
    echo ✗ Ошибка при сборке
    echo ========================================
    echo.
    echo Проверьте вывод выше для деталей.
    echo.
)

pause
