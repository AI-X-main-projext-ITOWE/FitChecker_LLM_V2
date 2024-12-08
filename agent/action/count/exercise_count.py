import logging

async def exercise_count(user_id: int, action_data: dict) -> dict:
    """
    운동 세트와 횟수를 처리하는 함수.
    """
    print("Received action_data:", action_data)  # 디버깅 로그 추가

    # action_data 검증 및 디폴트 값 설정
    sets = action_data.get("sets", 0)
    reps_per_set = action_data.get("reps_per_set", 0)

    if sets <= 0 or reps_per_set <= 0:
        logging.warning("Invalid sets or reps_per_set received. Defaulting to request re-entry.")
        return {
            "response": "운동 세트와 횟수가 제대로 설정되지 않았습니다. 다시 시도해주세요.",
            "follow_up_needed": True
        }

    # 총 반복 횟수 계산
    total_reps = sets * reps_per_set
    return {
        "response": f"운동 세트 {sets}개, 세트당 {reps_per_set}회 설정되었습니다. 총 {total_reps}회입니다.",
        "follow_up_needed": False
    }
