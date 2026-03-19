from __future__ import annotations

from ..types import EngineerProfile, Skill

# ---------------------------------------------------------------------------
# 기존 단일 텍스트 포맷 (하위호환 — 기존 노트북 04 등에서 사용)
# ---------------------------------------------------------------------------
SAMPLE_ENGINEERS = [
    {
        "text": """
        [기술스택]
        Java / Spring Boot / PostgreSQL / Redis / Docker

        [경력]
        8년차 백엔드 개발자.

        [프로젝트 경험]
        현대모비스(2023~2025): ERP 재고관리 모듈 개발. Spring Batch로 야간 정산 처리 자동화.
        LG CNS(2021~2023): 제조업 MES 시스템 API 개발. Oracle DB 쿼리 최적화로 조회속도 40% 개선.
        삼성SDS(2017~2021): 물류 ERP 시스템 개발. Spring Boot 기반 REST API 설계.""",
        "metadata": {
            "engineer_id": "eng-001",
            "grade": "SENIOR",
            "status": "AVAILABLE",
            "engineer_role": "DEVELOPER",
            "engineer_type": "FULL_TIME",
        },
    },
    {
        "text": """
        [기술스택]
        Java / Spring Boot / MySQL / Kafka / AWS

        [경력]
        5년차 백엔드 개발자.

        [프로젝트 경험]
        현대차(2024~2025): 딜러 관리 포털 백엔드 개발. JWT 인증 모듈 구현.
        SK하이닉스(2022~2024): 생산 관리 시스템 API 개발. Kafka 기반 이벤트 처리.
        스타트업(2020~2022): 쇼핑몰 주문 시스템 개발.""",
        "metadata": {
            "engineer_id": "eng-002",
            "grade": "INTERMEDIATE",
            "status": "AVAILABLE",
            "engineer_role": "DEVELOPER",
            "engineer_type": "FULL_TIME",
        },
    },
    {
        "text": """
        [기술스택]
        React / TypeScript / Redux / Recharts / Figma

        [경력]
        6년차 프론트엔드 개발자.

        [프로젝트 경험]
        기아차(2024~2025): 판매 통계 대시보드 개발. Recharts 기반 실시간 차트 구현.
        현대카드(2022~2024): 결제 현황 모니터링 화면 개발.
        NHN(2019~2022): 어드민 포털 React 전환.""",
        "metadata": {
            "engineer_id": "eng-003",
            "grade": "SENIOR",
            "status": "AVAILABLE",
            "engineer_role": "DEVELOPER",
            "engineer_type": "FULL_TIME",
        },
    },
    {
        "text": """
        [기술스택]
        React / JavaScript / Vue.js / Chart.js / CSS

        [경력]
        4년차 프론트엔드 개발자.

        [프로젝트 경험]
        포스코(2024~2025): 생산 현황 모니터링 대시보드 개발. Chart.js 활용.
        네이버(2022~2024): 광고 성과 리포트 화면 개발.
        에이전시(2021~2022): 다수 기업 웹사이트 퍼블리싱.""",
        "metadata": {
            "engineer_id": "eng-004",
            "grade": "INTERMEDIATE",
            "status": "AVAILABLE",
            "engineer_role": "DEVELOPER",
            "engineer_type": "FREELANCER",
        },
    },
    {
        "text": """
        [기술스택]
        Python / FastAPI / MongoDB / Docker / Kubernetes

        [경력]
        4년차 백엔드 개발자.

        [프로젝트 경험]
        쿠팡(2024~2025): 물류 최적화 알고리즘 서버 API 개발. FastAPI 기반 고성능 처리.
        배달의민족(2022~2024): 주문 관리 시스템 유지보수. MSA 환경에서 서비스 간 통신 최적화.
        테크 스타트업(2021~2022): 실시간 채팅 서버 구축.""",
        "metadata": {
            "engineer_id": "eng-005",
            "grade": "INTERMEDIATE",
            "status": "AVAILABLE",
            "engineer_role": "DEVELOPER",
            "engineer_type": "FULL_TIME",
        },
    },
    {
        "text": """
        [기술스택]
        HTML5 / CSS3 / SCSS / jQuery / Gulp / Cross Browsing

        [경력]
        5년차 웹 퍼블리셔.

        [프로젝트 경험]
        아모레퍼시픽(2024~2025): 공식 온라인몰 반응형 웹 리뉴얼. 시각 장애인을 위한 웹 접근성(WA) 인증 획득.
        무신사(2022~2024): 프로모션 페이지 제작 및 이벤트 인터랙션 구현.
        웹 에이전시(2020~2022): 다수의 브랜드 사이트 구축 및 유지보수.""",
        "metadata": {
            "engineer_id": "pub-001",
            "grade": "INTERMEDIATE",
            "status": "AVAILABLE",
            "engineer_role": "PUBLISHER",
            "engineer_type": "FULL_TIME",
        },
    },
    {
        "text": """
        [기술스택]
        Selenium / Appium / JMeter / Jira / Confluence

        [경력]
        7년차 QA 엔지니어.

        [프로젝트 경험]
        카카오뱅크(2023~2025): 모바일 앱 기능 테스트 및 자동화 스크립트 작성. 안정성 99% 달성.
        라인(2021~2023): 글로벌 메신저 부하 테스트 진행. 성능 병목 구간 탐색 및 리포트.
        안랩(2018~2021): 보안 소프트웨어 수동 및 자동화 테스트 진행.""",
        "metadata": {
            "engineer_id": "qa-001",
            "grade": "SENIOR",
            "status": "AVAILABLE",
            "engineer_role": "QA",
            "engineer_type": "FULL_TIME",
        },
    },
    {
        "text": """
        [기술스택]
        Figma / Adobe XD / Photoshop / Illustrator / Protopie

        [경력]
        6년차 UX/UI 디자이너.

        [프로젝트 경험]
        토스(2024~2025): 신규 금융 상품 가입 프로세스 UX 개선. 전환율 15% 상승.
        야놀자(2022~2024): 숙박 예약 화면 UI 컴포넌트 시스템 구축 및 가이드라인 제정.
        디자인 스튜디오(2019~2022): 브랜드 아이덴티티(BI) 및 앱 디자인 프로젝트 참여.""",
        "metadata": {
            "engineer_id": "des-001",
            "grade": "SENIOR",
            "status": "AVAILABLE",
            "engineer_role": "DESIGNER",
            "engineer_type": "FREELANCER",
        },
    },
    {
        "text": """
        [기술스택]
        Confluence / Slack / Notion / GA4 / SQL

        [경력]
        9년차 서비스 기획자(PM).

        [프로젝트 경험]
        당근마켓(2023~2025): 지역 커뮤니티 신규 피드 서비스 기획 및 런칭. MAU 20% 증대.
        직방(2020~2023): 부동산 매물 관리 시스템 백오피스 기획 및 프로세스 자동화.
        이커머스 기업(2016~2020): 주문/결제 서비스 운영 기획.""",
        "metadata": {
            "engineer_id": "pln-001",
            "grade": "SENIOR",
            "status": "AVAILABLE",
            "engineer_role": "PLANNER",
            "engineer_type": "FULL_TIME",
        },
    },
]

