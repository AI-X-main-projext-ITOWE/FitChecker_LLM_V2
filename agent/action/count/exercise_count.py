async def exercise_count_action(action_data: dict) -> dict:

    sets = action_data.get("sets", 0)  
    reps_per_set = action_data.get("reps_per_set", 0) 
    total_reps = action_data.get("total_reps", sets * reps_per_set)  

    if sets == 0 or reps_per_set == 0:
        response = "운동 세트와 횟수가 제대로 설정되지 않았습니다. 다시 시도해주세요."
    else:
        response = f"운동 세트 {sets}개, 세트당 {reps_per_set}회 설정되었습니다. 총 {total_reps}회입니다."

    return {
        "response": response,
        "follow_up_needed": False,    
        }