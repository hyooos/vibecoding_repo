# 계산기 예제 프로젝트

## 프로젝트 개요

이 프로젝트는 파이썬으로 만든 간단한 계산기 예제입니다.
`src/calculator.py`에 사칙연산 함수가 들어 있고, `src/main.py`에서 이를 실행합니다.
또한 `tests/test_calculator.py`에서 각 기능이 정상 동작하는지 테스트합니다.

## 폴더 구조

```text
codex-readme-demo/
├── AGENTS.md
├── README.md
├── requirements.txt
├── src/
│   ├── __init__.py
│   ├── calculator.py
│   └── main.py
└── tests/
    ├── __init__.py
    └── test_calculator.py
```

- `src/calculator.py`: 계산 함수를 모아 둔 파일
- `src/main.py`: 계산 함수를 실행하는 파일
- `tests/test_calculator.py`: 테스트 파일
- `requirements.txt`: 필요한 패키지 목록

## 설치 방법

1. 프로젝트 폴더로 이동합니다.

```bash
cd /Users/subin/Desktop/Bitamin/세션/세션27주차/codex-readme-demo
```

2. 가상환경을 생성합니다.

```bash
python3 -m venv .venv
```

3. 가상환경을 활성화합니다.

```bash
source .venv/bin/activate
```

4. 필요한 패키지를 설치합니다.

```bash
pip install -r requirements.txt
```

## 실행 방법

아래 명령어로 프로그램을 실행합니다.

```bash
python3 -m src.main
```

실행하면 사칙연산 예제가 출력됩니다.

## 테스트 방법

아래 명령어로 테스트를 실행합니다.

```bash
pytest -q
```

현재 테스트는 모두 통과하며, 결과는 `5 passed`입니다.

## 주요 함수 설명

### `add(a, b)`

두 수를 더합니다.

```python
add(2, 3)  # 5
```

### `subtract(a, b)`

첫 번째 수에서 두 번째 수를 뺍니다.

```python
subtract(5, 2)  # 3
```

### `multiply(a, b)`

두 수를 곱합니다.

```python
multiply(4, 6)  # 24
```

### `divide(a, b)`

첫 번째 수를 두 번째 수로 나눕니다.
단, 두 번째 수가 0이면 `ValueError`가 발생합니다.

```python
divide(8, 2)   # 4.0
divide(10, 0)  # ValueError
```