# ---------------------------------------------------------------------------
# 듀얼 텍스트 포맷 (PROCESS.md 기준 — capability / experience 분리)
# 팀 공용 테스트를 위해 100개의 고정 프로필을 직접 정의한다.
# ---------------------------------------------------------------------------
SAMPLE_ENGINEER_PROFILES: list[EngineerProfile] = [
    EngineerProfile(
        engineer_id="eng-001",
        grade="EXPERT",
        status="AVAILABLE",
        engineer_role="DEVELOPER",
        employment_type="FULL_TIME",
        capability_text="Java / Spring Boot / Spring Batch / PostgreSQL / Redis / Docker\n\n정보처리기사",
        experience_text="[소개]\n12년차 백엔드 아키텍트. 대규모 트래픽 서비스 설계와 운영에 강점이 있는 개발자.\n\n[프로젝트 경험]\n현대오토에버(2024~2025): 차량 데이터 수집 플랫폼 API 개발. 실시간 적재 파이프라인 구축과 배치 처리 시간 35% 단축.\n네이버(2022~2024): 광고 리포트 관리자 화면 개발. 대용량 차트 렌더링 최적화.\n배달의민족(2020~2022): 매장 운영 백오피스 개발. 운영 도구 개선으로 CS 처리 시간 단축.\n\n[경력]\nSI 프로젝트에서 커머스와 제조 백엔드 개발을 담당하며 기본기를 다졌다.",
    ),
    EngineerProfile(
        engineer_id="eng-002",
        grade="EXPERT",
        status="AVAILABLE",
        engineer_role="DEVELOPER",
        employment_type="FULL_TIME",
        capability_text="Java / Kotlin / Spring Boot / MySQL / Kafka / AWS\n\nSQLD",
        experience_text="[소개]\n12년차 백엔드 개발자. 제조, 물류, 금융 도메인 경험을 바탕으로 안정적인 서비스를 구축한 개발자.\n\n[프로젝트 경험]\n삼성SDS(2024~2025): 물류 운영 시스템 백엔드 개발. 정산 배치 안정화와 장애 대응 체계 수립.\n카카오(2022~2024): 사용자 활동 분석 API 개발. 이벤트 수집 구조 개선으로 데이터 유실률 감소.\n토스(2020~2022): 금융 상품 가입 프로세스 개발. 인증 및 심사 API 연동 품질 향상.\n\n[경력]\n스타트업에서 풀스택 개발과 운영 자동화를 맡으며 빠른 실행력을 키웠다.",
    ),
    EngineerProfile(
        engineer_id="eng-003",
        grade="EXPERT",
        status="AVAILABLE",
        engineer_role="DEVELOPER",
        employment_type="FULL_TIME",
        capability_text="Python / FastAPI / PostgreSQL / Docker / Kubernetes / Celery\n\nAWS SAA",
        experience_text="[소개]\n12년차 프론트엔드 개발자. 대시보드, 관리자 화면, 실시간 데이터 처리 경험이 풍부한 개발자.\n\n[프로젝트 경험]\nLG CNS(2024~2025): 제조 MES 연동 서비스 개발. Oracle 쿼리 튜닝으로 주요 조회 성능 개선.\n쿠팡(2022~2024): 주문·배송 도메인 서비스 개발. 비동기 처리 구조 도입으로 피크 시간대 안정성 확보.\n당근(2020~2022): 지역 서비스 추천 기능 개발. A/B 테스트 기반 추천 로직 개선.\n\n[경력]\n플랫폼 조직에서 공통 모듈과 개발 표준을 정비한 경험이 있다.",
    ),
    EngineerProfile(
        engineer_id="eng-004",
        grade="EXPERT",
        status="AVAILABLE",
        engineer_role="DEVELOPER",
        employment_type="FULL_TIME",
        capability_text="Python / Django / MySQL / Redis / Celery / AWS\n\n리눅스마스터 2급",
        experience_text="[소개]\n12년차 풀스택 개발자. API 설계와 성능 개선을 반복적으로 수행해 온 문제 해결형 개발자.\n\n[프로젝트 경험]\n네이버(2024~2025): 광고 리포트 관리자 화면 개발. 대용량 차트 렌더링 최적화.\n배달의민족(2022~2024): 매장 운영 백오피스 개발. 운영 도구 개선으로 CS 처리 시간 단축.\n무신사(2020~2022): 프로모션·쿠폰 서비스 개발. 트래픽 급증 구간 캐시 전략 적용.\n\n[경력]\n사내 레거시 서비스 개선 프로젝트를 통해 안정적인 전환 작업을 수행했다.",
    ),
    EngineerProfile(
        engineer_id="eng-005",
        grade="EXPERT",
        status="AVAILABLE",
        engineer_role="DEVELOPER",
        employment_type="FULL_TIME",
        capability_text="Node.js / NestJS / TypeScript / PostgreSQL / Redis / Swagger\n\nADsP",
        experience_text="[소개]\n12년차 데이터 플랫폼 개발자. MSA 전환, 클라우드 운영, 배포 자동화 경험을 함께 보유한 개발자.\n\n[프로젝트 경험]\n카카오(2024~2025): 사용자 활동 분석 API 개발. 이벤트 수집 구조 개선으로 데이터 유실률 감소.\n토스(2022~2024): 금융 상품 가입 프로세스 개발. 인증 및 심사 API 연동 품질 향상.\nSK하이닉스(2020~2022): 생산 모니터링 시스템 개발. 이벤트 기반 알림 구조 도입.\n\n[경력]\n도메인 조직과 협업하며 요구사항을 기술 설계로 구체화하는 역할을 맡아 왔다.",
    ),
    EngineerProfile(
        engineer_id="eng-006",
        grade="EXPERT",
        status="AVAILABLE",
        engineer_role="DEVELOPER",
        employment_type="FULL_TIME",
        capability_text="React / TypeScript / Next.js / TanStack Query / Storybook / Figma\n\n정보처리기사",
        experience_text="[소개]\n12년차 클라우드 플랫폼 개발자. 요구사항 분석부터 운영 안정화까지 전 과정을 폭넓게 수행한 개발자.\n\n[프로젝트 경험]\n쿠팡(2024~2025): 주문·배송 도메인 서비스 개발. 비동기 처리 구조 도입으로 피크 시간대 안정성 확보.\n당근(2022~2024): 지역 서비스 추천 기능 개발. A/B 테스트 기반 추천 로직 개선.\n포스코DX(2020~2022): 스마트팩토리 데이터 허브 개발. 현장 설비 데이터 표준화와 API 제공.\n\n[경력]\nSI 프로젝트에서 커머스와 제조 백엔드 개발을 담당하며 기본기를 다졌다.",
    ),
    EngineerProfile(
        engineer_id="eng-007",
        grade="EXPERT",
        status="AVAILABLE",
        engineer_role="DEVELOPER",
        employment_type="FULL_TIME",
        capability_text="React / Vue.js / TypeScript / Vite / Chart.js / Pinia\n\nSQLD",
        experience_text="[소개]\n12년차 AI 서비스 개발자. 대규모 트래픽 서비스 설계와 운영에 강점이 있는 개발자.\n\n[프로젝트 경험]\n배달의민족(2024~2025): 매장 운영 백오피스 개발. 운영 도구 개선으로 CS 처리 시간 단축.\n무신사(2022~2024): 프로모션·쿠폰 서비스 개발. 트래픽 급증 구간 캐시 전략 적용.\n야놀자(2020~2022): 숙박 예약 관리자 포털 개발. 운영 화면 공통 컴포넌트화.\n\n[경력]\n스타트업에서 풀스택 개발과 운영 자동화를 맡으며 빠른 실행력을 키웠다.",
    ),
    EngineerProfile(
        engineer_id="eng-008",
        grade="EXPERT",
        status="AVAILABLE",
        engineer_role="DEVELOPER",
        employment_type="FULL_TIME",
        capability_text="Go / Gin / PostgreSQL / gRPC / Prometheus / Grafana\n\nAWS SAA",
        experience_text="[소개]\n12년차 커머스 플랫폼 개발자. 제조, 물류, 금융 도메인 경험을 바탕으로 안정적인 서비스를 구축한 개발자.\n\n[프로젝트 경험]\n토스(2024~2025): 금융 상품 가입 프로세스 개발. 인증 및 심사 API 연동 품질 향상.\nSK하이닉스(2022~2024): 생산 모니터링 시스템 개발. 이벤트 기반 알림 구조 도입.\n직방(2020~2022): 매물 관리 백오피스 개발. 권한 체계 정비와 검색 응답 속도 개선.\n\n[경력]\n플랫폼 조직에서 공통 모듈과 개발 표준을 정비한 경험이 있다.",
    ),
    EngineerProfile(
        engineer_id="eng-009",
        grade="SENIOR",
        status="AVAILABLE",
        engineer_role="DEVELOPER",
        employment_type="FULL_TIME",
        capability_text="Java / Spring Cloud / Kafka / MongoDB / Elasticsearch / Docker\n\n리눅스마스터 2급",
        experience_text="[소개]\n8년차 핀테크 백엔드 개발자. 대시보드, 관리자 화면, 실시간 데이터 처리 경험이 풍부한 개발자.\n\n[프로젝트 경험]\n당근(2024~2025): 지역 서비스 추천 기능 개발. A/B 테스트 기반 추천 로직 개선.\n포스코DX(2022~2024): 스마트팩토리 데이터 허브 개발. 현장 설비 데이터 표준화와 API 제공.\n컬리(2020~2022): 정산·프로모션 엔진 개발. 배치 재처리 기능 추가로 운영 효율 향상.\n\n[경력]\n사내 레거시 서비스 개선 프로젝트를 통해 안정적인 전환 작업을 수행했다.",
    ),
    EngineerProfile(
        engineer_id="eng-010",
        grade="SENIOR",
        status="AVAILABLE",
        engineer_role="DEVELOPER",
        employment_type="FULL_TIME",
        capability_text="Flutter / Dart / Firebase / REST API / Figma / GitHub Actions\n\nADsP",
        experience_text="[소개]\n8년차 웹 애플리케이션 개발자. API 설계와 성능 개선을 반복적으로 수행해 온 문제 해결형 개발자.\n\n[프로젝트 경험]\n무신사(2024~2025): 프로모션·쿠폰 서비스 개발. 트래픽 급증 구간 캐시 전략 적용.\n야놀자(2022~2024): 숙박 예약 관리자 포털 개발. 운영 화면 공통 컴포넌트화.\n현대카드(2020~2022): 결제 승인 시스템 고도화. 승인 응답 시간 안정화와 장애 포인트 축소.\n\n[경력]\n도메인 조직과 협업하며 요구사항을 기술 설계로 구체화하는 역할을 맡아 왔다.",
    ),
    EngineerProfile(
        engineer_id="eng-011",
        grade="SENIOR",
        status="AVAILABLE",
        engineer_role="DEVELOPER",
        employment_type="FULL_TIME",
        capability_text="Kotlin / Android / Jetpack Compose / Retrofit / Room / Firebase\n\n정보처리기사",
        experience_text="[소개]\n8년차 모바일 앱 개발자. MSA 전환, 클라우드 운영, 배포 자동화 경험을 함께 보유한 개발자.\n\n[프로젝트 경험]\nSK하이닉스(2024~2025): 생산 모니터링 시스템 개발. 이벤트 기반 알림 구조 도입.\n직방(2022~2024): 매물 관리 백오피스 개발. 권한 체계 정비와 검색 응답 속도 개선.\n신한은행(2020~2022): 기업뱅킹 API 플랫폼 구축. 내부 연계 표준화와 배포 자동화 정착.\n\n[경력]\nSI 프로젝트에서 커머스와 제조 백엔드 개발을 담당하며 기본기를 다졌다.",
    ),
    EngineerProfile(
        engineer_id="eng-012",
        grade="SENIOR",
        status="AVAILABLE",
        engineer_role="DEVELOPER",
        employment_type="FULL_TIME",
        capability_text="TypeScript / React Native / Redux Toolkit / Expo / Firebase / Jest\n\nSQLD",
        experience_text="[소개]\n8년차 DevOps 엔지니어. 요구사항 분석부터 운영 안정화까지 전 과정을 폭넓게 수행한 개발자.\n\n[프로젝트 경험]\n포스코DX(2024~2025): 스마트팩토리 데이터 허브 개발. 현장 설비 데이터 표준화와 API 제공.\n컬리(2022~2024): 정산·프로모션 엔진 개발. 배치 재처리 기능 추가로 운영 효율 향상.\nCJ올리브영(2020~2022): 멤버십 서비스 개편. 쿠폰 정합성 검증 로직 강화.\n\n[경력]\n스타트업에서 풀스택 개발과 운영 자동화를 맡으며 빠른 실행력을 키웠다.",
    ),
    EngineerProfile(
        engineer_id="eng-013",
        grade="SENIOR",
        status="AVAILABLE",
        engineer_role="DEVELOPER",
        employment_type="FULL_TIME",
        capability_text="Java / Spring Boot / Spring Batch / PostgreSQL / Redis / Docker\n\n정보처리기사",
        experience_text="[소개]\n8년차 백엔드 아키텍트. 대규모 트래픽 서비스 설계와 운영에 강점이 있는 개발자.\n\n[프로젝트 경험]\n야놀자(2024~2025): 숙박 예약 관리자 포털 개발. 운영 화면 공통 컴포넌트화.\n현대카드(2022~2024): 결제 승인 시스템 고도화. 승인 응답 시간 안정화와 장애 포인트 축소.\n현대오토에버(2020~2022): 차량 데이터 수집 플랫폼 API 개발. 실시간 적재 파이프라인 구축과 배치 처리 시간 35% 단축.\n\n[경력]\n플랫폼 조직에서 공통 모듈과 개발 표준을 정비한 경험이 있다.",
    ),
    EngineerProfile(
        engineer_id="eng-014",
        grade="SENIOR",
        status="AVAILABLE",
        engineer_role="DEVELOPER",
        employment_type="FULL_TIME",
        capability_text="Java / Kotlin / Spring Boot / MySQL / Kafka / AWS\n\nSQLD",
        experience_text="[소개]\n8년차 백엔드 개발자. 제조, 물류, 금융 도메인 경험을 바탕으로 안정적인 서비스를 구축한 개발자.\n\n[프로젝트 경험]\n직방(2024~2025): 매물 관리 백오피스 개발. 권한 체계 정비와 검색 응답 속도 개선.\n신한은행(2022~2024): 기업뱅킹 API 플랫폼 구축. 내부 연계 표준화와 배포 자동화 정착.\n삼성SDS(2020~2022): 물류 운영 시스템 백엔드 개발. 정산 배치 안정화와 장애 대응 체계 수립.\n\n[경력]\n사내 레거시 서비스 개선 프로젝트를 통해 안정적인 전환 작업을 수행했다.",
    ),
    EngineerProfile(
        engineer_id="eng-015",
        grade="SENIOR",
        status="AVAILABLE",
        engineer_role="DEVELOPER",
        employment_type="FULL_TIME",
        capability_text="Python / FastAPI / PostgreSQL / Docker / Kubernetes / Celery\n\nAWS SAA",
        experience_text="[소개]\n8년차 프론트엔드 개발자. 대시보드, 관리자 화면, 실시간 데이터 처리 경험이 풍부한 개발자.\n\n[프로젝트 경험]\n컬리(2024~2025): 정산·프로모션 엔진 개발. 배치 재처리 기능 추가로 운영 효율 향상.\nCJ올리브영(2022~2024): 멤버십 서비스 개편. 쿠폰 정합성 검증 로직 강화.\nLG CNS(2020~2022): 제조 MES 연동 서비스 개발. Oracle 쿼리 튜닝으로 주요 조회 성능 개선.\n\n[경력]\n도메인 조직과 협업하며 요구사항을 기술 설계로 구체화하는 역할을 맡아 왔다.",
    ),
    EngineerProfile(
        engineer_id="eng-016",
        grade="SENIOR",
        status="AVAILABLE",
        engineer_role="DEVELOPER",
        employment_type="FULL_TIME",
        capability_text="Python / Django / MySQL / Redis / Celery / AWS\n\n리눅스마스터 2급",
        experience_text="[소개]\n8년차 풀스택 개발자. API 설계와 성능 개선을 반복적으로 수행해 온 문제 해결형 개발자.\n\n[프로젝트 경험]\n현대카드(2024~2025): 결제 승인 시스템 고도화. 승인 응답 시간 안정화와 장애 포인트 축소.\n현대오토에버(2022~2024): 차량 데이터 수집 플랫폼 API 개발. 실시간 적재 파이프라인 구축과 배치 처리 시간 35% 단축.\n네이버(2020~2022): 광고 리포트 관리자 화면 개발. 대용량 차트 렌더링 최적화.\n\n[경력]\nSI 프로젝트에서 커머스와 제조 백엔드 개발을 담당하며 기본기를 다졌다.",
    ),
    EngineerProfile(
        engineer_id="eng-017",
        grade="SENIOR",
        status="AVAILABLE",
        engineer_role="DEVELOPER",
        employment_type="FULL_TIME",
        capability_text="Node.js / NestJS / TypeScript / PostgreSQL / Redis / Swagger\n\nADsP",
        experience_text="[소개]\n8년차 데이터 플랫폼 개발자. MSA 전환, 클라우드 운영, 배포 자동화 경험을 함께 보유한 개발자.\n\n[프로젝트 경험]\n신한은행(2024~2025): 기업뱅킹 API 플랫폼 구축. 내부 연계 표준화와 배포 자동화 정착.\n삼성SDS(2022~2024): 물류 운영 시스템 백엔드 개발. 정산 배치 안정화와 장애 대응 체계 수립.\n카카오(2020~2022): 사용자 활동 분석 API 개발. 이벤트 수집 구조 개선으로 데이터 유실률 감소.\n\n[경력]\n스타트업에서 풀스택 개발과 운영 자동화를 맡으며 빠른 실행력을 키웠다.",
    ),
    EngineerProfile(
        engineer_id="eng-018",
        grade="SENIOR",
        status="AVAILABLE",
        engineer_role="DEVELOPER",
        employment_type="FULL_TIME",
        capability_text="React / TypeScript / Next.js / TanStack Query / Storybook / Figma\n\n정보처리기사",
        experience_text="[소개]\n8년차 클라우드 플랫폼 개발자. 요구사항 분석부터 운영 안정화까지 전 과정을 폭넓게 수행한 개발자.\n\n[프로젝트 경험]\nCJ올리브영(2024~2025): 멤버십 서비스 개편. 쿠폰 정합성 검증 로직 강화.\nLG CNS(2022~2024): 제조 MES 연동 서비스 개발. Oracle 쿼리 튜닝으로 주요 조회 성능 개선.\n쿠팡(2020~2022): 주문·배송 도메인 서비스 개발. 비동기 처리 구조 도입으로 피크 시간대 안정성 확보.\n\n[경력]\n플랫폼 조직에서 공통 모듈과 개발 표준을 정비한 경험이 있다.",
    ),
    EngineerProfile(
        engineer_id="eng-019",
        grade="SENIOR",
        status="AVAILABLE",
        engineer_role="DEVELOPER",
        employment_type="FULL_TIME",
        capability_text="React / Vue.js / TypeScript / Vite / Chart.js / Pinia\n\nSQLD",
        experience_text="[소개]\n8년차 AI 서비스 개발자. 대규모 트래픽 서비스 설계와 운영에 강점이 있는 개발자.\n\n[프로젝트 경험]\n현대오토에버(2024~2025): 차량 데이터 수집 플랫폼 API 개발. 실시간 적재 파이프라인 구축과 배치 처리 시간 35% 단축.\n네이버(2022~2024): 광고 리포트 관리자 화면 개발. 대용량 차트 렌더링 최적화.\n배달의민족(2020~2022): 매장 운영 백오피스 개발. 운영 도구 개선으로 CS 처리 시간 단축.\n\n[경력]\n사내 레거시 서비스 개선 프로젝트를 통해 안정적인 전환 작업을 수행했다.",
    ),
    EngineerProfile(
        engineer_id="eng-020",
        grade="SENIOR",
        status="AVAILABLE",
        engineer_role="DEVELOPER",
        employment_type="FULL_TIME",
        capability_text="Go / Gin / PostgreSQL / gRPC / Prometheus / Grafana\n\nAWS SAA",
        experience_text="[소개]\n8년차 커머스 플랫폼 개발자. 제조, 물류, 금융 도메인 경험을 바탕으로 안정적인 서비스를 구축한 개발자.\n\n[프로젝트 경험]\n삼성SDS(2024~2025): 물류 운영 시스템 백엔드 개발. 정산 배치 안정화와 장애 대응 체계 수립.\n카카오(2022~2024): 사용자 활동 분석 API 개발. 이벤트 수집 구조 개선으로 데이터 유실률 감소.\n토스(2020~2022): 금융 상품 가입 프로세스 개발. 인증 및 심사 API 연동 품질 향상.\n\n[경력]\n도메인 조직과 협업하며 요구사항을 기술 설계로 구체화하는 역할을 맡아 왔다.",
    ),
    EngineerProfile(
        engineer_id="eng-021",
        grade="SENIOR",
        status="AVAILABLE",
        engineer_role="DEVELOPER",
        employment_type="FULL_TIME",
        capability_text="Java / Spring Cloud / Kafka / MongoDB / Elasticsearch / Docker\n\n리눅스마스터 2급",
        experience_text="[소개]\n8년차 핀테크 백엔드 개발자. 대시보드, 관리자 화면, 실시간 데이터 처리 경험이 풍부한 개발자.\n\n[프로젝트 경험]\nLG CNS(2024~2025): 제조 MES 연동 서비스 개발. Oracle 쿼리 튜닝으로 주요 조회 성능 개선.\n쿠팡(2022~2024): 주문·배송 도메인 서비스 개발. 비동기 처리 구조 도입으로 피크 시간대 안정성 확보.\n당근(2020~2022): 지역 서비스 추천 기능 개발. A/B 테스트 기반 추천 로직 개선.\n\n[경력]\nSI 프로젝트에서 커머스와 제조 백엔드 개발을 담당하며 기본기를 다졌다.",
    ),
    EngineerProfile(
        engineer_id="eng-022",
        grade="SENIOR",
        status="AVAILABLE",
        engineer_role="DEVELOPER",
        employment_type="FULL_TIME",
        capability_text="Flutter / Dart / Firebase / REST API / Figma / GitHub Actions\n\nADsP",
        experience_text="[소개]\n8년차 웹 애플리케이션 개발자. API 설계와 성능 개선을 반복적으로 수행해 온 문제 해결형 개발자.\n\n[프로젝트 경험]\n네이버(2024~2025): 광고 리포트 관리자 화면 개발. 대용량 차트 렌더링 최적화.\n배달의민족(2022~2024): 매장 운영 백오피스 개발. 운영 도구 개선으로 CS 처리 시간 단축.\n무신사(2020~2022): 프로모션·쿠폰 서비스 개발. 트래픽 급증 구간 캐시 전략 적용.\n\n[경력]\n스타트업에서 풀스택 개발과 운영 자동화를 맡으며 빠른 실행력을 키웠다.",
    ),
    EngineerProfile(
        engineer_id="eng-023",
        grade="SENIOR",
        status="AVAILABLE",
        engineer_role="DEVELOPER",
        employment_type="FULL_TIME",
        capability_text="Kotlin / Android / Jetpack Compose / Retrofit / Room / Firebase\n\n정보처리기사",
        experience_text="[소개]\n8년차 모바일 앱 개발자. MSA 전환, 클라우드 운영, 배포 자동화 경험을 함께 보유한 개발자.\n\n[프로젝트 경험]\n카카오(2024~2025): 사용자 활동 분석 API 개발. 이벤트 수집 구조 개선으로 데이터 유실률 감소.\n토스(2022~2024): 금융 상품 가입 프로세스 개발. 인증 및 심사 API 연동 품질 향상.\nSK하이닉스(2020~2022): 생산 모니터링 시스템 개발. 이벤트 기반 알림 구조 도입.\n\n[경력]\n플랫폼 조직에서 공통 모듈과 개발 표준을 정비한 경험이 있다.",
    ),
    EngineerProfile(
        engineer_id="eng-024",
        grade="SENIOR",
        status="AVAILABLE",
        engineer_role="DEVELOPER",
        employment_type="FULL_TIME",
        capability_text="TypeScript / React Native / Redux Toolkit / Expo / Firebase / Jest\n\nSQLD",
        experience_text="[소개]\n8년차 DevOps 엔지니어. 요구사항 분석부터 운영 안정화까지 전 과정을 폭넓게 수행한 개발자.\n\n[프로젝트 경험]\n쿠팡(2024~2025): 주문·배송 도메인 서비스 개발. 비동기 처리 구조 도입으로 피크 시간대 안정성 확보.\n당근(2022~2024): 지역 서비스 추천 기능 개발. A/B 테스트 기반 추천 로직 개선.\n포스코DX(2020~2022): 스마트팩토리 데이터 허브 개발. 현장 설비 데이터 표준화와 API 제공.\n\n[경력]\n사내 레거시 서비스 개선 프로젝트를 통해 안정적인 전환 작업을 수행했다.",
    ),
    EngineerProfile(
        engineer_id="eng-025",
        grade="SENIOR",
        status="AVAILABLE",
        engineer_role="DEVELOPER",
        employment_type="FULL_TIME",
        capability_text="Java / Spring Boot / Spring Batch / PostgreSQL / Redis / Docker\n\n정보처리기사",
        experience_text="[소개]\n8년차 백엔드 아키텍트. 대규모 트래픽 서비스 설계와 운영에 강점이 있는 개발자.\n\n[프로젝트 경험]\n배달의민족(2024~2025): 매장 운영 백오피스 개발. 운영 도구 개선으로 CS 처리 시간 단축.\n무신사(2022~2024): 프로모션·쿠폰 서비스 개발. 트래픽 급증 구간 캐시 전략 적용.\n야놀자(2020~2022): 숙박 예약 관리자 포털 개발. 운영 화면 공통 컴포넌트화.\n\n[경력]\n도메인 조직과 협업하며 요구사항을 기술 설계로 구체화하는 역할을 맡아 왔다.",
    ),
    EngineerProfile(
        engineer_id="eng-026",
        grade="SENIOR",
        status="AVAILABLE",
        engineer_role="DEVELOPER",
        employment_type="FULL_TIME",
        capability_text="Java / Kotlin / Spring Boot / MySQL / Kafka / AWS\n\nSQLD",
        experience_text="[소개]\n8년차 백엔드 개발자. 제조, 물류, 금융 도메인 경험을 바탕으로 안정적인 서비스를 구축한 개발자.\n\n[프로젝트 경험]\n토스(2024~2025): 금융 상품 가입 프로세스 개발. 인증 및 심사 API 연동 품질 향상.\nSK하이닉스(2022~2024): 생산 모니터링 시스템 개발. 이벤트 기반 알림 구조 도입.\n직방(2020~2022): 매물 관리 백오피스 개발. 권한 체계 정비와 검색 응답 속도 개선.\n\n[경력]\nSI 프로젝트에서 커머스와 제조 백엔드 개발을 담당하며 기본기를 다졌다.",
    ),
    EngineerProfile(
        engineer_id="eng-027",
        grade="SENIOR",
        status="AVAILABLE",
        engineer_role="DEVELOPER",
        employment_type="FULL_TIME",
        capability_text="Python / FastAPI / PostgreSQL / Docker / Kubernetes / Celery\n\nAWS SAA",
        experience_text="[소개]\n8년차 프론트엔드 개발자. 대시보드, 관리자 화면, 실시간 데이터 처리 경험이 풍부한 개발자.\n\n[프로젝트 경험]\n당근(2024~2025): 지역 서비스 추천 기능 개발. A/B 테스트 기반 추천 로직 개선.\n포스코DX(2022~2024): 스마트팩토리 데이터 허브 개발. 현장 설비 데이터 표준화와 API 제공.\n컬리(2020~2022): 정산·프로모션 엔진 개발. 배치 재처리 기능 추가로 운영 효율 향상.\n\n[경력]\n스타트업에서 풀스택 개발과 운영 자동화를 맡으며 빠른 실행력을 키웠다.",
    ),
    EngineerProfile(
        engineer_id="eng-028",
        grade="SENIOR",
        status="AVAILABLE",
        engineer_role="DEVELOPER",
        employment_type="FULL_TIME",
        capability_text="Python / Django / MySQL / Redis / Celery / AWS\n\n리눅스마스터 2급",
        experience_text="[소개]\n8년차 풀스택 개발자. API 설계와 성능 개선을 반복적으로 수행해 온 문제 해결형 개발자.\n\n[프로젝트 경험]\n무신사(2024~2025): 프로모션·쿠폰 서비스 개발. 트래픽 급증 구간 캐시 전략 적용.\n야놀자(2022~2024): 숙박 예약 관리자 포털 개발. 운영 화면 공통 컴포넌트화.\n현대카드(2020~2022): 결제 승인 시스템 고도화. 승인 응답 시간 안정화와 장애 포인트 축소.\n\n[경력]\n플랫폼 조직에서 공통 모듈과 개발 표준을 정비한 경험이 있다.",
    ),
    EngineerProfile(
        engineer_id="eng-029",
        grade="SENIOR",
        status="AVAILABLE",
        engineer_role="DEVELOPER",
        employment_type="FULL_TIME",
        capability_text="Node.js / NestJS / TypeScript / PostgreSQL / Redis / Swagger\n\nADsP",
        experience_text="[소개]\n8년차 데이터 플랫폼 개발자. MSA 전환, 클라우드 운영, 배포 자동화 경험을 함께 보유한 개발자.\n\n[프로젝트 경험]\nSK하이닉스(2024~2025): 생산 모니터링 시스템 개발. 이벤트 기반 알림 구조 도입.\n직방(2022~2024): 매물 관리 백오피스 개발. 권한 체계 정비와 검색 응답 속도 개선.\n신한은행(2020~2022): 기업뱅킹 API 플랫폼 구축. 내부 연계 표준화와 배포 자동화 정착.\n\n[경력]\n사내 레거시 서비스 개선 프로젝트를 통해 안정적인 전환 작업을 수행했다.",
    ),
    EngineerProfile(
        engineer_id="eng-030",
        grade="SENIOR",
        status="AVAILABLE",
        engineer_role="DEVELOPER",
        employment_type="FULL_TIME",
        capability_text="React / TypeScript / Next.js / TanStack Query / Storybook / Figma\n\n정보처리기사",
        experience_text="[소개]\n8년차 클라우드 플랫폼 개발자. 요구사항 분석부터 운영 안정화까지 전 과정을 폭넓게 수행한 개발자.\n\n[프로젝트 경험]\n포스코DX(2024~2025): 스마트팩토리 데이터 허브 개발. 현장 설비 데이터 표준화와 API 제공.\n컬리(2022~2024): 정산·프로모션 엔진 개발. 배치 재처리 기능 추가로 운영 효율 향상.\nCJ올리브영(2020~2022): 멤버십 서비스 개편. 쿠폰 정합성 검증 로직 강화.\n\n[경력]\n도메인 조직과 협업하며 요구사항을 기술 설계로 구체화하는 역할을 맡아 왔다.",
    ),
    EngineerProfile(
        engineer_id="eng-031",
        grade="INTERMEDIATE",
        status="AVAILABLE",
        engineer_role="DEVELOPER",
        employment_type="FULL_TIME",
        capability_text="React / Vue.js / TypeScript / Vite / Chart.js / Pinia\n\nSQLD",
        experience_text="[소개]\n5년차 AI 서비스 개발자. 대규모 트래픽 서비스 설계와 운영에 강점이 있는 개발자.\n\n[프로젝트 경험]\n야놀자(2024~2025): 숙박 예약 관리자 포털 개발. 운영 화면 공통 컴포넌트화.\n현대카드(2022~2024): 결제 승인 시스템 고도화. 승인 응답 시간 안정화와 장애 포인트 축소.\n현대오토에버(2020~2022): 차량 데이터 수집 플랫폼 API 개발. 실시간 적재 파이프라인 구축과 배치 처리 시간 35% 단축.\n\n[경력]\nSI 프로젝트에서 커머스와 제조 백엔드 개발을 담당하며 기본기를 다졌다.",
    ),
    EngineerProfile(
        engineer_id="eng-032",
        grade="INTERMEDIATE",
        status="AVAILABLE",
        engineer_role="DEVELOPER",
        employment_type="FULL_TIME",
        capability_text="Go / Gin / PostgreSQL / gRPC / Prometheus / Grafana\n\nAWS SAA",
        experience_text="[소개]\n5년차 커머스 플랫폼 개발자. 제조, 물류, 금융 도메인 경험을 바탕으로 안정적인 서비스를 구축한 개발자.\n\n[프로젝트 경험]\n직방(2024~2025): 매물 관리 백오피스 개발. 권한 체계 정비와 검색 응답 속도 개선.\n신한은행(2022~2024): 기업뱅킹 API 플랫폼 구축. 내부 연계 표준화와 배포 자동화 정착.\n삼성SDS(2020~2022): 물류 운영 시스템 백엔드 개발. 정산 배치 안정화와 장애 대응 체계 수립.\n\n[경력]\n스타트업에서 풀스택 개발과 운영 자동화를 맡으며 빠른 실행력을 키웠다.",
    ),
    EngineerProfile(
        engineer_id="eng-033",
        grade="INTERMEDIATE",
        status="AVAILABLE",
        engineer_role="DEVELOPER",
        employment_type="FULL_TIME",
        capability_text="Java / Spring Cloud / Kafka / MongoDB / Elasticsearch / Docker\n\n리눅스마스터 2급",
        experience_text="[소개]\n5년차 핀테크 백엔드 개발자. 대시보드, 관리자 화면, 실시간 데이터 처리 경험이 풍부한 개발자.\n\n[프로젝트 경험]\n컬리(2024~2025): 정산·프로모션 엔진 개발. 배치 재처리 기능 추가로 운영 효율 향상.\nCJ올리브영(2022~2024): 멤버십 서비스 개편. 쿠폰 정합성 검증 로직 강화.\nLG CNS(2020~2022): 제조 MES 연동 서비스 개발. Oracle 쿼리 튜닝으로 주요 조회 성능 개선.\n\n[경력]\n플랫폼 조직에서 공통 모듈과 개발 표준을 정비한 경험이 있다.",
    ),
    EngineerProfile(
        engineer_id="eng-034",
        grade="INTERMEDIATE",
        status="AVAILABLE",
        engineer_role="DEVELOPER",
        employment_type="FULL_TIME",
        capability_text="Flutter / Dart / Firebase / REST API / Figma / GitHub Actions\n\nADsP",
        experience_text="[소개]\n5년차 웹 애플리케이션 개발자. API 설계와 성능 개선을 반복적으로 수행해 온 문제 해결형 개발자.\n\n[프로젝트 경험]\n현대카드(2024~2025): 결제 승인 시스템 고도화. 승인 응답 시간 안정화와 장애 포인트 축소.\n현대오토에버(2022~2024): 차량 데이터 수집 플랫폼 API 개발. 실시간 적재 파이프라인 구축과 배치 처리 시간 35% 단축.\n네이버(2020~2022): 광고 리포트 관리자 화면 개발. 대용량 차트 렌더링 최적화.\n\n[경력]\n사내 레거시 서비스 개선 프로젝트를 통해 안정적인 전환 작업을 수행했다.",
    ),
    EngineerProfile(
        engineer_id="eng-035",
        grade="INTERMEDIATE",
        status="AVAILABLE",
        engineer_role="DEVELOPER",
        employment_type="FULL_TIME",
        capability_text="Kotlin / Android / Jetpack Compose / Retrofit / Room / Firebase\n\n정보처리기사",
        experience_text="[소개]\n5년차 모바일 앱 개발자. MSA 전환, 클라우드 운영, 배포 자동화 경험을 함께 보유한 개발자.\n\n[프로젝트 경험]\n신한은행(2024~2025): 기업뱅킹 API 플랫폼 구축. 내부 연계 표준화와 배포 자동화 정착.\n삼성SDS(2022~2024): 물류 운영 시스템 백엔드 개발. 정산 배치 안정화와 장애 대응 체계 수립.\n카카오(2020~2022): 사용자 활동 분석 API 개발. 이벤트 수집 구조 개선으로 데이터 유실률 감소.\n\n[경력]\n도메인 조직과 협업하며 요구사항을 기술 설계로 구체화하는 역할을 맡아 왔다.",
    ),
    EngineerProfile(
        engineer_id="eng-036",
        grade="INTERMEDIATE",
        status="AVAILABLE",
        engineer_role="DEVELOPER",
        employment_type="FULL_TIME",
        capability_text="TypeScript / React Native / Redux Toolkit / Expo / Firebase / Jest\n\nSQLD",
        experience_text="[소개]\n5년차 DevOps 엔지니어. 요구사항 분석부터 운영 안정화까지 전 과정을 폭넓게 수행한 개발자.\n\n[프로젝트 경험]\nCJ올리브영(2024~2025): 멤버십 서비스 개편. 쿠폰 정합성 검증 로직 강화.\nLG CNS(2022~2024): 제조 MES 연동 서비스 개발. Oracle 쿼리 튜닝으로 주요 조회 성능 개선.\n쿠팡(2020~2022): 주문·배송 도메인 서비스 개발. 비동기 처리 구조 도입으로 피크 시간대 안정성 확보.\n\n[경력]\nSI 프로젝트에서 커머스와 제조 백엔드 개발을 담당하며 기본기를 다졌다.",
    ),
    EngineerProfile(
        engineer_id="eng-037",
        grade="INTERMEDIATE",
        status="AVAILABLE",
        engineer_role="DEVELOPER",
        employment_type="FULL_TIME",
        capability_text="Java / Spring Boot / Spring Batch / PostgreSQL / Redis / Docker\n\n정보처리기사",
        experience_text="[소개]\n5년차 백엔드 아키텍트. 대규모 트래픽 서비스 설계와 운영에 강점이 있는 개발자.\n\n[프로젝트 경험]\n현대오토에버(2024~2025): 차량 데이터 수집 플랫폼 API 개발. 실시간 적재 파이프라인 구축과 배치 처리 시간 35% 단축.\n네이버(2022~2024): 광고 리포트 관리자 화면 개발. 대용량 차트 렌더링 최적화.\n배달의민족(2020~2022): 매장 운영 백오피스 개발. 운영 도구 개선으로 CS 처리 시간 단축.\n\n[경력]\n스타트업에서 풀스택 개발과 운영 자동화를 맡으며 빠른 실행력을 키웠다.",
    ),
    EngineerProfile(
        engineer_id="eng-038",
        grade="INTERMEDIATE",
        status="AVAILABLE",
        engineer_role="DEVELOPER",
        employment_type="FULL_TIME",
        capability_text="Java / Kotlin / Spring Boot / MySQL / Kafka / AWS\n\nSQLD",
        experience_text="[소개]\n5년차 백엔드 개발자. 제조, 물류, 금융 도메인 경험을 바탕으로 안정적인 서비스를 구축한 개발자.\n\n[프로젝트 경험]\n삼성SDS(2024~2025): 물류 운영 시스템 백엔드 개발. 정산 배치 안정화와 장애 대응 체계 수립.\n카카오(2022~2024): 사용자 활동 분석 API 개발. 이벤트 수집 구조 개선으로 데이터 유실률 감소.\n토스(2020~2022): 금융 상품 가입 프로세스 개발. 인증 및 심사 API 연동 품질 향상.\n\n[경력]\n플랫폼 조직에서 공통 모듈과 개발 표준을 정비한 경험이 있다.",
    ),
    EngineerProfile(
        engineer_id="eng-039",
        grade="INTERMEDIATE",
        status="AVAILABLE",
        engineer_role="DEVELOPER",
        employment_type="FULL_TIME",
        capability_text="Python / FastAPI / PostgreSQL / Docker / Kubernetes / Celery\n\nAWS SAA",
        experience_text="[소개]\n5년차 프론트엔드 개발자. 대시보드, 관리자 화면, 실시간 데이터 처리 경험이 풍부한 개발자.\n\n[프로젝트 경험]\nLG CNS(2024~2025): 제조 MES 연동 서비스 개발. Oracle 쿼리 튜닝으로 주요 조회 성능 개선.\n쿠팡(2022~2024): 주문·배송 도메인 서비스 개발. 비동기 처리 구조 도입으로 피크 시간대 안정성 확보.\n당근(2020~2022): 지역 서비스 추천 기능 개발. A/B 테스트 기반 추천 로직 개선.\n\n[경력]\n사내 레거시 서비스 개선 프로젝트를 통해 안정적인 전환 작업을 수행했다.",
    ),
    EngineerProfile(
        engineer_id="eng-040",
        grade="INTERMEDIATE",
        status="AVAILABLE",
        engineer_role="DEVELOPER",
        employment_type="FULL_TIME",
        capability_text="Python / Django / MySQL / Redis / Celery / AWS\n\n리눅스마스터 2급",
        experience_text="[소개]\n5년차 풀스택 개발자. API 설계와 성능 개선을 반복적으로 수행해 온 문제 해결형 개발자.\n\n[프로젝트 경험]\n네이버(2024~2025): 광고 리포트 관리자 화면 개발. 대용량 차트 렌더링 최적화.\n배달의민족(2022~2024): 매장 운영 백오피스 개발. 운영 도구 개선으로 CS 처리 시간 단축.\n무신사(2020~2022): 프로모션·쿠폰 서비스 개발. 트래픽 급증 구간 캐시 전략 적용.\n\n[경력]\n도메인 조직과 협업하며 요구사항을 기술 설계로 구체화하는 역할을 맡아 왔다.",
    ),
    EngineerProfile(
        engineer_id="eng-041",
        grade="INTERMEDIATE",
        status="AVAILABLE",
        engineer_role="DEVELOPER",
        employment_type="FULL_TIME",
        capability_text="Node.js / NestJS / TypeScript / PostgreSQL / Redis / Swagger\n\nADsP",
        experience_text="[소개]\n5년차 데이터 플랫폼 개발자. MSA 전환, 클라우드 운영, 배포 자동화 경험을 함께 보유한 개발자.\n\n[프로젝트 경험]\n카카오(2024~2025): 사용자 활동 분석 API 개발. 이벤트 수집 구조 개선으로 데이터 유실률 감소.\n토스(2022~2024): 금융 상품 가입 프로세스 개발. 인증 및 심사 API 연동 품질 향상.\nSK하이닉스(2020~2022): 생산 모니터링 시스템 개발. 이벤트 기반 알림 구조 도입.\n\n[경력]\nSI 프로젝트에서 커머스와 제조 백엔드 개발을 담당하며 기본기를 다졌다.",
    ),
    EngineerProfile(
        engineer_id="eng-042",
        grade="INTERMEDIATE",
        status="AVAILABLE",
        engineer_role="DEVELOPER",
        employment_type="FULL_TIME",
        capability_text="React / TypeScript / Next.js / TanStack Query / Storybook / Figma\n\n정보처리기사",
        experience_text="[소개]\n5년차 클라우드 플랫폼 개발자. 요구사항 분석부터 운영 안정화까지 전 과정을 폭넓게 수행한 개발자.\n\n[프로젝트 경험]\n쿠팡(2024~2025): 주문·배송 도메인 서비스 개발. 비동기 처리 구조 도입으로 피크 시간대 안정성 확보.\n당근(2022~2024): 지역 서비스 추천 기능 개발. A/B 테스트 기반 추천 로직 개선.\n포스코DX(2020~2022): 스마트팩토리 데이터 허브 개발. 현장 설비 데이터 표준화와 API 제공.\n\n[경력]\n스타트업에서 풀스택 개발과 운영 자동화를 맡으며 빠른 실행력을 키웠다.",
    ),
    EngineerProfile(
        engineer_id="eng-043",
        grade="INTERMEDIATE",
        status="AVAILABLE",
        engineer_role="DEVELOPER",
        employment_type="FULL_TIME",
        capability_text="React / Vue.js / TypeScript / Vite / Chart.js / Pinia\n\nSQLD",
        experience_text="[소개]\n5년차 AI 서비스 개발자. 대규모 트래픽 서비스 설계와 운영에 강점이 있는 개발자.\n\n[프로젝트 경험]\n배달의민족(2024~2025): 매장 운영 백오피스 개발. 운영 도구 개선으로 CS 처리 시간 단축.\n무신사(2022~2024): 프로모션·쿠폰 서비스 개발. 트래픽 급증 구간 캐시 전략 적용.\n야놀자(2020~2022): 숙박 예약 관리자 포털 개발. 운영 화면 공통 컴포넌트화.\n\n[경력]\n플랫폼 조직에서 공통 모듈과 개발 표준을 정비한 경험이 있다.",
    ),
    EngineerProfile(
        engineer_id="eng-044",
        grade="INTERMEDIATE",
        status="AVAILABLE",
        engineer_role="DEVELOPER",
        employment_type="FULL_TIME",
        capability_text="Go / Gin / PostgreSQL / gRPC / Prometheus / Grafana\n\nAWS SAA",
        experience_text="[소개]\n5년차 커머스 플랫폼 개발자. 제조, 물류, 금융 도메인 경험을 바탕으로 안정적인 서비스를 구축한 개발자.\n\n[프로젝트 경험]\n토스(2024~2025): 금융 상품 가입 프로세스 개발. 인증 및 심사 API 연동 품질 향상.\nSK하이닉스(2022~2024): 생산 모니터링 시스템 개발. 이벤트 기반 알림 구조 도입.\n직방(2020~2022): 매물 관리 백오피스 개발. 권한 체계 정비와 검색 응답 속도 개선.\n\n[경력]\n사내 레거시 서비스 개선 프로젝트를 통해 안정적인 전환 작업을 수행했다.",
    ),
    EngineerProfile(
        engineer_id="eng-045",
        grade="INTERMEDIATE",
        status="AVAILABLE",
        engineer_role="DEVELOPER",
        employment_type="FULL_TIME",
        capability_text="Java / Spring Cloud / Kafka / MongoDB / Elasticsearch / Docker\n\n리눅스마스터 2급",
        experience_text="[소개]\n5년차 핀테크 백엔드 개발자. 대시보드, 관리자 화면, 실시간 데이터 처리 경험이 풍부한 개발자.\n\n[프로젝트 경험]\n당근(2024~2025): 지역 서비스 추천 기능 개발. A/B 테스트 기반 추천 로직 개선.\n포스코DX(2022~2024): 스마트팩토리 데이터 허브 개발. 현장 설비 데이터 표준화와 API 제공.\n컬리(2020~2022): 정산·프로모션 엔진 개발. 배치 재처리 기능 추가로 운영 효율 향상.\n\n[경력]\n도메인 조직과 협업하며 요구사항을 기술 설계로 구체화하는 역할을 맡아 왔다.",
    ),
    EngineerProfile(
        engineer_id="eng-046",
        grade="INTERMEDIATE",
        status="AVAILABLE",
        engineer_role="DEVELOPER",
        employment_type="FULL_TIME",
        capability_text="Flutter / Dart / Firebase / REST API / Figma / GitHub Actions\n\nADsP",
        experience_text="[소개]\n5년차 웹 애플리케이션 개발자. API 설계와 성능 개선을 반복적으로 수행해 온 문제 해결형 개발자.\n\n[프로젝트 경험]\n무신사(2024~2025): 프로모션·쿠폰 서비스 개발. 트래픽 급증 구간 캐시 전략 적용.\n야놀자(2022~2024): 숙박 예약 관리자 포털 개발. 운영 화면 공통 컴포넌트화.\n현대카드(2020~2022): 결제 승인 시스템 고도화. 승인 응답 시간 안정화와 장애 포인트 축소.\n\n[경력]\nSI 프로젝트에서 커머스와 제조 백엔드 개발을 담당하며 기본기를 다졌다.",
    ),
    EngineerProfile(
        engineer_id="eng-047",
        grade="INTERMEDIATE",
        status="AVAILABLE",
        engineer_role="DEVELOPER",
        employment_type="FULL_TIME",
        capability_text="Kotlin / Android / Jetpack Compose / Retrofit / Room / Firebase\n\n정보처리기사",
        experience_text="[소개]\n5년차 모바일 앱 개발자. MSA 전환, 클라우드 운영, 배포 자동화 경험을 함께 보유한 개발자.\n\n[프로젝트 경험]\nSK하이닉스(2024~2025): 생산 모니터링 시스템 개발. 이벤트 기반 알림 구조 도입.\n직방(2022~2024): 매물 관리 백오피스 개발. 권한 체계 정비와 검색 응답 속도 개선.\n신한은행(2020~2022): 기업뱅킹 API 플랫폼 구축. 내부 연계 표준화와 배포 자동화 정착.\n\n[경력]\n스타트업에서 풀스택 개발과 운영 자동화를 맡으며 빠른 실행력을 키웠다.",
    ),
    EngineerProfile(
        engineer_id="eng-048",
        grade="INTERMEDIATE",
        status="AVAILABLE",
        engineer_role="DEVELOPER",
        employment_type="FULL_TIME",
        capability_text="TypeScript / React Native / Redux Toolkit / Expo / Firebase / Jest\n\nSQLD",
        experience_text="[소개]\n5년차 DevOps 엔지니어. 요구사항 분석부터 운영 안정화까지 전 과정을 폭넓게 수행한 개발자.\n\n[프로젝트 경험]\n포스코DX(2024~2025): 스마트팩토리 데이터 허브 개발. 현장 설비 데이터 표준화와 API 제공.\n컬리(2022~2024): 정산·프로모션 엔진 개발. 배치 재처리 기능 추가로 운영 효율 향상.\nCJ올리브영(2020~2022): 멤버십 서비스 개편. 쿠폰 정합성 검증 로직 강화.\n\n[경력]\n플랫폼 조직에서 공통 모듈과 개발 표준을 정비한 경험이 있다.",
    ),
    EngineerProfile(
        engineer_id="eng-049",
        grade="INTERMEDIATE",
        status="AVAILABLE",
        engineer_role="DEVELOPER",
        employment_type="FREELANCER",
        capability_text="Java / Spring Boot / Spring Batch / PostgreSQL / Redis / Docker\n\n정보처리기사",
        experience_text="[소개]\n5년차 백엔드 아키텍트. 대규모 트래픽 서비스 설계와 운영에 강점이 있는 개발자.\n\n[프로젝트 경험]\n야놀자(2024~2025): 숙박 예약 관리자 포털 개발. 운영 화면 공통 컴포넌트화.\n현대카드(2022~2024): 결제 승인 시스템 고도화. 승인 응답 시간 안정화와 장애 포인트 축소.\n현대오토에버(2020~2022): 차량 데이터 수집 플랫폼 API 개발. 실시간 적재 파이프라인 구축과 배치 처리 시간 35% 단축.\n\n[경력]\n사내 레거시 서비스 개선 프로젝트를 통해 안정적인 전환 작업을 수행했다.",
    ),
    EngineerProfile(
        engineer_id="eng-050",
        grade="INTERMEDIATE",
        status="AVAILABLE",
        engineer_role="DEVELOPER",
        employment_type="FREELANCER",
        capability_text="Java / Kotlin / Spring Boot / MySQL / Kafka / AWS\n\nSQLD",
        experience_text="[소개]\n5년차 백엔드 개발자. 제조, 물류, 금융 도메인 경험을 바탕으로 안정적인 서비스를 구축한 개발자.\n\n[프로젝트 경험]\n직방(2024~2025): 매물 관리 백오피스 개발. 권한 체계 정비와 검색 응답 속도 개선.\n신한은행(2022~2024): 기업뱅킹 API 플랫폼 구축. 내부 연계 표준화와 배포 자동화 정착.\n삼성SDS(2020~2022): 물류 운영 시스템 백엔드 개발. 정산 배치 안정화와 장애 대응 체계 수립.\n\n[경력]\n도메인 조직과 협업하며 요구사항을 기술 설계로 구체화하는 역할을 맡아 왔다.",
    ),
    EngineerProfile(
        engineer_id="eng-051",
        grade="JUNIOR",
        status="AVAILABLE",
        engineer_role="DEVELOPER",
        employment_type="FREELANCER",
        capability_text="Python / FastAPI / PostgreSQL / Docker / Kubernetes / Celery\n\nAWS SAA",
        experience_text="[소개]\n2년차 프론트엔드 개발자. 대시보드, 관리자 화면, 실시간 데이터 처리 경험이 풍부한 개발자.\n\n[프로젝트 경험]\n컬리(2024~2025): 정산·프로모션 엔진 개발. 배치 재처리 기능 추가로 운영 효율 향상.\nCJ올리브영(2022~2024): 멤버십 서비스 개편. 쿠폰 정합성 검증 로직 강화.\nLG CNS(2020~2022): 제조 MES 연동 서비스 개발. Oracle 쿼리 튜닝으로 주요 조회 성능 개선.\n\n[경력]\nSI 프로젝트에서 커머스와 제조 백엔드 개발을 담당하며 기본기를 다졌다.",
    ),
    EngineerProfile(
        engineer_id="eng-052",
        grade="JUNIOR",
        status="AVAILABLE",
        engineer_role="DEVELOPER",
        employment_type="FREELANCER",
        capability_text="Python / Django / MySQL / Redis / Celery / AWS\n\n리눅스마스터 2급",
        experience_text="[소개]\n2년차 풀스택 개발자. API 설계와 성능 개선을 반복적으로 수행해 온 문제 해결형 개발자.\n\n[프로젝트 경험]\n현대카드(2024~2025): 결제 승인 시스템 고도화. 승인 응답 시간 안정화와 장애 포인트 축소.\n현대오토에버(2022~2024): 차량 데이터 수집 플랫폼 API 개발. 실시간 적재 파이프라인 구축과 배치 처리 시간 35% 단축.\n네이버(2020~2022): 광고 리포트 관리자 화면 개발. 대용량 차트 렌더링 최적화.\n\n[경력]\n스타트업에서 풀스택 개발과 운영 자동화를 맡으며 빠른 실행력을 키웠다.",
    ),
    EngineerProfile(
        engineer_id="eng-053",
        grade="JUNIOR",
        status="AVAILABLE",
        engineer_role="DEVELOPER",
        employment_type="FREELANCER",
        capability_text="Node.js / NestJS / TypeScript / PostgreSQL / Redis / Swagger\n\nADsP",
        experience_text="[소개]\n2년차 데이터 플랫폼 개발자. MSA 전환, 클라우드 운영, 배포 자동화 경험을 함께 보유한 개발자.\n\n[프로젝트 경험]\n신한은행(2024~2025): 기업뱅킹 API 플랫폼 구축. 내부 연계 표준화와 배포 자동화 정착.\n삼성SDS(2022~2024): 물류 운영 시스템 백엔드 개발. 정산 배치 안정화와 장애 대응 체계 수립.\n카카오(2020~2022): 사용자 활동 분석 API 개발. 이벤트 수집 구조 개선으로 데이터 유실률 감소.\n\n[경력]\n플랫폼 조직에서 공통 모듈과 개발 표준을 정비한 경험이 있다.",
    ),
    EngineerProfile(
        engineer_id="eng-054",
        grade="JUNIOR",
        status="AVAILABLE",
        engineer_role="DEVELOPER",
        employment_type="FREELANCER",
        capability_text="React / TypeScript / Next.js / TanStack Query / Storybook / Figma\n\n정보처리기사",
        experience_text="[소개]\n2년차 클라우드 플랫폼 개발자. 요구사항 분석부터 운영 안정화까지 전 과정을 폭넓게 수행한 개발자.\n\n[프로젝트 경험]\nCJ올리브영(2024~2025): 멤버십 서비스 개편. 쿠폰 정합성 검증 로직 강화.\nLG CNS(2022~2024): 제조 MES 연동 서비스 개발. Oracle 쿼리 튜닝으로 주요 조회 성능 개선.\n쿠팡(2020~2022): 주문·배송 도메인 서비스 개발. 비동기 처리 구조 도입으로 피크 시간대 안정성 확보.\n\n[경력]\n사내 레거시 서비스 개선 프로젝트를 통해 안정적인 전환 작업을 수행했다.",
    ),
    EngineerProfile(
        engineer_id="eng-055",
        grade="JUNIOR",
        status="AVAILABLE",
        engineer_role="DEVELOPER",
        employment_type="FREELANCER",
        capability_text="React / Vue.js / TypeScript / Vite / Chart.js / Pinia\n\nSQLD",
        experience_text="[소개]\n2년차 AI 서비스 개발자. 대규모 트래픽 서비스 설계와 운영에 강점이 있는 개발자.\n\n[프로젝트 경험]\n현대오토에버(2024~2025): 차량 데이터 수집 플랫폼 API 개발. 실시간 적재 파이프라인 구축과 배치 처리 시간 35% 단축.\n네이버(2022~2024): 광고 리포트 관리자 화면 개발. 대용량 차트 렌더링 최적화.\n배달의민족(2020~2022): 매장 운영 백오피스 개발. 운영 도구 개선으로 CS 처리 시간 단축.\n\n[경력]\n도메인 조직과 협업하며 요구사항을 기술 설계로 구체화하는 역할을 맡아 왔다.",
    ),
    EngineerProfile(
        engineer_id="eng-056",
        grade="JUNIOR",
        status="AVAILABLE",
        engineer_role="DEVELOPER",
        employment_type="FREELANCER",
        capability_text="Go / Gin / PostgreSQL / gRPC / Prometheus / Grafana\n\nAWS SAA",
        experience_text="[소개]\n2년차 커머스 플랫폼 개발자. 제조, 물류, 금융 도메인 경험을 바탕으로 안정적인 서비스를 구축한 개발자.\n\n[프로젝트 경험]\n삼성SDS(2024~2025): 물류 운영 시스템 백엔드 개발. 정산 배치 안정화와 장애 대응 체계 수립.\n카카오(2022~2024): 사용자 활동 분석 API 개발. 이벤트 수집 구조 개선으로 데이터 유실률 감소.\n토스(2020~2022): 금융 상품 가입 프로세스 개발. 인증 및 심사 API 연동 품질 향상.\n\n[경력]\nSI 프로젝트에서 커머스와 제조 백엔드 개발을 담당하며 기본기를 다졌다.",
    ),
    EngineerProfile(
        engineer_id="eng-057",
        grade="JUNIOR",
        status="AVAILABLE",
        engineer_role="DEVELOPER",
        employment_type="FREELANCER",
        capability_text="Java / Spring Cloud / Kafka / MongoDB / Elasticsearch / Docker\n\n리눅스마스터 2급",
        experience_text="[소개]\n2년차 핀테크 백엔드 개발자. 대시보드, 관리자 화면, 실시간 데이터 처리 경험이 풍부한 개발자.\n\n[프로젝트 경험]\nLG CNS(2024~2025): 제조 MES 연동 서비스 개발. Oracle 쿼리 튜닝으로 주요 조회 성능 개선.\n쿠팡(2022~2024): 주문·배송 도메인 서비스 개발. 비동기 처리 구조 도입으로 피크 시간대 안정성 확보.\n당근(2020~2022): 지역 서비스 추천 기능 개발. A/B 테스트 기반 추천 로직 개선.\n\n[경력]\n스타트업에서 풀스택 개발과 운영 자동화를 맡으며 빠른 실행력을 키웠다.",
    ),
    EngineerProfile(
        engineer_id="eng-058",
        grade="JUNIOR",
        status="AVAILABLE",
        engineer_role="DEVELOPER",
        employment_type="FREELANCER",
        capability_text="Flutter / Dart / Firebase / REST API / Figma / GitHub Actions\n\nADsP",
        experience_text="[소개]\n2년차 웹 애플리케이션 개발자. API 설계와 성능 개선을 반복적으로 수행해 온 문제 해결형 개발자.\n\n[프로젝트 경험]\n네이버(2024~2025): 광고 리포트 관리자 화면 개발. 대용량 차트 렌더링 최적화.\n배달의민족(2022~2024): 매장 운영 백오피스 개발. 운영 도구 개선으로 CS 처리 시간 단축.\n무신사(2020~2022): 프로모션·쿠폰 서비스 개발. 트래픽 급증 구간 캐시 전략 적용.\n\n[경력]\n플랫폼 조직에서 공통 모듈과 개발 표준을 정비한 경험이 있다.",
    ),
    EngineerProfile(
        engineer_id="eng-059",
        grade="JUNIOR",
        status="AVAILABLE",
        engineer_role="DEVELOPER",
        employment_type="FREELANCER",
        capability_text="Kotlin / Android / Jetpack Compose / Retrofit / Room / Firebase\n\n정보처리기사",
        experience_text="[소개]\n2년차 모바일 앱 개발자. MSA 전환, 클라우드 운영, 배포 자동화 경험을 함께 보유한 개발자.\n\n[프로젝트 경험]\n카카오(2024~2025): 사용자 활동 분석 API 개발. 이벤트 수집 구조 개선으로 데이터 유실률 감소.\n토스(2022~2024): 금융 상품 가입 프로세스 개발. 인증 및 심사 API 연동 품질 향상.\nSK하이닉스(2020~2022): 생산 모니터링 시스템 개발. 이벤트 기반 알림 구조 도입.\n\n[경력]\n사내 레거시 서비스 개선 프로젝트를 통해 안정적인 전환 작업을 수행했다.",
    ),
    EngineerProfile(
        engineer_id="eng-060",
        grade="JUNIOR",
        status="AVAILABLE",
        engineer_role="DEVELOPER",
        employment_type="FREELANCER",
        capability_text="TypeScript / React Native / Redux Toolkit / Expo / Firebase / Jest\n\nSQLD",
        experience_text="[소개]\n2년차 DevOps 엔지니어. 요구사항 분석부터 운영 안정화까지 전 과정을 폭넓게 수행한 개발자.\n\n[프로젝트 경험]\n쿠팡(2024~2025): 주문·배송 도메인 서비스 개발. 비동기 처리 구조 도입으로 피크 시간대 안정성 확보.\n당근(2022~2024): 지역 서비스 추천 기능 개발. A/B 테스트 기반 추천 로직 개선.\n포스코DX(2020~2022): 스마트팩토리 데이터 허브 개발. 현장 설비 데이터 표준화와 API 제공.\n\n[경력]\n도메인 조직과 협업하며 요구사항을 기술 설계로 구체화하는 역할을 맡아 왔다.",
    ),
    EngineerProfile(
        engineer_id="des-001",
        grade="EXPERT",
        status="AVAILABLE",
        engineer_role="DESIGNER",
        employment_type="FULL_TIME",
        capability_text="Figma / FigJam / Photoshop / Illustrator / ProtoPie / Zeplin\n\nGTQ 1급",
        experience_text="[소개]\n12년차 UX 디자이너. 서비스 흐름 개선과 디자인 시스템 구축 경험이 풍부한 디자이너.\n\n[프로젝트 경험]\n토스(2024~2025): 신규 금융 상품 가입 UX 개선. 가입 이탈률 감소와 핵심 과업 완료율 상승.\n무신사(2022~2024): 프로모션 허브 화면 설계. 콘텐츠 소비 동선 정리.\n컬리(2020~2022): 장바구니·결제 UX 개선. 결제 완료율 향상.\n\n[경력]\n에이전시에서 브랜드 사이트와 모바일 앱 프로젝트를 다수 수행했다.",
    ),
    EngineerProfile(
        engineer_id="des-002",
        grade="EXPERT",
        status="AVAILABLE",
        engineer_role="DESIGNER",
        employment_type="FULL_TIME",
        capability_text="Figma / After Effects / Illustrator / Maze / Notion / Jira\n\n웹디자인기능사",
        experience_text="[소개]\n12년차 UI 디자이너. 사용자 리서치 기반으로 문제를 정의하고 화면 구조를 설계하는 디자이너.\n\n[프로젝트 경험]\n야놀자(2024~2025): 숙소 상세·예약 화면 UI 리뉴얼. 모바일 전환율 개선.\n직방(2022~2024): 매물 상세 정보 구조 재설계. 핵심 정보 인지 속도 개선.\n당근(2020~2022): 지역 피드 탐색 경험 개편. 콘텐츠 탐색 전환율 개선.\n\n[경력]\n사내 프로덕트 조직에서 리서치와 디자인 시스템 운영을 병행했다.",
    ),
    EngineerProfile(
        engineer_id="des-003",
        grade="SENIOR",
        status="AVAILABLE",
        engineer_role="DESIGNER",
        employment_type="FULL_TIME",
        capability_text="Sketch / Figma / Principle / Photoshop / Zeplin / Miro\n\n없음",
        experience_text="[소개]\n8년차 프로덕트 디자이너. 금융, 커머스, 콘텐츠 서비스에서 일관된 UI 품질을 만들어 온 디자이너.\n\n[프로젝트 경험]\n오늘의집(2024~2025): 검색 및 탐색 경험 개편. 필터 사용성과 정보 구조 개선.\n카카오페이(2022~2024): 송금 프로세스 디자인 시스템 반영. 일관된 컴포넌트 적용.\n토스(2020~2022): 신규 금융 상품 가입 UX 개선. 가입 이탈률 감소와 핵심 과업 완료율 상승.\n\n[경력]\n스타트업에서 PM, 개발자와 밀접하게 협업하며 서비스 초기 구조를 설계했다.",
    ),
    EngineerProfile(
        engineer_id="des-004",
        grade="SENIOR",
        status="AVAILABLE",
        engineer_role="DESIGNER",
        employment_type="FULL_TIME",
        capability_text="Figma / Adobe XD / Illustrator / GA4 / Hotjar / Notion\n\nGTQ 1급",
        experience_text="[소개]\n8년차 브랜드 디자이너. 복잡한 업무 프로세스를 이해하기 쉬운 화면 구조로 풀어내는 디자이너.\n\n[프로젝트 경험]\n무신사(2024~2025): 프로모션 허브 화면 설계. 콘텐츠 소비 동선 정리.\n컬리(2022~2024): 장바구니·결제 UX 개선. 결제 완료율 향상.\n야놀자(2020~2022): 숙소 상세·예약 화면 UI 리뉴얼. 모바일 전환율 개선.\n\n[경력]\n정량·정성 데이터를 함께 보며 화면 우선순위를 조정해 온 경험이 있다.",
    ),
    EngineerProfile(
        engineer_id="des-005",
        grade="SENIOR",
        status="AVAILABLE",
        engineer_role="DESIGNER",
        employment_type="FULL_TIME",
        capability_text="Figma / FigJam / Dovetail / Excel / Notion / Confluence\n\n없음",
        experience_text="[소개]\n8년차 UX 리서처. 서비스 흐름 개선과 디자인 시스템 구축 경험이 풍부한 디자이너.\n\n[프로젝트 경험]\n직방(2024~2025): 매물 상세 정보 구조 재설계. 핵심 정보 인지 속도 개선.\n당근(2022~2024): 지역 피드 탐색 경험 개편. 콘텐츠 탐색 전환율 개선.\n오늘의집(2020~2022): 검색 및 탐색 경험 개편. 필터 사용성과 정보 구조 개선.\n\n[경력]\n에이전시에서 브랜드 사이트와 모바일 앱 프로젝트를 다수 수행했다.",
    ),
    EngineerProfile(
        engineer_id="des-006",
        grade="SENIOR",
        status="AVAILABLE",
        engineer_role="DESIGNER",
        employment_type="FULL_TIME",
        capability_text="Figma / FigJam / Photoshop / Illustrator / ProtoPie / Zeplin\n\nGTQ 1급",
        experience_text="[소개]\n8년차 UX 디자이너. 사용자 리서치 기반으로 문제를 정의하고 화면 구조를 설계하는 디자이너.\n\n[프로젝트 경험]\n카카오페이(2024~2025): 송금 프로세스 디자인 시스템 반영. 일관된 컴포넌트 적용.\n토스(2022~2024): 신규 금융 상품 가입 UX 개선. 가입 이탈률 감소와 핵심 과업 완료율 상승.\n무신사(2020~2022): 프로모션 허브 화면 설계. 콘텐츠 소비 동선 정리.\n\n[경력]\n사내 프로덕트 조직에서 리서치와 디자인 시스템 운영을 병행했다.",
    ),
    EngineerProfile(
        engineer_id="des-007",
        grade="INTERMEDIATE",
        status="AVAILABLE",
        engineer_role="DESIGNER",
        employment_type="FULL_TIME",
        capability_text="Figma / After Effects / Illustrator / Maze / Notion / Jira\n\n웹디자인기능사",
        experience_text="[소개]\n5년차 UI 디자이너. 금융, 커머스, 콘텐츠 서비스에서 일관된 UI 품질을 만들어 온 디자이너.\n\n[프로젝트 경험]\n컬리(2024~2025): 장바구니·결제 UX 개선. 결제 완료율 향상.\n야놀자(2022~2024): 숙소 상세·예약 화면 UI 리뉴얼. 모바일 전환율 개선.\n직방(2020~2022): 매물 상세 정보 구조 재설계. 핵심 정보 인지 속도 개선.\n\n[경력]\n스타트업에서 PM, 개발자와 밀접하게 협업하며 서비스 초기 구조를 설계했다.",
    ),
    EngineerProfile(
        engineer_id="des-008",
        grade="INTERMEDIATE",
        status="AVAILABLE",
        engineer_role="DESIGNER",
        employment_type="FULL_TIME",
        capability_text="Sketch / Figma / Principle / Photoshop / Zeplin / Miro\n\n없음",
        experience_text="[소개]\n5년차 프로덕트 디자이너. 복잡한 업무 프로세스를 이해하기 쉬운 화면 구조로 풀어내는 디자이너.\n\n[프로젝트 경험]\n당근(2024~2025): 지역 피드 탐색 경험 개편. 콘텐츠 탐색 전환율 개선.\n오늘의집(2022~2024): 검색 및 탐색 경험 개편. 필터 사용성과 정보 구조 개선.\n카카오페이(2020~2022): 송금 프로세스 디자인 시스템 반영. 일관된 컴포넌트 적용.\n\n[경력]\n정량·정성 데이터를 함께 보며 화면 우선순위를 조정해 온 경험이 있다.",
    ),
    EngineerProfile(
        engineer_id="des-009",
        grade="INTERMEDIATE",
        status="AVAILABLE",
        engineer_role="DESIGNER",
        employment_type="FREELANCER",
        capability_text="Figma / Adobe XD / Illustrator / GA4 / Hotjar / Notion\n\nGTQ 1급",
        experience_text="[소개]\n5년차 브랜드 디자이너. 서비스 흐름 개선과 디자인 시스템 구축 경험이 풍부한 디자이너.\n\n[프로젝트 경험]\n토스(2024~2025): 신규 금융 상품 가입 UX 개선. 가입 이탈률 감소와 핵심 과업 완료율 상승.\n무신사(2022~2024): 프로모션 허브 화면 설계. 콘텐츠 소비 동선 정리.\n컬리(2020~2022): 장바구니·결제 UX 개선. 결제 완료율 향상.\n\n[경력]\n에이전시에서 브랜드 사이트와 모바일 앱 프로젝트를 다수 수행했다.",
    ),
    EngineerProfile(
        engineer_id="des-010",
        grade="INTERMEDIATE",
        status="AVAILABLE",
        engineer_role="DESIGNER",
        employment_type="FREELANCER",
        capability_text="Figma / FigJam / Dovetail / Excel / Notion / Confluence\n\n없음",
        experience_text="[소개]\n5년차 UX 리서처. 사용자 리서치 기반으로 문제를 정의하고 화면 구조를 설계하는 디자이너.\n\n[프로젝트 경험]\n야놀자(2024~2025): 숙소 상세·예약 화면 UI 리뉴얼. 모바일 전환율 개선.\n직방(2022~2024): 매물 상세 정보 구조 재설계. 핵심 정보 인지 속도 개선.\n당근(2020~2022): 지역 피드 탐색 경험 개편. 콘텐츠 탐색 전환율 개선.\n\n[경력]\n사내 프로덕트 조직에서 리서치와 디자인 시스템 운영을 병행했다.",
    ),
    EngineerProfile(
        engineer_id="des-011",
        grade="JUNIOR",
        status="AVAILABLE",
        engineer_role="DESIGNER",
        employment_type="FREELANCER",
        capability_text="Figma / FigJam / Photoshop / Illustrator / ProtoPie / Zeplin\n\nGTQ 1급",
        experience_text="[소개]\n2년차 UX 디자이너. 금융, 커머스, 콘텐츠 서비스에서 일관된 UI 품질을 만들어 온 디자이너.\n\n[프로젝트 경험]\n오늘의집(2024~2025): 검색 및 탐색 경험 개편. 필터 사용성과 정보 구조 개선.\n카카오페이(2022~2024): 송금 프로세스 디자인 시스템 반영. 일관된 컴포넌트 적용.\n토스(2020~2022): 신규 금융 상품 가입 UX 개선. 가입 이탈률 감소와 핵심 과업 완료율 상승.\n\n[경력]\n스타트업에서 PM, 개발자와 밀접하게 협업하며 서비스 초기 구조를 설계했다.",
    ),
    EngineerProfile(
        engineer_id="des-012",
        grade="JUNIOR",
        status="AVAILABLE",
        engineer_role="DESIGNER",
        employment_type="FREELANCER",
        capability_text="Figma / After Effects / Illustrator / Maze / Notion / Jira\n\n웹디자인기능사",
        experience_text="[소개]\n2년차 UI 디자이너. 복잡한 업무 프로세스를 이해하기 쉬운 화면 구조로 풀어내는 디자이너.\n\n[프로젝트 경험]\n무신사(2024~2025): 프로모션 허브 화면 설계. 콘텐츠 소비 동선 정리.\n컬리(2022~2024): 장바구니·결제 UX 개선. 결제 완료율 향상.\n야놀자(2020~2022): 숙소 상세·예약 화면 UI 리뉴얼. 모바일 전환율 개선.\n\n[경력]\n정량·정성 데이터를 함께 보며 화면 우선순위를 조정해 온 경험이 있다.",
    ),
    EngineerProfile(
        engineer_id="qa-001",
        grade="EXPERT",
        status="AVAILABLE",
        engineer_role="QA",
        employment_type="FULL_TIME",
        capability_text="Selenium / Appium / JMeter / Jira / Confluence / TestRail\n\nISTQB CTFL",
        experience_text="[소개]\n12년차 QA 엔지니어. 테스트 자동화와 릴리즈 품질 관리 경험이 풍부한 QA 엔지니어.\n\n[프로젝트 경험]\n카카오뱅크(2024~2025): 모바일 앱 회귀 테스트 자동화. 배포 전 검증 리드타임 단축.\n토스증권(2022~2024): 주식 거래 앱 E2E 테스트 구축. 핵심 거래 시나리오 자동화.\n현대카드(2020~2022): 결제 단말 연계 검증. 릴리즈 체크리스트 표준화.\n\n[경력]\nSI 프로젝트에서 수동 테스트와 결함 관리를 담당하며 QA 기본기를 다졌다.",
    ),
    EngineerProfile(
        engineer_id="qa-002",
        grade="SENIOR",
        status="AVAILABLE",
        engineer_role="QA",
        employment_type="FULL_TIME",
        capability_text="Playwright / Python / Jenkins / Allure / PostgreSQL / Grafana\n\nSQLD",
        experience_text="[소개]\n8년차 테스트 자동화 엔지니어. 금융, 커머스, 모바일 앱 품질 검증과 성능 테스트를 수행한 QA 엔지니어.\n\n[프로젝트 경험]\n라인(2024~2025): 글로벌 메신저 부하 테스트. 병목 구간 식별과 튜닝 가이드 제공.\n배달의민족(2022~2024): 주문·결제 회귀 테스트 운영. 장애 예방 시나리오 확대.\n카카오뱅크(2020~2022): 모바일 앱 회귀 테스트 자동화. 배포 전 검증 리드타임 단축.\n\n[경력]\n사내 QA 조직에서 자동화 프레임워크와 테스트 리포팅 체계를 구축했다.",
    ),
    EngineerProfile(
        engineer_id="qa-003",
        grade="SENIOR",
        status="AVAILABLE",
        engineer_role="QA",
        employment_type="FULL_TIME",
        capability_text="Cypress / TypeScript / GitHub Actions / Jira / BrowserStack / Postman\n\n없음",
        experience_text="[소개]\n8년차 품질관리 엔지니어. 요구사항 분석부터 테스트 케이스 설계, 결함 관리까지 주도한 QA 엔지니어.\n\n[프로젝트 경험]\n안랩(2024~2025): 보안 솔루션 품질 검증. 결함 재현율 향상과 케이스 표준화.\n쿠팡(2022~2024): 정산 시스템 API 테스트. 계산 로직 검증 체계 정비.\n라인(2020~2022): 글로벌 메신저 부하 테스트. 병목 구간 식별과 튜닝 가이드 제공.\n\n[경력]\n애자일 조직에서 개발자와 함께 요구사항 단계부터 품질 기준을 정의했다.",
    ),
    EngineerProfile(
        engineer_id="qa-004",
        grade="SENIOR",
        status="AVAILABLE",
        engineer_role="QA",
        employment_type="FULL_TIME",
        capability_text="Postman / Newman / k6 / SQL / Slack / Confluence\n\nISTQB CTFL",
        experience_text="[소개]\n8년차 성능 테스트 엔지니어. 개발 조직과 긴밀히 협업하며 품질 게이트를 정착시켜 온 QA 엔지니어.\n\n[프로젝트 경험]\n토스증권(2024~2025): 주식 거래 앱 E2E 테스트 구축. 핵심 거래 시나리오 자동화.\n현대카드(2022~2024): 결제 단말 연계 검증. 릴리즈 체크리스트 표준화.\n안랩(2020~2022): 보안 솔루션 품질 검증. 결함 재현율 향상과 케이스 표준화.\n\n[경력]\n운영 이슈 분석을 통해 테스트 범위와 회귀 시나리오를 지속적으로 보완했다.",
    ),
    EngineerProfile(
        engineer_id="qa-005",
        grade="SENIOR",
        status="AVAILABLE",
        engineer_role="QA",
        employment_type="FULL_TIME",
        capability_text="Appium / Java / Rest Assured / Jenkins / Jira / TestRail\n\n정보처리기사",
        experience_text="[소개]\n8년차 QA 엔지니어. 테스트 자동화와 릴리즈 품질 관리 경험이 풍부한 QA 엔지니어.\n\n[프로젝트 경험]\n배달의민족(2024~2025): 주문·결제 회귀 테스트 운영. 장애 예방 시나리오 확대.\n카카오뱅크(2022~2024): 모바일 앱 회귀 테스트 자동화. 배포 전 검증 리드타임 단축.\n토스증권(2020~2022): 주식 거래 앱 E2E 테스트 구축. 핵심 거래 시나리오 자동화.\n\n[경력]\nSI 프로젝트에서 수동 테스트와 결함 관리를 담당하며 QA 기본기를 다졌다.",
    ),
    EngineerProfile(
        engineer_id="qa-006",
        grade="INTERMEDIATE",
        status="AVAILABLE",
        engineer_role="QA",
        employment_type="FULL_TIME",
        capability_text="Selenium / Appium / JMeter / Jira / Confluence / TestRail\n\nISTQB CTFL",
        experience_text="[소개]\n5년차 테스트 자동화 엔지니어. 금융, 커머스, 모바일 앱 품질 검증과 성능 테스트를 수행한 QA 엔지니어.\n\n[프로젝트 경험]\n쿠팡(2024~2025): 정산 시스템 API 테스트. 계산 로직 검증 체계 정비.\n라인(2022~2024): 글로벌 메신저 부하 테스트. 병목 구간 식별과 튜닝 가이드 제공.\n배달의민족(2020~2022): 주문·결제 회귀 테스트 운영. 장애 예방 시나리오 확대.\n\n[경력]\n사내 QA 조직에서 자동화 프레임워크와 테스트 리포팅 체계를 구축했다.",
    ),
    EngineerProfile(
        engineer_id="qa-007",
        grade="INTERMEDIATE",
        status="AVAILABLE",
        engineer_role="QA",
        employment_type="FULL_TIME",
        capability_text="Playwright / Python / Jenkins / Allure / PostgreSQL / Grafana\n\nSQLD",
        experience_text="[소개]\n5년차 품질관리 엔지니어. 요구사항 분석부터 테스트 케이스 설계, 결함 관리까지 주도한 QA 엔지니어.\n\n[프로젝트 경험]\n현대카드(2024~2025): 결제 단말 연계 검증. 릴리즈 체크리스트 표준화.\n안랩(2022~2024): 보안 솔루션 품질 검증. 결함 재현율 향상과 케이스 표준화.\n쿠팡(2020~2022): 정산 시스템 API 테스트. 계산 로직 검증 체계 정비.\n\n[경력]\n애자일 조직에서 개발자와 함께 요구사항 단계부터 품질 기준을 정의했다.",
    ),
    EngineerProfile(
        engineer_id="qa-008",
        grade="INTERMEDIATE",
        status="AVAILABLE",
        engineer_role="QA",
        employment_type="FULL_TIME",
        capability_text="Cypress / TypeScript / GitHub Actions / Jira / BrowserStack / Postman\n\n없음",
        experience_text="[소개]\n5년차 성능 테스트 엔지니어. 개발 조직과 긴밀히 협업하며 품질 게이트를 정착시켜 온 QA 엔지니어.\n\n[프로젝트 경험]\n카카오뱅크(2024~2025): 모바일 앱 회귀 테스트 자동화. 배포 전 검증 리드타임 단축.\n토스증권(2022~2024): 주식 거래 앱 E2E 테스트 구축. 핵심 거래 시나리오 자동화.\n현대카드(2020~2022): 결제 단말 연계 검증. 릴리즈 체크리스트 표준화.\n\n[경력]\n운영 이슈 분석을 통해 테스트 범위와 회귀 시나리오를 지속적으로 보완했다.",
    ),
    EngineerProfile(
        engineer_id="qa-009",
        grade="JUNIOR",
        status="AVAILABLE",
        engineer_role="QA",
        employment_type="FREELANCER",
        capability_text="Postman / Newman / k6 / SQL / Slack / Confluence\n\nISTQB CTFL",
        experience_text="[소개]\n2년차 QA 엔지니어. 테스트 자동화와 릴리즈 품질 관리 경험이 풍부한 QA 엔지니어.\n\n[프로젝트 경험]\n라인(2024~2025): 글로벌 메신저 부하 테스트. 병목 구간 식별과 튜닝 가이드 제공.\n배달의민족(2022~2024): 주문·결제 회귀 테스트 운영. 장애 예방 시나리오 확대.\n카카오뱅크(2020~2022): 모바일 앱 회귀 테스트 자동화. 배포 전 검증 리드타임 단축.\n\n[경력]\nSI 프로젝트에서 수동 테스트와 결함 관리를 담당하며 QA 기본기를 다졌다.",
    ),
    EngineerProfile(
        engineer_id="qa-010",
        grade="JUNIOR",
        status="AVAILABLE",
        engineer_role="QA",
        employment_type="FREELANCER",
        capability_text="Appium / Java / Rest Assured / Jenkins / Jira / TestRail\n\n정보처리기사",
        experience_text="[소개]\n2년차 테스트 자동화 엔지니어. 금융, 커머스, 모바일 앱 품질 검증과 성능 테스트를 수행한 QA 엔지니어.\n\n[프로젝트 경험]\n안랩(2024~2025): 보안 솔루션 품질 검증. 결함 재현율 향상과 케이스 표준화.\n쿠팡(2022~2024): 정산 시스템 API 테스트. 계산 로직 검증 체계 정비.\n라인(2020~2022): 글로벌 메신저 부하 테스트. 병목 구간 식별과 튜닝 가이드 제공.\n\n[경력]\n사내 QA 조직에서 자동화 프레임워크와 테스트 리포팅 체계를 구축했다.",
    ),
    EngineerProfile(
        engineer_id="pln-001",
        grade="EXPERT",
        status="AVAILABLE",
        engineer_role="PLANNER",
        employment_type="FULL_TIME",
        capability_text="Confluence / Notion / Jira / GA4 / SQL / Figma\n\nSQLD",
        experience_text="[소개]\n12년차 서비스 기획자. 데이터 기반으로 문제를 정의하고 서비스 흐름을 설계하는 기획자.\n\n[프로젝트 경험]\n당근(2024~2025): 지역 커뮤니티 피드 서비스 기획. 핵심 지표 관리와 기능 고도화.\n카카오모빌리티(2022~2024): 배차 운영 화면 개선. 운영 효율 향상.\n야놀자(2020~2022): 숙소 운영 정책 관리 기능 기획. 운영자 입력 오류 감소.\n\n[경력]\n운영 기획에서 출발해 서비스 정책과 백오피스 설계 경험을 쌓았다.",
    ),
    EngineerProfile(
        engineer_id="pln-002",
        grade="SENIOR",
        status="AVAILABLE",
        engineer_role="PLANNER",
        employment_type="FULL_TIME",
        capability_text="Amplitude / Mixpanel / Excel / Slack / PowerPoint / Notion\n\nADsP",
        experience_text="[소개]\n8년차 PM. 백오피스, 운영 도구, 고객 여정 개선 프로젝트를 이끈 서비스 기획자.\n\n[프로젝트 경험]\n직방(2024~2025): 매물 운영 백오피스 개편. 운영 프로세스 단순화.\n토스(2022~2024): 고객센터 상담 관리 기능 기획. 응답 시간 단축.\n당근(2020~2022): 지역 커뮤니티 피드 서비스 기획. 핵심 지표 관리와 기능 고도화.\n\n[경력]\n프로덕트 조직에서 데이터 분석가, 디자이너, 개발자와 협업하며 기능을 출시했다.",
    ),
    EngineerProfile(
        engineer_id="pln-003",
        grade="SENIOR",
        status="AVAILABLE",
        engineer_role="PLANNER",
        employment_type="FULL_TIME",
        capability_text="Miro / Notion / GA4 / Looker Studio / SQL / Slack\n\n없음",
        experience_text="[소개]\n8년차 프로덕트 오너. 요구사항 정리와 이해관계자 조율에 강점이 있는 PM.\n\n[프로젝트 경험]\n컬리(2024~2025): 프로모션 관리 도구 기획. 마케터 셀프서브 운영 지원.\n무신사(2022~2024): 상품 등록 프로세스 개선. 등록 오류 감소.\n직방(2020~2022): 매물 운영 백오피스 개편. 운영 프로세스 단순화.\n\n[경력]\nB2B SaaS 환경에서 고객 요구사항을 제품 기능으로 구체화한 경험이 있다.",
    ),
    EngineerProfile(
        engineer_id="pln-004",
        grade="SENIOR",
        status="AVAILABLE",
        engineer_role="PLANNER",
        employment_type="FULL_TIME",
        capability_text="Jira / Confluence / Excel / Figma / Tableau / SQL\n\nSQLD",
        experience_text="[소개]\n8년차 플랫폼 기획자. 운영 정책과 화면 기획을 함께 다룰 수 있는 실무형 기획자.\n\n[프로젝트 경험]\n카카오모빌리티(2024~2025): 배차 운영 화면 개선. 운영 효율 향상.\n야놀자(2022~2024): 숙소 운영 정책 관리 기능 기획. 운영자 입력 오류 감소.\n컬리(2020~2022): 프로모션 관리 도구 기획. 마케터 셀프서브 운영 지원.\n\n[경력]\n여러 부서의 요구사항을 조율하며 우선순위를 정리하는 역할을 맡아 왔다.",
    ),
    EngineerProfile(
        engineer_id="pln-005",
        grade="INTERMEDIATE",
        status="AVAILABLE",
        engineer_role="PLANNER",
        employment_type="FULL_TIME",
        capability_text="Confluence / Notion / Jira / GA4 / SQL / Figma\n\nSQLD",
        experience_text="[소개]\n5년차 서비스 기획자. 데이터 기반으로 문제를 정의하고 서비스 흐름을 설계하는 기획자.\n\n[프로젝트 경험]\n토스(2024~2025): 고객센터 상담 관리 기능 기획. 응답 시간 단축.\n당근(2022~2024): 지역 커뮤니티 피드 서비스 기획. 핵심 지표 관리와 기능 고도화.\n카카오모빌리티(2020~2022): 배차 운영 화면 개선. 운영 효율 향상.\n\n[경력]\n운영 기획에서 출발해 서비스 정책과 백오피스 설계 경험을 쌓았다.",
    ),
    EngineerProfile(
        engineer_id="pln-006",
        grade="INTERMEDIATE",
        status="AVAILABLE",
        engineer_role="PLANNER",
        employment_type="FULL_TIME",
        capability_text="Amplitude / Mixpanel / Excel / Slack / PowerPoint / Notion\n\nADsP",
        experience_text="[소개]\n5년차 PM. 백오피스, 운영 도구, 고객 여정 개선 프로젝트를 이끈 서비스 기획자.\n\n[프로젝트 경험]\n무신사(2024~2025): 상품 등록 프로세스 개선. 등록 오류 감소.\n직방(2022~2024): 매물 운영 백오피스 개편. 운영 프로세스 단순화.\n토스(2020~2022): 고객센터 상담 관리 기능 기획. 응답 시간 단축.\n\n[경력]\n프로덕트 조직에서 데이터 분석가, 디자이너, 개발자와 협업하며 기능을 출시했다.",
    ),
    EngineerProfile(
        engineer_id="pln-007",
        grade="INTERMEDIATE",
        status="AVAILABLE",
        engineer_role="PLANNER",
        employment_type="FREELANCER",
        capability_text="Miro / Notion / GA4 / Looker Studio / SQL / Slack\n\n없음",
        experience_text="[소개]\n5년차 프로덕트 오너. 요구사항 정리와 이해관계자 조율에 강점이 있는 PM.\n\n[프로젝트 경험]\n야놀자(2024~2025): 숙소 운영 정책 관리 기능 기획. 운영자 입력 오류 감소.\n컬리(2022~2024): 프로모션 관리 도구 기획. 마케터 셀프서브 운영 지원.\n무신사(2020~2022): 상품 등록 프로세스 개선. 등록 오류 감소.\n\n[경력]\nB2B SaaS 환경에서 고객 요구사항을 제품 기능으로 구체화한 경험이 있다.",
    ),
    EngineerProfile(
        engineer_id="pln-008",
        grade="JUNIOR",
        status="AVAILABLE",
        engineer_role="PLANNER",
        employment_type="FREELANCER",
        capability_text="Jira / Confluence / Excel / Figma / Tableau / SQL\n\nSQLD",
        experience_text="[소개]\n2년차 플랫폼 기획자. 운영 정책과 화면 기획을 함께 다룰 수 있는 실무형 기획자.\n\n[프로젝트 경험]\n당근(2024~2025): 지역 커뮤니티 피드 서비스 기획. 핵심 지표 관리와 기능 고도화.\n카카오모빌리티(2022~2024): 배차 운영 화면 개선. 운영 효율 향상.\n야놀자(2020~2022): 숙소 운영 정책 관리 기능 기획. 운영자 입력 오류 감소.\n\n[경력]\n여러 부서의 요구사항을 조율하며 우선순위를 정리하는 역할을 맡아 왔다.",
    ),
    EngineerProfile(
        engineer_id="pub-001",
        grade="SENIOR",
        status="AVAILABLE",
        engineer_role="PUBLISHER",
        employment_type="FULL_TIME",
        capability_text="HTML5 / CSS3 / SCSS / JavaScript / jQuery / 웹 접근성\n\n웹디자인기능사",
        experience_text="[소개]\n8년차 웹 퍼블리셔. 반응형 웹 구축과 웹 접근성 대응 경험이 풍부한 퍼블리셔.\n\n[프로젝트 경험]\n아모레퍼시픽(2024~2025): 공식 온라인몰 반응형 웹 리뉴얼. 웹 접근성 인증 대응.\n현대백화점(2022~2024): 브랜드 캠페인 사이트 제작. 크로스브라우징 품질 확보.\n신세계인터내셔날(2020~2022): 시즌 캠페인 사이트 구축. 디바이스 대응 범위 확대.\n\n[경력]\n에이전시에서 다양한 산업군의 웹사이트 구축과 운영을 담당했다.",
    ),
    EngineerProfile(
        engineer_id="pub-002",
        grade="SENIOR",
        status="AVAILABLE",
        engineer_role="PUBLISHER",
        employment_type="FULL_TIME",
        capability_text="HTML5 / CSS3 / Tailwind CSS / Alpine.js / Figma / 접근성 진단\n\nGTQ 1급",
        experience_text="[소개]\n8년차 퍼블리셔. 디자인 시안을 정교하게 구현하고 운영 효율을 높이는 퍼블리셔.\n\n[프로젝트 경험]\n무신사(2024~2025): 프로모션 페이지 퍼블리싱. 반복 제작 가능한 템플릿화.\n롯데ON(2022~2024): 기획전 랜딩 페이지 운영. 배포 리드타임 단축.\n아모레퍼시픽(2020~2022): 공식 온라인몰 반응형 웹 리뉴얼. 웹 접근성 인증 대응.\n\n[경력]\n인하우스 커머스 조직에서 디자인 시스템 기반 퍼블리싱을 수행했다.",
    ),
    EngineerProfile(
        engineer_id="pub-003",
        grade="SENIOR",
        status="AVAILABLE",
        engineer_role="PUBLISHER",
        employment_type="FULL_TIME",
        capability_text="HTML5 / SCSS / Gulp / Swiper / Cross Browsing / 웹 표준\n\n없음",
        experience_text="[소개]\n8년차 반응형 웹 퍼블리셔. 이벤트 페이지, 브랜드 사이트, 커머스 프론트 퍼블리싱 경험이 많은 퍼블리셔.\n\n[프로젝트 경험]\nCJ ENM(2024~2025): 콘텐츠 이벤트 페이지 구축. 모바일 인터랙션 최적화.\n올리브영(2022~2024): 브랜드전 페이지 퍼블리싱. 운영 생산성 향상.\n무신사(2020~2022): 프로모션 페이지 퍼블리싱. 반복 제작 가능한 템플릿화.\n\n[경력]\n웹 표준과 접근성 가이드를 정비하며 팀 내 품질 기준을 수립했다.",
    ),
    EngineerProfile(
        engineer_id="pub-004",
        grade="INTERMEDIATE",
        status="AVAILABLE",
        engineer_role="PUBLISHER",
        employment_type="FULL_TIME",
        capability_text="HTML5 / CSS Modules / Storybook / 웹 접근성 / 디자인 시스템\n\n웹디자인기능사",
        experience_text="[소개]\n5년차 UI 퍼블리셔. 디자인 시스템과 컴포넌트 기반 퍼블리싱에 익숙한 퍼블리셔.\n\n[프로젝트 경험]\n현대백화점(2024~2025): 브랜드 캠페인 사이트 제작. 크로스브라우징 품질 확보.\n신세계인터내셔날(2022~2024): 시즌 캠페인 사이트 구축. 디바이스 대응 범위 확대.\nCJ ENM(2020~2022): 콘텐츠 이벤트 페이지 구축. 모바일 인터랙션 최적화.\n\n[경력]\n디자이너와 개발자 사이에서 구현 기준을 맞추는 역할을 지속적으로 맡아 왔다.",
    ),
    EngineerProfile(
        engineer_id="pub-005",
        grade="INTERMEDIATE",
        status="AVAILABLE",
        engineer_role="PUBLISHER",
        employment_type="FULL_TIME",
        capability_text="HTML5 / CSS3 / JavaScript / GSAP / SVG / 웹 접근성\n\nGTQ 1급",
        experience_text="[소개]\n5년차 웹 퍼블리셔. 반응형 웹 구축과 웹 접근성 대응 경험이 풍부한 퍼블리셔.\n\n[프로젝트 경험]\n롯데ON(2024~2025): 기획전 랜딩 페이지 운영. 배포 리드타임 단축.\n아모레퍼시픽(2022~2024): 공식 온라인몰 반응형 웹 리뉴얼. 웹 접근성 인증 대응.\n현대백화점(2020~2022): 브랜드 캠페인 사이트 제작. 크로스브라우징 품질 확보.\n\n[경력]\n에이전시에서 다양한 산업군의 웹사이트 구축과 운영을 담당했다.",
    ),
    EngineerProfile(
        engineer_id="pub-006",
        grade="INTERMEDIATE",
        status="AVAILABLE",
        engineer_role="PUBLISHER",
        employment_type="FULL_TIME",
        capability_text="HTML5 / CSS3 / SCSS / JavaScript / jQuery / 웹 접근성\n\n웹디자인기능사",
        experience_text="[소개]\n5년차 퍼블리셔. 디자인 시안을 정교하게 구현하고 운영 효율을 높이는 퍼블리셔.\n\n[프로젝트 경험]\n올리브영(2024~2025): 브랜드전 페이지 퍼블리싱. 운영 생산성 향상.\n무신사(2022~2024): 프로모션 페이지 퍼블리싱. 반복 제작 가능한 템플릿화.\n롯데ON(2020~2022): 기획전 랜딩 페이지 운영. 배포 리드타임 단축.\n\n[경력]\n인하우스 커머스 조직에서 디자인 시스템 기반 퍼블리싱을 수행했다.",
    ),
    EngineerProfile(
        engineer_id="pub-007",
        grade="INTERMEDIATE",
        status="AVAILABLE",
        engineer_role="PUBLISHER",
        employment_type="FULL_TIME",
        capability_text="HTML5 / CSS3 / Tailwind CSS / Alpine.js / Figma / 접근성 진단\n\nGTQ 1급",
        experience_text="[소개]\n5년차 반응형 웹 퍼블리셔. 이벤트 페이지, 브랜드 사이트, 커머스 프론트 퍼블리싱 경험이 많은 퍼블리셔.\n\n[프로젝트 경험]\n신세계인터내셔날(2024~2025): 시즌 캠페인 사이트 구축. 디바이스 대응 범위 확대.\nCJ ENM(2022~2024): 콘텐츠 이벤트 페이지 구축. 모바일 인터랙션 최적화.\n올리브영(2020~2022): 브랜드전 페이지 퍼블리싱. 운영 생산성 향상.\n\n[경력]\n웹 표준과 접근성 가이드를 정비하며 팀 내 품질 기준을 수립했다.",
    ),
    EngineerProfile(
        engineer_id="pub-008",
        grade="INTERMEDIATE",
        status="AVAILABLE",
        engineer_role="PUBLISHER",
        employment_type="FREELANCER",
        capability_text="HTML5 / SCSS / Gulp / Swiper / Cross Browsing / 웹 표준\n\n없음",
        experience_text="[소개]\n5년차 UI 퍼블리셔. 디자인 시스템과 컴포넌트 기반 퍼블리싱에 익숙한 퍼블리셔.\n\n[프로젝트 경험]\n아모레퍼시픽(2024~2025): 공식 온라인몰 반응형 웹 리뉴얼. 웹 접근성 인증 대응.\n현대백화점(2022~2024): 브랜드 캠페인 사이트 제작. 크로스브라우징 품질 확보.\n신세계인터내셔날(2020~2022): 시즌 캠페인 사이트 구축. 디바이스 대응 범위 확대.\n\n[경력]\n디자이너와 개발자 사이에서 구현 기준을 맞추는 역할을 지속적으로 맡아 왔다.",
    ),
    EngineerProfile(
        engineer_id="pub-009",
        grade="JUNIOR",
        status="AVAILABLE",
        engineer_role="PUBLISHER",
        employment_type="FREELANCER",
        capability_text="HTML5 / CSS Modules / Storybook / 웹 접근성 / 디자인 시스템\n\n웹디자인기능사",
        experience_text="[소개]\n2년차 웹 퍼블리셔. 반응형 웹 구축과 웹 접근성 대응 경험이 풍부한 퍼블리셔.\n\n[프로젝트 경험]\n무신사(2024~2025): 프로모션 페이지 퍼블리싱. 반복 제작 가능한 템플릿화.\n롯데ON(2022~2024): 기획전 랜딩 페이지 운영. 배포 리드타임 단축.\n아모레퍼시픽(2020~2022): 공식 온라인몰 반응형 웹 리뉴얼. 웹 접근성 인증 대응.\n\n[경력]\n에이전시에서 다양한 산업군의 웹사이트 구축과 운영을 담당했다.",
    ),
    EngineerProfile(
        engineer_id="pub-010",
        grade="JUNIOR",
        status="AVAILABLE",
        engineer_role="PUBLISHER",
        employment_type="FREELANCER",
        capability_text="HTML5 / CSS3 / JavaScript / GSAP / SVG / 웹 접근성\n\nGTQ 1급",
        experience_text="[소개]\n2년차 퍼블리셔. 디자인 시안을 정교하게 구현하고 운영 효율을 높이는 퍼블리셔.\n\n[프로젝트 경험]\nCJ ENM(2024~2025): 콘텐츠 이벤트 페이지 구축. 모바일 인터랙션 최적화.\n올리브영(2022~2024): 브랜드전 페이지 퍼블리싱. 운영 생산성 향상.\n무신사(2020~2022): 프로모션 페이지 퍼블리싱. 반복 제작 가능한 템플릿화.\n\n[경력]\n인하우스 커머스 조직에서 디자인 시스템 기반 퍼블리싱을 수행했다.",
    ),
]

