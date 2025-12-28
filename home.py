import streamlit as st
import streamlit.components.v1 as components
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

# 로고 파일 (png/jpg 모두 허용)
LOGO_CANDIDATES = ["logo.png", "logo.jpg", "logo.jpeg"]

def find_logo_path() -> str | None:
    for p in LOGO_CANDIDATES:
        if Path(p).exists():
            return p
    return None

def img_to_base64(img_path: str) -> str:
    return base64.b64encode(Path(img_path).read_bytes()).decode("utf-8")

logo_path = find_logo_path()
logo_b64 = img_to_base64(logo_path) if logo_path else None

# -----------------------------
# 스타일
# -----------------------------
st.markdown(
    """
    <style>
      /* Streamlit 기본 헤더/푸터 숨김 (원하면 제거 가능) */
      header {visibility: hidden;}
      footer {visibility: hidden;}
      #MainMenu {visibility: hidden;}

      .wrap {
        max-width: 920px;
        margin: 0 auto;
        padding: 8px 10px 28px;
      }

      /* 모바일 대응: 폰트 자동 조절 */
      .title {
        text-align: center;
        font-size: clamp(30px, 4.2vw, 46px);
        font-weight: 900;
        letter-spacing: -1px;
        margin-top: 6px;
        margin-bottom: 2px;
      }
      .subtitle {
        text-align: center;
        font-size: clamp(30px, 4.2vw, 46px);
        font-weight: 900;
        letter-spacing: -1px;
        margin-top: -4px;
        margin-bottom: 18px;
      }

      .logo {
        display: flex;
        justify-content: center;
        margin: 10px 0 24px;
      }
      .logo img {
        width: 280px;
        max-width: 72vw;
        height: auto;
        filter: drop-shadow(0px 10px 18px rgba(0,0,0,0.12));
      }

      .menu {
        display: grid;
        gap: 14px;
        margin-top: 8px;
      }

      .btn {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 18px 18px;
        border-radius: 16px;
        border: 1px solid rgba(0,0,0,0.08);
        background: #ffffff;
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
        min-width: 0;
      }
      .dot {
        width: 10px;
        height: 10px;
        border-radius: 50%;
        background: #111;
        flex: 0 0 auto;
      }
      .label {
        font-size: clamp(18px, 2.2vw, 24px);
        font-weight: 900;
        letter-spacing: -0.6px;
        color: #111;
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
      }
      .arrow {
        font-size: 20px;
        color: rgba(0,0,0,0.45);
        font-weight: 700;
        margin-left: 12px;
        flex: 0 0 auto;
      }

      .footerline {
        text-align: center;
        margin-top: 18px;
        color: rgba(0,0,0,0.45);
        font-size: 13px;
      }

      section.main > div { padding-top: 18px; }
    </style>
    """,
    unsafe_allow_html=True
)

# -----------------------------
# 화면 렌더링 (상단: 타이틀/로고)
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
    st.info("로고 파일을 찾지 못했습니다. logo.png 또는 logo.jpg를 프로젝트 폴더에 넣어주세요.")

# -----------------------------
# 메뉴 버튼 (components.html로 안전 렌더링)
# -----------------------------
menu_html = '<div class="menu">'
for label, url in MENU:
    menu_html += f"""
<a class="btn" href="{url}" target="_blank" rel="noopener noreferrer">
  <div class="btn-left">
    <div class="dot"></div>
    <div class="label">{label}</div>
  </div>
  <div class="arrow">↗</div>
</a>
""".strip()
menu_html += "</div>"

# 버튼 개수에 맞게 높이 자동-ish 설정 (대충)
components.html(menu_html, height=95 * len(MENU) + 30, scrolling=False)

# -----------------------------
# 하단 푸터
# -----------------------------
st.markdown(
    '<div class="footerline">ⓒ AFOURS Co., Ltd. | E-편한 출고 통합시스템</div>',
    unsafe_allow_html=True
)
st.markdown("</div>", unsafe_allow_html=True)
