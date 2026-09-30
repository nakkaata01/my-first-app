import streamlit as st
import ollama

# 画面のタイトルを設定
st.title("💬 Ollama チャットボット")

# セッション状態（履歴保存用）の初期化
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# 過去のチャット履歴を表示
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ユーザーからの入力を受け付ける
if user_input := st.chat_input("メッセージを入力してください..."):
    # ユーザーの入力を画面に表示＆履歴に追加
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Ollamaからの応答をストリーミング（逐次）表示
    with st.chat_message("assistant"):
        response_placeholder = st.empty()
        full_response = ""
        
        # ollama.chat の stream=True を使って文字を少しずつ取得
        stream = ollama.chat(
            model='llama3', # 使用するモデル名（事前にollama runしたもの）
            messages=st.session_state.messages,
            stream=True,
        )
        
        for chunk in stream:
            full_response += chunk['message']['content']
            response_placeholder.markdown(full_response + "▌")
            
        response_placeholder.markdown(full_response)
        
    # アシスタントの応答を履歴に追加
    st.session_state.messages.append({"role": "assistant", "content": full_response})
