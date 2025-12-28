import streamlit as st
from pathlib import Path
import base64

# -----------------------------
# 기본 설정
# -----------------------------
st.set_page_config(
    page_title="E-편한 출고 | 출고통합시스템",
    page_icon="📦",
    layout="centered",
)

# -----------------------------
# 링크 매핑 (위에서부터 순서대로)
# -----------------------------
MENU = [
    ("제안 상품 등록", "https://newappuct-3jvtvi9fafvdhqhzmstvs3.streamlit.app"),
    ("피킹용 주문서 출력", "https://g89qgzdijtiiazrp2rvflj.streamlit.app"),
    ("합배/단품 나누어서 송장 출력", "https://songjangg.streamlit.app"),
    ("쿠팡/스마트스토어 송장 출력", "https://coupsmartconvert.streamlit.app"),
    ("창고입당용 주문서 변환 및 송장번호 등록용", "https://finalbalzoo.streamlit.app"),
]

LOGO_PATH = "logo.png"  # 로고 파일명/경로

# -----------------------------
# 유틸: 로고를 HTML로 중앙 정렬 출력
# -----------------------------
def img_to_base64(img_path: str) -> str | None:
    p = Path(img_path)
    if not p.exists():
        return None
    return base64.b64encode(p.read_bytes()).decode("utf-8")

logo_b64 = img_to_base64(LOGO_PATH)

# -----------------------------
# 스타일 (버튼형 메뉴 + 전체 톤)
# -----------------------------
st.markdown(
    """
    <style>
      .wrap {
        max-width: 920px;
        margin: 0 auto;
        padding: 10px 8px 30px;
      }
      .title {
        text-align: center;
        font-size: 44px;
        font-weight: 900;
        letter-spacing: -1px;
        margin-top: 6px;
        margin-bottom: 4px;
      }
      .subtitle {
        text-align: center;
        font-size: 44px;
        font-weight: 900;
        letter-spacing: -1px;
        margin-top: -6px;
        margin-bottom: 18px;
      }
      .logo {
        display: flex;
        justify-content: center;
        margin: 10px 0 26px;
      }
      .logo img {
        width: 280px;
        max-width: 70vw;
        height: auto;
        filter: drop-shadow(0px 10px 18px rgba(0,0,0,0.12));
      }

      .menu {
        display: grid;
        gap: 14px;
        margin-top: 10px;
      }
      .btn {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 18px 18px;
        border-radius: 16px;
        border: 1px solid rgba(0,0,0,0.08);
        background: rgba(255,255,255,0.9);
        box-shadow: 0px 8px 20px rgba(0,0,0,0.06);
        text-decoration: none !important;
        transition: transform 0.08s ease, box-shadow 0.08s ease, border 0.08s ease;
      }
      .btn:hover {
        transform: translateY(-1px);
        box-shadow: 0px 12px 26px rgba(0,0,0,0.09);
        border: 1px solid rgba(0,0,0,0.14);
      }
      .btn-left {
        display: flex;
        align-items: center;
        gap: 12px;
      }
      .dot {
        width: 10px;
        height: 10px;
        border-radius: 50%;
        background: #111;
        flex: 0 0 auto;
      }
      .label {
        font-size: 24px;
        font-weight: 900;
        letter-spacing: -0.6px;
        color: #111;
      }
      .arrow {
        font-size: 20px;
        color: rgba(0,0,0,0.45);
        font-weight: 700;
      }

      .footer {
        text-align: center;
        margin-top: 20px;
        color: rgba(0,0,0,0.45);
        font-size: 13px;
      }

      /* Streamlit 상단 여백 조금 줄이기 */
      section.main > div { padding-top: 20px; }
    </style>
    """,
    unsafe_allow_html=True
)

# -----------------------------
# 화면 렌더링
# -----------------------------
st.markdown('<div class="wrap">', unsafe_allow_html=True)

st.markdown('<div class="title">E- 편한 출고</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">출고통합시스템</div>', unsafe_allow_html=True)

if logo_b64:
    st.markdown(
        f"""
        <div class="logo">
          <img src="data:image/png;base64,{logo_b64}" alt="logo">
        </div>
        """,
        unsafe_allow_html=True
    )
else:
    # 로고 파일이 없을 때 대체 표시
    st.info("로고 파일을 찾지 못했습니다. 프로젝트 폴더에 'logo.png'를 넣어주세요.")

# 메뉴 버튼들
menu_html = ['<div class="menu">']
for label, url in MENU:
    menu_html.append(
        f"""
        <a class="btn" href="{url}" target="_blank" rel="noopener noreferrer">
          <div class="btn-left">
            <div class="dot"></div>
            <div class="label">{label}</div>
          </div>
          <div class="arrow">↗</div>
        </a>
        """
    )
menu_html.append("</div>")

st.markdown("\n".join(menu_html), unsafe_allow_html=True)

st.markdown(
    '<div class="footer">ⓒ AFOURS Co., Ltd. | E-편한 출고 통합시스템</div>',
    unsafe_allow_html=True
)

st.markdown("</div>", unsafe_allow_html=True)
