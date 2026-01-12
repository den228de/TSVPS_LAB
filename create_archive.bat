@echo off
chcp 65001 >nul
echo ╔════════════════════════════════════════════════════════════╗
echo ║         СОЗДАНИЕ АРХИВА СО ВСЕМИ ПРИЛОЖЕНИЯМИ             ║
echo ╚════════════════════════════════════════════════════════════╝
echo.

set ARCHIVE_NAME=TSVPS_Applications.zip
set TEMP_DIR=TSVPS_Apps_Temp

echo [1/4] Создание временной папки...
if exist "%TEMP_DIR%" rmdir /s /q "%TEMP_DIR%"
mkdir "%TEMP_DIR%"
echo ✓ Папка создана
echo.

echo [2/4] Копирование приложений...

echo   - Сортировка камней (быстрая версия)...
if exist "dist\StonePartition.exe" (
    copy "dist\StonePartition.exe" "%TEMP_DIR%\1_StonePartition.exe" >nul
    echo     ✓ StonePartition.exe
) else (
    echo     ✗ Файл не найден
)

echo   - Сортировка камней (полная версия)...
if exist "dist\StonePartition_Full.exe" (
    copy "dist\StonePartition_Full.exe" "%TEMP_DIR%\2_StonePartition_Full.exe" >nul
    echo     ✓ StonePartition_Full.exe
) else (
    echo     ✗ Файл не найден
)

echo   - Поиск клик в графе...
if exist "Клики\dist\CliqueFinderGUI.exe" (
    copy "Клики\dist\CliqueFinderGUI.exe" "%TEMP_DIR%\3_CliqueFinderGUI.exe" >nul
    echo     ✓ CliqueFinderGUI.exe
) else (
    echo     ✗ Файл не найден
)

echo   - Симуляция гиперкубов...
if exist "кубы\dist\HypercubeSimulator.exe" (
    copy "кубы\dist\HypercubeSimulator.exe" "%TEMP_DIR%\4_HypercubeSimulator.exe" >nul
    echo     ✓ HypercubeSimulator.exe
) else (
    echo     ✗ Файл не найден
)

echo   - Нейронная сеть...
if exist "нейронка\dist\NeuralNetwork.exe" (
    copy "нейронка\dist\NeuralNetwork.exe" "%TEMP_DIR%\5_NeuralNetwork.exe" >nul
    echo     ✓ NeuralNetwork.exe
) else (
    echo     ✗ Файл не найден
)

echo.
echo [3/4] Создание README файла...
(
echo ЛАБОРАТОРНЫЕ РАБОТЫ - ГОТОВЫЕ ПРИЛОЖЕНИЯ
echo ========================================
echo.
echo Все приложения готовы к запуску на любом компьютере с Windows.
echo Python НЕ требуется!
echo.
echo СПИСОК ПРИЛОЖЕНИЙ:
echo.
echo 1. StonePartition.exe
echo    Сортировка камней ^(быстрая версия^)
echo    Сравнение алгоритмов разбиения камней на кучи
echo.
echo 2. StonePartition_Full.exe
echo    Сортировка камней ^(полная версия^)
echo    Расширенное тестирование алгоритмов
echo.
echo 3. CliqueFinderGUI.exe
echo    Поиск клик в графе
echo    Поиск максимальных клик в неориентированном графе
echo.
echo 4. HypercubeSimulator.exe
echo    Симуляция сети гиперкубов
echo    Моделирование топологии и поиск кратчайших путей
echo.
echo 5. NeuralNetwork.exe
echo    Нейронная сеть
echo    Обучение и тестирование нейронной сети
echo.
echo ========================================
echo.
echo ЗАПУСК:
echo Просто дважды кликните на нужный .exe файл
echo.
echo АВТОР: Андрей
echo ГОД: 2026
) > "%TEMP_DIR%\README.txt"
echo ✓ README.txt создан
echo.

echo [4/4] Создание ZIP архива...
powershell -Command "Compress-Archive -Path '%TEMP_DIR%\*' -DestinationPath '%ARCHIVE_NAME%' -Force"
if exist "%ARCHIVE_NAME%" (
    echo ✓ Архив создан
) else (
    echo ✗ Ошибка создания архива
    goto :cleanup
)

echo.
echo [5/4] Очистка временных файлов...
rmdir /s /q "%TEMP_DIR%"
echo ✓ Временные файлы удалены
echo.

echo ╔════════════════════════════════════════════════════════════╗
echo ║                  АРХИВ СОЗДАН УСПЕШНО!                     ║
echo ╚════════════════════════════════════════════════════════════╝
echo.
echo Файл: %ARCHIVE_NAME%
echo.
for %%A in ("%ARCHIVE_NAME%") do echo Размер: %%~zA байт
echo.
echo Архив содержит все собранные приложения и готов для
echo переноса на другой компьютер.
echo.
goto :end

:cleanup
rmdir /s /q "%TEMP_DIR%"

:end
pause
