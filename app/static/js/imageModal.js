import api from './service.js';

let isEventListenerSet = false;
let isImageEventSet = false;

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

    // 이미지 컨테이너 이벤트 설정
    const imageUploadInput = document.getElementById('imageUpload');
    
    // 이미지 클릭 이벤트
    imageContainer.querySelector('.modal-image-overlay').addEventListener('click', () => {
        imageUploadInput.click();
    });

    // 파일 선택 시 이벤트
    imageUploadInput.addEventListener('change', (e) => {
        const file = e.target.files[0];
        if (file) {
            if (validateImageFile(file)) {
                previewImage(file);
            } else {
                alert('이미지 파일만 업로드 가능합니다.');
            }
        }
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
            <span class="modal-gender-badge ${imageGender === 'other' ? 'active' : ''}" data-gender="other">기타</span>
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
            deleteImage(modal.dataset.imageId);
        }
    });

    closeBtn.addEventListener('click', () => {
        closeModal();
    });

    close.addEventListener('click', () => {
        closeModal();
    });

    saveBtn.addEventListener('click', (e) => {
        const modal = document.getElementById('imageModal');
        const activeGender = document.querySelector('.modal-gender-badge.active')?.dataset.gender;
        const activeAge = document.querySelector('.modal-age-badge.active')?.dataset.age;
        const activeEmotion = document.querySelector('.modal-emotion-badge.active')?.dataset.emotion;

        const imageUpload = document.getElementById('imageUpload');
        const selectedFile = imageUpload.files[0];

        const isNewImage = modal.dataset.imageId === 'null';

        const imageData = {
            gender: activeGender,
            ageGroup: activeAge,
            emotion: activeEmotion,
            file: selectedFile
        };

        if (isNewImage) {
            createNewImage(imageData);
        } else {
            updateImage(modal.dataset.imageId, imageData);
        }
    });
}

async function createNewImage(imageData) {
    if (!validateImageData(imageData)) {
        return false;
    }

    try {
        const formData = new FormData();
        formData.append('gender', imageData.gender);
        formData.append('ageGroup', imageData.ageGroup);
        formData.append('emotion', imageData.emotion);
        formData.append('image', imageData.file);

        await api.postFormData('/api/v1/admin/default-image', formData);

        alert('이미지가 성공적으로 등록되었습니다.');
        closeModal();
        window.location.reload();
        return true;

    } catch (error) {
        console.error('Image upload error:', error);
        alert('이미지 등록에 실패했습니다.');
        return false;
    }
}

async function updateImage(imageId, imageData) {
    if (!validateImageData(imageData, true)) {  // true는 이미지 수정모드
        return false;
    }

    try {
        const formData = new FormData();
        formData.append('gender', imageData.gender);
        formData.append('ageGroup', imageData.ageGroup);
        formData.append('emotion', imageData.emotion);

        // 새 이미지가 선택된 경우 새 이미지를, 아닌 경우 기존 이미지를 사용
        if (imageData.file) {
            formData.append('image', imageData.file);
        }

        await api.putFormData(`/api/v1/admin/default-image/${imageId}`, formData);

        alert('이미지가 성공적으로 수정되었습니다.');
        closeModal();
        window.location.reload();
        return true;

    } catch (error) {
        console.error('Image update error:', error);
        alert('이미지 수정에 실패했습니다.');
        return false;
    }
}

async function deleteImage(imageId) {
    try {
        await api.delete(`/api/v1/admin/default-image/${imageId}`);
        alert('이미지가 성공적으로 삭제되었습니다.');
        closeModal();
        window.location.reload();
        return true;
    } catch (error) {
        console.error('Image delete error:', error);
        alert('이미지 삭제에 실패했습니다.');
        return false;
    }
}

async function urlToFile(url) {
    try {
        const response = await fetch(url, {
            mode: 'no-cors'
        });
        const blob = await response.blob();
        return new File([blob], 'image.jpg', { type: blob.type });
    } catch (error) {
        console.error('Error converting URL to File:', error);
        throw error;
    }
}

// validateImageData 함수 수정 (이미지 필수 여부를 옵션으로)
function validateImageData(data, isUpdate = false) {
    // 성별 검증
    if (!data.gender) {
        alert('성별을 선택해주세요.');
        return false;
    }

    // 나이대 검증
    if (!data.ageGroup) {
        alert('나이대를 선택해주세요.');
        return false;
    }

    // 감정 검증
    if (!data.emotion) {
        alert('감정을 선택해주세요.');
        return false;
    }

    // 이미지 검증 (수정 시에는 선택적)
    if (!isUpdate && !data.file) {
        alert('이미지를 선택해주세요.');
        return false;
    }

    // 파일이 있는 경우에만 파일 검증
    if (data.file) {
        // 파일 타입 검증
        const validTypes = ['image/jpeg', 'image/png', 'image/gif'];
        if (!validTypes.includes(data.file.type)) {
            alert('유효한 이미지 파일이 아닙니다. (jpeg, png, gif만 가능)');
            return false;
        }

        // 파일 크기 검증 (5MB 제한)
        const maxSize = 5 * 1024 * 1024;
        if (data.file.size > maxSize) {
            alert('파일 크기가 너무 큽니다. (최대 5MB)');
            return false;
        }
    }

    return true;
}

function closeModal() {
    const modal = document.getElementById('imageModal');
    modal.classList.remove('show');
    setTimeout(() => {
        modal.style.display = "none";
    }, 200);
}

export { showModal, closeModal };