import api from './service.js';

document.addEventListener('DOMContentLoaded', () => {
    loadCharacterDetail();
});

async function loadCharacterDetail() {
    // try {
        const currentUrl = window.location.href;
        const id = currentUrl.split('/').pop();

        const data = await api.get(`/api/v1/admin/character/${id}`);
        console.log(data)

        updateCharacterUI(data);
    // } catch (error) {
    //     console.error('캐릭터 데이터를 불러오는데 실패했습니다:');
    // }
}

function updateCharacterUI(characterData) {
    // 기본 정보 업데이트
    document.getElementById('character-name').textContent = characterData.characterName;
    document.getElementById('character-status').textContent = characterData.characterIsPublic ? 'public' : 'private';
    document.getElementById('character-greeting').textContent = characterData.characterGreeting;

    // 이미지 업데이트
    if (characterData.characterProfile) {
        document.getElementById('character-image').src = characterData.characterProfile;
    }

    // 통계 업데이트
    document.getElementById('character-like-count').textContent = characterData.characterLikes;
    document.getElementById('character-use-count').textContent = characterData.characterUsageCount;
    document.getElementById('character-update-date').textContent = characterData.characterUpdatedAt ? new Date(characterData.characterUpdatedAt).toLocaleDateString('ko-KR', { year: 'numeric', month: '2-digit', day: '2-digit' }) : '';

    // 상세 정보 업데이트
    document.getElementById('character-gender').textContent = characterData.characterGender;
    document.getElementById('character-personality').textContent = characterData.characterPersonality;
    
    if (characterData.characterRelationships && characterData.characterRelationships.length > 0) {
        // 관계 이름만 추출하여 쉼표로 구분된 문자열로 변환
        const relationshipsText = characterData.characterRelationships
            .map(rel => rel.relationshipName)
            .join(', ');
        document.getElementById('character-relationships').textContent = relationshipsText;
    } else {
        document.getElementById('character-relationships').textContent = '없음';
    }
    document.getElementById('character-creator').textContent = characterData.characterCreatedAt;

    document.getElementById('character-description').textContent = characterData.characterDescription;
    document.getElementById('character-detail').textContent = characterData.characterDetails;
}
