import { useState, useEffect } from 'react';
import './App.css';

function App() {
  const [messages, setMessages] = useState([]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [userName, setUserName] = useState('');
  const [showNameInput, setShowNameInput] = useState(true);
  const [affectionLevel, setAffectionLevel] = useState(0);
  const [affectionChange, setAffectionChange] = useState(0);
  const [showAffectionBar, setShowAffectionBar] = useState(true);
  // 🎭 감정 시스템 2단계 state
  const [currentEmotion, setCurrentEmotion] = useState({
    emotion: '수줍음',
    intensity: 5,
    emoji: '😊',
    color: '#ffb3d9',
    reason: '기본 감정',
    confidence: 0.8
  });
  


  // 컴포넌트 마운트 시 저장된 사용자 정보 확인
  useEffect(() => {
    const savedUserName = localStorage.getItem('kaoruko_user_name');
    const savedAffection = localStorage.getItem('kaoruko_affection_level');
    const sessionStarted = localStorage.getItem('kaoruko_session_active');
    
    // 세션이 활성 상태이고 저장된 사용자가 있는 경우에만 복원
    if (savedUserName && sessionStarted === 'true') {
      setUserName(savedUserName);
      setShowNameInput(false);
      if (savedAffection) {
        setAffectionLevel(parseInt(savedAffection));
      }
      // 환영 메시지 추가
      const welcomeMessage = {
        text: `어... ${savedUserName}님, 다시 만나서 반가워요... 기다리고 있었어요.`,
        sender: 'bot',
      };
      setMessages([welcomeMessage]);
    } else {
      // 세션이 없거나 비활성 상태면 초기화
      localStorage.removeItem('kaoruko_user_name');
      localStorage.removeItem('kaoruko_affection_level');
      localStorage.removeItem('kaoruko_session_active');
    }
  }, []);

  // 사용자 정보가 변경될 때마다 로컬스토리지에 저장
  useEffect(() => {
    if (userName) {
      localStorage.setItem('kaoruko_user_name', userName);
      localStorage.setItem('kaoruko_session_active', 'true');
    }
  }, [userName]);

  useEffect(() => {
    if (userName) { // 사용자가 있을 때만 호감도 저장
      localStorage.setItem('kaoruko_affection_level', affectionLevel.toString());
    }
  }, [affectionLevel, userName]);

  // 페이지 종료/새로고침 시 세션 관리
  useEffect(() => {
    const handleBeforeUnload = () => {
      // 브라우저 탭이 닫히거나 새로고침될 때 세션 유지
      if (userName) {
        localStorage.setItem('kaoruko_session_active', 'true');
      }
    };

    const handleVisibilityChange = () => {
      // 탭이 숨겨질 때 세션 정보 저장
      if (document.visibilityState === 'hidden' && userName) {
        localStorage.setItem('kaoruko_session_active', 'true');
      }
    };

    window.addEventListener('beforeunload', handleBeforeUnload);
    document.addEventListener('visibilitychange', handleVisibilityChange);

    return () => {
      window.removeEventListener('beforeunload', handleBeforeUnload);
      document.removeEventListener('visibilitychange', handleVisibilityChange);
    };
  }, [userName]);

  // 호감도에 따른 관계 단계 계산
  const getRelationshipStage = (level) => {
    if (level < 0) return "멀어진사람";
    if (level >= 81) return "특별한사람";
    if (level >= 61) return "절친";
    if (level >= 41) return "친구";
    if (level >= 21) return "지인";
    return "낯선사람";
  };

  // 호감도 하트 표시는 이제 JSX에서 직접 렌더링

  // 호감도 진행률 계산
  const getProgressPercentage = (level) => {
    // 음수인 경우는 부정적 진행을 -100 기준으로 퍼센트 표시
    if (level < 0) {
      return Math.min(100, (Math.abs(level) / 100) * 100);
    }

    const ranges = [
      [0, 20], [21, 40], [41, 60], [61, 80], [81, 100]
    ];
    
    for (const [min, max] of ranges) {
      if (level >= min && level <= max) {
        return ((level - min) / (max - min)) * 100;
      }
    }
    return 0;
  };

  // 🎮 이벤트 처리 함수
  const handleEvents = (events) => {
    events.forEach(event => {
      if (event.type === 'milestone_achievement') {
        // 호감도 이정표 달성 이벤트
        showMilestoneModal(event);
      } else if (event.type === 'special_conversation') {
        // 특별 대화 이벤트
        addSpecialMessage(event.message);
      }
    });
  };

  // 호감도 이정표 달성 모달 표시
  const showMilestoneModal = (event) => {
    // 특별한 축하 메시지를 채팅에 추가
    const milestoneMessage = {
      text: `🎉 ${event.title}\n\n${event.message}`,
      sender: 'system',
      isEvent: true,
      eventType: 'milestone'
    };
    
    setMessages(prevMessages => [...prevMessages, milestoneMessage]);
    
    // 특별 대화 추가
    if (event.special_dialogue) {
      event.special_dialogue.forEach((dialogue, index) => {
        setTimeout(() => {
          const dialogueMessage = {
            text: dialogue,
            sender: 'bot',
            isEvent: true
          };
          setMessages(prevMessages => [...prevMessages, dialogueMessage]);
        }, (index + 1) * 2000); // 2초 간격으로 대화 추가
      });
    }
  };

  // 특별 메시지 추가
  const addSpecialMessage = (message) => {
    const specialMessage = {
      text: message,
      sender: 'bot',
      isSpecial: true
    };
    setMessages(prevMessages => [...prevMessages, specialMessage]);
  };

  const handleNameSubmit = async (e) => {
    e.preventDefault();
    if (userName.trim() === '') return;
    
    try {
      // 새로운 사용자 이름으로 시작할 때 해당 사용자의 이전 데이터 초기화
      await fetch('http://localhost:8001/new-user', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ 
          message: '',
          user_name: userName 
        }),
      });
    } catch (error) {
      console.error("Failed to clear user data:", error);
    }
    
    setShowNameInput(false);
    // 카오루코의 첫 인사 메시지 추가
    const welcomeMessage = {
      text: `아... 안녕하세요, ${userName}님. 와구리 카오루코라고 합니다... 만나뵙게 되어 반갑습니다.`,
      sender: 'bot',
    };
    setMessages([welcomeMessage]);
  };

  const handleNewUser = async () => {
    // 새로운 사용자로 시작 확인
    if (window.confirm('새로운 사용자로 시작하시겠어요? 현재 대화와 호감도가 모두 초기화됩니다.')) {
      try {
        // 백엔드에 사용자 데이터 초기화 요청
        if (userName) {
          await fetch('http://localhost:8001/new-user', {
            method: 'POST',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify({ 
              message: '',
              user_name: userName 
            }),
          });
        }
      } catch (error) {
        console.error("Failed to clear user data:", error);
      }
      
      // 로컬스토리지 완전 정리
      localStorage.removeItem('kaoruko_user_name');
      localStorage.removeItem('kaoruko_affection_level');
      localStorage.removeItem('kaoruko_session_active');
      
      // 상태 즉시 초기화
      setMessages([]);
      setUserName('');
      setShowNameInput(true);
      setAffectionLevel(0);
      setAffectionChange(0);
    }
  };

  const handleEndConversation = () => {
    // 대화 종료 확인
    if (window.confirm('정말로 대화를 종료하시겠어요? 카오루코가... 조금 아쉬워할 것 같아요...')) {
      // 세션을 비활성 상태로 설정 (즉시)
      localStorage.setItem('kaoruko_session_active', 'false');
      
      // 마지막 인사 메시지 추가
      const farewell = {
        text: `${userName}님... 오늘 대화해주셔서 고마웠어요. 또... 또 만나요... 안녕히 가세요...`,
        sender: 'bot',
      };
      setMessages(prev => [...prev, farewell]);
      
      // 3초 후에 완전 초기화
      setTimeout(() => {
        // 로컬스토리지 완전 정리
        localStorage.removeItem('kaoruko_user_name');
        localStorage.removeItem('kaoruko_affection_level');
        localStorage.removeItem('kaoruko_session_active');
        
        // 상태 초기화
        setMessages([]);
        setUserName('');
        setShowNameInput(true);
        setAffectionLevel(0);
        setAffectionChange(0);
      }, 3000);
    }
  };

  const handleSendMessage = async (e) => {
    e.preventDefault();
    if (inputValue.trim() === '' || isLoading) return;

    const userMessage = {
      text: inputValue,
      sender: 'user',
    };

    setMessages(prevMessages => [...prevMessages, userMessage]);
    setInputValue('');
    setIsLoading(true);

    try {
      const response = await fetch('http://localhost:8001/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ 
          message: userMessage.text,
          user_name: userName 
        }),
      });

      if (!response.ok) {
        throw new Error(`Network response was not ok: ${response.statusText}`);
      }

      const data = await response.json();
      
      // 호감도 정보 업데이트
      if (data.affection_level !== undefined) {
        setAffectionLevel(data.affection_level);
      }
      if (data.affection_change !== undefined && data.affection_change !== 0) {
        setAffectionChange(data.affection_change);
        // 호감도 변화 알림을 3초 후 제거
        setTimeout(() => setAffectionChange(0), 3000);
      }
      
      // 🎭 감정 정보 업데이트
      if (data.emotion) {
        setCurrentEmotion({
          emotion: data.emotion,
          intensity: data.emotion_intensity || 5,
          emoji: data.emotion_emoji || '😊',
          color: data.emotion_color || '#ffb3d9',
          reason: data.emotion_reason || '',
          confidence: data.emotion_confidence || 0.8
        });
      }
      
      const botMessage = {
        text: data.reply,
        sender: 'bot',
      };

      setMessages(prevMessages => [...prevMessages, botMessage]);
      
      // 🎮 이벤트 처리
      if (data.events && data.events.length > 0) {
        handleEvents(data.events);
      }

    } catch (error) {
      console.error("Failed to fetch:", error);
      const errorMessage = {
        text: '어, 어...? 뭔가... 연결이 안 되는 것 같아요... 카오루코가 잠시 자리를 비웠나봐요... 조금만 기다렸다가 다시 말 걸어주시겠어요...?',
        sender: 'bot',
      };
      setMessages(prevMessages => [...prevMessages, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  // 속마음 텍스트를 파싱하는 함수
  const parseInnerThoughts = (text) => {
    // *내용* 패턴을 찾아서 속마음으로 변환
    const parts = [];
    let lastIndex = 0;
    const regex = /\*([^*]+)\*/g;
    let match;

    while ((match = regex.exec(text)) !== null) {
      // 일반 텍스트 부분 추가
      if (match.index > lastIndex) {
        parts.push({
          type: 'normal',
          text: text.slice(lastIndex, match.index)
        });
      }
      
      // 속마음 부분 추가
      parts.push({
        type: 'inner-thought',
        text: match[1]
      });
      
      lastIndex = regex.lastIndex;
    }
    
    // 마지막 일반 텍스트 부분 추가
    if (lastIndex < text.length) {
      parts.push({
        type: 'normal',
        text: text.slice(lastIndex)
      });
    }
    
    return parts.length > 0 ? parts : [{ type: 'normal', text }];
  };

  if (showNameInput) {
    return (
      <div className="name-input-container">
        <div className="name-input-card">
          <img src="/kaoruko.png" alt="Kaoruko Waguri" className="character-image" />
          <h2>🌸 와구리 카오루코</h2>
          <p>키쿄 사립 학원 고등학생</p>
          <form onSubmit={handleNameSubmit} className="name-form">
            <label htmlFor="userName">당신의 이름을 알려주세요...</label>
            <input
              type="text"
              id="userName"
              value={userName}
              onChange={(e) => setUserName(e.target.value)}
              placeholder="이름을 입력해주세요"
              autoComplete="off"
            />
            <button type="submit">시작하기</button>
          </form>
        </div>
      </div>
    );
  }

  return (
    <div className="chat-container">
      <div className="chat-header">
        <div className="header-main">
          <img src="/kaoruko.png" alt="Kaoruko Waguri" className="header-image" />
          <div className="header-info">
            <div className="character-name">
              <h2>🌸 와구리 카오루코</h2>
              <span className="character-subtitle">키쿄 사립학원 · 17세</span>
              {/* 🎭 감정 표시 */}
              <div className="emotion-display" style={{ backgroundColor: currentEmotion.color }}>
                <span className="emotion-emoji" style={{ 
                  transform: `scale(${1 + (currentEmotion.intensity / 20)})`,
                  filter: `brightness(${0.8 + (currentEmotion.intensity / 50)})`
                }}>
                  {currentEmotion.emoji}
                </span>
                <span className="emotion-name">{currentEmotion.emotion}</span>
                <div className="emotion-intensity">
                  {Array.from({ length: 10 }, (_, i) => (
                    <span key={i} className={`intensity-dot ${i < currentEmotion.intensity ? 'active' : ''}`} />
                  ))}
                </div>
              </div>
              

            </div>
            <p className="greeting-text">안녕하세요 {userName}님... 오늘도 잘 부탁드립니다</p>
          </div>
          <div className="header-buttons">
            <button className="new-user-btn" onClick={handleNewUser} title="새로운 사용자로 시작">
              <span className="btn-icon">🆕</span>
              <span className="btn-text">새로시작</span>
            </button>
            <button className="end-conversation-btn" onClick={handleEndConversation} title="대화 종료">
              <span className="btn-icon">👋</span>
              <span className="btn-text">종료</span>
            </button>
          </div>
        </div>
        
        <div className="affection-card">
          <div className="affection-header">
            <span className={`relationship-badge ${affectionLevel < 0 ? 'negative' : ''}`}>{getRelationshipStage(affectionLevel)}</span>
            <span className="affection-score">{affectionLevel}<span className="max-score">/100</span></span>
            <button 
              className="toggle-affection-btn"
              onClick={() => setShowAffectionBar(!showAffectionBar)}
              title={showAffectionBar ? "호감도 바 숨기기" : "호감도 바 보이기"}
            >
              {showAffectionBar ? '🌸' : '�'}
            </button>
          </div>
          
          {showAffectionBar && (
            <>
              <div className="hearts-display">
            {[1, 2, 3, 4, 5].map((heart) => {
              if (affectionLevel >= 0) {
                const filledCount = Math.floor(affectionLevel / 20) + 1;
                return (
                  <span
                    key={heart}
                    className={`heart ${filledCount >= heart ? 'filled' : 'empty'}`}
                  >
                    💖
                  </span>
                );
              } else {
                // 음수일 때는 부서진 하트로 표시
                const brokenCount = Math.min(5, Math.ceil(Math.abs(affectionLevel) / 20));
                return (
                  <span
                    key={heart}
                    className={`heart negative ${brokenCount >= heart ? 'broken' : 'empty'}`}
                  >
                    �
                  </span>
                );
              }
            })}
          </div>
          
          <div className="progress-container">
            <div className="progress-track">
              <div 
                className={`progress-fill ${affectionLevel < 0 ? 'negative' : ''}`}
                style={{
                  width: `${getProgressPercentage(affectionLevel)}%`,
                  ...(affectionLevel < 0 && { 
                    marginLeft: `${100 - getProgressPercentage(affectionLevel)}%`,
                    marginRight: 0
                  })
                }}
              ></div>
            </div>
                <span className="progress-text">{Math.round(getProgressPercentage(affectionLevel))}%</span>
              </div>
              
              {affectionChange !== 0 && (
                <div className={`affection-notification ${affectionChange > 0 ? 'positive' : 'negative'}`}>
                  <span className="change-icon">{affectionChange > 0 ? '💕' : '💔'}</span>
                  <span className="change-text">
                    {affectionChange > 0 ? '+' : ''}{affectionChange}
                  </span>
                </div>
              )}
            </>
          )}
        </div>
      </div>
      <div className="message-list">
        {messages.map((msg, index) => (
          <div key={index} className={`message ${msg.sender}`}>
            <div className="message-content">
              {msg.sender === 'bot' ? (
                // 카오루코 메시지는 속마음 파싱 적용
                parseInnerThoughts(msg.text).map((part, partIndex) => (
                  <span key={partIndex} className={part.type === 'inner-thought' ? 'inner-thought' : ''}>
                    {part.type === 'inner-thought' ? `(${part.text})` : part.text}
                  </span>
                ))
              ) : (
                // 사용자 메시지는 그대로
                msg.text
              )}
            </div>
          </div>
        ))}
        {isLoading && (
          <div className="message bot">
            <span className="typing-indicator">...</span>
          </div>
        )}
      </div>
      <form className="message-form" onSubmit={handleSendMessage}>
        <input
          type="text"
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          placeholder="카오루코에게 메시지를 보내보세요..."
          disabled={isLoading}
        />
        <button type="submit" disabled={isLoading}>
          {isLoading ? '💭' : '💌 전송'}
        </button>
      </form>
    </div>
  );
}

export default App;
