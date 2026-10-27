@echo off
rem Recopie la configuration Claude Code versionnee (claude\) a la racine de l espace de travail.
rem A lancer une fois par poste, puis apres chaque modification de claude\.
setlocal
for %%I in ("%~dp0..") do set "DOCS=%%~fI"
for %%I in ("%DOCS%\..") do set "RACINE=%%~fI"

copy /Y "%DOCS%\claude\CLAUDE-racine.md" "%RACINE%\CLAUDE.md" >nul
copy /Y "%DOCS%\claude\mcp.json" "%RACINE%\.mcp.json" >nul
if not exist "%RACINE%\.claude" mkdir "%RACINE%\.claude"
copy /Y "%DOCS%\claude\settings.json" "%RACINE%\.claude\settings.json" >nul
robocopy "%DOCS%\claude\skills" "%RACINE%\.claude\skills" /E /NFL /NDL /NJH /NJS /NP >nul
if errorlevel 8 (
  echo Echec de la copie des skills.
  exit /b 1
)

echo Configuration Claude Code installee dans %RACINE%
exit /b 0
