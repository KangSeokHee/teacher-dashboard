
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from db_utils import init_db, get_all_students, get_scores, get_attendance, get_assignments, submit_assignment, add_student
from fpdf import FPDF
import os
import tempfile

init_db()

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

users = {"teacher1": "pw123", "admin": "admin123"}

def login():
    st.title("🔐 로그인")
    user = st.text_input("아이디")
    pw = st.text_input("비밀번호", type="password")
    if st.button("로그인"):
        if user in users and users[user] == pw:
            st.session_state.logged_in = True
            st.session_state.user = user
            st.success("로그인 성공!")
            st.rerun()
        else:
            st.error("아이디 또는 비밀번호가 올바르지 않습니다.")

if not st.session_state.logged_in:
    login()
    st.stop()

# 사이드바: 학생 등록
st.sidebar.header("📚 학생 등록")
new_name = st.sidebar.text_input("학생 이름")
new_grade = st.sidebar.selectbox("학년", [f"초등학교 {i}학년" for i in range(1, 7)] + [f"중학교 {i}학년" for i in range(1, 4)] + [f"고등학교 {i}학년" for i in range(1, 4)])

if st.sidebar.button("등록"):
    if new_name:
        add_student(new_name, new_grade)
        st.sidebar.success("등록 완료!")
    else:
        st.sidebar.warning("학생 이름을 입력해주세요.")

# 간단히 평균 점수 예시
st.title("📊 학생 대시보드 예시")
students = get_all_students()
for name, grade in students:
    st.subheader(f"{name} ({grade})")
    scores = get_scores(name)
    if scores:
        df = pd.DataFrame(scores, columns=["과목", "점수"])
        st.dataframe(df)
    else:
        st.info("성적 정보 없음")

if st.button("🔓 로그아웃"):
    st.session_state.logged_in = False
    st.rerun()
