import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from textblob import TextBlob
import nltk
from nltk.corpus import stopwords
from wordcloud import WordCloud

# NLTK 데이터 다운로드
nltk.download('punkt')
nltk.download('stopwords')

# 한국어 감정 분석을 위한 함수
def analyze_sentiment_ko(text):
    # 여기에 한국어 감정 분석 로직을 구현해야 합니다.
    # 예시로 간단한 키워드 기반 감정 분석을 수행합니다.
    positive_words = ['만족', '좋았', '유익', '도움']
    negative_words = ['불만', '어려웠', '부족']
    
    score = sum([1 for word in positive_words if word in text]) - \
            sum([1 for word in negative_words if word in text])
    
    if score > 0:
        return 'Positive'
    elif score < 0:
        return 'Negative'
    else:
        return 'Neutral'

# 앱 제목
st.title('교육 만족도 서베이 분석')

# 파일 업로더
uploaded_file = st.file_uploader("CSV 파일을 업로드하세요", type="csv")

if uploaded_file is not None:
    # 데이터 로드
    df = pd.read_csv(uploaded_file)
    
    # 데이터 미리보기
    st.subheader('데이터 미리보기')
    st.write(df.head())
    
    # 만족도 관련 수치 데이터 시각화
    st.subheader('만족도 분석')
    
    # 교육 만족도
    fig, ax = plt.subplots(figsize=(10, 6))
    df['참여하신 교육에 대한 만족도'].value_counts().plot(kind='bar', ax=ax)
    plt.title('교육에 대한 만족도')
    plt.xlabel('만족도')
    plt.ylabel('응답 수')
    st.pyplot(fig)
    
    # 강사 만족도
    fig, ax = plt.subplots(figsize=(10, 6))
    df['강사에 대한 만족도'].value_counts().plot(kind='bar', ax=ax)
    plt.title('강사에 대한 만족도')
    plt.xlabel('만족도')
    plt.ylabel('응답 수')
    st.pyplot(fig)
    
    # 업무 도움 정도
    fig, ax = plt.subplots(figsize=(10, 6))
    df['교육이 본인의 업무, 연구, 학업에 도움이 되었는가'].value_counts().plot(kind='bar', ax=ax)
    plt.title('업무/연구/학업에 대한 도움 정도')
    plt.xlabel('도움 정도')
    plt.ylabel('응답 수')
    st.pyplot(fig)
    
    # 텍스트 데이터 감정 분석
    st.subheader('만족스러웠던 점 감정 분석')
    
    # 감정 분석 수행
    df['sentiment'] = df['만족스러웠던 점'].apply(analyze_sentiment_ko)
    
    # 감정 분석 결과 시각화
    fig, ax = plt.subplots(figsize=(10, 6))
    df['sentiment'].value_counts().plot(kind='pie', autopct='%1.1f%%', ax=ax)
    plt.title('만족스러웠던 점에 대한 감정 분석')
    st.pyplot(fig)
    
    # 워드클라우드 생성
    st.subheader('만족스러웠던 점 워드클라우드')
    text = ' '.join(df['만족스러웠던 점'])
    wordcloud = WordCloud(width=800, height=400, background_color='white', font_path='/usr/share/fonts/truetype/nanum/NanumGothic.ttf').generate(text)
    
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis('off')
    st.pyplot(fig)

else:
    st.info('CSV 파일을 업로드해주세요.')
