
import streamlit as st
st.set_page_config(page_title="선생님 대시보드", layout="wide")

import pandas as pd
import matplotlib.pyplot as plt
from db_utils import init_db, get_all_students, get_scores, get_attendance, get_assignments, submit_assignment, add_student, add_score, add_assignment
from fpdf import FPDF
import os
import tempfile
from datetime import date

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

# 학생 등록
st.sidebar.header("📚 학생 등록")
new_name = st.sidebar.text_input("학생 이름")
new_grade = st.sidebar.selectbox("학년", [f"초등학교 {i}학년" for i in range(1, 7)] + [f"중학교 {i}학년" for i in range(1, 4)] + [f"고등학교 {i}학년" for i in range(1, 4)])

if st.sidebar.button("등록"):
    if new_name:
        add_student(new_name, new_grade)
        st.sidebar.success("등록 완료!")

st.title("📊 선생님 대시보드")

students = get_all_students()
for name, grade in students:
    st.subheader(f"{name} ({grade})")
    scores = get_scores(name)
    if scores:
        df = pd.DataFrame(scores, columns=["과목", "점수"])
        st.dataframe(df)
    else:
        st.info("성적 정보 없음")

# 성적 등록
st.markdown("---")
st.header("📥 성적 등록")
sel_student = st.selectbox("학생 선택", [s[0] for s in students], key="성적등록")
subject = st.text_input("과목명")
score = st.number_input("점수", min_value=0, max_value=100, step=1)

if st.button("성적 등록"):
    if subject:
        add_score(sel_student, subject, score)
        st.success(f"{sel_student}의 {subject} 성적이 등록되었습니다.")
        st.rerun()
    else:
        st.warning("과목명을 입력해주세요.")

# 과제 등록
st.markdown("---")
st.header("📌 과제 등록")
title = st.text_input("과제 제목")
desc = st.text_area("과제 설명")
due = st.date_input("마감일", min_value=date.today())

if st.button("과제 전체 배포"):
    if title and desc:
        for s in students:
            add_assignment(s[0], title, desc, due.isoformat(), "", False)
        st.success("전체 학생에게 과제가 배포되었습니다.")
        st.rerun()
    else:
        st.warning("과제 제목과 설명을 모두 입력해주세요.")

if st.button("🔓 로그아웃"):
    st.session_state.logged_in = False
    st.rerun()
