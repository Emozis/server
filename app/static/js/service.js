// API 호출을 위한 공통 함수
const api = {
    // 기본 요청 함수
    async fetchWithAuth(url, options = {}) {
        const token = localStorage.getItem('accessToken');
        
        if (!token) {
            window.location.href = '/admin/login';
            throw new Error('No token found');
        }

        // 기본 헤더 설정
        const headers = {
            'Authorization': `Bearer ${token}`,
            'Content-Type': 'application/json',
            ...options.headers
        };

        try {
            const response = await fetch(url, {
                ...options,
                headers
            });

            // 토큰 관련 에러 처리
            if (response.status === 401) {
                window.location.href = '/admin/login';
                throw new Error('Unauthorized');
            }

            if (response.status === 403) {
                throw new Error('Permission denied');
            }

            if (!response.ok) {
                throw new Error(`HTTP error! status: ${response.status}`);
            }

            // 응답이 있는 경우에만 JSON으로 파싱
            const contentType = response.headers.get('content-type');
            if (contentType && contentType.includes('application/json')) {
                return await response.json();
            }
            
            return response;

        } catch (error) {
            console.error('API Error:', error);
            throw error;
        }
    },

    // GET 요청
    async get(url) {
        return this.fetchWithAuth(url, {
            method: 'GET'
        });
    },

    // POST 요청
    async post(url, data) {
        return this.fetchWithAuth(url, {
            method: 'POST',
            body: JSON.stringify(data)
        });
    },

    // PUT 요청
    async put(url, data) {
        return this.fetchWithAuth(url, {
            method: 'PUT',
            body: JSON.stringify(data)
        });
    },

    // DELETE 요청
    async delete(url) {
        return this.fetchWithAuth(url, {
            method: 'DELETE'
        });
    }
};

export default api;