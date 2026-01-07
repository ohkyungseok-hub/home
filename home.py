import streamlit as st
import streamlit.components.v1 as components
from pathlib import Path
import base64
import json
from datetime import datetime

# ============================================================
# 기본 설정
# ============================================================
st.set_page_config(
    page_title="E-편한 출고 | 출고통합시스템",
    page_icon="📦",
    layout="centered",
)

# ============================================================
# 설정값
# ============================================================
SCROLL_SECONDS = 10
NOTICE_FILE = Path("notices.json")

# Streamlit Cloud 권장: .streamlit/secrets.toml에 ADMIN_PASSWORD="비번" 설정
ADMIN_PASSWORD = st.secrets.get("ADMIN_PASSWORD", "admin1234")

# ============================================================
# 공지 기본값 (파일 없거나 깨졌을 때 사용)
# ============================================================
DEFAULT_NOTICES = [
    "2025-01-05 쿠팡 송장 포맷 업데이트 예정",
    "금일(12/28) 18:00 시스템 점검 예정",
    "신규 기능: 제안상품 자동 분류 기능 추가",
    "출고 마감: 평일 16:30 / 토 12:00",
]

# ============================================================
# 메뉴
# ============================================================
MENU = [
    ("📦", "제안 상품 등록", "https://newappuct-3jvtvi9fafvdhqhzmstvs3.streamlit.app"),
    ("🧾", "피킹용 주문서 출력", "https://g89qgzdijtiiazrp2rvflj.streamlit.app"),
    ("🚚", "합배/단품 나누어서 송장 출력", "https://songjangg.streamlit.app"),
    ("🏬", "쿠팡/스마트스토어 송장 출력", "https://coupsmartconvert.streamlit.app"),
    ("📋", "송장번호 등록용", "https://cjcjsongjang.streamlit.app/"),
    ("💰", "일일 매출 계산하기", "https://countdaily.streamlit.app/"),
    ("⚙️", "스마트스토어 상품변환", "https://smartconver.streamlit.app/"),
]

# ============================================================
# 로고
# ============================================================
LOGO_CANDIDATES = ["logo.png", "logo.jpg", "logo.jpeg"] 

def find_logo_path():
    for p in LOGO_CANDIDATES:
        if Path(p).exists():
            return p
    return None

def img_to_base64(img_path: str) -> str:
    return base64.b64encode(Path(img_path).read_bytes()).decode("utf-8")

logo_path = find_logo_path()
logo_b64 = img_to_base64(logo_path) if logo_path else None

# ============================================================
# 공지 로드/저장
# ============================================================
def load_notices() -> list[str]:
    if NOTICE_FILE.exists():
        try:
            data = json.loads(NOTICE_FILE.read_text(encoding="utf-8"))
            if isinstance(data, list):
                out = [str(x).strip() for x in data if str(x).strip()]
                return out if out else DEFAULT_NOTICES.copy()
        except Exception:
            pass
    return DEFAULT_NOTICES.copy()

def save_notices(notices: list[str]) -> None:
    clean = [str(n).strip() for n in notices if str(n).strip()]
    NOTICE_FILE.write_text(json.dumps(clean, ensure_ascii=False, indent=2), encoding="utf-8")

# 세션 상태 초기화
if "notices" not in st.session_state:
    st.session_state["notices"] = load_notices()
if "admin_ok" not in st.session_state:
    st.session_state["admin_ok"] = False

