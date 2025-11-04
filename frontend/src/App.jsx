import { useState } from 'react';
import './App.css';

function App() {
  const [messages, setMessages] = useState([]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [userName, setUserName] = useState('');
  const [showNameInput, setShowNameInput] = useState(true);

  const handleNameSubmit = (e) => {
    e.preventDefault();
    if (userName.trim() === '') return;
    
    setShowNameInput(false);
    // 카오루코의 첫 인사 메시지 추가
    const welcomeMessage = {
      text: `아... 안녕하세요, ${userName}님. 와구리 카오루코라고 합니다... 만나뵙게 되어 반갑습니다.`,
      sender: 'bot',
    };
    setMessages([welcomeMessage]);
  };

  const handleEndConversation = () => {
    // 대화 종료 확인
    if (window.confirm('정말로 대화를 종료하시겠어요? 카오루코가... 조금 아쉬워할 것 같아요...')) {
      // 마지막 인사 메시지 추가
      const farewell = {
        text: `${userName}님... 오늘 대화해주셔서 고마웠어요. 또... 또 만나요... 안녕히 가세요...`,
        sender: 'bot',
      };
      setMessages(prev => [...prev, farewell]);
      
      // 3초 후에 초기화
      setTimeout(() => {
        setMessages([]);
        setUserName('');
        setShowNameInput(true);
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
      
      const botMessage = {
        text: data.reply,
        sender: 'bot',
      };

      setMessages(prevMessages => [...prevMessages, botMessage]);

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
        <img src="/kaoruko.png" alt="Kaoruko Waguri" className="header-image" />
        <div className="header-text">
          <h2>🌸 와구리 카오루코</h2>
          <p>안녕하세요 {userName}님... 오늘도 잘 부탁드립니다</p>
        </div>
        <button className="end-conversation-btn" onClick={handleEndConversation} title="대화 종료">
          👋 종료
        </button>
      </div>
      <div className="message-list">
        {messages.map((msg, index) => (
          <div key={index} className={`message ${msg.sender}`}>
            {msg.text}
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
