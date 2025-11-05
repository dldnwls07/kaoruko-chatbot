@echo off
chcp 65001 >nul
echo 🛠️ 개발 환경을 설정합니다...
echo.

REM Python 가상환경 확인 및 설치
echo [1/4] Python 백엔드 의존성 설치 중...
cd /d "%~dp0backend"
if not exist "venv" (
    echo 가상환경을 생성합니다...
    python -m venv venv
)
call venv\Scripts\activate
pip install -r requirements.txt
echo ✅ 백엔드 의존성 설치 완료

REM Node.js 의존성 설치
echo.
echo [2/4] Node.js 프론트엔드 의존성 설치 중...
cd /d "%~dp0frontend"
if not exist "node_modules" (
    npm install
) else (
    echo ✅ 프론트엔드 의존성이 이미 설치되어 있습니다
)

REM 환경 파일 체크
echo.
echo [3/4] 환경 설정 확인 중...
cd /d "%~dp0backend"
if not exist ".env" (
    if exist ".env.template" (
        copy .env.template .env
        echo ⚠️  .env 파일이 생성되었습니다. API 키를 설정해주세요!
    )
)

REM API 키 체크
cd /d "%~dp0"
if not exist "api_key.txt" (
    echo ⚠️  api_key.txt 파일이 없습니다. OpenAI API 키를 추가해주세요!
)

echo.
echo [4/4] 설정 완료!
echo 🚀 이제 '챗봇_실행.bat'를 실행하세요!
echo.
pause