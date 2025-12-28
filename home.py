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
# 공지 데이터 (여기만 수정)
# -----------------------------
NOTICES = [
    "미로상사 sku는 항상 50개 이상 유지합시다",
    "주7일 출고가 시작되었습니다",
    "퇴근시 화기 점검 필수",
    "로이로라가 보고 있습니다"
]

# 스크롤 속도(초) - 숫자 클수록 느림
SCROLL_SECONDS = 10

# -----------------------------
# 링크 매핑 (아이콘, 라벨, URL)
# -----------------------------
MENU = [
    ("📦", "제안 상품 일괄등록", "https://newappuct-3jvtvi9fafvdhqhzmstvs3.streamlit.app"),
    ("🧾", "피킹용 주문서 출력", "https://g89qgzdijtiiazrp2rvflj.streamlit.app"),
    ("🚚", "합배/단품 나누어서 송장 출력", "https://songjangg.streamlit.app"),
    ("🏬", "쿠팡/스마트스토어 송장 출력", "https://coupsmartconvert.streamlit.app"),
    ("📋", "창고임당용 주문서 변환 및 송장번호 등록용", "https://finalbalzoo.streamlit.app"),
]

# -----------------------------
# 로고
# -----------------------------
LOGO_CANDIDATES = ["logo.png", "logo.jpg", "logo.jpeg"]

def find_logo_path():
    for p in LOGO_CANDIDATES:
        if Path(p).exists():
            return p
    return None

def img_to_base64(img_path):
    return base64.b64encode(Path(img_path).read_bytes()).decode("utf-8")

logo_path = find_logo_path()
logo_b64 = img_to_base64(logo_path) if logo_path else None

# -----------------------------
# 스타일
# -----------------------------
st.markdown(
    f"""
    <style>
      header, footer, #MainMenu {{visibility: hidden;}}

      .wrap {{
        max-width: 920px;
        margin: 0 auto;
        padding: 8px 10px 28px;
      }}

      /* =========================
         공지 자동 스크롤 보드
         ========================= */
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

      /* 보이는 창(높이) */
      .ticker {{
        height: 54px;              /* 공지 2줄 정도 보이게 */
        overflow: hidden;
        position: relative;
      }}

      /* 실제 움직이는 영역 */
      .ticker-inner {{
        display: grid;
        gap: 6px;
        will-change: transform;
        animation: scrollUp {SCROLL_SECONDS}s linear infinite;
      }}

      /* 마우스 올리면 멈춤 */
      .ticker:hover .ticker-inner {{
        animation-play-state: paused;
      }}

      .notice-item {{
        font-size: 15px;
        line-height: 1.5;
        color: #111;
        white-space: nowrap;
        overflow: hidden;
        text-overflow: ellipsis;
      }}

      /* 위로 스크롤 애니메이션 */
      @keyframes scrollUp {{
        0%   {{ transform: translateY(0); }}
        100% {{ transform: translateY(-50%); }}
      }}

      /* =========================
         타이틀/로고/메뉴
         ========================= */
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

      .logo {{
        display: flex;
        justify-content: center;
        margin: 10px 0 24px;
      }}
      .logo img {{
        width: 220px;
        max-width: 72vw;
        filter: drop-shadow(0px 10px 18px rgba(0,0,0,0.12));
      }}

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

      .icon {{ font-size: 28px; line-height: 1; }}
      .label {{
        font-size: clamp(22px, 2.6vw, 30px);
        font-weight: 900;
        overflow: hidden;
        text-overflow: ellipsis;
        white-space: nowrap;
        color: #111;
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

# -----------------------------
# 화면 렌더링
# -----------------------------
st.markdown('<div class="wrap">', unsafe_allow_html=True)

# ✅ 공지 자동 스크롤 (무한 루프 위해 2번 반복)
items = ""
for n in NOTICES:
    items += f'<div class="notice-item">📢 {n}</div>'

ticker_html = f"""
<div class="notice-box">
  <div class="notice-title">📌 공지사항 (마우스 올리면 일시정지)</div>
  <div class="ticker">
    <div class="ticker-inner">
      {items}
      {items}
    </div>
  </div>
</div>
"""
st.markdown(ticker_html, unsafe_allow_html=True)

# 타이틀/로고
st.markdown('<div class="title">E- 편한 출고</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">출고통합시스템</div>', unsafe_allow_html=True)

if logo_b64:
    st.markdown(
        f'<div class="logo"><img src="data:image/png;base64,{logo_b64}"></div>',
        unsafe_allow_html=True
    )

# 메뉴 (components.html로 안전 렌더링)
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

# 푸터
st.markdown(
    '<div class="footerline">ⓒ AFOURS Co., Ltd. | E-편한 출고 통합시스템</div>',
    unsafe_allow_html=True
)
st.markdown("</div>", unsafe_allow_html=True)
