@echo off
setlocal
call "C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Auxiliary\Build\vcvars64.bat" >nul 2>&1
if errorlevel 1 (
    echo vcvars64 failed
    exit /b 1
)
set "VCXPROJ=D:\OSIS_Solver\osisProject\YIL_Command\YIL_Command.vcxproj"
echo === Build yilCommand Release x64 ===
msbuild "%VCXPROJ%" /t:Rebuild /p:Configuration=Release /p:Platform=x64 /m /v:minimal /nologo 2>&1
echo --- exit: %errorlevel% ---
if exist "D:\OSIS_Solver\osisProject\YIL_Command\Release\yilCommand.dll" (
    copy /Y "D:\OSIS_Solver\osisProject\YIL_Command\Release\yilCommand.dll" "D:\OSIS_Solver\Rbin64\yilCommand.dll" >nul
    copy /Y "D:\OSIS_Solver\osisProject\YIL_Command\Release\yilCommand.pdb" "D:\OSIS_Solver\Rbin64\yilCommand.pdb" >nul 2>nul
    echo Deployed: D:\OSIS_Solver\Rbin64\yilCommand.dll
)
exit /b %errorlevel%
