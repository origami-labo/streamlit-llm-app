from dotenv import load_dotenv

load_dotenv()

import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage, HumanMessage
from dotenv import load_dotenv

# .envファイルから環境変数（OPENAI_API_KEYなど）を読み込む
load_dotenv()

# 「入力テキスト」と「ラジオボタンでの選択値」を受け取り、LLMからの回答を返す関数
def generate_response(input_text, expert_type):
    # ラジオボタンの選択値に応じてシステムメッセージを変更
    if expert_type == "プロの料理研究家":
        system_prompt = "あなたはプロの料理研究家です。初心者にもわかりやすく、美味しく作るコツを交えて回答してください。"
    elif expert_type == "優秀なプログラマー":
        system_prompt = "あなたは優秀なプログラマーです。技術的な質問に対して、論理的で分かりやすい解説やコード例を交えて回答してください。"
    else: # ベテランのフィットネストレーナー
        system_prompt = "あなたはベテランのフィットネストレーナーです。健康や運動に関する質問に対して、科学的根拠に基づいた適切なアドバイスを熱血な口調で回答してください。"

    # モデルの初期化（LangChainのChat modelsを利用）
    llm = ChatOpenAI(model_name="gpt-4o-mini", temperature=0)
    
    # プロンプトのメッセージリストを作成
    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=input_text)
    ]
    
    # LLMにプロンプトを渡して回答を生成
    result = llm.invoke(messages)
    
    # 生成された回答テキストを戻り値として返す
    return result.content


# --- Streamlitの画面構築 ---

st.title("AI専門家への相談アプリ")

# アプリの概要や操作方法をユーザーに明示するテキスト
st.write("### アプリの概要")
st.write("このアプリは、AIが特定の分野の専門家としてあなたの質問に回答するチャットボットです。")
st.write("### 操作方法")
st.write("1. 相談したい「専門家の種類」をラジオボタンから選択してください。")
st.write("2. 下部の入力フォームに相談内容や質問を入力してください。")
st.write("3. 「相談する」ボタンを押すと、専門家からの回答が表示されます。")

st.divider()

# ラジオボタンで専門家の種類を選択
selected_expert = st.radio(
    "相談する専門家の種類を選択してください。",
    ["プロの料理研究家", "優秀なプログラマー", "ベテランのフィットネストレーナー"]
)

# 入力フォーム（テキスト入力）
user_input = st.text_input(label="相談内容や質問を入力してください。")

# ボタンが押されたときの処理
if st.button("相談する"):
    # 入力フォームが空でないか確認
    if user_input:
        # ローディングアニメーションを表示しながら関数を実行
        with st.spinner("専門家が回答を考えています..."):
            response = generate_response(user_input, selected_expert)
        
        # 回答結果を画面上に表示
        st.write("### 専門家からの回答")
        st.write(response)
    else:
        # 入力フォームが空のままボタンが押された場合はエラーメッセージを表示
        st.error("相談内容を入力してから「相談する」ボタンを押してください。")