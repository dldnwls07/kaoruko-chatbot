# GitHub 업로드 가이드

## 🚀 프로젝트 GitHub 업로드 방법

### 1️⃣ 사전 준비
- Git 설치 확인: `git --version`
- GitHub 계정 준비

### 2️⃣ 로컬 Git 초기화
```bash
# 프로젝트 폴더에서 실행
git init
git add .
git commit -m "🌸 카오루코 챗봇 프로젝트 초기 커밋"
```

### 3️⃣ GitHub에서 새 저장소 생성
1. [GitHub](https://github.com)에서 로그인
2. "New repository" 클릭
3. 저장소 이름: `kaoruko-chatbot` (또는 원하는 이름)
4. Public/Private 선택
5. "Create repository" 클릭

### 4️⃣ 원격 저장소 연결 및 푸시
```bash
# GitHub에서 제공하는 URL 사용
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git
git branch -M main
git push -u origin main
```

## ⚠️ 업로드되지 않는 파일들 (.gitignore)
다음 파일들은 보안상 GitHub에 업로드되지 않습니다:

### 🔒 민감한 정보
- `backend/.env` - API 키 포함
- `api_key.txt` - API 키 파일

### 💾 개인 데이터
- `*.db` - 개인 채팅 기록
- `chat_history.db` - 대화 기록 데이터베이스

### 🗂️ 시스템 파일
- `__pycache__/` - Python 캐시
- `node_modules/` - Node.js 의존성
- `.history/` - 히스토리 파일

## 🔧 다른 사용자가 프로젝트 사용하는 방법

### 1. 저장소 클론
```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git
cd YOUR_REPOSITORY
```

### 2. API 키 설정
```bash
# 템플릿 복사
cp backend/.env.template backend/.env
# .env 파일에서 API 키 입력
```

### 3. 의존성 설치
```bash
# Python 의존성
cd backend
pip install -r requirements.txt

# Node.js 의존성
cd ../frontend
npm install
```

### 4. 실행
```bash
# 프로젝트 루트에서
카오루코_실행.bat
```

## 📝 커밋 메시지 컨벤션 (권장)
- `✨ feat: 새로운 기능 추가`
- `🐛 fix: 버그 수정`
- `📚 docs: 문서 수정`
- `🎨 style: 코드 스타일 변경`
- `♻️ refactor: 코드 리팩토링`
- `🌸 kaoruko: 카오루코 관련 변경사항`