# ============================================================
# 스타일
# ============================================================
st.markdown(
    f"""
    <style>
      header, footer, #MainMenu {{visibility: hidden;}}

      .wrap {{
        max-width: 920px;
        margin: 0 auto;
        padding: 8px 10px 28px;
      }}

      /* ===== 공지 자동 스크롤 ===== */
      .notice-box {{
        background: #f8f9fb;
        border: 1px solid rgba(0,0,0,0.08);
        border-radius: 14px;
        padding: 14px 18px;
        margin-bottom: 18px;
        box-shadow: 0px 6px 14px rgba(0,0,0,0.04);
      }}
      .notice-title {{
        font-size: 18px;
        font-weight: 900;
        margin-bottom: 10px;
      }}
      .ticker {{
        height: 54px;
        overflow: hidden;
      }}
      .ticker-inner {{
        display: grid;
        gap: 6px;
        animation: scrollUp {SCROLL_SECONDS}s linear infinite;
      }}
      .ticker:hover .ticker-inner {{
        animation-play-state: paused;
      }}
      .notice-item {{
        font-size: 15px;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
      }}
      @keyframes scrollUp {{
        0% {{ transform: translateY(0); }}
        100% {{ transform: translateY(-50%); }}
      }}

      /* ===== 타이틀 ===== */
      .title {{
        text-align: center;
        font-size: clamp(30px, 4.2vw, 46px);
        font-weight: 900;
        margin-bottom: 2px;
      }}
      .subtitle {{
        text-align: center;
        font-size: clamp(30px, 4.2vw, 46px);
        font-weight: 900;
        margin-bottom: 18px;
      }}

      /* ===== 로고 (실무용 베스트) ===== */
      .logo {{
        display: flex;
        justify-content: center;
        margin: 10px 0 24px;
      }}
      .logo img {{
        width: 280px;
        max-width: 72vw;
        height: auto;

        border-radius: 18px;
        border: 1px solid rgba(0,0,0,0.08);
        box-shadow: 0 8px 24px rgba(0,0,0,0.12);
        background: #fff;
      }}

      /* ===== 메뉴 ===== */
      .menu {{
        display: grid;
        gap: 14px;
      }}
      .btn {{
        display: flex;
        justify-content: space-between;
        align-items: center;
        padding: 22px;
        border-radius: 16px;
        background: #fff;
        border: 1px solid rgba(0,0,0,0.08);
        box-shadow: 0px 8px 20px rgba(0,0,0,0.06);
        text-decoration: none !important;
      }}
      .btn-left {{
        display: flex;
        align-items: center;
        gap: 12px;
        min-width: 0;
      }}
      .icon {{ font-size: 28px; }}
      .label {{
        font-size: clamp(22px, 2.6vw, 30px);
        font-weight: 900;
        color: #111;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
      }}
      .arrow {{ font-size: 20px; color: rgba(0,0,0,0.45); }}

      .footerline {{
        text-align: center;
        margin-top: 18px;
        font-size: 13px;
        color: rgba(0,0,0,0.45);
      }}
    </style>
    """,
    unsafe_allow_html=True
)

# ============================================================
# 사이드바: 페이지 선택
# ============================================================
st.sidebar.title("📦 출고통합시스템")
page = st.sidebar.radio("이동", ["홈", "공지 관리자"], index=0)

