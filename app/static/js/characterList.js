import api from './service.js';

// DOM이 로드된 후 실행
document.addEventListener('DOMContentLoaded', () => {
    loadCharacters();
});

// 캐릭터 목록을 불러오는 함수
async function loadCharacters() {
    try {
        const data = await api.get('/api/v1/admin/character/all');
        const characters = Array.isArray(data) ? data : data.items || data.characters || [];
        
        // tbody 엘리먼트 선택
        const tbody = document.querySelector('.character-table tbody');
        tbody.innerHTML = ''; // 기존 데이터 초기화
        
        // 데이터 렌더링
        characters.forEach((character, index) => {
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td>${index + 1}</td>
                <td>${character.characterName}</td>
                <td><img src="${character.characterProfile || ''}" alt="프로필 이미지" /></td>
                <td>${character.characterGender}</td>
                <td>${character.characterPersonality}</td>
                <td>${character.relationship || '-'}</td>
                <td>${character.characterCreatedAt ? new Date(character.characterCreatedAt).toLocaleDateString('ko-KR', { year: 'numeric', month: '2-digit', day: '2-digit' }) : ''}</td>
                <td>${character.user.userName}</td>
            `;
            
            // 행 클릭 이벤트 추가
            tr.addEventListener('click', () => {
                // character.id를 사용하여 상세 페이지로 이동
                window.location.href = `/admin/character/detail/${character.id}`;
            });

            tbody.appendChild(tr);
        });
    } catch (error) {
        console.error('데이터를 불러오는데 실패했습니다:', error);
    }
}