# API 비교 도구

이 프로젝트는 기존 API와 신규 API 엔드포인트를 비교하는 도구입니다.

## 사용법

각 디렉토리의 `*_api.py` 파일을 실행하면 API 비교를 수행하고 HTML 리포트를 생성합니다.

```bash
# 예시: 메인 배너 API 비교
python home/01_main-banner/main-banner_api.py
```

## 출력

- 콘솔에 비교 결과 출력
- HTML 리포트 파일 자동 생성 (각 스크립트 실행 디렉토리에 생성됨)

## 예시 리포트

생성되는 HTML 리포트의 예시:

<img width="1061" height="1127" alt="Image" src="https://github.com/user-attachments/assets/5a83ebc9-c178-457f-a3d9-89f5c2f15cfa" />

## 디렉토리 구조

- `home/` - API 테스트 스크립트들
- `home/config/` - 도메인 설정
- `home/api_comparator.py` - API 비교 로직

각 `*_api.py` 파일은 독립적으로 실행 가능하며, 실행 시 해당 API의 비교 결과를 담은 HTML 파일이 생성됩니다.
