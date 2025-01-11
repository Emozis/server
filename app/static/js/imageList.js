import api from './service.js';

document.addEventListener('DOMContentLoaded', () => {
    fetchImageList();
    setupEventListeners();
});

function setupEventListeners() {
    const createImgBtn = document.getElementById('createImg');
    if (createImgBtn) {
        createImgBtn.addEventListener('click', () => {
            window.location.href = 'imageCreate.html';
        });
    }

    // 모달 닫기 이벤트들
    const modal = document.getElementById('imageModal');
    const closeBtn = document.querySelector('.close');
    
    // X 버튼 클릭시 닫기
    closeBtn.onclick = () => {
        closeModal();
    }

    // 모달 외부 클릭시 닫기
    window.onclick = (event) => {
        if (event.target == modal) {
            closeModal();
        }
    }
}


async function fetchImageList() {
    try {
        const data = await api.get('/api/v1/default-image');
        renderImageList(data);
    } catch (error) {
        alert('이미지 목록을 불러오는데 실패했습니다.');
    }
}

// 이미지 리스트를 화면에 렌더링하는 함수
function renderImageList(images) {
    const container = document.querySelector('.image-grid-container');
    container.innerHTML = '';

    images.forEach(image => {
        const imageElement = createImageElement(image);
        container.appendChild(imageElement);
    });
}

// 성별 배지 생성 함수
function getGenderBadge(gender) {
    const genderMap = {
        'female': '여성',
        'male': '남성',
        'other': '기타'
    };
    return `<span class="badge gender-badge ${gender}">${genderMap[gender] || '기타'}</span>`;
}

// 나이대 배지 생성 함수
function getAgeBadge(ageGroup) {
    const ageGroups = {
        'youth': '청년',
        'middle_age': '중년',
        'elderly': '노인'
    };
    return `<span class="badge age-badge ${ageGroup}">${ageGroups[ageGroup] || ageGroup}</span>`;
}

// 감정 배지 생성 함수
function getEmotionBadge(emotion) {
    const emotions = {
        'A': '기쁨/행복/활기찬',
        'B': '슬픔',
        'C': '우울/불안',
        'D': '버럭',
        'E': '따분/까칠/도도'
    };
    return `<span class="badge emotion-badge ${emotion}">${emotions[emotion] || emotion}</span>`;
}

function showModal(image) {
    const modal = document.getElementById('imageModal');
    const modalImage = document.getElementById('modalImage');
    const modalInfo = document.getElementById('modalInfo');

    modalImage.src = image.imageUrl;
    modalImage.onerror = () => {
        modalImage.src = '/static/image/characterDefault.png';
    };

    const createdDate = new Date(image.imageCreatedAt);
    const formattedDate = createdDate.toLocaleDateString('ko-KR', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit'
    });

    modalInfo.innerHTML = `
        <h2>${image.imageName}</h2>
        <div class="badges-container">
            ${getGenderBadge(image.imageGender)}
            ${getAgeBadge(image.imageAgeGroup)}
            ${getEmotionBadge(image.imageEmotion)}
        </div>
        <p>생성일: ${formattedDate}</p>
    `;

    modal.style.display = "block";
    setTimeout(() => {
        modal.classList.add('show');
    }, 10);
}

function closeModal() {
    const modal = document.getElementById('imageModal');
    modal.classList.remove('show');
    setTimeout(() => {
        modal.style.display = "none";
    }, 200); // transition 시간과 동일하게 설정
}

// 개별 이미지 요소를 생성하는 함수
function createImageElement(image) {
    const imageItem = document.createElement('div');
    imageItem.className = 'image-item';

    imageItem.addEventListener('click', () => {
        showModal(image);
    });

    const createdDate = new Date(image.imageCreatedAt);
    const formattedDate = createdDate.toLocaleDateString('ko-KR', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit'
    });

    imageItem.innerHTML = `
        <img src="${image.imageUrl}" alt="프로필 이미지" class="profile-image" onerror="this.src='/static/image/characterDefault.png'"/>
        <div class="image-item-content">
            <h3>${image.imageName}</h3>
            <p class="badges-container">
                ${getGenderBadge(image.imageGender)}
                ${getAgeBadge(image.imageAgeGroup)}
                ${getEmotionBadge(image.imageEmotion)}
            </p>
            <p>${formattedDate}</p>
        </div>
    `;

    return imageItem;
}