@echo off
chcp 65001 >nul
echo 🛑 AI 챗봇 서버를 종료합니다...
echo.

REM Python 백엔드 서버 종료
echo [1/3] 백엔드 서버를 종료하는 중...
taskkill /f /im "python.exe" >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ Python 서버 종료 완료
) else (
    echo ℹ️  Python 서버가 실행 중이 아닙니다
)

REM Node.js 프론트엔드 서버 종료  
echo [2/3] 프론트엔드 서버를 종료하는 중...
taskkill /f /im "node.exe" >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ Node.js 서버 종료 완료
) else (
    echo ℹ️  Node.js 서버가 실행 중이 아닙니다
)

REM 관련 CMD 창 종료
echo [3/3] 터미널 창들을 정리하는 중...
taskkill /f /fi "windowtitle eq AI Chatbot Backend*" >nul 2>&1
taskkill /f /fi "windowtitle eq AI Chatbot Frontend*" >nul 2>&1

echo.
echo ✅ 모든 챗봇 서버가 완전히 종료되었습니다!
echo 🌐 브라우저 탭도 닫아주세요
echo.
timeout /t 3 /nobreak >nul