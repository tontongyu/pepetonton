import streamlit as st
import json
import os

# 1. 基本設定やデータ読み込みの関数
SAVE_FILE = "points_data.json"
TEACHER_PASSWORD = st.secrets["general"]["password"]

def load_data():
    if os.path.exists(SAVE_FILE):
        with open(SAVE_FILE, "r") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                return {"points": 0}
    return {"points": 0}

def save_data(data):
    with open(SAVE_FILE, "w") as f:
        json.dump(data, f)

# ★重要★ 呼び出す前に「display_stamp_card」を定義します
def display_stamp_card(points, max_stamps=20):
    st.subheader("スタンプカード")
    cols_per_row = 5
    rows = (max_stamps // cols_per_row)
    
    with st.container(border=True):
        for r in range(rows):
            cols = st.columns(cols_per_row)
            for c in range(cols_per_row):
                current_idx = r * cols_per_row + c + 1
                with cols[c]:
                    if current_idx <= points:
                        st.markdown(
                            f"<div style='text-align: center; font-size: 30px; "
                            f"background-color: #FFEB3B; border-radius: 50%; "
                            f"width: 50px; height: 50px; line-height: 50px; margin: auto;'>"
                            f"💮</div>", 
                            unsafe_allow_html=True
                        )
                    else:
                        st.markdown(
                            f"<div style='text-align: center; font-size: 20px; color: #E0E0E0; "
                            f"border: 2px dashed #E0E0E0; border-radius: 50%; "
                            f"width: 50px; height: 50px; line-height: 50px; margin: auto;'>"
                            f"{current_idx}</div>", 
                            unsafe_allow_html=True
                        )

# 2. データの初期化
if 'points' not in st.session_state:
    data = load_data()
    st.session_state.points = data.get("points", 0)

# 3. メインの表示（ここで関数を呼び出す）
st.title("家庭教師ポイント管理")
st.metric(label="現在のスタンプ数", value=f"{st.session_state.points} 個")

# ここで呼び出し
display_stamp_card(st.session_state.points)

st.divider()

# 4. サイドバーと管理操作（先生モードなど）
st.sidebar.header("メニュー")
mode = st.sidebar.radio("モード切替", ["生徒モード", "先生モード"])

# （以下、以前のコードと同様）
if mode == "先生モード":
    password = st.sidebar.text_input("先生用パスワードを入力", type="password")
    if password == TEACHER_PASSWORD:
        st.sidebar.success("認証されました")
        num_to_add = st.number_input("付与するポイント数", min_value=1, value=1, step=1)
        if st.button(f"{num_to_add} ポイント付与する"):
            st.session_state.points += num_to_add
            save_data({"points": st.session_state.points})
            st.rerun()
    # ...（中略）...
            
        if st.sidebar.button("ポイントをリセット"):
            st.session_state.points = 0
            save_data({"points": 0})
            st.rerun()
            
    elif password != "":
        st.sidebar.error("パスワードが違います")
    else:
        st.sidebar.info("パスワードを入力してEnterキーを押してください。")

else:
    st.info("生徒モード：現在のポイントを確認できます。先生がポイントを付与するとここに反映されます。")
