# BC Anchor Impact Lab Frontend

확정된 M1~M5 결과를 심사·시연 환경에서 탐색하는 Streamlit presentation layer입니다. 앱은 분석을 다시 계산하거나 후보·순위·포트폴리오를 변경하지 않습니다.

## 설치와 실행

```powershell
cd BC_Anchor_Impact_Lab_FINAL/07_app
pip install -r requirements.txt
streamlit run app.py
```

프로젝트 루트에서는 다음과 같이 실행할 수 있습니다.

```powershell
streamlit run BC_Anchor_Impact_Lab_FINAL/07_app/app.py
```

## 공식 데이터

앱의 배포용 데이터 소스는 앱 내부 `data/`입니다. 원본 `../03_frontend/`의 아래 세 파일을 복사한 뒤, GitHub에 로컬 사용자 경로가 노출되지 않도록 JSON의 Windows 절대경로형 provenance 문자열만 파일명으로 축약했습니다. 분석값·후보·점수·순위는 변경하지 않았습니다. 원본과 배포본 SHA256은 각각 `source_asset_hashes.json`, `asset_hashes.json`에 기록했습니다.

- `frontend_core.json`: Home, 핵심 Anchor 9, 지역별 처방, 실제 사례, 방법론
- `frontend_data.json`: 255개 지역과 460개 공식 후보 탐색, 핵심 후보의 M2 저장값 연결
- `M2_AXIS_MAPPING.csv`: M2 6축 표시명·저장 변수·해석

경로는 `app.py` 위치를 기준으로 `pathlib.Path`로 계산하며 상위 폴더나 로컬 Windows 경로에 의존하지 않습니다. 지도 좌표가 공식 데이터에 없어 Peer Group 분포와 지역 검색 UI를 사용합니다.

## 화면

1. **Home** — 핵심 질문, 주요 숫자, M1~M5 흐름
2. **전국 상권 탐색** — 시도·시군구·Peer Group별 255개 지역 탐색
3. **후보 분석** — 460개 공식 후보 필터와 저장 결과 비교
4. **핵심 Anchor 9** — 핵심 후보 카드와 M1~M5 상세 스토리
5. **지역별 처방** — Anchor, Linkage 3, Protection 1 및 실행안
6. **실제 사례 검증** — 외부 3개 사례의 저장 결과와 해석 주의사항
7. **방법론 및 한계** — 분석 단계, M2 6축 정의, 공식 한계

주요 화면은 사이드바 대신 일반적인 SaaS형 상단 텍스트 내비게이션으로 이동합니다. Home에서 시도·시군구를 선택하면 해당 지역 탐색으로 바로 이동합니다. 핵심 후보 상세는 왼쪽 진단, 오른쪽 지역 전략, 하단 실행 KPI를 한 작업 화면에 연결하고 평가 방법과 주의사항은 필요할 때 펼쳐봅니다.

## 검증

```powershell
python validate_app.py
python validate_ui.py
python -m py_compile app.py components/*.py utils/*.py styles.py validate_app.py
```

검증 결과는 UTF-8 BOM CSV인 `app_validation.csv`에 저장됩니다. 기존 FINAL 분석 파일은 읽기 전용으로 취급하며, 앱 자체 산출물은 `07_app/` 안에만 생성합니다.
