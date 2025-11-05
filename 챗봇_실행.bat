@echo off
chcp 65001 >nul
echo 💕 AI 챗봇을 시작합니다...
echo.

REM 백엔드 서버 시작
echo [1/3] 백엔드 서버를 시작하는 중...
cd /d "%~dp0backend"
start "AI Chatbot Backend" cmd /k "python main.py"

REM 잠시 대기 (서버 부팅 시간)
timeout /t 3 /nobreak >nul

REM 프론트엔드 개발 서버 시작  
echo [2/3] 프론트엔드를 시작하는 중...
cd /d "%~dp0frontend"
start "AI Chatbot Frontend" cmd /k "npm run dev"

REM 서버 준비 시간 대기
echo [3/3] 서버 준비 중... (5초 대기)
timeout /t 5 /nobreak >nul

REM 브라우저 자동 열기
echo 🌐 브라우저를 자동으로 열고 있습니다...
start "" "http://localhost:5173"

echo.
echo ✅ AI 챗봇이 시작되었습니다!
echo 🌐 웹페이지가 자동으로 열렸습니다!
echo 🔧 API 서버: http://localhost:8001
echo.
echo 🌸 와구리 카오루코와 💜 레제 중 선택하세요!
echo 💡 간편 종료: '챗봇_종료.bat' 파일을 실행하세요
echo 💡 수동 종료: 각 터미널에서 Ctrl+C를 누르세요
echo.
echo 📱 사용 완료 시:
echo    🔴 간단한 방법: 챗봇_종료.bat 더블클릭
echo    🔧 수동 방법: 각 터미널에서 Ctrl+C 후 창 닫기
echo.
pause