# %%
# 导入Streamlit库
from database import *

import pandas as pd
import streamlit as st
import os
# st.set_page_config(layout="wide")

"""
> Dongdong Kong, CUG, 2023
"""
# # Streamlit应用程序的标题
# st.title("Hello, World!")

# # 在应用程序中显示文本
# st.write("这是一个简单的Streamlit示例，显示 'Hello, World!'")

# # 在应用程序中显示图像
# # st.image("https://www.streamlit.io/images/brand/streamlit-logo-primary-colormark-darktext.png")

# # 在应用程序中添加交互元素（例如按钮）
# if st.button("点击我"):
#     st.write("你点击了按钮！")
# 在应用程序中添加用户输入
# user_input = st.text_input("请输入一些文本")
# st.write("你输入的文本是:", user_input)

# %%
# print(os.getcwd())

# %%
# 添加站点列表啊
# stationInfo = pd.read_csv("data/st_met2481.csv")
# site = 59287

# %%
# cursor = db_open()
# tbl = "Met_hourly"
# site = 59287
