# EMOG!

**Where Emotions Come to Life**

eMoGi는 감정을 다양하게 표현하는 공간으로, "emotion"과 "emoji"를 결합한 이름에서 비롯되었습니다. 이 프로젝트는 사용자들이 감정을 다양한 방식으로 표현할 수 있도록 돕는 것을 목표로 합니다.

## 🚀 Backend Development

### Overview

백엔드 팀은 안정적이고 확장 가능한 서버 인프라를 구축하여 사용자들이 원활하게 서비스를 이용할 수 있도록 지원합니다. 소셜 로그인부터 실시간 채팅, 클라우드 인프라스트럭처까지 포괄적인 서버 시스템을 구현했습니다.

### Technologies

#### Core Technologies

- **FastAPI**: 고성능 웹 프레임워크를 활용한 RESTful API 구현
- **WebSocket**: 실시간 채팅을 위한 양방향 통신 구현
- **OAuth 2.0**: Google 소셜 로그인 구현
- **AWS Services**: 클라우드 기반 인프라스트럭처 구축

#### Cloud Infrastructure

- **Terraform**: Infrastructure as Code를 통한 AWS 리소스 관리
- **Amazon S3**: 이미지 저장소로 활용
- **CloudFront**: CDN을 통한 이미지 전송 최적화 및 보안 강화

### Infrastructure Overview


<img src="https://github.com/user-attachments/assets/092b6e8d-99ed-4ee6-a387-5eb0828dd9fa" width="70%">

## 📒 Features

#### Authentication & Authorization

- 소셜 로그인: Google OAuth 2.0을 통한 간편 로그인 구현
- 세션 관리: 사용자 인증 상태 유지 및 보안 강화

#### Real-time Communication

- WebSocket 채팅: 실시간 양방향 통신 구현
- Stream 처리: AI 응답 로딩 시간 최적화
- 채팅방 관리: CRUD 작업을 통한 채팅방 생성 및 관리

#### Cloud Infrastructure

- 확장 가능한 아키텍처: Terraform을 통한 인프라스트럭처 자동화
- 이미지 처리 파이프라인: S3와 CloudFront를 연동한 효율적인 이미지 관리
- 보안 강화: CloudFront를 통한 S3 직접 접근 제한

## 🌟 Future Improvements

- **Redis 도입**

  - Refresh Token 관리 구현으로 인증 시스템 개선
  - WebSocket 세션 상태 관리를 통한 채팅 시스템 안정성 강화
  - 캐싱 레이어 추가를 통한 전반적인 응답 속도 개선

- **Application Load Balancer (ALB) 구현**

  - 서버 부하 분산을 통한 시스템 안정성 향상
  - 무중단 배포 환경 구축
  - 가용성 향상을 위한 다중 가용영역(Multi-AZ) 구성

- **AWS CloudWatch 기반 모니터링**

  - 리소스 사용량 및 성능 지표 실시간 모니터링
  - CloudWatch Logs를 통한 중앙화된 로그 관리
  - CloudWatch Alarms를 통한 임계값 기반 모니터링
