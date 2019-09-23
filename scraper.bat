echo off

CALL  "%USERPROFILE%\Anaconda3\Scripts\activate.bat" lema
python "%USERPROFILE%\lead-machine\src\main.py"
cmd \k
echo on 