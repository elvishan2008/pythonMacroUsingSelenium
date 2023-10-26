# Selenium을 활용한 매크로 프로젝트

이 프로젝트는 Selenium을 활용하여 다양한 웹사이트의 매크로를 실행하는 것을 목표로 합니다.

## 주요 기능

1. **반응 속도 테스트 매크로 (`run_ex1` 함수)**
    - 특정 웹 페이지에 접속하여 버튼을 빠르게 클릭하는 테스트를 수행합니다.

2. **스도쿠 자동 풀이 매크로 (`run_ex2` 함수)**
    - 스도쿠 문제를 자동으로 푸는 테스트를 수행합니다.
    - 문제 및 정답 데이터는 API를 통해 획득합니다.

3. **메인 매크로 실행 (`run_main` 함수)**
    - 웹 페이지 내에서 네이버 예약을 자동화하여 실행합니다.

## 사용한 라이브러리 및 도구

이 프로젝트를 사용하기 전에 다음 도구 및 라이브러리가 필요합니다:

- Python 3
- Chrome Browser
- ChromeDriver (compatible with your Chrome Browser version)
- browsermob-proxy
- 필요한 Python 라이브러리들 (예: selenium, browsermobproxy, requests 등)

#### ChromeDriver 설치

1. 먼저, 본인의 Chrome 브라우저 버전을 확인합니다. (`chrome://version`에 접속)
2. [ChromeDriver 다운로드 페이지](https://sites.google.com/a/chromium.org/chromedriver/downloads)에서 해당 버전에 맞는 ChromeDriver를 다운로드합니다.
3. 다운로드한 파일을 적절한 위치에 압축 해제합니다. (예: `C:/Program Files/Google/Chrome/Application/`)

#### browsermob-proxy 설치

1. [browsermob-proxy 공식 다운로드 페이지](https://github.com/lightbody/browsermob-proxy/releases)에서 최신 버전의 browsermob-proxy를 다운로드합니다.
2. 다운로드한 파일을 적절한 위치에 압축 해제합니다. (예: `C:/Program Files/browsermob-proxy-2.1.4/`)

#### Python 라이브러리 설치

다음의 명령어를 통해 필요한 Python 라이브러리를 설치합니다:

```bash
pip install selenium browsermobproxy requests webdriver-manager
```

## 사용법

1. `driver_path` 변수를 본인의 chromedriver 경로에 맞게 설정합니다.
2. 필요한 라이브러리 및 도구를 설치합니다.
3. 주석 처리된 `run_ex1`, `run_ex2` 또는 `run_main` 함수 중 원하는 함수를 주석 해제하고 실행합니다.


