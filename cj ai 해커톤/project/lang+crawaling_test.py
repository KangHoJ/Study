import os
#허깅페이스 개인 APIKey
os.environ['HUGGINGFACEHUB_API_TOKEN'] = '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'
import streamlit as st
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from langchain.llms import HuggingFaceHub
from crawling import crawling

st.title('질문해보세요')

# 사용자로부터 URL 입력 받기
url = st.text_input('URL을 작성해주세요')
search_button = st.button("검색", type="primary")

# URL이 입력되고 검색 버튼이 눌렸을 때 동작
if url and search_button:
    # 크롤링을 통해 기사 내용 가져오기
    title , text = crawling(url)
    # combined_question = f"{title} {text}"

    # 모델 구현
    repo_id = 'EleutherAI/polyglot-ko-1.3b'
    llm = HuggingFaceHub(repo_id=repo_id, model_kwargs={"temperature": 0.5, "max_length": 64})
    
    # 프롬프트 템플릿
    template = f"질문: {title} 은 기사 제목이랑 어울릴까?\n대답:"
    prompt = PromptTemplate(template=template, input_variables=['title'])
    
    # LLM Chain 객체 생성
    llm_chain = LLMChain(prompt=prompt, llm=llm)
    answer = llm_chain.run(question="")

    st.write("결과 : ", answer)
    