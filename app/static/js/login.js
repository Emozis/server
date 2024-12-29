document.addEventListener('DOMContentLoaded', () => {
    const loginBtn = document.querySelector('.loginBtn');
    const idInput = document.querySelectorAll('.idInput');
    
    loginBtn.addEventListener('click', handleLogin);
    // Enter 키로도 로그인할 수 있도록 설정
    idInput.forEach(input => {
        input.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                handleLogin();
            }
        });
    });
});

function isValidEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

async function handleLogin() {
    const [emailInput, passwordInput] = document.querySelectorAll('.idInput');
    const email = emailInput.value.trim();
    const password = passwordInput.value.trim();

    // 입력값 검증
    if (!email) {
        emailInput.focus();
        return;
    }
    
    if (!password) {
        passwordInput.focus();
        return;
    }
    
    if (!isValidEmail(email)) {
        alert('유효한 이메일 형식이 아닙니다.');
        emailInput.focus();
        return;
    }
    
    try {
        const response = await fetch('/api/v1/auth/login/admin', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                userEmail: email,
                userPassword: password
            })
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw errorData;
        }

        const data = await response.json();
        
        // 로그인 성공 처리
        console.log('로그인 성공:', data);
        
        // 로컬 스토리지에 토큰 저장 (만약 서버에서 토큰을 보내준다면)
        if (data.accessToken) {
            localStorage.setItem('accessToken', data.accessToken);
        }
        
        // 관리자 페이지로 리다이렉트
        window.location.href = '/admin/dashboard';
        
    } catch (error) {
        console.error('로그인 에러:', error);
        
        // 401 에러의 경우 서버에서 받은 메시지 표시
        if (error.detail && error.detail.message) {
            alert(error.detail.message);
        } else {
            alert('로그인에 실패했습니다. 아이디와 비밀번호를 확인해주세요.');
        }

        // 입력값 초기화
        emailInput.value = '';
        passwordInput.value = '';
        
        // ID 입력창에 포커스
        emailInput.focus();
    }
}