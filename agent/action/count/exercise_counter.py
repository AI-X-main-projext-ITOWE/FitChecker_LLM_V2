def exercise_counter(action_data: dict):
    sets = action_data.get("sets", 0)
    reps_per_set = action_data.get("reps_per_set", 0)
    exercise = action_data.get("exercise", "unknown")

    # Counter 처리 로직 예제 (한글 출력)
    print(f"운동 시작 - 운동 이름: {exercise}, 세트 수: {sets}, 반복 횟수: {reps_per_set}")
    
    # 한글 반환 메시지
    return [exercise, sets, reps_per_set]
