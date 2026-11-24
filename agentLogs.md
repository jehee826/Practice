# Agent Activity Logs

> 이 문서는 `GEMINI.md`에 따라 승인 절차 예외 대상으로 자동 기록됩니다. AI가 작성한 코드 변경 내역과 Q&A·리뷰 내역을 혼동되지 않게 섹션별로 분리하여 관리합니다.

---

## AI Code Changes

### 2026-11-24 16:20 | 프로젝트 개인지침 생성
- **대상 파일**: `practice/GEMINI.md`
- **상세 내용**: 학습 중심, 기본 읽기 전용 및 2회 승인 원칙, 모호함 확인 원칙, 주 작업공간(`practice`) 설정을 명시한 프로젝트 규칙 파일 생성.

### 2026-11-24 21:18 | FastAPI · Spring Boot 최소 Docker 환경 및 폴더 뼈대 생성
- **대상 파일/폴더**:
  - `practice/simple_fastAPI/Dockerfile`, `practice/simple_fastAPI/compose.yaml`
  - `practice/simple_SpringBoot/Dockerfile`, `practice/simple_SpringBoot/compose.yaml`
  - `practice/simple_SpringBoot/gradle/wrapper`, `src/main/java`, `src/main/resources`, `src/test/java`
- **상세 내용**:
  - FastAPI: `python:3.12-slim` 기반, `uvicorn main:app --host 0.0.0.0 --port 8000 --reload`, Windows 바인드 마운트 감지를 위한 `WATCHFILES_FORCE_POLLING=true` 설정.
  - Spring Boot: 초기 `eclipse-temurin:21-jdk` 기반 `./gradlew bootRun` 구성 및 `gradle_cache` 볼륨, 디렉터리 뼈대 생성 (`.dockerignore` 제외).

### 2026-11-24 21:49 | `/api/status` 및 Swagger UI 최소 구동 코드 구성
- **대상 파일**:
  - `practice/simple_fastAPI/requirements.txt`, `practice/simple_fastAPI/main.py`
  - `practice/simple_SpringBoot/Dockerfile`, `practice/simple_SpringBoot/compose.yaml`
  - `practice/simple_SpringBoot/settings.gradle`, `practice/simple_SpringBoot/build.gradle`
  - `practice/simple_SpringBoot/src/main/java/com/example/demo/PracticeApplication.java`, `StatusController.java`
- **상세 내용**:
  - **FastAPI**: `fastapi`, `uvicorn[standard]` 의존성 추가 및 `GET /api/status` (`{"status": "ok"}`) 엔드포인트 구현 (기본 Swagger `/docs`).
  - **Spring Boot**: 호스트 Gradle/JDK 미설치 환경에 맞춰 `Dockerfile` 베이스를 `gradle:8-jdk21` (`USER root`, `gradle bootRun --no-daemon`)로 전환하고 `compose.yaml` 캐시 경로를 `/home/gradle/.gradle`로 일치시킴. `build.gradle`에 Spring Boot `3.4.13`, Java 21 toolchain, `spring-boot-starter-web`, `springdoc-openapi-starter-webmvc-ui:2.8.6`(`/swagger-ui/index.html`), `spring-boot-devtools`를 추가하고 `PracticeApplication` 및 `GET /api/status` (`Map.of("status", "ok")`) 구현.

### 2026-11-25 00:27 | 프로젝트 개인지침(`GEMINI.md`) 개정 및 로그 체계 도입
- **대상 파일**: `practice/GEMINI.md`, `practice/agentLogs.md`
- **상세 내용**: 멘토 역할(승인 없는 완성 코드 출력 금지), 질문 시 짧은 예시 스니펫 제공, 미사여구 배제 간결 출력, `practice/agentLogs.md` 승인 예외 및 섹션 분리 자동 기록 규칙을 `GEMINI.md`에 반영하고 `agentLogs.md` 초기화.

---

## Q&A & Mentoring Logs

### 2026-11-24 21:57 | Docker 네트워크 풀 고갈(`all predefined address pools have been fully subnetted`) 원인 분석
- **질문**: `docker compose down`을 했는데 왜 서브넷 풀이 계속 차 있는지, 메모리 누수(`malloc`/`free`)와 비슷한 구조인지 질문.
- **답변 요지**: `docker ps -a` 및 `docker network inspect` 확인 결과, 과거 `archive-*` 및 `simple_fastapi-app-1` 컨테이너가 `down`이 아닌 `stop`(`Exited`) 상태로 남아 네트워크를 점유 중이었음. `stop`은 프로세스만 멈추고 네트워크를 해제하지 않지만 `down`은 컨테이너와 네트워크(`free`)를 함께 정리함을 설명.

