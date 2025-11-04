#!/usr/bin/env python3
"""
음수 호감도 기능 테스트 스크립트
"""
import requests
import json

def test_negative_affection():
    base_url = "http://localhost:8001"
    
    # 테스트 사용자 데이터 초기화
    print("🧹 사용자 데이터 초기화...")
    try:
        response = requests.post(f"{base_url}/new-user", 
                               json={"message": "", "user_name": "테스터"})
        print(f"초기화 응답: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"❌ 초기화 실패: {e}")
        return
    
    # 정상적인 대화로 시작
    print("\n💬 정상적인 대화 시작...")
    try:
        response = requests.post(f"{base_url}/chat", 
                               json={"message": "안녕하세요", "user_name": "테스터"})
        data = response.json()
        print(f"첫 대화 후 호감도: {data.get('affection_level', 'N/A')}")
        print(f"카오루코 응답: {data.get('reply', '')[:50]}...")
    except requests.exceptions.RequestException as e:
        print(f"❌ 정상 대화 실패: {e}")
        return
    
    # 무례한 메시지로 음수 트리거 테스트
    print("\n😠 무례한 메시지 테스트...")
    rude_messages = [
        "너 정말 바보야!",
        "멍청한 놈아",
        "꺼져버려!",
    ]
    
    for msg in rude_messages:
        try:
            response = requests.post(f"{base_url}/chat", 
                                   json={"message": msg, "user_name": "테스터"})
            data = response.json()
            affection = data.get('affection_level', 'N/A')
            change = data.get('affection_change', 0)
            
            print(f"메시지: '{msg}'")
            print(f"호감도: {affection} (변화: {change:+d})")
            print(f"카오루코 응답: {data.get('reply', '')[:50]}...")
            print("---")
        except requests.exceptions.RequestException as e:
            print(f"❌ 무례한 메시지 테스트 실패: {e}")
    
    print("\n✅ 음수 호감도 테스트 완료!")

if __name__ == "__main__":
    print("🌸 음수 호감도 기능 테스트 시작!")
    test_negative_affection()