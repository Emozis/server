let isEventListenerSet = false;

function showModal(image) {
    const modal = document.getElementById('imageModal');
    const modalImage = document.getElementById('modalImage');
    const modalTitle = document.getElementById('modalTitle');
    const modalDate = document.getElementById('modalDate');
    const genderBadgeContainer = document.getElementById('genderBadgeContainer');
    const ageBadgeContainer = document.getElementById('ageBadgeContainer');
    const emotionBadgeContainer = document.getElementById('emotionBadgeContainer');

    modal.dataset.imageId = image.imageId;

    modalImage.src = image.imageUrl;
    modalImage.onerror = () => {
        modalImage.src = '/static/image/characterDefault.png';
    };
    
    const imageContainer = document.querySelector('.modal-image-container');
    imageContainer.innerHTML = `
        <input type="file" id="imageUpload" accept="image/*" style="display: none;">
        <img id="modalImage" src="${image.imageUrl}" alt="상세 이미지" onerror="this.src='/static/image/characterDefault.png'">
        <div class="modal-image-overlay">
            <img src="/static/image/icon-camera.svg" alt="이미지 변경">
        </div>
    `;

    document.getElementById('imageUpload').addEventListener('change', (e) => {
        const file = e.target.files[0];
        if (file) {
            if (validateImageFile(file)) {
                previewImage(file);
            } else {
                alert('이미지 파일만 업로드 가능합니다.');
            }
        }
    });

    imageContainer.addEventListener('click', () => {
        document.getElementById('imageUpload').click();
    });

    modalTitle.textContent = image.imageName;

    setupModalDate(image.imageCreatedAt);
    setupGenderBadges(image.imageGender);
    setupAgeBadges(image.imageAgeGroup);
    setupEmotionBadges(image.imageEmotion);

    if (!isEventListenerSet) {
        setupModalButtons();
        isEventListenerSet = true;
    }

    modal.style.display = "block";
    setTimeout(() => {
        modal.classList.add('show');
    }, 10);
}

function validateImageFile(file) {
    const validTypes = ['image/jpeg', 'image/png', 'image/gif'];
    return validTypes.includes(file.type);
}

function previewImage(file) {
    const reader = new FileReader();
    reader.onload = (e) => {
        const modalImage = document.getElementById('modalImage');
        modalImage.src = e.target.result;
        
        // 선택된 파일을 모달에 저장 (나중에 서버 전송시 사용)
        const modal = document.getElementById('imageModal');
        modal.dataset.selectedFile = file.name;
    };
    reader.readAsDataURL(file);
}

function setupModalDate(createdAt) {
    const modalDate = document.getElementById('modalDate');

    if (createdAt === '-') {
        modalDate.textContent = 'create at: -';
        return;
    }

    const createdDate = new Date(createdAt);
    const formattedDate = createdDate.toLocaleDateString('ko-KR', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit'
    });
    modalDate.textContent = `create at: ${formattedDate}`;
}

function setupGenderBadges(imageGender) {
    const genderBadgeContainer = document.getElementById('genderBadgeContainer');
    genderBadgeContainer.innerHTML = `
        <div class="modal-gender-group">
            <span class="modal-gender-badge ${imageGender === 'female' ? 'active' : ''}" data-gender="female">여성</span>
            <span class="modal-gender-badge ${imageGender === 'male' ? 'active' : ''}" data-gender="male">남성</span>
        </div>
    `;

    const genderBadges = genderBadgeContainer.querySelectorAll('.modal-gender-badge');
    genderBadges.forEach(badge => {
        badge.addEventListener('click', () => {
            genderBadges.forEach(b => b.classList.remove('active'));
            badge.classList.add('active');
        });
    });
}

function setupAgeBadges(imageAgeGroup) {
    const ageBadgeContainer = document.getElementById('ageBadgeContainer');
    ageBadgeContainer.innerHTML = `
        <div class="modal-age-group">
            <span class="modal-age-badge ${imageAgeGroup === 'youth' ? 'active' : ''}" data-age="youth">청년</span>
            <span class="modal-age-badge ${imageAgeGroup === 'middle_age' ? 'active' : ''}" data-age="middle_age">중년</span>
            <span class="modal-age-badge ${imageAgeGroup === 'elderly' ? 'active' : ''}" data-age="elderly">노인</span>
        </div>
    `;

    const ageBadges = ageBadgeContainer.querySelectorAll('.modal-age-badge');
    ageBadges.forEach(badge => {
        badge.addEventListener('click', () => {
            ageBadges.forEach(b => b.classList.remove('active'));
            badge.classList.add('active');
        });
    });
}

function setupEmotionBadges(imageEmotion) {
    const emotions = {
        'A': '기쁨/행복/활기찬',
        'B': '슬픔',
        'C': '우울/불안',
        'D': '버럭',
        'E': '따분/까칠/도도'
    };

    const emotionBadgeContainer = document.getElementById('emotionBadgeContainer');
    emotionBadgeContainer.innerHTML = `
        <div class="modal-emotion-group">
            ${Object.entries(emotions).map(([key, value]) => `
                <span class="modal-emotion-badge ${imageEmotion === key ? 'active' : ''}" 
                      data-emotion="${key}">${value}</span>
            `).join('')}
        </div>
    `;

    const emotionBadges = emotionBadgeContainer.querySelectorAll('.modal-emotion-badge');
    emotionBadges.forEach(badge => {
        badge.addEventListener('click', () => {
            emotionBadges.forEach(b => b.classList.remove('active'));
            badge.classList.add('active');
        });
    });
}

function setupModalButtons() {
    const modal = document.getElementById('imageModal');
    const close = modal.querySelector('.close');
    const deleteBtn = modal.querySelector('.delete-btn');
    const closeBtn = modal.querySelector('.close-btn');
    const saveBtn = modal.querySelector('.save-btn');

    deleteBtn.addEventListener('click', () => {
        if (confirm('정말 삭제하시겠습니까?')) {
            console.log('Delete clicked');
        }
    });

    closeBtn.addEventListener('click', () => {
        closeModal();
    });

    close.addEventListener('click', () => {
        closeModal();
    });

    saveBtn.addEventListener('click', (e) => {
        const activeGender = document.querySelector('.modal-gender-badge.active').dataset.gender;
        const activeAge = document.querySelector('.modal-age-badge.active').dataset.age;
        const activeEmotion = document.querySelector('.modal-emotion-badge.active').dataset.emotion;

        console.log({
            image_id: modal.dataset.imageId, // 이미지 ID를 저장하기 위해 showModal에서 설정 필요
            gender: activeGender,
            ageGroup: activeAge,
            emotion: activeEmotion
        });
    });
}

function closeModal() {
    const modal = document.getElementById('imageModal');
    modal.classList.remove('show');
    setTimeout(() => {
        modal.style.display = "none";
    }, 200);
}

export { showModal, closeModal };