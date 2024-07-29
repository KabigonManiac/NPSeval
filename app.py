import streamlit as st
import pandas as pd

def calculate_Ej(n, N, start_week, preview_weeks, error_rates, previous_error):
    Ej = 0
    actual_start_week = 13 + start_week
    for j in range(1, n+1):
        if j < actual_start_week - preview_weeks[0]:
            o_j = previous_error
        elif j < actual_start_week - preview_weeks[1]:
            o_j = error_rates[preview_weeks[0]]
        elif j < actual_start_week:
            o_j = error_rates[preview_weeks[1]]
        else:
            o_j = 0  # 실적 발표 이후 오차율 0%
        Ej += o_j * ((n - j + 1) / N)
    return Ej

def create_comparison_table(start_week, preview_weeks, previous_error):
    error_rates = [0.05, 0.10, 0.15, 0.20, 0.25, 0.30]
    table = pd.DataFrame(index=error_rates, columns=error_rates)
    n = 26
    N = sum(range(1, 27))
    
    for i, error_n in enumerate(error_rates):
        for j, error_n_minus_1 in enumerate(error_rates):
            error_dict = {preview_weeks[0]: error_n, preview_weeks[1]: error_n_minus_1}
            Ej = calculate_Ej(n, N, start_week, preview_weeks, error_dict, previous_error)
            table.iloc[i, j] = f"{Ej:.4f}"
    
    table.index = [f"{rate:.0%}" for rate in table.index]
    table.columns = [f"{rate:.0%}" for rate in table.columns]
    return table

# Streamlit 앱 시작
st.title('연금 프리뷰 점수 계산')

# 실적 발표 시점 선택
week_options = ['1주차', '2주차', '3주차', '4주차', '5주차', '6주차']
selected_week = st.selectbox('실적 발표 시점을 선택하세요:', week_options, index=4)

# 선택된 주차를 숫자로 변환
start_week = week_options.index(selected_week) + 1

# 프리뷰 비교 시점 선택
preview_options = [f'{i}주 전' for i in range(start_week-1, 1, -1)]  # 2주 전까지만 선택 가능하도록 수정
selected_preview = st.selectbox('프리뷰 시점을 선택하세요:', preview_options, index=2)
preview_1 = start_week - preview_options.index(selected_preview)
preview_2 = preview_1 - 1  # 자동으로 1주 늦은 시점 설정

preview_weeks = [preview_1, preview_2]

# 선택된 프리뷰 시점 표시
st.write(f"선택된 프리뷰 시점: {preview_1}주 전과 {preview_2}주 전")

# 직전 리뷰 오차율별 표 생성
previous_error_rates = [0.5, 0.4, 0.3, 0.2, 0.1]

for rate in previous_error_rates:
    st.subheader(f"직전 리뷰 오차율 {rate:.0%}인 경우")
    table = create_comparison_table(start_week, preview_weeks, rate)
    st.write(f"행: {preview_1}주 전 프리뷰 오차율, 열: {preview_2}주 전 프리뷰 오차율")
    st.dataframe(table)

# 설명 추가
st.markdown(f"""
### 설명:
- 이 프로그램은 6개월 동안의 주간 예측 (총 26주)에 대한 점수를 계산합니다.
- 실적 발표 시점과 두 개의 연속된 프리뷰 비교 시점을 선택할 수 있습니다.
- 각 표는 {preview_1}주 전 프리뷰와 {preview_2}주 전 프리뷰의 오차율 조합에 따른 Ej 값을 보여줍니다.
- {preview_1}주 전보다 이전의 프리뷰 오차율은 {preview_1}주 전 프리뷰의 오차율과 동일하다고 가정합니다.
- {preview_2}주 전부터 실적 발표 시점까지의 프리뷰 오차율은 {preview_2}주 전 프리뷰의 오차율과 동일하다고 가정합니다.
- 점수가 낮을수록 (0에 가까울수록) 예측 성과가 좋음을 의미합니다.
""")