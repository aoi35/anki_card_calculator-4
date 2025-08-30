import streamlit as st
from streamlit_javascript import st_javascript

# ===== Convert "hh:mm" string to decimal hours =====
def time_to_hours(time_str):
    try:
        hours, minutes = map(int, time_str.split(":"))
        return hours + minutes / 60
    except:
        st.error("Invalid time format. Example: 6:23")
        return None

# ===== Calculate new Anki cards =====
def calculate_new_cards(input_hours, anki_hours, total_cards, due_cards, new_ratio=0.25,
                        safe_min=10, safe_max=300):
    avg_sec_per_card = (anki_hours * 3600) / total_cards
    base_new_cards = (anki_hours * 3600 * new_ratio) / avg_sec_per_card
    input_factor = min(2.0, max(0.5, input_hours / 6))
    due_factor = max(0.3, 1 - due_cards / 100)
    new_cards = int(base_new_cards * input_factor * due_factor)
    new_cards = max(safe_min, min(safe_max, new_cards))
    return new_cards

st.title("New Card Limit Calculator / 新規カード上限計算")

# ===== ブラウザlocalStorageから前回比率を読み込む =====
last_ratio = st_javascript("return localStorage.getItem('last_ratio') || '4:1';")

# 入力フォーム
input_time = st.text_input("昨日Inputに使った時間 / Yesterday's Input time (例: 2:00)", "2:00")
anki_time = st.text_input("昨日暗記カードにかかった時間 / Yesterday's Anki time (例: 0:30)", "0:30")
ratio_input = st.text_input("理想のInput:暗記カードの比率 / The ideal input:Anki ratio (例: 4:1)", last_ratio)
total_cards = st.number_input("昨日の総レビュー枚数 (新規+復習) / Total cards reviewed yesterday (new + review)", min_value=1, value=10)
due_cards = st.number_input("今日が期限のカード枚数 / Cards due today", min_value=0, value=30)

# ===== 計算ボタン =====
if st.button("Calculate / 計算"):
    input_hours = time_to_hours(input_time)
    anki_hours = time_to_hours(anki_time)
    
    try:
        input_part, anki_part = map(float, ratio_input.split(":"))
        new_ratio = anki_part / (input_part + anki_part)
    except:
        st.error("Invalid ratio format. Example: 4:1")
        new_ratio = 0.25
    
    if input_hours is not None and anki_hours is not None:
        new_cards = calculate_new_cards(input_hours, anki_hours, total_cards, due_cards, new_ratio=new_ratio)
        st.success(f"Ideal number of new cards: {new_cards}\n推奨新規カード枚数: {new_cards}")
        # ブラウザに保存
        st_javascript(f"localStorage.setItem('last_ratio', '{ratio_input}');")