# ============================================================
# 페이지: 홈
# ============================================================
if page == "홈":
    st.markdown('<div class="wrap">', unsafe_allow_html=True)

    notices = st.session_state["notices"]
    if not notices:
        notices = ["공지사항이 없습니다."]

    items = "".join([f'<div class="notice-item">📢 {n}</div>' for n in notices])

    st.markdown(
        f"""
        <div class="notice-box">
          <div class="notice-title">📌 공지사항 (마우스 올리면 일시정지)</div>
          <div class="ticker">
            <div class="ticker-inner">
              {items}
              {items}
            </div>
          </div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown('<div class="title">E- 편한 출고</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">출고통합시스템</div>', unsafe_allow_html=True)

    if logo_b64:
        st.markdown(
            f'<div class="logo"><img src="data:image/png;base64,{logo_b64}"></div>',
            unsafe_allow_html=True
        )
    else:
        st.info("로고 파일(logo.png / logo.jpg)이 프로젝트 폴더에 필요합니다.")

    menu_html = '<div class="menu">'
    for icon, label, url in MENU:
        menu_html += f"""
<a class="btn" href="{url}" target="_blank" rel="noopener noreferrer">
  <div class="btn-left">
    <div class="icon">{icon}</div>
    <div class="label">{label}</div>
  </div>
  <div class="arrow">↗</div>
</a>
""".strip()
    menu_html += "</div>"

    components.html(menu_html, height=120 * len(MENU) + 40, scrolling=False)

    st.markdown(
        '<div class="footerline">ⓒ AFOURS Co., Ltd. | E-편한 출고 통합시스템</div>',
        unsafe_allow_html=True
    )
    st.markdown("</div>", unsafe_allow_html=True)

# ============================================================
# 페이지: 공지 관리자 (정상 동작/에러 방지)
# ============================================================
else:
    st.title("🔐 공지 관리자")

    with st.expander("비밀번호 입력", expanded=not st.session_state["admin_ok"]):
        pw = st.text_input("관리자 비밀번호", type="password", placeholder="비밀번호를 입력하세요", key="admin_pw")
        if st.button("로그인", key="admin_login"):
            st.session_state["admin_ok"] = (pw == ADMIN_PASSWORD)
            st.rerun()

    if not st.session_state["admin_ok"]:
        st.warning("로그인 후 공지를 수정할 수 있습니다.")
        st.caption("※ 비밀번호는 secrets.toml에 ADMIN_PASSWORD로 설정하는 것을 권장합니다.")
        st.stop()

    st.success("관리자 인증 완료 ✅")
    st.subheader("현재 공지 목록 (수정 후 저장)")

    # 공지 편집/삭제
    for i in range(len(st.session_state["notices"])):
        col1, col2 = st.columns([8, 1.6])
        with col1:
            st.text_input(
                f"{i+1}.",
                value=st.session_state["notices"][i],
                key=f"notice_edit_{i}",
            )
        with col2:
            if st.button("삭제", key=f"notice_delete_{i}"):
                st.session_state["notices"].pop(i)

                # 인덱스 기반 키 정리
                for k in list(st.session_state.keys()):
                    if k.startswith("notice_edit_"):
                        del st.session_state[k]

                save_notices(st.session_state["notices"])
                st.success("삭제 완료 ✅")
                st.rerun()

    st.divider()

    # ✅ 공지 추가 (form + clear_on_submit로 에러 방지)
    st.subheader("공지 추가")
    with st.form("notice_add_form", clear_on_submit=True):
        new_notice = st.text_input(
            "새 공지 내용",
            placeholder="예) 2025-01-05 쿠팡 송장 포맷 업데이트 예정",
            key="new_notice_input",
        )
        submitted = st.form_submit_button("추가")

    if submitted:
        if new_notice.strip():
            st.session_state["notices"].append(new_notice.strip())
            save_notices(st.session_state["notices"])

            for k in list(st.session_state.keys()):
                if k.startswith("notice_edit_"):
                    del st.session_state[k]

            st.success("추가 완료 ✅")
            st.rerun()
        else:
            st.warning("공지 내용을 입력하세요.")

    st.divider()

    # 저장/복원
    c1, c2, c3 = st.columns([2, 2, 6])
    with c1:
        if st.button("저장", key="notice_save"):
            updated = []
            for i in range(len(st.session_state["notices"])):
                val = st.session_state.get(f"notice_edit_{i}", st.session_state["notices"][i])
                val = str(val).strip()
                if val:
                    updated.append(val)

            st.session_state["notices"] = updated
            save_notices(st.session_state["notices"])

            for k in list(st.session_state.keys()):
                if k.startswith("notice_edit_"):
                    del st.session_state[k]

            st.success("저장 완료 ✅ 홈 화면에 즉시 반영됩니다.")
            st.rerun()

    with c2:
        if st.button("기본값 복원", key="notice_reset"):
            st.session_state["notices"] = DEFAULT_NOTICES.copy()
            save_notices(st.session_state["notices"])

            for k in list(st.session_state.keys()):
                if k.startswith("notice_edit_"):
                    del st.session_state[k]

            st.info("기본값으로 복원했습니다.")
            st.rerun()

    st.caption(f"마지막 확인: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
