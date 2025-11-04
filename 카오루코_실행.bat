@echo off
chcp 65001 > nul 2>&1

echo ========================================
echo      🌸 카오루코 챗봇 시작하기 🌸
echo ========================================
echo.

echo [1/2] 백엔드 서버 시작 중... (포트 8001)
cd backend
start "Kaoruko Backend" cmd /k "chcp 65001 > nul && python main.py"
cd ..

timeout /t 3 > nul

echo [2/2] 프론트엔드 서버 시작 중... (포트 5173)  
cd frontend
start "Kaoruko Frontend" cmd /k "chcp 65001 > nul && npm run dev"
cd ..

timeout /t 5 > nul

echo.
echo ✅ 서버 시작 완료!
echo.
echo 🌐 웹 브라우저에서 접속:
echo    http://localhost:5173
echo.
echo 💕 카오루코와 대화하세요!
echo.

echo Opening browser automatically...
timeout /t 2 > nul
start http://localhost:5173

echo.
echo ========================================
echo        Servers are now running!
echo ========================================
echo * Backend: http://localhost:8001
echo * Frontend: http://localhost:5173
echo.
echo To stop servers, close the terminal windows.
echo This window will remain open to keep servers running.
echo.
echo Press Ctrl+C to stop all servers.

:loop
timeout /t 30 > nul
goto loop