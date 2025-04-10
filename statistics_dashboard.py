import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from db_utils import get_all_students, get_scores, get_attendance, get_assignments, submit_assignment

from db_utils import init_db
init_db()

from fpdf import FPDF
import os
import tempfile

# 로그인 설정
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

st.set_page_config(page_title="📊 학급 통계 분석", layout="wide")
st.title("📊 학생별 통계 대시보드")
st.markdown("각종 항목에 대한 통계 분석 결과를 시각적으로 확인하세요.")

students = get_all_students()

# 평균 성적
st.subheader("🧮 평균 성적 분석")
avg_scores = []
for name, _ in students:
    scores = get_scores(name)
    if scores:
        점수값들 = [s for _, s in scores]
        avg = sum(점수값들) / len(점수값들)
        avg_scores.append((name, avg))

if avg_scores:
    df_score = pd.DataFrame(avg_scores, columns=["이름", "평균 점수"])
    fig, ax = plt.subplots()
    df_score.set_index("이름").plot(kind="bar", legend=False, ax=ax)
    ax.set_ylabel("점수")
    st.pyplot(fig)
else:
    st.info("아직 성적 데이터가 없습니다.")

# 출석률
st.subheader("📅 출석률 분석")
attendance_rates = []
for name, _ in students:
    출결 = get_attendance(name)
    총 = len(출결)
    출석수 = len([s for _, s in 출결 if s == "출석"])
    출석률 = (출석수 / 총) * 100 if 총 > 0 else 0
    attendance_rates.append((name, 출석률))

if attendance_rates:
    df_att = pd.DataFrame(attendance_rates, columns=["이름", "출석률 (%)"])
    fig2, ax2 = plt.subplots()
    df_att.set_index("이름").plot(kind="bar", legend=False, color="green", ax=ax2)
    ax2.set_ylabel("출석률 (%)")
    st.pyplot(fig2)
else:
    st.info("출결 데이터가 없습니다.")

# 과제 제출률
st.subheader("📝 과제 제출률 분석")
submit_rates = []
for name, _ in students:
    과제 = get_assignments(name)
    총과제 = len(과제)
    제출완료 = len([1 for _, _, _, _, s in 과제 if s == 1])
    제출률 = (제출완료 / 총과제) * 100 if 총과제 > 0 else 0
    submit_rates.append((name, 제출률))

if submit_rates:
    df_sub = pd.DataFrame(submit_rates, columns=["이름", "제출률 (%)"])
    fig3, ax3 = plt.subplots()
    df_sub.set_index("이름").plot(kind="bar", legend=False, color="orange", ax=ax3)
    ax3.set_ylabel("제출률 (%)")
    st.pyplot(fig3)
else:
    st.info("과제 데이터가 없습니다.")

# 로그아웃
st.markdown("---")
if st.button("🔓 로그아웃"):
    st.session_state.logged_in = False
    st.rerun()
