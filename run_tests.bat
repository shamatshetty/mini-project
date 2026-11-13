@echo off
set "PATH=C:\Users\ASUS\AppData\Local\Microsoft\WinGet\Packages\BrechtSanders.WinLibs.POSIX.UCRT_Microsoft.Winget.Source_8wekyb3d8bbwe\mingw64\bin;%PATH%"
echo ========================================================
echo        RUNNING ALL TESTS: SMART HOSTEL SYSTEM
echo ========================================================
echo.
echo [1/2] Running Circular FIFO Queue and Room Allotment Unit Tests...
.\test_fifo.exe
if %ERRORLEVEL% NEQ 0 (
    echo [FAIL] Unit Tests Failed!
    exit /b %ERRORLEVEL%
)
echo.
echo [2/2] Running Automated FIFO Demonstration Scenario...
.\hostel.exe --demo
if %ERRORLEVEL% NEQ 0 (
    echo [FAIL] Demonstration Scenario Failed!
    exit /b %ERRORLEVEL%
)
echo.
echo ========================================================
echo        *** ALL AUTOMATED TEST SUITES PASSED! ***
echo ========================================================
