import { useState, useEffect } from 'react';
import './App.css';

function App() {
  const [messages, setMessages] = useState([]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [userName, setUserName] = useState('');
  const [selectedCharacter, setSelectedCharacter] = useState('');
  const [showCharacterSelect, setShowCharacterSelect] = useState(true);
  const [showNameInput, setShowNameInput] = useState(false);
  const [affectionLevel, setAffectionLevel] = useState(0);
  const [affectionChange, setAffectionChange] = useState(0);
  const [showAffectionBar, setShowAffectionBar] = useState(true);
  
  // 🪙 코인 시스템 상태
  const [coins, setCoins] = useState(0);
  const [totalCoins, setTotalCoins] = useState(0);
  const [coinChange, setCoinChange] = useState(0);
  const [firstLogin, setFirstLogin] = useState(true);
  
    // � 상점 관련 상태
  const [showShop, setShowShop] = useState(false);
  const [currentTheme, setCurrentTheme] = useState('default');
  const [ownedItems, setOwnedItems] = useState(['default']);
  const [purchaseAnimation, setPurchaseAnimation] = useState('');
  
  // 🚀 부스터 관련 상태
  const [activeBooster, setActiveBooster] = useState(null);
  const [boosterTimeLeft, setBoosterTimeLeft] = useState(0);
  
  // 📋 구매 확인 및 인벤토리 상태
  const [showPurchaseConfirm, setShowPurchaseConfirm] = useState(false);
  const [selectedPurchaseItem, setSelectedPurchaseItem] = useState(null);
  const [showInventory, setShowInventory] = useState(false);
  
  // 🛠️ 개발자 모드 상태
  const [isDevMode, setIsDevMode] = useState(false);
  const [devAffectionLock, setDevAffectionLock] = useState(false);
  
  // 🎭 감정 시스템 2단계 state
  const [currentEmotion, setCurrentEmotion] = useState({
    emotion: '수줍음',
    intensity: 5,
    emoji: '😊',
    color: '#ffb3d9',
    reason: '기본 감정',
    confidence: 0.8
  });

  // 캐릭터별 감정 색상 가져오기
  const getEmotionColor = () => {
    if (selectedCharacter === 'reze') {
      // 레제용 보라색 베이스 색상들
      const rezeColors = {
        '수줍음': '#9932cc',
        '기쁨': '#8a2be2', 
        '흥미': '#7b68ee',
        '사랑': '#ba55d3',
        '슬픔': '#4b0082',
        '화남': '#6a0dad'
      };
      return rezeColors[currentEmotion.emotion] || '#8a2be2';
    } else {
      // 와구리용 핑크 베이스 색상들 (기본)
      const kaokurukoColors = {
        '수줍음': '#ffb3d9',
        '기쁨': '#ff69b4',
        '흥미': '#ffc0cb',
        '사랑': '#ff1493',
        '슬픔': '#db7093',
        '화남': '#dc143c'
      };
      return kaokurukoColors[currentEmotion.emotion] || '#ffb3d9';
    }
  };

  // 🛍️ 상점 아이템 데이터
  const shopItems = {
    themes: [
      { 
        id: 'purple', 
        name: '보라색 테마', 
        price: 50, 
        description: '우아한 보라색으로 변경',
        icon: '💜',
        type: 'theme'
      },
      { 
        id: 'blue', 
        name: '파란색 테마', 
        price: 50, 
        description: '시원한 파란색으로 변경',
        icon: '💙',
        type: 'theme'
      },
      { 
        id: 'green', 
        name: '초록색 테마', 
        price: 75, 
        description: '자연스러운 초록색으로 변경',
        icon: '💚',
        type: 'theme'
      },
      { 
        id: 'orange', 
        name: '주황색 테마', 
        price: 75, 
        description: '따뜻한 주황색으로 변경',
        icon: '🧡',
        type: 'theme'
      }
    ],
    boosters: [
      {
        id: 'affection_2x_5min',
        name: '호감도 2배 (5분)',
        price: 30,
        description: '5분간 호감도 획득량 2배',
        icon: '💕',
        type: 'booster',
        duration: 300000, // 5분 (밀리초)
        multiplier: 2
      },
      {
        id: 'affection_3x_3min',
        name: '호감도 3배 (3분)',
        price: 50,
        description: '3분간 호감도 획득량 3배',
        icon: '💖',
        type: 'booster',
        duration: 180000, // 3분
        multiplier: 3
      },
      {
        id: 'coin_2x_10min',
        name: '코인 2배 (10분)',
        price: 40,
        description: '10분간 코인 획득량 2배',
        icon: '🪙✨',
        type: 'booster',
        duration: 600000, // 10분
        multiplier: 2,
        coinBooster: true
      }
    ],
    direct: [
      {
        id: 'buy_affection_5',
        name: '호감도 +5',
        price: 100,
        description: '즉시 호감도 5 증가',
        icon: '💘',
        type: 'direct',
        affectionGain: 5
      },
      {
        id: 'buy_affection_10',
        name: '호감도 +10',
        price: 180,
        description: '즉시 호감도 10 증가',
        icon: '💝',
        type: 'direct',
        affectionGain: 10
      }
    ]
  };

  // 🛒 구매 확인 모달 열기
  const handlePurchaseClick = (item) => {
    // 테마 아이템이 이미 구매된 경우 직접 적용
    if (item.type === 'theme' && ownedItems.includes(item.id)) {
      handleThemeChange(item.id);
      return;
    }
    
    // 코인이 부족한 경우 알림
    if (coins < item.price) {
      alert(`코인이 부족합니다! (필요: ${item.price}코인, 보유: ${coins}코인)`);
      return;
    }
    
    setSelectedPurchaseItem(item);
    setShowPurchaseConfirm(true);
  };

  // 🛒 구매 확정 처리 함수
  const handlePurchaseConfirm = () => {
    const item = selectedPurchaseItem;
    if (!item || coins < item.price) return;

    // 코인 차감
    setCoins(prev => prev - item.price);
    setPurchaseAnimation(item.id);
    setTimeout(() => setPurchaseAnimation(''), 2000);
    
    // 아이템 타입별 처리
    if (item.type === 'theme' && !ownedItems.includes(item.id)) {
      // 테마 아이템: 소유 목록에 추가 후 즉시 적용
      setOwnedItems(prev => [...prev, item.id]);
      handleThemeChange(item.id);
    } else if (item.type === 'booster') {
      // 부스터 아이템: 반복 구매 가능
      setActiveBooster(item);
      setBoosterTimeLeft(item.duration);
      
      // 타이머 시작
      const startTime = Date.now();
      const timer = setInterval(() => {
        const elapsed = Date.now() - startTime;
        const remaining = item.duration - elapsed;
        
        if (remaining <= 0) {
          setActiveBooster(null);
          setBoosterTimeLeft(0);
          clearInterval(timer);
        } else {
          setBoosterTimeLeft(remaining);
        }
      }, 1000);
    } else if (item.type === 'direct') {
      // 직접 구매 아이템: 반복 구매 가능
      if (item.affectionGain) {
        setAffectionLevel(prev => prev + item.affectionGain);
      }
      if (item.coinGain) {
        setCoins(prev => prev + item.coinGain);
        setTotalCoins(prev => prev + item.coinGain);
      }
    }
    
    // 모달 닫기
    setShowPurchaseConfirm(false);
    setSelectedPurchaseItem(null);
  };

  // 🎨 테마 변경 함수
  const handleThemeChange = (themeId) => {
    setCurrentTheme(themeId);
    const chatContainer = document.querySelector('.chat-container');
    if (chatContainer) {
      // 기존 테마 클래스 제거
      chatContainer.classList.remove('theme-purple', 'theme-blue', 'theme-green', 'theme-orange');
      // 새 테마 적용
      if (themeId !== 'default') {
        chatContainer.classList.add(`theme-${themeId}`);
      }
    }
  };
  


  // 컴포넌트 마운트 시 저장된 사용자 정보 확인
  useEffect(() => {
    const savedUserName = localStorage.getItem('chatbot_user_name');
    const savedCharacter = localStorage.getItem('chatbot_selected_character');
    const savedAffection = localStorage.getItem('chatbot_affection_level');
    const sessionStarted = localStorage.getItem('chatbot_session_active');
    
    // 세션이 활성 상태이고 저장된 정보가 있는 경우에만 복원
    if (savedUserName && savedCharacter && sessionStarted === 'true') {
      setUserName(savedUserName);
      setSelectedCharacter(savedCharacter);
      setShowCharacterSelect(false);
      setShowNameInput(false);
      if (savedAffection) {
        setAffectionLevel(parseInt(savedAffection));
      }
      
      // 🪙 코인 정보 복원
      const savedCoins = localStorage.getItem('chatbot_coins');
      const savedTotalCoins = localStorage.getItem('chatbot_total_coins');
      const savedFirstLogin = localStorage.getItem('chatbot_first_login');
      
      if (savedCoins) {
        setCoins(parseInt(savedCoins));
      }
      if (savedTotalCoins) {
        setTotalCoins(parseInt(savedTotalCoins));
      }
      if (savedFirstLogin !== null) {
        setFirstLogin(savedFirstLogin === 'true');
      }
      
      // 🎨 테마 및 소유 아이템 정보 복원
      const savedTheme = localStorage.getItem('chatbot_current_theme');
      const savedOwnedItems = localStorage.getItem('chatbot_owned_items');
      
      if (savedTheme) {
        setCurrentTheme(savedTheme);
      }
      if (savedOwnedItems) {
        setOwnedItems(JSON.parse(savedOwnedItems));
      }
      
      // 🛠️ 개발자 모드 상태 복원
      const savedDevMode = localStorage.getItem('chatbot_dev_mode');
      const savedDevAffectionLock = localStorage.getItem('chatbot_dev_affection_lock');
      
      if (savedDevMode === 'true') {
        setIsDevMode(true);
        console.log('🛠️ 개발자 모드 복원됨');
      }
      if (savedDevAffectionLock === 'true') {
        setDevAffectionLock(true);
        console.log('🔒 개발자 호감도 락 복원됨');
      }
      
      // 캐릭터별 환영 메시지
      const welcomeMessage = savedCharacter === 'kaoruko' 
        ? { text: `어... ${savedUserName}님, 다시 만나서 반가워요... 기다리고 있었어요.`, sender: 'bot' }
        : { text: `${savedUserName}님! 다시 만나네요. 어디 갔다 온 거예요?`, sender: 'bot' };
      
      setMessages([welcomeMessage]);
    } else {
      // 세션이 없거나 비활성 상태면 초기화
      localStorage.removeItem('chatbot_user_name');
      localStorage.removeItem('chatbot_selected_character');
      localStorage.removeItem('chatbot_affection_level');
      localStorage.removeItem('chatbot_session_active');
      
      // 🪙 코인 정보도 초기화
      localStorage.removeItem('chatbot_coins');
      localStorage.removeItem('chatbot_total_coins');
      localStorage.removeItem('chatbot_first_login');
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

  // 🪙 코인 정보 저장
  useEffect(() => {
    if (userName) { // 사용자가 있을 때만 코인 정보 저장
      localStorage.setItem('chatbot_coins', coins.toString());
      localStorage.setItem('chatbot_total_coins', totalCoins.toString());
      localStorage.setItem('chatbot_first_login', firstLogin.toString());
    }
  }, [coins, totalCoins, firstLogin, userName]);

  // 🎨 테마 및 소유 아이템 정보 저장
  useEffect(() => {
    if (userName) {
      localStorage.setItem('chatbot_current_theme', currentTheme);
      localStorage.setItem('chatbot_owned_items', JSON.stringify(ownedItems));
    }
  }, [currentTheme, ownedItems, userName]);

  // 🎨 테마 적용 (컴포넌트 마운트 시 및 테마 변경 시)
  useEffect(() => {
    const chatContainer = document.querySelector('.chat-container');
    if (chatContainer && currentTheme !== 'default') {
      // 기존 테마 클래스 모두 제거
      chatContainer.classList.remove('theme-purple', 'theme-blue', 'theme-green', 'theme-orange');
      // 새 테마 적용
      chatContainer.classList.add(`theme-${currentTheme}`);
    }
  }, [currentTheme]);

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

  // 캐릭터 선택 핸들러
  const handleCharacterSelect = (character) => {
    setSelectedCharacter(character);
    setShowCharacterSelect(false);
    setShowNameInput(true);
  };

  // 호감도에 따른 관계 단계 계산
  const getRelationshipStage = (level) => {
    if (level < 0) return "멀어진사람";
    if (level >= 81) return "특별한사람";
    if (level >= 61) return "절친";
    if (level >= 41) return "친구";
    if (level >= 21) return "지인";
    return "낯선사람";
  };

  // 호감도에 맞는 감정 상태 업데이트
  const updateEmotionByAffection = (level) => {
    if (level >= 81) {
      setCurrentEmotion({
        emotion: '사랑',
        intensity: 9,
        emoji: '🥰',
        color: selectedCharacter === 'reze' ? '#ff69b4' : '#ffb3d9',
        reason: '깊은 애정',
        confidence: 0.95
      });
    } else if (level >= 61) {
      setCurrentEmotion({
        emotion: '친밀함',
        intensity: 7,
        emoji: '😊',
        color: selectedCharacter === 'reze' ? '#dda0dd' : '#ffcccb',
        reason: '친근한 관계',
        confidence: 0.85
      });
    } else if (level >= 41) {
      setCurrentEmotion({
        emotion: '호감',
        intensity: 6,
        emoji: '😄',
        color: selectedCharacter === 'reze' ? '#ba55d3' : '#ffd1dc',
        reason: '좋은 인상',
        confidence: 0.75
      });
    } else if (level >= 21) {
      setCurrentEmotion({
        emotion: '관심',
        intensity: 4,
        emoji: '🙂',
        color: selectedCharacter === 'reze' ? '#9370db' : '#ffe4e1',
        reason: '약간의 관심',
        confidence: 0.65
      });
    } else if (level >= 0) {
      setCurrentEmotion({
        emotion: '평범',
        intensity: 3,
        emoji: '😐',
        color: selectedCharacter === 'reze' ? '#8a2be2' : '#f0f0f0',
        reason: '무난한 관계',
        confidence: 0.5
      });
    } else {
      setCurrentEmotion({
        emotion: '불편함',
        intensity: 2,
        emoji: '😞',
        color: selectedCharacter === 'reze' ? '#4b0082' : '#ffb6c1',
        reason: '좋지 않은 관계',
        confidence: 0.8
      });
    }
  };

  // 호감도 변화에 대한 캐릭터 반응 메시지
  const getAffectionReactionMessage = (oldLevel, newLevel, character) => {
    const levelDiff = newLevel - oldLevel;
    const isKaoruko = character !== 'reze';
    
    // 큰 변화일 때 (50 이상 차이)
    if (Math.abs(levelDiff) >= 50) {
      if (newLevel >= 81) {
        return isKaoruko 
          ? "어...? 갑자기 마음이 이렇게 뜨거워지는 게... 이상해요. 강희님한테 이런 감정을 느끼다니... 💕" 
          : "뭐야... 갑자기 이 기분은? 강희한테 이런 감정을 느끼게 될 줄은 몰랐는데... 흥미롭군. 💜";
      } else if (newLevel >= 61) {
        return isKaoruko
          ? "어? 왠지 강희님이 정말 좋아 보여요! 친한 친구가 된 것 같아서 기뻐요~ 😊"
          : "흠... 강희가 꽤 괜찮은 놈인 것 같네. 이 정도면 나쁘지 않아.";
      } else if (newLevel >= 21) {
        return isKaoruko
          ? "강희님에 대해서 좀 더 알고 싶어졌어요. 좋은 사람인 것 같아요!"
          : "강희... 처음보단 나아 보이는군. 그럭저럭 괜찮은 것 같아.";
      } else if (newLevel >= 0) {
        return isKaoruko
          ? "음... 강희님과는 평범한 관계인 것 같아요. 그냥 그런 사이?"
          : "강희인가? 그냥 그런 놈이네. 특별할 건 없어 보이고.";
      } else {
        return isKaoruko
          ? "어... 왠지 강희님과 있으면 불편해요. 뭔가 안 좋은 일이 있었나?"
          : "강희... 뭔가 마음에 안 들어. 가까이 오지 마.";
      }
    }
    
    // 일반적인 변화
    if (levelDiff > 0) {
      return isKaoruko
        ? "어? 왠지 강희님이 더 좋아 보여요! 😊"
        : "흠... 강희가 조금 나아 보이네.";
    } else if (levelDiff < 0) {
      return isKaoruko
        ? "어... 왠지 기분이 별로예요. 뭔가 서운해요..."
        : "tch... 강희한테 실망했어.";
    } else {
      return isKaoruko
        ? "어라? 뭔가 이상한 기분이에요..."
        : "뭔가... 이상하네?";
    }
  };

  // 호감도 하트 표시는 이제 JSX에서 직접 렌더링

  // 호감도 진행률 계산
  const getProgressPercentage = (level) => {
    // 음수인 경우는 부정적 진행을 -100 기준으로 퍼센트 표시
    if (level < 0) {
      return Math.min(100, (Math.abs(level) / 100) * 100);
    }

    // 0-100을 직접 퍼센트로 변환 (더 직관적)
    return Math.min(100, Math.max(0, level));
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
    
    // 로컬스토리지에 사용자 정보 저장
    localStorage.setItem('chatbot_user_name', userName);
    localStorage.setItem('chatbot_selected_character', selectedCharacter);
    localStorage.setItem('chatbot_session_active', 'true');
    
    // 🪙 첫 로그인 환영 보너스 (100코인)
    if (firstLogin) {
      setCoins(100);
      setTotalCoins(100);
      setFirstLogin(false);
      setCoinChange(100);
      setTimeout(() => setCoinChange(0), 5000); // 5초간 표시
    }
    
    setShowNameInput(false);
    
    // 캐릭터별 첫 인사 메시지
    const welcomeMessage = selectedCharacter === 'kaoruko' 
      ? { text: `아... 안녕하세요, ${userName}님. 와구리 카오루코라고 합니다... 만나뵙게 되어 반갑습니다.`, sender: 'bot' }
      : { text: `안녕하세요! ${userName}님이네요? 저는 레제예요! ${userName}님 같이 재미있는 사람은 처음이에요!`, sender: 'bot' };
    
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
      localStorage.removeItem('chatbot_user_name');
      localStorage.removeItem('chatbot_selected_character');
      localStorage.removeItem('chatbot_affection_level');
      localStorage.removeItem('chatbot_session_active');
      localStorage.removeItem('chatbot_coins');
      localStorage.removeItem('chatbot_total_coins');
      localStorage.removeItem('chatbot_first_login');
      localStorage.removeItem('chatbot_current_theme');
      localStorage.removeItem('chatbot_owned_items');
      
      // 상태 즉시 초기화
      setMessages([]);
      setUserName('');
      setSelectedCharacter('');
      setShowCharacterSelect(true);
      setShowNameInput(false);
      setAffectionLevel(0);
      setAffectionChange(0);
      setCoins(0);
      setTotalCoins(0);
      setFirstLogin(true);
      setCurrentTheme('default');
      setOwnedItems(['default']);
      setActiveBooster(null);
      setBoosterTimeLeft(0);
    }
  };

  const handleEndConversation = () => {
    // 캐릭터별 종료 확인 메시지
    const confirmMessage = selectedCharacter === 'kaoruko' 
      ? '정말로 대화를 종료하시겠어요? 카오루코가... 조금 아쉬워할 것 같아요...'
      : '정말로 대화를 종료하시겠어요? 레제랑 더 놀고 싶지 않아요?';
      
    if (window.confirm(confirmMessage)) {
      // 세션을 비활성 상태로 설정 (즉시)
      localStorage.setItem('chatbot_session_active', 'false');
      
      // 캐릭터별 마지막 인사 메시지
      const farewell = selectedCharacter === 'kaoruko'
        ? { text: `${userName}님... 오늘 대화해주셔서 고마웠어요. 또... 또 만나요... 안녕히 가세요...`, sender: 'bot' }
        : { text: `${userName}님! 오늘 정말 재밌었어요! 또 만나요~ 안녕!`, sender: 'bot' };
        
      setMessages(prev => [...prev, farewell]);
      
      // 3초 후에 완전 초기화
      setTimeout(() => {
        // 로컬스토리지 완전 정리
        localStorage.removeItem('chatbot_user_name');
        localStorage.removeItem('chatbot_selected_character');
        localStorage.removeItem('chatbot_affection_level');
        localStorage.removeItem('chatbot_session_active');
        localStorage.removeItem('chatbot_coins');
        localStorage.removeItem('chatbot_total_coins');
        localStorage.removeItem('chatbot_first_login');
        localStorage.removeItem('chatbot_current_theme');
        localStorage.removeItem('chatbot_owned_items');
        
        // 상태 초기화
        setMessages([]);
        setUserName('');
        setSelectedCharacter('');
        setShowCharacterSelect(true);
        setShowNameInput(false);
        setAffectionLevel(0);
        setAffectionChange(0);
        setCoins(0);
        setTotalCoins(0);
        setFirstLogin(true);
        setCurrentTheme('default');
        setOwnedItems(['default']);
        setActiveBooster(null);
        setBoosterTimeLeft(0);
      }, 3000);
    }
  };

  const handleSendMessage = async (e) => {
    e.preventDefault();
    if (inputValue.trim() === '' || isLoading) return;

    // 🛠️ 개발자 치트 명령어
    const message = inputValue.trim();
    console.log('입력된 메시지:', message); // 디버깅용
    if (message.startsWith('/dev')) {
      console.log('개발자 명령어 감지!'); // 디버깅용
      const command = message.split(' ')[1];
      console.log('명령어:', command); // 디버깅용
      
      if (command === 'maxaffection' || command === 'max호감도' || command === '호감도100') {
        console.log('호감도 100 설정 시작, 현재 호감도:', affectionLevel);
        const oldAffection = affectionLevel;
        const newAffection = 100;
        
        // 호감도 업데이트
        setAffectionLevel(newAffection);
        setAffectionChange(newAffection - oldAffection);
        setTimeout(() => setAffectionChange(0), 3000);
        
        // 개발자 모드 활성화 - 서버 응답으로 호감도가 덮어쓰이지 않도록 보호
        setIsDevMode(true);
        setDevAffectionLock(true);
        
        // 호감도에 맞는 감정 상태 업데이트
        updateEmotionByAffection(newAffection);
        
        // localStorage에 즉시 저장
        localStorage.setItem('kaoruko_affection_level', newAffection.toString());
        localStorage.setItem('kaoruko_dev_mode', 'true');
        
        // 캐릭터가 호감도 변화를 인지한 메시지 추가
        const characterReactionMessage = {
          text: getAffectionReactionMessage(oldAffection, newAffection, selectedCharacter),
          sender: 'bot',
        };
        
        const systemMessage = {
          text: `🛠️ [개발자 모드] 호감도가 ${oldAffection} → ${newAffection}으로 설정되었습니다!`,
          sender: 'system',
        };
        
        setMessages(prevMessages => [...prevMessages, systemMessage, characterReactionMessage]);
        setInputValue('');
        return;
      }
      
      // 동적 코인 지급 시스템 (예: /dev coins1000, /dev coins500)
      if (command.startsWith('coins')) {
        const coinAmountStr = command.replace('coins', '');
        const coinAmount = parseInt(coinAmountStr);
        
        if (isNaN(coinAmount) || coinAmount <= 0) {
          const systemMessage = {
            text: '🛠️ [개발자 모드] 올바른 코인 수량을 입력하세요. (예: /dev coins1000)',
            sender: 'system',
          };
          setMessages(prevMessages => [...prevMessages, systemMessage]);
          setInputValue('');
          return;
        }
        
        if (coinAmount > 100000) {
          const systemMessage = {
            text: '🛠️ [개발자 모드] 한 번에 최대 100,000코인까지만 지급 가능합니다.',
            sender: 'system',
          };
          setMessages(prevMessages => [...prevMessages, systemMessage]);
          setInputValue('');
          return;
        }
        
        setCoins(prev => prev + coinAmount);
        setTotalCoins(prev => prev + coinAmount);
        setCoinChange(coinAmount);
        setTimeout(() => setCoinChange(0), 3000);
        
        // localStorage에 저장
        localStorage.setItem('chatbot_coins', (coins + coinAmount).toString());
        localStorage.setItem('chatbot_total_coins', (totalCoins + coinAmount).toString());
        
        const systemMessage = {
          text: `🛠️ [개발자 모드] ${coinAmount.toLocaleString()}코인이 지급되었습니다! 💰`,
          sender: 'system',
        };
        setMessages(prevMessages => [...prevMessages, systemMessage]);
        setInputValue('');
        return;
      }
      
      if (command === 'allitems' || command === '모든아이템') {
        setOwnedItems(['default', 'purple', 'blue', 'green', 'orange']);
        
        const systemMessage = {
          text: '🛠️ [개발자 모드] 모든 테마 아이템을 획득했습니다!',
          sender: 'system',
        };
        setMessages(prevMessages => [...prevMessages, systemMessage]);
        setInputValue('');
        return;
      }
      
      // 호감도 특정 값 설정 (예: /dev affection 50)
      if (command === 'affection' || command === '호감도') {
        const value = parseInt(message.split(' ')[2]);
        if (!isNaN(value) && value >= -100 && value <= 100) {
          console.log(`호감도 ${value} 설정 시작`);
          const oldAffection = affectionLevel;
          const newAffection = value;
          
          // 호감도 업데이트
          setAffectionLevel(newAffection);
          setAffectionChange(newAffection - oldAffection);
          setTimeout(() => setAffectionChange(0), 3000);
          
          // 개발자 모드 활성화 - 서버 응답으로 호감도가 덮어쓰이지 않도록 보호
          setIsDevMode(true);
          setDevAffectionLock(true);
          
          // 호감도에 맞는 감정 상태 업데이트
          updateEmotionByAffection(newAffection);
          
          localStorage.setItem('kaoruko_affection_level', newAffection.toString());
          localStorage.setItem('kaoruko_dev_mode', 'true');
          
          // 캐릭터가 호감도 변화를 인지한 메시지 추가
          const characterReactionMessage = {
            text: getAffectionReactionMessage(oldAffection, newAffection, selectedCharacter),
            sender: 'bot',
          };
          
          const systemMessage = {
            text: `🛠️ [개발자 모드] 호감도가 ${oldAffection} → ${newAffection}로 설정되었습니다!`,
            sender: 'system',
          };
          
          setMessages(prevMessages => [...prevMessages, systemMessage, characterReactionMessage]);
          setInputValue('');
          return;
        } else {
          const errorMessage = {
            text: `🛠️ [개발자 모드] 잘못된 호감도 값입니다. (-100 ~ 100 사이의 숫자를 입력하세요)\n예: /dev affection 50`,
            sender: 'system',
          };
          setMessages(prevMessages => [...prevMessages, errorMessage]);
          setInputValue('');
          return;
        }
      }
      
      if (command === 'reset' || command === '리셋') {
        // 개발자 모드 해제 및 일반 모드로 복원
        setIsDevMode(false);
        setDevAffectionLock(false);
        localStorage.removeItem('kaoruko_dev_mode');
        
        const resetMessage = {
          text: '🛠️ [개발자 모드] 개발자 모드가 해제되었습니다. 이제 서버와 정상적으로 동기화됩니다.',
          sender: 'system',
        };
        setMessages(prevMessages => [...prevMessages, resetMessage]);
        setInputValue('');
        return;
      }
      
      if (command === 'status' || command === '상태') {
        // 개발자 모드 상태 확인
        const statusMessage = {
          text: `🛠️ [개발자 모드 상태]
개발자 모드: ${isDevMode ? '활성화' : '비활성화'}
호감도 락: ${devAffectionLock ? '잠김' : '해제'}
현재 호감도: ${affectionLevel}
관계 단계: ${getRelationshipStage(affectionLevel)}`,
          sender: 'system',
        };
        setMessages(prevMessages => [...prevMessages, statusMessage]);
        setInputValue('');
        return;
      }
      
      if (command === 'help' || command === '도움말') {
        const helpMessage = {
          text: `🛠️ [개발자 명령어 목록]
/dev maxaffection - 호감도 100 설정
/dev affection [숫자] - 호감도를 특정 값으로 설정 (-100~100)
/dev coins[숫자] - 원하는 코인 지급 (예: /dev coins500, /dev coins10000)
/dev allitems - 모든 아이템 획득
/dev reset - 개발자 모드 해제 (서버 동기화 복원)
/dev status - 개발자 모드 상태 확인
/dev test - 테스트 메시지
/dev help - 도움말 표시

💡 팁: coins 명령어는 1~100,000 범위에서 자유롭게 사용 가능합니다!`,
          sender: 'system',
        };
        setMessages(prevMessages => [...prevMessages, helpMessage]);
        setInputValue('');
        return;
      }
      
      if (command === 'test' || command === '테스트') {
        console.log('테스트 명령어 실행됨!');
        const testMessage = {
          text: '🛠️ [개발자 모드] 테스트 성공! 개발자 명령어가 정상 작동합니다.',
          sender: 'system',
        };
        setMessages(prevMessages => [...prevMessages, testMessage]);
        setInputValue('');
        return;
      }
      
      // 인식되지 않은 개발자 명령어
      const unknownMessage = {
        text: `🛠️ [개발자 모드] 알 수 없는 명령어: "${command}"\n/dev help로 사용 가능한 명령어를 확인하세요.`,
        sender: 'system',
      };
      setMessages(prevMessages => [...prevMessages, unknownMessage]);
      setInputValue('');
      return;
    }

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
      
      // 호감도 정보 업데이트 (개발자 모드가 아닐 때만)
      if (data.affection_level !== undefined && !devAffectionLock) {
        setAffectionLevel(data.affection_level);
      }
      if (data.affection_change !== undefined && data.affection_change !== 0) {
        setAffectionChange(data.affection_change);
        // 호감도 변화 알림을 3초 후 제거
        setTimeout(() => setAffectionChange(0), 3000);
        
        // 🪙 호감도 변화시 보너스 코인 지급 (호감도 +1당 20코인)
        if (data.affection_change > 0) {
          // 부스터 배수 적용 (코인 부스터만)
          const coinMultiplier = activeBooster?.coinBooster ? activeBooster.multiplier : 1;
          const bonusCoins = data.affection_change * 20 * coinMultiplier;
          setCoins(prev => prev + bonusCoins);
          setTotalCoins(prev => prev + bonusCoins);
          setCoinChange(bonusCoins);
          setTimeout(() => setCoinChange(0), 3000);
        }
      }
      
      // 🪙 대화 기본 보상 (1회당 5코인)
      // 부스터 배수 적용 (코인 부스터만)
      const coinMultiplier = activeBooster?.coinBooster ? activeBooster.multiplier : 1;
      const chatReward = 5 * coinMultiplier;
      setCoins(prev => prev + chatReward);
      setTotalCoins(prev => prev + chatReward);
      if (data.affection_change === undefined || data.affection_change === 0) {
        setCoinChange(chatReward);
        setTimeout(() => setCoinChange(0), 3000);
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

  // 캐릭터 선택 화면
  if (showCharacterSelect) {
    return (
      <div className="character-select-container">
        <div className="character-select-card">
          <h1>💕 AI 챗봇 선택</h1>
          <p>대화하고 싶은 캐릭터를 선택해주세요</p>
          
          <div className="character-options">
            <div 
              className="character-option kaoruko"
              onClick={() => handleCharacterSelect('kaoruko')}
            >
              <img src="/kaoruko.png" alt="Kaoruko Waguri" className="character-preview" />
              <h3>🌸 와구리 카오루코</h3>
              <p className="character-desc">키쿄 사립학원 · 17세</p>
              <p className="character-personality">수줍고 정중하며 상냥한 단데레 타입</p>
            </div>
            
            <div 
              className="character-option reze"
              onClick={() => handleCharacterSelect('reze')}
            >
              <img src="/Reze.png" alt="Reze" className="character-preview" />
              <h3>🩸 레제</h3>
              <p className="character-desc">카페 종업원 · 16세</p>
              <p className="character-personality">호기심 많고 직설적인 매닉 픽시 드림 걸</p>
            </div>
          </div>
        </div>
      </div>
    );
  }

  if (showNameInput) {
    const characterInfo = selectedCharacter === 'kaoruko' 
      ? {
          image: '/Waguri_main.png',
          alt: 'Kaoruko Waguri',
          name: '🌸 와구리 카오루코',
          desc: '키쿄 사립 학원 고등학생',
          label: '당신의 이름을 알려주세요...',
          placeholder: '이름을 입력해주세요'
        }
      : {
          image: '/Reze_main.png',
          alt: 'Reze',
          name: '🩸 레제',
          desc: '카페 종업원',
          label: '이름이 뭐예요?',
          placeholder: '이름을 알려주세요!'
        };

    return (
      <div className={`name-input-container ${selectedCharacter}`}>
        <div className="name-input-card">
          <button 
            className="back-button"
            onClick={() => {
              setShowNameInput(false);
              setShowCharacterSelect(true);
              setSelectedCharacter('');
            }}
          >
            ← 캐릭터 다시 선택
          </button>
          <img src={characterInfo.image} alt={characterInfo.alt} className="character-image" />
          <h2>{characterInfo.name}</h2>
          <p>{characterInfo.desc}</p>
          <form onSubmit={handleNameSubmit} className="name-form">
            <label htmlFor="userName">{characterInfo.label}</label>
            <input
              type="text"
              id="userName"
              value={userName}
              onChange={(e) => setUserName(e.target.value)}
              placeholder={characterInfo.placeholder}
              autoComplete="off"
            />
            <button type="submit">시작하기</button>
          </form>
        </div>
      </div>
    );
  }

  // 캐릭터 정보 가져오기
  const getCharacterInfo = () => {
    return selectedCharacter === 'kaoruko' 
      ? {
          image: '/kaoruko_profile.png',
          alt: 'Kaoruko Waguri',
          name: '🌸 와구리 카오루코',
          subtitle: '키쿄 사립학원 · 17세',
          greeting: `안녕하세요 ${userName}님... 오늘도 잘 부탁드립니다`
        }
      : {
          image: '/Reze_profile.png',
          alt: 'Reze',
          name: '🩸 레제',
          subtitle: '카페 종업원 · 16세',
          greeting: `${userName}님! 오늘은 뭐 할까요?`
        };
  };

  const characterInfo = getCharacterInfo();

  return (
    <div className={`chat-container ${selectedCharacter} ${currentTheme !== 'default' ? `theme-${currentTheme}` : ''}`}>
      <div className="chat-header">
        <div className="header-main">
          <img src={characterInfo.image} alt={characterInfo.alt} className="header-image" />
          <div className="header-info">
            <div className="character-name">
              <h2>{characterInfo.name}</h2>
              <span className="character-subtitle">{characterInfo.subtitle}</span>
              {/* 🎭 감정 표시 */}
              <div className="emotion-display" style={{ backgroundColor: getEmotionColor() }}>
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
            <p className="greeting-text">{characterInfo.greeting}</p>
          </div>
          <div className="header-buttons">
            {/* 첫 번째 줄: 상점/인벤토리/코인 */}
            <div className="button-row-top">
              <button className="shop-btn" onClick={() => setShowShop(true)} title="상점">
                <span className="btn-icon">🛍️</span>
              </button>
              
              <button className="inventory-btn" onClick={() => setShowInventory(true)} title="인벤토리">
                <span className="btn-icon">🎒</span>
              </button>
              
              <div className="coin-display" title={`총 누적: ${totalCoins}코인`}>
                <span className="coin-icon">🪙</span>
                <span className="coin-amount">{coins}</span>
                {coinChange > 0 && (
                  <div className="coin-gain-animation">+{coinChange}</div>
                )}
              </div>
            </div>
            
            {/* 두 번째 줄: 새로시작/종료 */}
            <div className="button-row-bottom">
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
              {selectedCharacter === 'reze' 
                ? (showAffectionBar ? '💜' : '🖤') 
                : (showAffectionBar ? '🩷' : '❤️')
              }
            </button>
          </div>
          
          {showAffectionBar && (
            <>
              <div className="hearts-display">
            {[1, 2, 3, 4, 5].map((heart) => {
              if (affectionLevel >= 0) {
                const filledCount = Math.floor(affectionLevel / 20) + 1;
                const heartIcon = selectedCharacter === 'reze' ? '💜' : '💖';
                return (
                  <span
                    key={heart}
                    className={`heart ${filledCount >= heart ? 'filled' : 'empty'}`}
                  >
                    {heartIcon}
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
                    💔
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
                  <span className="change-icon">
                    {affectionChange > 0 
                      ? (selectedCharacter === 'reze' ? '�' : '�💕')
                      : '💔'
                    }
                  </span>
                  <span className="change-text">
                    {affectionChange > 0 ? '+' : ''}{affectionChange}
                  </span>
                </div>
              )}
              
              {/* 🚀 부스터 상태 표시 */}
              {activeBooster && (
                <div className="booster-status">
                  <span className="booster-icon">{activeBooster.icon}</span>
                  <span className="booster-text">
                    {activeBooster.name} - {Math.ceil(boosterTimeLeft / 1000)}초
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
          placeholder={selectedCharacter === 'reze' ? '레제에게 메시지를 보내보세요...' : '와구리 카오루코 에게 메시지를 보내보세요...'}
          disabled={isLoading}
        />
        <button type="submit" disabled={isLoading}>
          {isLoading ? '💭' : '💌 전송'}
        </button>
      </form>

      {/* 🛍️ 상점 모달 */}
      {showShop && (
        <div className="shop-modal" onClick={(e) => e.target.className === 'shop-modal' && setShowShop(false)}>
          <div className="shop-content">
            <button className="shop-close" onClick={() => setShowShop(false)}>×</button>
            
            <div className="shop-header">
              <h2>🛍️ 상점</h2>
              <div className="coin-display">
                <span className="coin-icon">🪙</span>
                <span className="coin-amount">{coins}</span>
              </div>
            </div>

            <div className="shop-section">
              <h3>🚀 부스터</h3>
              <div className="shop-items">
                {shopItems.boosters.map(booster => (
                  <div 
                    key={booster.id}
                    className={`shop-item ${purchaseAnimation === booster.id ? 'purchase-animation' : ''}`}
                    onClick={() => handlePurchaseClick(booster)}
                  >
                    <div className="shop-item-icon">{booster.icon}</div>
                    <div className="shop-item-name">{booster.name}</div>
                    <div className="shop-item-description">{booster.description}</div>
                    <div className="shop-item-price">
                      <span className="coin-icon">🪙</span>
                      {booster.price}
                    </div>
                  </div>
                ))}
              </div>
            </div>

            <div className="shop-section">
              <h3>💎 즉시 구매</h3>
              <div className="shop-items">
                {shopItems.direct.map(item => (
                  <div 
                    key={item.id}
                    className={`shop-item ${purchaseAnimation === item.id ? 'purchase-animation' : ''}`}
                    onClick={() => handlePurchaseClick(item)}
                  >
                    <div className="shop-item-icon">{item.icon}</div>
                    <div className="shop-item-name">{item.name}</div>
                    <div className="shop-item-description">{item.description}</div>
                    <div className="shop-item-price">
                      <span className="coin-icon">🪙</span>
                      {item.price}
                    </div>
                  </div>
                ))}
              </div>
            </div>
            
            <div className="shop-section">
              <h3>🎨 테마</h3>
              <div className="shop-items">
                {shopItems.themes.map(theme => (
                  <div 
                    key={theme.id}
                    className={`shop-item ${ownedItems.includes(theme.id) ? 'owned' : ''} ${purchaseAnimation === theme.id ? 'purchase-animation' : ''} ${currentTheme === theme.id ? 'active' : ''}`}
                    onClick={() => handlePurchaseClick(theme)}
                  >
                    <div className="shop-item-icon">{theme.icon}</div>
                    <div className="shop-item-name">{theme.name}</div>
                    <div className="shop-item-description">{theme.description}</div>
                    <div className="shop-item-price">
                      {ownedItems.includes(theme.id) ? (
                        currentTheme === theme.id ? '사용중' : '적용하기'
                      ) : (
                        <>
                          <span className="coin-icon">🪙</span>
                          {theme.price}
                        </>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      )}

      {/* 📋 구매 확인 팝업 모달 */}
      {showPurchaseConfirm && selectedPurchaseItem && (
        <div className="purchase-popup-overlay" onClick={(e) => e.target.className === 'purchase-popup-overlay' && setShowPurchaseConfirm(false)}>
          <div className="purchase-popup-modal">
            <div className="purchase-popup-header">
              <h3>🛒 구매 확인</h3>
              <button className="popup-close-btn" onClick={() => setShowPurchaseConfirm(false)}>✕</button>
            </div>
            <div className="purchase-item-preview">
              <div className="item-icon-large">{selectedPurchaseItem.icon}</div>
              <div className="item-details">
                <div className="item-name">{selectedPurchaseItem.name}</div>
                <div className="item-description">{selectedPurchaseItem.description}</div>
              </div>
            </div>
            <div className="purchase-price-info">
              <div className="price-row">
                <span>가격</span>
                <span className="price-value">
                  <span className="coin-icon">🪙</span>
                  {selectedPurchaseItem.price}코인
                </span>
              </div>
              <div className="balance-row">
                <span>보유 코인</span>
                <span className="balance-value">{coins}🪙</span>
              </div>
              <hr className="price-divider" />
              <div className="remaining-row">
                <span>구매 후 잔액</span>
                <span className={`remaining-value ${coins - selectedPurchaseItem.price < 0 ? 'insufficient' : 'sufficient'}`}>
                  {coins - selectedPurchaseItem.price}🪙
                </span>
              </div>
            </div>
            <div className="purchase-popup-buttons">
              <button className="popup-btn popup-cancel" onClick={() => setShowPurchaseConfirm(false)}>
                취소
              </button>
              <button 
                className={`popup-btn popup-confirm ${coins < selectedPurchaseItem.price ? 'disabled' : ''}`}
                onClick={handlePurchaseConfirm}
                disabled={coins < selectedPurchaseItem.price}
              >
                구매하기
              </button>
            </div>
          </div>
        </div>
      )}

      {/* 🎒 인벤토리 모달 */}
      {showInventory && (
        <div className="inventory-modal" onClick={(e) => e.target.className === 'inventory-modal' && setShowInventory(false)}>
          <div className="inventory-content">
            <button className="inventory-close" onClick={() => setShowInventory(false)}>×</button>
            
            <div className="inventory-header">
              <h2>🎒 인벤토리</h2>
              <div className="inventory-info">
                보유 테마: {ownedItems.length - 1}개 {/* default 제외 */}
              </div>
            </div>

            <div className="inventory-section">
              <h3>🎨 보유 테마</h3>
              <div className="inventory-items">
                {/* 기본 테마 */}
                <div 
                  className={`inventory-item ${currentTheme === 'default' ? 'active' : ''}`}
                  onClick={() => handleThemeChange('default')}
                >
                  <div className="inventory-item-icon">🎨</div>
                  <div className="inventory-item-name">기본 테마</div>
                  <div className="inventory-item-status">
                    {currentTheme === 'default' ? '사용중' : '적용하기'}
                  </div>
                </div>
                
                {/* 구매한 테마들 */}
                {shopItems.themes
                  .filter(theme => ownedItems.includes(theme.id))
                  .map(theme => (
                    <div 
                      key={theme.id}
                      className={`inventory-item ${currentTheme === theme.id ? 'active' : ''}`}
                      onClick={() => handleThemeChange(theme.id)}
                    >
                      <div className="inventory-item-icon">{theme.icon}</div>
                      <div className="inventory-item-name">{theme.name}</div>
                      <div className="inventory-item-status">
                        {currentTheme === theme.id ? '사용중' : '적용하기'}
                      </div>
                    </div>
                  ))}
              </div>
              
              {ownedItems.length === 1 && (
                <div className="empty-inventory">
                  <p>아직 구매한 테마가 없습니다.</p>
                  <button 
                    className="go-to-shop" 
                    onClick={() => {
                      setShowInventory(false);
                      setShowShop(true);
                    }}
                  >
                    상점으로 가기
                  </button>
                </div>
              )}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default App;
