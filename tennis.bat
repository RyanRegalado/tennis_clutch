@echo off
setlocal

if "%1"=="" goto help
if "%1"=="help" goto help
if "%1"=="download" goto download
if "%1"=="download-year" goto download-year
if "%1"=="download-slam" goto download-slam

:help
echo Tennis Data Download Commands:
echo   tennis download                    - Download all data
echo   tennis download-year 2024          - Download specific year
echo   tennis download-slam 2024 usopen   - Download specific tournament
goto end

:download
python src\download_data_refactored.py
goto end

:download-year
python src\download_data_refactored.py %2
goto end

:download-slam
python src\download_data_refactored.py %2 %3
goto end

:end
endlocal
