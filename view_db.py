#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sqlite3
import os
from datetime import datetime

def view_chat_database():
    """
    SQLite 데이터베이스의 채팅 기록을 보여주는 함수
    """
    
    # 데이터베이스 파일 경로
    db_path = os.path.join("backend", "chat_history.db")
    
    # 데이터베이스 파일이 존재하는지 확인
    if not os.path.exists(db_path):
        print("❌ 데이터베이스 파일을 찾을 수 없습니다!")
        print(f"경로: {os.path.abspath(db_path)}")
        return
    
    try:
        # SQLite 데이터베이스 연결
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # 테이블 목록 확인
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        
        print("🌸 카오루코 채팅 데이터베이스 뷰어")
        print("=" * 50)
        print(f"📁 데이터베이스 위치: {os.path.abspath(db_path)}")
        print(f"📊 테이블 목록: {[table[0] for table in tables]}")
        print()
        
        # 채팅 기록 조회
        cursor.execute("""
            SELECT id, user_message, bot_reply, timestamp, user_name 
            FROM chat_history 
            ORDER BY timestamp DESC 
            LIMIT 20
        """)
        
        records = cursor.fetchall()
        
        if not records:
            print("💬 저장된 채팅 기록이 없습니다.")
        else:
            print(f"💬 최근 채팅 기록 ({len(records)}개):")
            print("-" * 80)
            
            for i, record in enumerate(records, 1):
                chat_id, user_msg, bot_reply, timestamp, user_name = record
                
                # 타임스탬프 포맷팅
                try:
                    dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
                    formatted_time = dt.strftime('%Y-%m-%d %H:%M:%S')
                except:
                    formatted_time = timestamp
                
                print(f"\n[{i}] ID: {chat_id} | 시간: {formatted_time}")
                print(f"👤 {user_name or '사용자'}: {user_msg}")
                print(f"🌸 카오루코: {bot_reply}")
                print("-" * 40)
        
        # 통계 정보
        cursor.execute("SELECT COUNT(*) FROM chat_history")
        total_count = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(DISTINCT user_name) FROM chat_history WHERE user_name IS NOT NULL")
        unique_users = cursor.fetchone()[0]
        
        print(f"\n📈 통계:")
        print(f"  총 대화 수: {total_count}개")
        print(f"  사용자 수: {unique_users}명")
        
        conn.close()
        
    except sqlite3.Error as e:
        print(f"❌ 데이터베이스 오류: {e}")
    except Exception as e:
        print(f"❌ 예상치 못한 오류: {e}")

def delete_all_chats():
    """
    모든 채팅 기록을 삭제하는 함수 (주의: 복구 불가능!)
    """
    db_path = os.path.join("backend", "chat_history.db")
    
    if not os.path.exists(db_path):
        print("❌ 데이터베이스 파일을 찾을 수 없습니다!")
        return
    
    confirm = input("⚠️  정말로 모든 채팅 기록을 삭제하시겠어요? (yes/no): ")
    if confirm.lower() != 'yes':
        print("❌ 삭제가 취소되었습니다.")
        return
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM chat_history")
        deleted_count = cursor.rowcount
        
        conn.commit()
        conn.close()
        
        print(f"✅ {deleted_count}개의 채팅 기록이 삭제되었습니다.")
        
    except sqlite3.Error as e:
        print(f"❌ 데이터베이스 오류: {e}")

if __name__ == "__main__":
    print("🌸 카오루코 데이터베이스 관리 도구")
    print("1. 채팅 기록 보기")
    print("2. 모든 채팅 기록 삭제")
    print("3. 종료")
    
    while True:
        try:
            choice = input("\n선택하세요 (1-3): ").strip()
            
            if choice == '1':
                view_chat_database()
            elif choice == '2':
                delete_all_chats()
            elif choice == '3':
                print("👋 안녕히 가세요!")
                break
            else:
                print("❌ 올바른 번호를 선택해주세요 (1-3)")
                
        except KeyboardInterrupt:
            print("\n\n👋 프로그램을 종료합니다.")
            break
        except Exception as e:
            print(f"❌ 오류가 발생했습니다: {e}")