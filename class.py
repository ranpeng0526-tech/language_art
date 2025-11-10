import streamlit as st
import openai
from openai import OpenAI

# 从 secrets.toml 读取 API 密钥
client = OpenAI(
    api_key=st.secrets["moonshot"]["api_key"],
    base_url=st.secrets["moonshot"]["base_url"]
)


def judge_level(text):
    response = client.chat.completions.create(
        model="moonshot-v1-8k",  # 修改为正确的模型名称
        messages=[
            {"role": "system", "content": "### 定位：语义歧视分析专家\n ### 任务：请对用户输入的句子进行歧视性分析，并用 1 到 5 之间的数字表示其歧视程度。1 表示没有歧视，5 表示极为歧视。\n ###输出 ：只输出数字，不需要额外解释。"},
            {"role": "user", "content": text},
        ],
        temperature=0.7
    )
    # 添加调试信息
    print(f"Response type: {type(response)}")
    print(f"Response: {response}")
    return response.choices[0].message.content

def tiao_zheng(text):
    response = client.chat.completions.create(
        model="moonshot-v1-8k",  # 修改为正确的模型名称
        messages=[
            {"role": "system", "content": "### 定位：语言表述专家\n ### 任务：将歧视性语句换一种方法表述，使表述中不包含歧视语义。"},
            {"role": "user", "content": text},
        ],
        temperature=0.7
    )
    return response.choices[0].message.content

st.set_page_config(page_title="我的第一个网页面")
st.title("Hello Streamlit❤️❤️❤️")
user_input = st.text_area("请输入需要分析的句子", height=100)
if st.button("开始分析"):
    if user_input.strip() == "":
        st.warning("请输入有效的句子进行分析。")
    else:
        with st.spinner('正在分析中...'):
            try:
                with st.spinner('正在分析中...'):
                    score = judge_level(user_input)
                    st.success(f"歧视程度评分：{score}")
                    
                    # 检查分数是否为1
                    score_str = str(score).strip()
                    if score_str != '1':
                        with st.spinner('正在生成优化建议...'):
                            result = tiao_zheng(user_input)
                            st.success(f"调整后的表述：{result}")
                    else:
                        st.info("✅ 该表述没有歧视性，无需调整。")
            except AttributeError as e:
                st.error(f"API 响应格式错误: {e}")
                st.info("💡 提示：可能是 API 密钥或 base_url 配置不正确")
            except Exception as e:
                st.error(f"分析过程中出现错误: {e}😭")
                st.info("💡 请检查网络连接和 API 配置")