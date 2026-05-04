import streamlit as st
import json
import os

# 保存先のファイル名
SAVE_FILE = "points_data.json"
# 先生用のパスワード（ここを自由に変更してください）
TEACHER_PASSWORD = "mayu0907"

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

# データの初期化
if 'points' not in st.session_state:
    data = load_data()
    st.session_state.points = data.get("points", 0)

st.title("家庭教師ポイント管理")

# 現在のポイント表示
st.metric(label="現在のスタンプ数", value=f"{st.session_state.points} 個")

st.divider()

# サイドバーに管理用メニューを作成
st.sidebar.header("メニュー")
mode = st.sidebar.radio("モード切替", ["生徒モード", "先生モード"])

if mode == "先生モード":
    # 修正ポイント：パスワード入力
    password = st.sidebar.text_input("先生用パスワードを入力し、Enterで確定", type="password")
    
    if password == TEACHER_PASSWORD:
        st.sidebar.success("認証されました")
        
        st.subheader("【先生用操作パネル】")
        # 確実にボタンが表示されるよう、メインエリアに配置
        num_to_add = st.number_input("付与するポイント数", min_value=1, value=1, step=1)
        
        if st.button(f"{num_to_add} ポイント付与する"):
            st.session_state.points += num_to_add
            save_data({"points": st.session_state.points})
            st.success(f"{num_to_add} ポイント付与しました。")
            # 5秒後に自動でメッセージを消す代わりに、再描画して数値を更新
            st.rerun()
            
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