import streamlit as st

st.title("New Card Limit Calculator / 新規カード上限計算")

# ===== セッションに前回値を保持 =====
if 'input_time' not in st.session_state:
    st.session_state['input_time'] = "2:00"
if 'anki_time' not in st.session_state:
    st.session_state['anki_time'] = "0:30"
if 'ratio_input' not in st.session_state:
    st.session_state['ratio_input'] = "4:1"
if 'total_cards' not in st.session_state:
    st.session_state['total_cards'] = 10
if 'due_cards' not in st.session_state:
    st.session_state['due_cards'] = 0

# ===== 入力フォーム =====
input_time = st.text_input("昨日Inputに使った時間 / Yesterday's Input time (例: 2:00)", st.session_state['input_time'])
anki_time = st.text_input("昨日暗記カードにかかった時間 / Yesterday's Anki time (例: 0:30)", st.session_state['anki_time'])
ratio_input = st.text_input("理想のInput:暗記カードの比率 / The ideal input:Anki ratio (例: 4:1)", st.session_state['ratio_input'])
total_cards = st.number_input("昨日の総レビュー枚数 (新規+復習) / Total cards reviewed yesterday (new + review)", min_value=1, value=st.session_state['total_cards'])
due_cards = st.number_input("今日が期限のカード枚数 / Cards due today", min_value=0, value=st.session_state['due_cards'])

# ===== 計算ボタン =====
if st.button("Calculate / 計算"):
    # 入力値をセッションに保存
    st.session_state['input_time'] = input_time
    st.session_state['anki_time'] = anki_time
    st.session_state['ratio_input'] = ratio_input
    st.session_state['total_cards'] = total_cards
    st.session_state['due_cards'] = due_cards
    
    # 時間を小数に変換
    def time_to_hours(time_str):
        try:
            h, m = map(int, time_str.split(":"))
            return h + m/60
        except:
            st.error("Invalid time format. Example: 2:30")
            return None

    input_hours = time_to_hours(input_time)
    anki_hours = time_to_hours(anki_time)
    
    try:
        input_part, anki_part = map(float, ratio_input.split(":"))
        ideal_ratio = anki_part / (input_part + anki_part)
    except:
        st.error("Invalid ratio format. Example: 4:1")
        ideal_ratio = 0.25

    if input_hours is not None and anki_hours is not None:
        # 新規カード計算ロジック
        actual_ratio = anki_hours / (input_hours + anki_hours)
        if abs(actual_ratio - ideal_ratio) < 0.01:
            new_cards = total_cards - due_cards
        else:
            sec_per_card = (anki_hours*3600)/total_cards
            ideal_anki_seconds = input_hours*3600*ideal_ratio
            new_cards = int(ideal_anki_seconds / sec_per_card - due_cards)
        new_cards = max(5, new_cards)
        st.success(f"Ideal number of new cards: {new_cards}\n推奨新規カード枚数: {new_cards}")