assert len(SAMPLE_ENGINEER_PROFILES) == 100

# ---------------------------------------------------------------------------
# 스킬 임베딩용 샘플 데이터
# skill_id 는 DB INSERT 순서와 대응 (1-based).
# embed_text = skill.name 그대로 사용 — LLM 1차 정규화 후 2차 정규화(벡터 매칭) 용도.
# ---------------------------------------------------------------------------
SAMPLE_SKILLS: list[Skill] = [
    # ── LANGUAGE ─────────────────────────────────────────────────────────────
    Skill(skill_id=1,   name="Java",           category="LANGUAGE",   embed_text="Java"),
    Skill(skill_id=2,   name="Kotlin",          category="LANGUAGE",   embed_text="Kotlin"),
    Skill(skill_id=5,   name="Python",          category="LANGUAGE",   embed_text="Python"),
    Skill(skill_id=8,   name="JavaScript",      category="LANGUAGE",   embed_text="JavaScript"),
    Skill(skill_id=9,   name="TypeScript",      category="LANGUAGE",   embed_text="TypeScript"),
    Skill(skill_id=13,  name="Go",              category="LANGUAGE",   embed_text="Go"),
    Skill(skill_id=12,  name="C#",              category="LANGUAGE",   embed_text="C#"),
    Skill(skill_id=16,  name="Swift",           category="LANGUAGE",   embed_text="Swift"),
    Skill(skill_id=15,  name="Rust",            category="LANGUAGE",   embed_text="Rust"),
    Skill(skill_id=36,  name="SQL",             category="LANGUAGE",   embed_text="SQL"),
    # ── FRAMEWORK ────────────────────────────────────────────────────────────
    Skill(skill_id=53,  name="Spring Boot",     category="FRAMEWORK",  embed_text="Spring Boot"),
    Skill(skill_id=57,  name="Spring Batch",    category="FRAMEWORK",  embed_text="Spring Batch"),
    Skill(skill_id=55,  name="Spring Security", category="FRAMEWORK",  embed_text="Spring Security"),
    Skill(skill_id=56,  name="Spring Data JPA", category="FRAMEWORK",  embed_text="Spring Data JPA"),
    Skill(skill_id=82,  name="FastAPI",         category="FRAMEWORK",  embed_text="FastAPI"),
    Skill(skill_id=81,  name="Django",          category="FRAMEWORK",  embed_text="Django"),
    Skill(skill_id=68,  name="NestJS",          category="FRAMEWORK",  embed_text="NestJS"),
    Skill(skill_id=72,  name="React",           category="FRAMEWORK",  embed_text="React"),
    Skill(skill_id=73,  name="Next.js",         category="FRAMEWORK",  embed_text="Next.js"),
    Skill(skill_id=74,  name="Vue.js",          category="FRAMEWORK",  embed_text="Vue.js"),
    Skill(skill_id=119, name="LangChain",       category="FRAMEWORK",  embed_text="LangChain"),
    Skill(skill_id=113, name="PyTorch",         category="FRAMEWORK",  embed_text="PyTorch"),
    # ── DATABASE ─────────────────────────────────────────────────────────────
    Skill(skill_id=143, name="PostgreSQL",      category="DATABASE",   embed_text="PostgreSQL"),
    Skill(skill_id=144, name="MySQL",           category="DATABASE",   embed_text="MySQL"),
    Skill(skill_id=157, name="Redis",           category="DATABASE",   embed_text="Redis"),
    Skill(skill_id=156, name="MongoDB",         category="DATABASE",   embed_text="MongoDB"),
    Skill(skill_id=158, name="Elasticsearch",   category="DATABASE",   embed_text="Elasticsearch"),
    Skill(skill_id=147, name="Oracle Database", category="DATABASE",   embed_text="Oracle Database"),
    Skill(skill_id=166, name="DynamoDB",        category="DATABASE",   embed_text="DynamoDB"),
    Skill(skill_id=173, name="Snowflake",       category="DATABASE",   embed_text="Snowflake"),
    Skill(skill_id=171, name="ClickHouse",      category="DATABASE",   embed_text="ClickHouse"),
    Skill(skill_id=179, name="Memcached",       category="DATABASE",   embed_text="Memcached"),
    # ── CLOUD ─────────────────────────────────────────────────────────────────
    Skill(skill_id=243, name="AWS",             category="CLOUD",      embed_text="AWS"),
    Skill(skill_id=246, name="Amazon EKS",      category="CLOUD",      embed_text="Amazon EKS"),
    Skill(skill_id=256, name="Amazon Lambda",   category="CLOUD",      embed_text="Amazon Lambda"),
    Skill(skill_id=247, name="Amazon S3",       category="CLOUD",      embed_text="Amazon S3"),
    Skill(skill_id=248, name="Amazon RDS",      category="CLOUD",      embed_text="Amazon RDS"),
    Skill(skill_id=285, name="Google Cloud",    category="CLOUD",      embed_text="Google Cloud"),
    Skill(skill_id=272, name="Microsoft Azure", category="CLOUD",      embed_text="Microsoft Azure"),
    Skill(skill_id=294, name="Firebase",        category="CLOUD",      embed_text="Firebase"),
    Skill(skill_id=303, name="Vercel",          category="CLOUD",      embed_text="Vercel"),
    Skill(skill_id=301, name="Cloudflare",      category="CLOUD",      embed_text="Cloudflare"),
    # ── DEVOPS ────────────────────────────────────────────────────────────────
    Skill(skill_id=307, name="Docker",          category="DEVOPS",     embed_text="Docker"),
    Skill(skill_id=311, name="Kubernetes",      category="DEVOPS",     embed_text="Kubernetes"),
    Skill(skill_id=318, name="GitHub Actions",  category="DEVOPS",     embed_text="GitHub Actions"),
    Skill(skill_id=329, name="Terraform",       category="DEVOPS",     embed_text="Terraform"),
    Skill(skill_id=314, name="Helm",            category="DEVOPS",     embed_text="Helm"),
    Skill(skill_id=316, name="Argo CD",         category="DEVOPS",     embed_text="Argo CD"),
    Skill(skill_id=335, name="Prometheus",      category="DEVOPS",     embed_text="Prometheus"),
    Skill(skill_id=336, name="Grafana",         category="DEVOPS",     embed_text="Grafana"),
    Skill(skill_id=332, name="Ansible",         category="DEVOPS",     embed_text="Ansible"),
    Skill(skill_id=317, name="Jenkins",         category="DEVOPS",     embed_text="Jenkins"),
    # ── INFRA ─────────────────────────────────────────────────────────────────
    Skill(skill_id=181, name="Linux",           category="INFRA",      embed_text="Linux"),
    Skill(skill_id=190, name="Nginx",           category="INFRA",      embed_text="Nginx"),
    Skill(skill_id=236, name="Apache Kafka",    category="INFRA",      embed_text="Apache Kafka"),
    Skill(skill_id=234, name="RabbitMQ",        category="INFRA",      embed_text="RabbitMQ"),
    Skill(skill_id=202, name="Keycloak",        category="INFRA",      embed_text="Keycloak"),
    Skill(skill_id=209, name="Vault",           category="INFRA",      embed_text="Vault"),
    Skill(skill_id=206, name="Consul",          category="INFRA",      embed_text="Consul"),
    Skill(skill_id=210, name="MinIO",           category="INFRA",      embed_text="MinIO"),
    # ── DESIGN ───────────────────────────────────────────────────────────────
    Skill(skill_id=244, name="DDD",                     category="DESIGN", embed_text="DDD"),
    Skill(skill_id=252, name="MSA",                     category="DESIGN", embed_text="MSA"),
    Skill(skill_id=249, name="Clean Architecture",      category="DESIGN", embed_text="Clean Architecture"),
    Skill(skill_id=254, name="CQRS",                    category="DESIGN", embed_text="CQRS"),
    Skill(skill_id=253, name="Event-Driven Architecture", category="DESIGN", embed_text="Event-Driven Architecture"),
    Skill(skill_id=246, name="TDD",                     category="DESIGN", embed_text="TDD"),
    Skill(skill_id=243, name="REST API Design",          category="DESIGN", embed_text="REST API Design"),
    Skill(skill_id=270, name="Design System",            category="DESIGN", embed_text="Design System"),
    # ── TOOL ──────────────────────────────────────────────────────────────────
    Skill(skill_id=372, name="Git",             category="TOOL",       embed_text="Git"),
    Skill(skill_id=378, name="Jira",            category="TOOL",       embed_text="Jira"),
    Skill(skill_id=360, name="Postman",         category="TOOL",       embed_text="Postman"),
    Skill(skill_id=362, name="Swagger",         category="TOOL",       embed_text="Swagger"),
    Skill(skill_id=396, name="SonarQube",       category="TOOL",       embed_text="SonarQube"),
    Skill(skill_id=406, name="k6",              category="TOOL",       embed_text="k6"),
    Skill(skill_id=351, name="DataGrip",        category="TOOL",       embed_text="DataGrip"),
    Skill(skill_id=383, name="Figma",           category="TOOL",       embed_text="Figma"),
    # ── OTHER ─────────────────────────────────────────────────────────────────
    Skill(skill_id=432, name="MLOps",               category="OTHER",  embed_text="MLOps"),
    Skill(skill_id=435, name="RAG",                 category="OTHER",  embed_text="RAG"),
    Skill(skill_id=430, name="ETL",                 category="OTHER",  embed_text="ETL"),
    Skill(skill_id=411, name="Agile",               category="OTHER",  embed_text="Agile"),
    Skill(skill_id=441, name="SRE",                 category="OTHER",  embed_text="SRE"),
    Skill(skill_id=420, name="Performance Tuning",  category="OTHER",  embed_text="Performance Tuning"),
    Skill(skill_id=434, name="Prompt Engineering",  category="OTHER",  embed_text="Prompt Engineering"),
    Skill(skill_id=417, name="Code Review",         category="OTHER",  embed_text="Code Review"),
]
