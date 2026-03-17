from __future__ import annotations

from ..types import EngineerProfile

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
        현대모비스(2023~2025): ERP 재고관리 모듈 개발. Spring Batch로 야간 정산 처리 자동화. 포지션: 백엔드 리드.
        LG CNS(2021~2023): 제조업 MES 시스템 API 개발. Oracle DB 쿼리 최적화로 조회속도 40% 개선. 포지션: 백엔드 개발자.
        삼성SDS(2017~2021): 물류 ERP 시스템 개발. Spring Boot 기반 REST API 설계. 포지션: 백엔드 개발자.""",
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
        현대차(2024~2025): 딜러 관리 포털 백엔드 개발. JWT 인증 모듈 구현. 포지션: 백엔드 개발자.
        SK하이닉스(2022~2024): 생산 관리 시스템 API 개발. Kafka 기반 이벤트 처리. 포지션: 백엔드 개발자.
        스타트업(2020~2022): 쇼핑몰 주문 시스템 개발. 포지션: 풀스택 개발자.""",
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
        기아차(2024~2025): 판매 통계 대시보드 개발. Recharts 기반 실시간 차트 구현. 포지션: 프론트 리드.
        현대카드(2022~2024): 결제 현황 모니터링 화면 개발. 포지션: 프론트엔드 개발자.
        NHN(2019~2022): 어드민 포털 React 전환. 포지션: 프론트엔드 개발자.""",
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
        포스코(2024~2025): 생산 현황 모니터링 대시보드 개발. Chart.js 활용. 포지션: 프론트엔드 개발자.
        네이버(2022~2024): 광고 성과 리포트 화면 개발. 포지션: 프론트엔드 개발자.
        에이전시(2021~2022): 다수 기업 웹사이트 퍼블리싱. 포지션: 퍼블리셔.""",
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
        테크 스타트업(2021~2022): 실시간 채팅 서버 구축. 포지션: 백엔드 개발자.""",
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
        웹 에이전시(2020~2022): 다수의 브랜드 사이트 구축 및 유지보수. 포지션: 시니어 퍼블리셔.""",
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
        안랩(2018~2021): 보안 소프트웨어 수동 및 자동화 테스트 진행. 포지션: QA 리드.""",
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
        디자인 스튜디오(2019~2022): 브랜드 아이덴티티(BI) 및 앱 디자인 프로젝트 참여. 포지션: 메인 디자이너.""",
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
        이커머스 기업(2016~2020): 주문/결제 서비스 운영 기획. 포지션: PM.""",
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
# ---------------------------------------------------------------------------
SAMPLE_ENGINEER_PROFILES: list[EngineerProfile] = [
    EngineerProfile(
        engineer_id="eng-001",
        grade="SENIOR",
        status="AVAILABLE",
        engineer_role="DEVELOPER",
        employment_type="FULL_TIME",
        capability_text=(
            "Java / Spring Boot / Spring Batch / PostgreSQL / Redis / Docker\n"
            "\n"
            "정보처리기사"
        ),
        experience_text=(
            "[소개]\n"
            "MSA 아키텍처 기반 백엔드 전문. 제조업/물류 도메인 경험 다수.\n"
            "\n"
            "[프로젝트 경험]\n"
            "현대모비스(2023~2025): ERP 재고관리 모듈 개발. Spring Batch로 야간 정산 처리 자동화. 포지션: 백엔드 리드.\n"
            "LG CNS(2021~2023): 제조업 MES 시스템 API 개발. Oracle DB 쿼리 최적화로 조회속도 40% 개선. 포지션: 백엔드 개발자.\n"
            "삼성SDS(2017~2021): 물류 ERP 시스템 개발. Spring Boot 기반 REST API 설계. 포지션: 백엔드 개발자.\n"
            "\n"
            "[경력]\n"
            "현대오토에버(2015~2017): 백엔드 개발자. ERP 연동 API 개발."
        ),
    ),
    EngineerProfile(
        engineer_id="eng-002",
        grade="INTERMEDIATE",
        status="AVAILABLE",
        engineer_role="DEVELOPER",
        employment_type="FULL_TIME",
        capability_text=(
            "Java / Spring Boot / Spring Security / MySQL / Kafka / AWS"
        ),
        experience_text=(
            "[소개]\n"
            "자동차/반도체 제조 도메인 백엔드 개발. 이벤트 기반 아키텍처 경험.\n"
            "\n"
            "[프로젝트 경험]\n"
            "현대차(2024~2025): 딜러 관리 포털 백엔드 개발. JWT 인증 모듈 구현. 포지션: 백엔드 개발자.\n"
            "SK하이닉스(2022~2024): 생산 관리 시스템 API 개발. Kafka 기반 이벤트 처리. 포지션: 백엔드 개발자.\n"
            "스타트업(2020~2022): 쇼핑몰 주문 시스템 개발. 포지션: 풀스택 개발자."
        ),
    ),
    EngineerProfile(
        engineer_id="eng-003",
        grade="SENIOR",
        status="AVAILABLE",
        engineer_role="DEVELOPER",
        employment_type="FULL_TIME",
        capability_text=(
            "React / TypeScript / Redux / Recharts / Figma / Storybook"
        ),
        experience_text=(
            "[소개]\n"
            "자동차/금융 도메인 프론트엔드 전문. 대시보드 및 데이터 시각화 경험 풍부.\n"
            "\n"
            "[프로젝트 경험]\n"
            "기아차(2024~2025): 판매 통계 대시보드 개발. Recharts 기반 실시간 차트 구현. 포지션: 프론트 리드.\n"
            "현대카드(2022~2024): 결제 현황 모니터링 화면 개발. 포지션: 프론트엔드 개발자.\n"
            "NHN(2019~2022): 어드민 포털 React 전환. 포지션: 프론트엔드 개발자."
        ),
    ),
    EngineerProfile(
        engineer_id="eng-004",
        grade="INTERMEDIATE",
        status="AVAILABLE",
        engineer_role="DEVELOPER",
        employment_type="FREELANCER",
        capability_text=(
            "React / JavaScript / Vue.js / Chart.js / CSS / Webpack"
        ),
        experience_text=(
            "[소개]\n"
            "제조/광고 도메인 프론트엔드 개발. 차트 기반 대시보드 경험.\n"
            "\n"
            "[프로젝트 경험]\n"
            "포스코(2024~2025): 생산 현황 모니터링 대시보드 개발. Chart.js 활용. 포지션: 프론트엔드 개발자.\n"
            "네이버(2022~2024): 광고 성과 리포트 화면 개발. 포지션: 프론트엔드 개발자.\n"
            "에이전시(2021~2022): 다수 기업 웹사이트 퍼블리싱. 포지션: 퍼블리셔."
        ),
    ),
    EngineerProfile(
        engineer_id="eng-005",
        grade="INTERMEDIATE",
        status="AVAILABLE",
        engineer_role="DEVELOPER",
        employment_type="FULL_TIME",
        capability_text=(
            "Python / FastAPI / MongoDB / Docker / Kubernetes / Celery"
        ),
        experience_text=(
            "[소개]\n"
            "물류/이커머스 도메인 백엔드 개발. MSA 및 컨테이너 오케스트레이션 경험.\n"
            "\n"
            "[프로젝트 경험]\n"
            "쿠팡(2024~2025): 물류 최적화 알고리즘 서버 API 개발. FastAPI 기반 고성능 처리. 포지션: 백엔드 개발자.\n"
            "배달의민족(2022~2024): 주문 관리 시스템 유지보수. MSA 환경에서 서비스 간 통신 최적화. 포지션: 백엔드 개발자.\n"
            "테크 스타트업(2021~2022): 실시간 채팅 서버 구축. 포지션: 백엔드 개발자."
        ),
    ),
    EngineerProfile(
        engineer_id="pub-001",
        grade="INTERMEDIATE",
        status="AVAILABLE",
        engineer_role="PUBLISHER",
        employment_type="FULL_TIME",
        capability_text=(
            "HTML5 / CSS3 / SCSS / jQuery / Gulp / Cross Browsing / 웹 접근성"
        ),
        experience_text=(
            "[소개]\n"
            "반응형 웹 퍼블리싱 전문. 웹 접근성(WA) 인증 경험.\n"
            "\n"
            "[프로젝트 경험]\n"
            "아모레퍼시픽(2024~2025): 공식 온라인몰 반응형 웹 리뉴얼. 웹 접근성(WA) 인증 획득. 포지션: 시니어 퍼블리셔.\n"
            "무신사(2022~2024): 프로모션 페이지 제작 및 이벤트 인터랙션 구현. 포지션: 퍼블리셔.\n"
            "웹 에이전시(2020~2022): 다수의 브랜드 사이트 구축 및 유지보수. 포지션: 시니어 퍼블리셔."
        ),
    ),
    EngineerProfile(
        engineer_id="qa-001",
        grade="SENIOR",
        status="AVAILABLE",
        engineer_role="QA",
        employment_type="FULL_TIME",
        capability_text=(
            "Selenium / Appium / JMeter / Jira / Confluence / TestRail"
        ),
        experience_text=(
            "[소개]\n"
            "금융/보안 도메인 QA 전문. 테스트 자동화 및 성능 테스트 경험 풍부.\n"
            "\n"
            "[프로젝트 경험]\n"
            "카카오뱅크(2023~2025): 모바일 앱 기능 테스트 및 자동화 스크립트 작성. 안정성 99% 달성. 포지션: QA 리드.\n"
            "라인(2021~2023): 글로벌 메신저 부하 테스트 진행. 성능 병목 구간 탐색 및 리포트. 포지션: QA 엔지니어.\n"
            "안랩(2018~2021): 보안 소프트웨어 수동 및 자동화 테스트 진행. 포지션: QA 리드."
        ),
    ),
    EngineerProfile(
        engineer_id="des-001",
        grade="SENIOR",
        status="AVAILABLE",
        engineer_role="DESIGNER",
        employment_type="FREELANCER",
        capability_text=(
            "Figma / Adobe XD / Photoshop / Illustrator / Protopie / Zeplin"
        ),
        experience_text=(
            "[소개]\n"
            "핀테크/여행 도메인 UX/UI 전문. 디자인 시스템 구축 경험.\n"
            "\n"
            "[프로젝트 경험]\n"
            "토스(2024~2025): 신규 금융 상품 가입 프로세스 UX 개선. 전환율 15% 상승. 포지션: UX 디자이너.\n"
            "야놀자(2022~2024): 숙박 예약 화면 UI 컴포넌트 시스템 구축 및 가이드라인 제정. 포지션: UI 디자이너.\n"
            "디자인 스튜디오(2019~2022): 브랜드 아이덴티티(BI) 및 앱 디자인 프로젝트 참여. 포지션: 메인 디자이너."
        ),
    ),
    EngineerProfile(
        engineer_id="pln-001",
        grade="SENIOR",
        status="AVAILABLE",
        engineer_role="PLANNER",
        employment_type="FULL_TIME",
        capability_text=(
            "Confluence / Slack / Notion / GA4 / SQL / Mixpanel"
        ),
        experience_text=(
            "[소개]\n"
            "이커머스/부동산 도메인 서비스 기획 전문. 데이터 기반 의사결정 경험.\n"
            "\n"
            "[프로젝트 경험]\n"
            "당근마켓(2023~2025): 지역 커뮤니티 신규 피드 서비스 기획 및 런칭. MAU 20% 증대. 포지션: PM.\n"
            "직방(2020~2023): 부동산 매물 관리 시스템 백오피스 기획 및 프로세스 자동화. 포지션: 서비스 기획자.\n"
            "이커머스 기업(2016~2020): 주문/결제 서비스 운영 기획. 포지션: PM."
        ),
    ),
]
