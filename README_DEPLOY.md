# Streamlit Community Cloud 배포

## GitHub 업로드 대상

`BC_Anchor_Impact_Lab_FINAL/07_app/` 전체를 업로드합니다. `data/`의 JSON 2개와 CSV 1개는 앱 실행에 필수입니다. `.gitignore`에 지정된 캐시·검증 결과 파일은 제외합니다. 배포 JSON은 분석값을 유지하고 로컬 Windows provenance 경로만 파일명으로 축약한 사본입니다.

## Community Cloud 설정

- Main file path: `BC_Anchor_Impact_Lab_FINAL/07_app/app.py`
- Python: `runtime.txt`의 Python 3.12
- 패키지: 같은 폴더의 `requirements.txt`
- Secrets: 필요 없음

저장소 루트를 `07_app`으로 올리는 경우 Main file path는 `app.py`입니다.

## 배포 후 확인

Home, 상권 탐색, 후보 분석, Anchor 9, 지역 전략, 실제 사례, 방법론의 7개 페이지와 Home 지역 선택 이동을 확인합니다.

## 데이터 보호

M1~M5 분석값, 점수, 순위, 후보, Peer, Anchor와 외부 검증 결과를 수정하거나 재계산하지 않습니다. 원본 및 배포 asset hash는 `data/`의 두 manifest로 확인합니다.
