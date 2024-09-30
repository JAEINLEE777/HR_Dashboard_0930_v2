import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from textblob import TextBlob

# 데이터 로드
@st.cache_data
def load_data():
    data = {
        "참여하신 교육에 대한 만족도": ["보통", "보통", "매우 만족", "만족", "매우 만족", "매우 만족", "보통", "매우 만족", "만족", "매우 만족"],
        "강사에 대한 만족도": ["매우 만족", "매우 만족", "보통", "보통", "만족", "매우 만족", "보통", "만족", "매우 만족", "만족"],
        "교육이 본인의 업무, 연구, 학업에 도움이 되었는가": ["매우 도움이 되었다", "매우 도움이 되었다", "도움이 되었다", "도움이 되었다", "매우 도움이 되었다", "매우 도움이 되었다", "매우 도움이 되었다", "보통이다", "도움이 되었다", "매우 도움이 되었다"],
        "교육을 동료 및 학생들에게 추천하시겠습니까": ["매우 그렇다", "그렇다", "그렇지 않다", "보통이다", "보통이다", "그렇지 않다", "매우 그렇다", "매우 그렇다", "보통이다", "그렇다"],
        "재수강할 의사가 있습니까": ["매우 그렇다", "매우 그렇다", "매우 그렇다", "매우 그렇다", "보통이다", "보통이다", "그렇다", "그렇다", "매우 그렇다", "그렇다"],
        "만족스러웠던 점": [
            "Obsidian을 사용한 연결 노트 관리 방법이 혁신적이었습니다.",
            "실제 업무에서 바로 활용 가능한 기술을 배울 수 있었습니다.",
            "구체적이고 실습 위주의 교육이 매우 인상적이었습니다.",
            "Obsidian을 사용한 연결 노트 관리 방법이 혁신적이었습니다.",
            "Obsidian을 사용한 연결 노트 관리 방법이 혁신적이었습니다.",
            "Obsidian을 사용한 연결 노트 관리 방법이 혁신적이었습니다.",
            "개인 지식 관리를 체계적으로 할 수 있는 새로운 방법을 알게 되어 좋았습니다.",
            "오랫동안 찾고 있던 개인 지식 관리 방법을 알게 되어 매우 만족했습니다.",
            "실제 업무에서 바로 활용 가능한 기술을 배울 수 있었습니다.",
            "강사님의 실습 중심 설명 덕분에 쉽게 이해할 수 있었습니다."
        ],
        "성별": ["여성", "여성", "남성", "여성", "여성", "남성", "여성", "남성", "남성", "여성"],
        "연령": [38, 31, 29, 40, 42, 48, 39, 49, 28, 49],
        "부서": ["관리부", "영업부", "마케팅부", "인사부", "기술개발부", "기술개발부", "마케팅부", "관리부", "마케팅부", "관리부"]
    }
    return pd.DataFrame(data)

def main():
    st.title('교육 만족도 서베이 분석 앱')

    df = load_data()

    st.subheader('데이터 미리보기')
    st.write(df.head())

    # 정량적 데이터 시각화
    st.subheader('정량적 데이터 시각화')
    columns = ['참여하신 교육에 대한 만족도', '강사에 대한 만족도', '교육이 본인의 업무, 연구, 학업에 도움이 되었는가', 
               '교육을 동료 및 학생들에게 추천하시겠습니까', '재수강할 의사가 있습니까']
    selected_column = st.selectbox('시각화할 열을 선택하세요:', columns)

    fig, ax = plt.subplots(figsize=(10, 6))
    df[selected_column].value_counts().plot(kind='bar', ax=ax)
    plt.title(f'{selected_column} 분포')
    plt.xlabel('응답')
    plt.ylabel('빈도')
    st.pyplot(fig)

    # 성별에 따른 만족도 분석
    st.subheader('성별에 따른 만족도 분석')
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.boxplot(x='성별', y='참여하신 교육에 대한 만족도', data=df, ax=ax)
    plt.title('성별에 따른 교육 만족도')
    st.pyplot(fig)

    # 연령대에 따른 만족도 분석
    st.subheader('연령대에 따른 만족도 분석')
    df['연령대'] = pd.cut(df['연령'], bins=[20, 30, 40, 50, 60], labels=['20대', '30대', '40대', '50대'])
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.boxplot(x='연령대', y='참여하신 교육에 대한 만족도', data=df, ax=ax)
    plt.title('연령대에 따른 교육 만족도')
    st.pyplot(fig)

    # 부서별 만족도 분석
    st.subheader('부서별 만족도 분석')
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.boxplot(x='부서', y='참여하신 교육에 대한 만족도', data=df, ax=ax)
    plt.title('부서별 교육 만족도')
    plt.xticks(rotation=45)
    st.pyplot(fig)

    # 텍스트 데이터 감정 분석
    st.subheader('텍스트 데이터 감정 분석')
    
    def analyze_sentiment(text):
        return TextBlob(text).sentiment.polarity

    df['sentiment'] = df['만족스러웠던 점'].apply(analyze_sentiment)
    
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.histplot(df['sentiment'], kde=True, ax=ax)
    plt.title('감정 분석 결과')
    plt.xlabel('감정 점수')
    plt.ylabel('빈도')
    st.pyplot(fig)
    
    # 긍정적/부정적 응답 표시
    st.subheader('응답 예시')
    positive_responses = df[df['sentiment'] > 0]['만족스러웠던 점'].head()
    negative_responses = df[df['sentiment'] < 0]['만족스러웠던 점'].head()
    
    st.write('긍정적인 응답 예시:')
    st.write(positive_responses)
    
    st.write('부정적인 응답 예시:')
    st.write(negative_responses)

if __name__ == "__main__":
    main()
