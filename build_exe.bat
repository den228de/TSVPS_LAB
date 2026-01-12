@echo off
chcp 65001 >nul
echo ========================================
echo Сборка ОБЕИХ версий приложения
echo ========================================
echo.

echo Будут собраны:
echo 1. StonePartition_Fast.exe - быстрая версия (5-10 сек)
echo 2. StonePartition_Full.exe - полная версия (30-60 сек)
echo.
pause

echo.
echo ========================================
echo Сборка быстрой версии...
echo ========================================
call build_exe_fast.bat

echo.
echo.
echo ========================================
echo Сборка полной версии...
echo ========================================
call build_exe_full.bat

echo.
echo.
echo ========================================
echo ✓ Обе версии собраны!
echo ========================================
echo.
echo Файлы в папке dist:
dir dist\*.exe
echo.
echo Готово! Теперь у вас есть две версии:
echo - StonePartition_Fast.exe - для быстрой демонстрации
echo - StonePartition_Full.exe - для преподавателя (полные тесты)
echo.

pause
