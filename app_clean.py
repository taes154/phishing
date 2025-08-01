import streamlit as st
import numpy as np
import pickle
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences

@st.cache_resource
def load_tokenizer():
    with open('tokenizer.pkl', 'rb') as f:
        return pickle.load(f)

@st.cache_resource
def load_phishing_model():
    return load_model('phishing_model.keras')

def predict_phishing(text, tokenizer, model, max_len=100):
    seq = tokenizer.texts_to_sequences([text])
    padded = pad_sequences(seq, maxlen=max_len)
    pred = model.predict(padded)[0][0]
    return pred

def main():
    st.markdown(
        """
        <style>
        /* 나눔고딕 웹폰트 적용 */
        @import url('https://fonts.googleapis.com/css2?family=MalgumGothic&display=swap');

        html, body, [class*="css"] {
            font-family: 'Nanum Gothic', sans-serif !important;
        }

        .center-text {
            text-align: center;
        }

        div.stButton {
            width: 100%;
            max-width: 700px;
            margin: 1rem auto;
            text-align: center;
        }

        div.stButton > button {
            background-color: #007bff;
            color: white;
            border-radius: 30px;
            padding: 1rem 0;
            font-size: 1.3rem;
            font-weight: 600;
            border: none;
            cursor: pointer;
            transition: background-color 0.3s ease;
            width: 100%;
            max-width: 700px;
            display: inline-block;
        }

        div.stButton > button:hover {
            background-color: #0056b3;
            color: white;
        }

        textarea {
            max-width: 700px;
        }
        </style>
        """, unsafe_allow_html=True
    )

    st.markdown('<h1 class="center-text">🛡️ 피싱 탐지기</h1>', unsafe_allow_html=True)
    st.markdown('<p class="center-text">아래에 의심되는 웹사이트 URL을 입력하면 피싱 여부를 판단합니다.</p>', unsafe_allow_html=True)

    user_input = st.text_area("", height=200, placeholder="이곳에 URL을 입력하세요.")

    analyze_clicked = st.button("🔍 분석하기")

    if analyze_clicked:
        if not user_input.strip():
            st.warning("입력값이 비어 있습니다. URL을 입력해주세요.")
        else:
            tokenizer = load_tokenizer()
            model = load_phishing_model()
            probability = predict_phishing(user_input, tokenizer, model)
            percentage = probability * 100

            if probability >= 0.5:
                st.error(f"🚨 피싱 가능성이 높습니다! (확률: {percentage:.0f}%)")
            else:
                st.success(f"✅ 안전한 메시지, URL로 보입니다. (확률: {percentage:.0f}%)")

    st.markdown("---")
    st.markdown('<p class="center-text">⚠️ 본 탐지기의 결과는 정확하지 않습니다.</p>', unsafe_allow_html=True)

if __name__ == '__main__':
    main()
