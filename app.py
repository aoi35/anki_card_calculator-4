import streamlit as st

# ===== Convert "hh:mm" string to decimal hours =====
def time_to_hours(time_str):
    try:
        hours, minutes = map(int, time_str.split(":"))
        return hours + minutes / 60
    except:
        st.error("Invalid time format. Example: 6:23")
        return None

# ===== Calculate new Anki cards =====
def calculate_new_cards(input_hours, anki_hours, total_cards, due_cards, ideal_ratio=0.25, min_new=5):
    # 昨日の1枚あたり処理時間（秒/枚）
    sec_per_card = (anki_hours * 3600) / total_cards
    
    # 今日理想のAnki時間（秒）
    ideal_anki_seconds = input_hours * 3600 * ideal_ratio
    
    # 今日処理可能な総枚数
    total_possible = ideal_anki_seconds / sec_per_card
    
    # 今日が期限のカードを引く
    new_cards = total_possible - due_cards
    
    # 最低値5枚
    new_cards = max(min_new, int(round(new_cards)))
    
    return new_cards

st.title("New Card Limit Calculator / 新規カード上限計算")

# 入力フォーム
input_time = st.text_input("昨日Inputに使った時間 / Yesterday's Input time (例: 2:00)", "2:00")
anki_time = st.text_input("昨日暗記カードにかかった時間 / Yesterday's Anki time (例: 0:30)", "0:30")
ratio_input = st.text_input("理想のInput:暗記カードの比率 / The ideal input:Anki ratio (例: 4:1)", "4:1")
total_cards = st.number_input("昨日の総レビュー枚数 (新規+復習) / Total cards reviewed yesterday (new + review)", min_value=1, value=10)
due_cards = st.number_input("今日が期限のカード枚数 / Cards due today", min_value=0, value=0)

# ===== 計算ボタン =====
if st.button("Calculate / 計算"):
    input_hours = time_to_hours(input_time)
    anki_hours = time_to_hours(anki_time)
    
    try:
        input_part, anki_part = map(float, ratio_input.split(":"))
        ideal_ratio = anki_part / (input_part + anki_part)
    except:
        st.error("Invalid ratio format. Example: 4:1")
        ideal_ratio = 0.25
    
    if input_hours is not None and anki_hours is not None:
        new_cards = calculate_new_cards(input_hours, anki_hours, total_cards, due_cards, ideal_ratio=ideal_ratio, min_new=5)
        st.success(f"Ideal number of new cards: {new_cards}\n推奨新規カード枚数: {new_cards}")
