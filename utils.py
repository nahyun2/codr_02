"""
utils.py

공통 유틸리티 함수 모음(입력 검증 등).

`read_int(prompt, min_val=None, max_val=None)`
- 입력 앞뒤 공백을 제거합니다.
- 빈 입력은 재입력을 요청합니다.
- 정수 변환 실패 시 재입력을 요청합니다.
- 범위(min_val, max_val) 밖의 입력은 재입력을 요청합니다.
- `KeyboardInterrupt`/`EOFError`는 호출자쪽에서 처리하도록 그대로 전달합니다.

예시:
    from utils import read_int
    choice = read_int("선택: ", 1, 5)

이 함수는 프로그램 전반에서 숫자 입력 검증용으로 재사용됩니다.
"""

from typing import Optional


def read_int(prompt: str, min_val: Optional[int] = None, max_val: Optional[int] = None) -> int:
    """사용자에게 정수 입력을 안전하게 받는다.

    동작:
    - 입력을 `strip()` 후 처리
    - 빈 입력: 재입력 요청
    - 정수 변환 실패: 재입력 요청
    - 범위 밖 입력: 재입력 요청

    예외:
    - 사용자가 Ctrl+C 또는 입력 스트림 종료(EOF)를 발생시키면
      해당 예외는 호출자에게 전달된다 (저장/종료 로직은 호출자가 처리).
    """
    while True:
        try:
            raw = input(prompt)
        except (KeyboardInterrupt, EOFError):
            # 호출자가 안전 종료를 담당하게 하기 위해 예외를 재발생
            raise

        if raw is None:
            print("입력이 감지되지 않았습니다. 다시 시도하세요.")
            continue

        s = raw.strip()
        if s == "":
            print("입력이 비었습니다. 값을 입력하세요.")
            continue

        try:
            val = int(s)
        except ValueError:
            print("잘못된 입력입니다. 숫자를 입력하세요.")
            continue

        if (min_val is not None and val < min_val) or (max_val is not None and val > max_val):
            if min_val is not None and max_val is not None:
                print(f"허용 범위를 벗어났습니다. {min_val}~{max_val} 사이의 숫자를 입력하세요.")
            elif min_val is not None:
                print(f"{min_val} 이상의 숫자를 입력하세요.")
            else:
                print(f"{max_val} 이하의 숫자를 입력하세요.")
            continue

        return val
