"""
사용 가능한 Gemini 모델 목록 확인
"""
import os
import google.generativeai as genai
from dotenv import load_dotenv

# 환경 변수 로드
load_dotenv(os.path.join('backend', '.env'))

# API 키 설정
api_key = os.getenv("GOOGLE_API_KEY")
if api_key:
    genai.configure(api_key=api_key)
    
    print("🔍 사용 가능한 Gemini 모델 목록:")
    print("=" * 40)
    
    for model in genai.list_models():
        if 'generateContent' in model.supported_generation_methods:
            print(f"✅ {model.name}")
            print(f"   - 설명: {model.display_name}")
            print(f"   - 지원 메소드: {', '.join(model.supported_generation_methods)}")
            print()
else:
    print("❌ API 키를 찾을 수 없습니다!")