@echo off
setlocal
call "C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Auxiliary\Build\vcvars64.bat" >nul 2>&1
if errorlevel 1 (
    echo vcvars64 failed
    exit /b 1
)
cd /d "D:\OSIS_Solver\osisPython\PySolver"
msbuild PySolver.vcxproj /t:Rebuild /p:Configuration=Release /p:Platform=x64 /p:AdditionalLibraryDirectories="D:\OSIS_Solver\lib64;%(AdditionalLibraryDirectories)" /m /v:minimal /nologo 2>&1
echo --- exit: %errorlevel% ---
exit /b %errorlevel%