### 2026-11-24 22:10 | Spring Boot Docker 컨테이너 실시간 컴파일 반영
- **질문**: 떠 있는 Spring Boot 컨테이너 내부에서 명령어로 컴파일만 실행해 실시간 반영할 수 있는지, 빌드 시 복사된 코드 때문에 안 되는 것은 아닌지 질문.
- **답변 요지**: `compose.yaml`의 `.:/app` 바인드 마운트로 호스트 수정 내용이 즉시 컨테이너에 공유되므로, `docker compose exec app gradle classes --no-daemon` 실행 시 `spring-boot-devtools`가 `.class` 변경을 감지해 앱만 재시작함을 안내.

### 2026-11-24 22:28 ~ 22:46 | VS Code Java/Python 실시간 오류 감지 및 Java 25 / Gradle 8.14.3 충돌 해결
- **질문**: React ESLint처럼 타이핑 시 오타를 잡는 Extension 추천, Docker 전용 사용 시 로컬 JDK 필요 여부, Python 환경 차이, Temurin 21 설치 후 `Can't use Java 25.0.4.1 and Gradle 8.14.3 to import Gradle project androi` 오류 원인.
- **답변 요지**:
  - Java는 `Extension Pack for Java`(`redhat.java`), `Spring Boot Extension Pack`, `Error Lens` 권장. Docker 실행 자체엔 로컬 JDK가 불필요하나 에디터 언어 서버 구동용으로 로컬 JDK 21(또는 `Dev Containers`) 필요. Python은 문법 엔진(`Pylance`/`Ruff`) 자체는 로컬 인터프리터 없이 동작하나 서드파티 import 검사는 가상환경 필요.
  - Temurin 21 설치 시 `Set or override JAVA_HOME variable` 활성화 필요 안내.
  - `Java 25.0.4.1` 오류는 상위 `vscode-workspace`가 열려 있어 `Personal_Archive/frontend/android`(Gradle 8.14.3)까지 스캔된 것과 VS Code Java 확장의 내장 Java 25 사용이 겹쳐 발생. `java.import.gradle.java.home`을 JDK 21로 고정하고 `simple_SpringBoot` 단독 폴더 오픈 권장. 팝업에서 `Upgrade Gradle` 버튼은 타 프로젝트 wrapper 변경 위험으로 클릭 금지 안내.

### 2026-11-24 22:51 ~ 22:56 | `.gitignore` 최소 원칙 & Container Tools Extension
- **질문**: 존재하지도 않는 `*.jar`나 중복 `*.class`를 `.gitignore`에 미리 넣은 이유 질문 및 `Container Tools` 확장 용도 질문.
- **답변 요지**: 관성적 템플릿 대신 현재 실제 존재하는 빌드 산출물(`.gradle/`, `build/`, `bin/`)만 제외해도 충분함을 인정·안내. `Container Tools`는 `Dockerfile`/`compose.yaml` 문법 검사 및 VS Code 내 컨테이너/네트워크 GUI 관리 확장임을 설명.

### 2026-11-24 23:22 ~ 00:12 | FastAPI SSE + 가짜 LLM 실습 설계 및 `APIRouter` 동작 원리
- **질문**: FastAPI `APIRouter` 사용법, `FastAPI(prefix="/api")` TypeError 원인, `app`과 `router` 관계, 상대/절대 import 기준, 전역 `/api` prefix 구성, `main.py` 위치 이동 후 `Dockerfile` 수정 여부 및 `app.include_router(api_router)` 배치 오류 점검.
- **답변 요지**:
  - `prefix`는 `FastAPI()`가 아니라 `APIRouter`/`include_router` 전용. Python 데코레이터는 Spring Boot Component Scan과 달리 자동 등록되지 않으며, `include_router`는 호출 시점의 라우트만 복사하므로 하위 라우터 → `api_router` → 맨 마지막 `app.include_router(api_router)` 순서로 조립해야 함을 설명.
  - `import`는 현재 파일 기준이 아니라 실행 작업 디렉터리(`/app`) 기준이며, 같은 폴더 참조 시 `from . import ...` 상대 임포트 가능.
  - `main.py` 루트 이동 후 `Dockerfile`의 `uvicorn main:app`과 일치하므로 `Dockerfile` 수정 불필요, `main.py` 내 잘못된 import 경로(`from api.fake_llm import fake_llm` → `from api import fake_llm`) 및 `app.include_router(api_router)` 위치 오류 지적.

### 2026-11-25 00:15 | GitHub 원격 저장소(`Practice.git`) 연결 방법
- **질문**: 새 GitHub 레포지토리를 `practice` 폴더에 연결하고 push하는 절차 질문.
- **답변 요지**: `practice/` 내 이미 `git init`이 되어 있고 `.gitignore`에 `.gradle/`, `build/`, `bin/`, `.env`가 설정되어 있음을 확인 후 `cd practice` → `git remote add origin ...` → `git branch -M main` → `git add .` → `git commit` → `git push -u origin main` 순서 안내.
