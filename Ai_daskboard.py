"""
╔══════════════════════════════════════════════════════════════════════╗
║     POWER BI STYLE — AI SALES DASHBOARD  v2.0                       ║
║     Built by  : Ankit Prajapati                                      ║
║     Stack     : Streamlit · Plotly · Pandas · Claude AI              ║
╚══════════════════════════════════════════════════════════════════════╝
Run: streamlit run app.py
"""

# ── Standard Library ─────────────────────────────────────────────────
import io
import re
import warnings
from datetime import datetime, date

# ── Third-Party ──────────────────────────────────────────────────────
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import streamlit as st
import requests

warnings.filterwarnings("ignore")

# ════════════════════════════════════════════════════════════════════
# PAGE CONFIG  (must be FIRST Streamlit call)
# ════════════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="AI Sales Dashboard — Ankit Prajapati",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ════════════════════════════════════════════════════════════════════
# DESIGN TOKENS
# ════════════════════════════════════════════════════════════════════
PLOTLY_TEMPLATE = "plotly_dark"
CHART_BG        = "rgba(14,17,32,0)"
PAPER_BG        = "rgba(14,17,32,0)"
GRID_COLOR      = "rgba(255,255,255,0.06)"
FONT_COLOR      = "#e2e8f0"

C_BLUE   = "#2563eb"
C_CYAN   = "#06b6d4"
C_PURPLE = "#7c3aed"
C_GOLD   = "#f59e0b"
C_GREEN  = "#10b981"
C_RED    = "#ef4444"
C_PINK   = "#ec4899"
C_TEAL   = "#14b8a6"
C_INDIGO = "#4f46e5"
C_ROSE   = "#f43f5e"

BAR_SEQ = [C_BLUE, C_CYAN, C_PURPLE, C_GOLD, C_GREEN, C_PINK, C_TEAL, C_RED, C_INDIGO, C_ROSE]

# ════════════════════════════════════════════════════════════════════
# GLOBAL CSS
# ════════════════════════════════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@400;600;700&display=swap');

/* ── Base ─────────────────────────────────────────────────────── */
html, body, [class*="css"], .stApp {
    font-family: 'Inter', sans-serif !important;
    background: #080b18 !important;
    color: #e2e8f0 !important;
}
.stApp {
    background:
        radial-gradient(ellipse 80% 50% at 50% -20%, rgba(37,99,235,0.12), transparent),
        linear-gradient(rgba(37,99,235,0.025) 1px, transparent 1px),
        linear-gradient(90deg, rgba(37,99,235,0.025) 1px, transparent 1px),
        #080b18 !important;
    background-size: 100% 100%, 48px 48px, 48px 48px !important;
}

/* ── Sidebar ─────────────────────────────────────────────────── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg,#090c1d 0%,#0d1128 60%,#0a0e1f 100%) !important;
    border-right: 1px solid rgba(99,102,241,0.2) !important;
    width: 290px !important;
}
[data-testid="stSidebar"] * { color: #e2e8f0 !important; }
[data-testid="stSidebarContent"] { padding: 0 !important; }

/* ── Main area ───────────────────────────────────────────────── */
.main .block-container {
    padding: 1rem 1.8rem 3rem !important;
    max-width: 100% !important;
}

/* ── Header banner ───────────────────────────────────────────── */
.dash-header {
    background: linear-gradient(135deg,#0c0f24 0%,#141040 45%,#0c0f24 100%);
    border: 1px solid rgba(124,58,237,0.3);
    border-radius: 16px; padding: 22px 32px;
    margin-bottom: 18px; position: relative; overflow: hidden;
}
.dash-header::before {
    content:''; position:absolute; inset:0;
    background: linear-gradient(90deg,rgba(37,99,235,0.12) 0%,transparent 55%);
}
.dash-header::after {
    content:''; position:absolute;
    right:-60px; top:-60px; width:220px; height:220px;
    background: radial-gradient(circle,rgba(124,58,237,0.15),transparent 70%);
    border-radius:50%;
}
.dash-header-title {
    font-size: 1.85rem; font-weight: 900; letter-spacing:-.03em;
    background: linear-gradient(90deg,#60a5fa 0%,#a78bfa 50%,#34d399 100%);
    -webkit-background-clip:text; -webkit-text-fill-color:transparent;
    background-clip:text; margin:0; position:relative; z-index:1;
}
.dash-header-sub {
    color:#64748b; font-size:.85rem; margin-top:4px;
    position:relative; z-index:1;
}
.dash-badge {
    display:inline-block;
    background:rgba(124,58,237,0.18);
    border:1px solid rgba(124,58,237,0.4);
    color:#a78bfa; border-radius:50px;
    padding:3px 13px; font-size:.7rem;
    font-weight:700; letter-spacing:.1em; text-transform:uppercase;
    position:relative; z-index:1;
}
.dash-by {
    font-size:.78rem; color:#475569; margin-top:8px;
    position:relative; z-index:1;
}
.dash-by span {
    background:linear-gradient(90deg,#60a5fa,#a78bfa);
    -webkit-background-clip:text; -webkit-text-fill-color:transparent;
    background-clip:text; font-weight:700;
}

/* ── KPI cards ───────────────────────────────────────────────── */
.kpi-card {
    background: linear-gradient(145deg,#0c1028 0%,#141830 100%);
    border: 1px solid rgba(37,99,235,0.2);
    border-radius: 16px; padding: 20px 18px 16px;
    position: relative; overflow: hidden;
    transition: transform .25s ease, box-shadow .25s ease;
    cursor: default;
}
.kpi-card:hover { transform: translateY(-4px); }
.kpi-card::before {
    content:''; position:absolute; top:0; left:0; right:0; height:3px;
    border-radius:16px 16px 0 0;
}
.kpi-card.blue::before   { background:linear-gradient(90deg,#2563eb,#06b6d4); }
.kpi-card.purple::before { background:linear-gradient(90deg,#7c3aed,#ec4899); }
.kpi-card.gold::before   { background:linear-gradient(90deg,#f59e0b,#10b981); }
.kpi-card.teal::before   { background:linear-gradient(90deg,#14b8a6,#06b6d4); }
.kpi-glow-blue   { box-shadow: 0 0 32px rgba(37,99,235,.16), 0 4px 12px rgba(0,0,0,.5); }
.kpi-glow-purple { box-shadow: 0 0 32px rgba(124,58,237,.16), 0 4px 12px rgba(0,0,0,.5); }
.kpi-glow-gold   { box-shadow: 0 0 32px rgba(245,158,11,.16), 0 4px 12px rgba(0,0,0,.5); }
.kpi-glow-teal   { box-shadow: 0 0 32px rgba(20,184,166,.16), 0 4px 12px rgba(0,0,0,.5); }
.kpi-icon   { font-size:1.7rem; margin-bottom:8px; display:block; }
.kpi-label  { font-size:.68rem; text-transform:uppercase; letter-spacing:.14em; color:#475569; font-weight:700; margin-bottom:5px; }
.kpi-value  { font-family:'JetBrains Mono',monospace; font-size:2rem; font-weight:700; color:#f1f5f9; line-height:1; }
.kpi-delta  { font-size:.75rem; color:#10b981; margin-top:7px; font-weight:600; }
.kpi-delta.neg { color:#ef4444; }
.kpi-sparkline { height:36px; margin-top:8px; opacity:.7; }

/* ── Slicer panel ────────────────────────────────────────────── */
.slicer-bar {
    background: linear-gradient(135deg,#0d1028,#121630);
    border: 1px solid rgba(37,99,235,0.18);
    border-radius: 14px; padding: 14px 18px;
    margin-bottom: 16px; display:flex; flex-wrap:wrap; gap:12px;
    align-items: flex-end;
}
.slicer-title {
    font-size:.68rem; text-transform:uppercase; letter-spacing:.12em;
    color:#475569; font-weight:700; margin-bottom:5px;
}

/* ── Chart cards ─────────────────────────────────────────────── */
.chart-card {
    background: linear-gradient(145deg,#0d1028 0%,#101424 100%);
    border: 1px solid rgba(37,99,235,0.13);
    border-radius: 14px; padding: 16px 16px 8px;
    margin-bottom: 16px; position:relative; overflow:hidden;
    transition: border-color .2s;
}
.chart-card:hover { border-color: rgba(37,99,235,0.28); }
.chart-card::after {
    content:''; position:absolute; inset:0;
    background: radial-gradient(ellipse at top left,rgba(37,99,235,0.04),transparent 65%);
    pointer-events:none;
}
.chart-title   { font-size:.82rem; font-weight:700; color:#94a3b8; text-transform:uppercase; letter-spacing:.1em; margin-bottom:3px; }
.chart-subtitle{ font-size:.73rem; color:#334155; margin-bottom:6px; }

/* ── Section labels ──────────────────────────────────────────── */
.section-label {
    font-size:.68rem; font-weight:800; letter-spacing:.16em;
    text-transform:uppercase; color:#1e293b;
    padding:12px 0 6px; border-top:1px solid rgba(255,255,255,0.03);
    margin-top:4px;
}

/* ── Insight cards ───────────────────────────────────────────── */
.insight-card {
    background:rgba(10,13,28,0.6);
    border:1px solid rgba(255,255,255,0.06);
    border-left:3px solid #2563eb;
    border-radius:10px; padding:13px 17px;
    margin-bottom:9px; font-size:.88rem; line-height:1.7; color:#cbd5e1;
}
.insight-card.success { border-left-color:#10b981; }
.insight-card.warning { border-left-color:#f59e0b; }
.insight-card.danger  { border-left-color:#ef4444; }

/* ── Conclusion ──────────────────────────────────────────────── */
.conclusion-box {
    background:linear-gradient(135deg,rgba(37,99,235,0.07),rgba(124,58,237,0.05));
    border:1px solid rgba(124,58,237,0.22);
    border-radius:14px; padding:22px 26px;
    font-size:.93rem; line-height:1.85; color:#cbd5e1;
    margin-top:14px;
}

/* ── Tabs ────────────────────────────────────────────────────── */
.stTabs [data-baseweb="tab-list"] {
    gap:3px; background:transparent;
    border-bottom:1px solid rgba(255,255,255,0.06);
}
.stTabs [data-baseweb="tab"] {
    background:transparent; border:none;
    border-radius:8px 8px 0 0; color:#475569 !important;
    font-weight:700; font-size:.86rem; padding:9px 20px;
}
.stTabs [aria-selected="true"] {
    background:rgba(37,99,235,0.1) !important;
    color:#60a5fa !important;
    border-bottom:2px solid #2563eb;
}

/* ── Buttons ─────────────────────────────────────────────────── */
.stButton > button {
    background:linear-gradient(135deg,#2563eb,#7c3aed) !important;
    color:#fff !important; border:none !important;
    border-radius:8px !important; font-weight:700 !important;
}
.stDownloadButton > button {
    background:transparent !important;
    border:1px solid rgba(37,99,235,0.4) !important;
    color:#60a5fa !important; border-radius:8px !important; font-weight:700 !important;
}

/* ── Selects ─────────────────────────────────────────────────── */
[data-baseweb="select"] { background:#0d1028 !important; }
[data-baseweb="select"] * { color:#e2e8f0 !important; }

/* ── Scrollbar ───────────────────────────────────────────────── */
::-webkit-scrollbar { width:5px; height:5px; }
::-webkit-scrollbar-track { background:#090c1d; }
::-webkit-scrollbar-thumb { background:#1e3a8a; border-radius:3px; }

/* ── DataFrames ──────────────────────────────────────────────── */
[data-testid="stDataFrame"] { border-radius:10px; overflow:hidden; }
[data-testid="stFileUploadDropzone"] {
    background:rgba(37,99,235,0.05) !important;
    border:1.5px dashed rgba(37,99,235,0.3) !important;
    border-radius:10px !important;
}
.stAlert { border-radius:10px !important; }
hr { border-color:rgba(255,255,255,0.04) !important; }
#MainMenu, footer, [data-testid="stToolbar"] { display:none !important; }

/* ── Sidebar profile card ────────────────────────────────────── */
.profile-wrap {
    padding: 20px 16px 0;
    text-align: center;
}
.profile-logo {
    font-family:'JetBrains Mono',monospace;
    font-size:1.05rem; font-weight:800;
    background:linear-gradient(90deg,#60a5fa,#a78bfa);
    -webkit-background-clip:text; -webkit-text-fill-color:transparent;
    background-clip:text; letter-spacing:-.01em;
}
.profile-tagline {
    font-size:.65rem; color:#334155; letter-spacing:.1em;
    text-transform:uppercase; margin-top:1px;
}
.profile-divider {
    margin:14px 10px;
    height:1px;
    background:linear-gradient(90deg,transparent,rgba(124,58,237,0.45),transparent);
}
.dev-card {
    background:linear-gradient(145deg,rgba(37,99,235,0.1),rgba(124,58,237,0.08));
    border:1px solid rgba(124,58,237,0.28);
    border-radius:14px; padding:16px 12px 14px;
    margin:0 8px; position:relative; overflow:hidden;
}
.dev-card::before {
    content:''; position:absolute;
    top:-30px; right:-30px; width:80px; height:80px;
    background:radial-gradient(circle,rgba(124,58,237,0.3),transparent 70%);
    border-radius:50%;
}
.dev-card::after {
    content:''; position:absolute;
    bottom:-20px; left:-20px; width:60px; height:60px;
    background:radial-gradient(circle,rgba(37,99,235,0.2),transparent 70%);
    border-radius:50%;
}
.dev-avatar {
    width:52px; height:52px; border-radius:50%;
    background:linear-gradient(135deg,#2563eb,#7c3aed);
    display:flex; align-items:center; justify-content:center;
    font-weight:900; font-size:1.15rem; color:#fff;
    margin:0 auto 10px;
    box-shadow:0 0 22px rgba(124,58,237,0.45);
    position:relative; z-index:1;
    border:2px solid rgba(255,255,255,0.1);
}
.dev-name {
    font-weight:800; font-size:1rem; letter-spacing:-.01em;
    background:linear-gradient(90deg,#60a5fa,#c084fc);
    -webkit-background-clip:text; -webkit-text-fill-color:transparent;
    background-clip:text; margin-bottom:4px;
    position:relative; z-index:1;
}
.dev-role {
    display:inline-block;
    background:rgba(124,58,237,0.18);
    border:1px solid rgba(124,58,237,0.32);
    color:#a78bfa; border-radius:50px;
    padding:2px 12px; font-size:.67rem;
    font-weight:700; letter-spacing:.09em; text-transform:uppercase;
    position:relative; z-index:1; margin-bottom:8px;
}
.dev-skills {
    display:flex; flex-wrap:wrap; gap:4px;
    justify-content:center; margin-top:8px;
    position:relative; z-index:1;
}
.dev-skill-tag {
    background:rgba(37,99,235,0.15);
    border:1px solid rgba(37,99,235,0.25);
    color:#93c5fd; border-radius:4px;
    padding:1px 7px; font-size:.62rem; font-weight:600;
}

/* ── Slicer chips ────────────────────────────────────────────── */
.slicer-section {
    background:linear-gradient(145deg,#0d1028,#101424);
    border:1px solid rgba(37,99,235,0.15);
    border-radius:12px; padding:14px 16px; margin-bottom:14px;
}
.slicer-header {
    font-size:.68rem; font-weight:800; letter-spacing:.14em;
    text-transform:uppercase; color:#4f46e5;
    border-left:3px solid #4f46e5;
    padding-left:8px; margin-bottom:10px;
}

/* ── Metric row mini ─────────────────────────────────────────── */
.mini-metric {
    text-align:center;
    background:rgba(37,99,235,0.08);
    border:1px solid rgba(37,99,235,0.18);
    border-radius:10px; padding:12px 10px;
}
.mini-metric-label { font-size:.65rem; color:#475569; text-transform:uppercase; letter-spacing:.1em; margin-bottom:3px; }
.mini-metric-val   { font-family:'JetBrains Mono',monospace; font-size:1.3rem; font-weight:700; color:#60a5fa; }

/* ── Footer watermark ────────────────────────────────────────── */
.footer-watermark {
    text-align:center; padding:20px 0 8px;
    font-size:.72rem; color:#1e293b; line-height:1.9;
}
.footer-watermark .name {
    background:linear-gradient(90deg,#60a5fa,#a78bfa);
    -webkit-background-clip:text; -webkit-text-fill-color:transparent;
    background-clip:text; font-weight:700;
}
</style>
""", unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════════
# PLOTLY CHART HELPER
# ════════════════════════════════════════════════════════════════════
def apply_chart_theme(fig: go.Figure, height: int = 340) -> go.Figure:
    fig.update_layout(
        paper_bgcolor=PAPER_BG, plot_bgcolor=CHART_BG,
        font=dict(family="Inter", color=FONT_COLOR, size=11),
        height=height,
        margin=dict(l=8, r=8, t=28, b=8),
        legend=dict(bgcolor="rgba(0,0,0,0)",
                    bordercolor="rgba(255,255,255,0.07)", borderwidth=1,
                    font=dict(size=10)),
        xaxis=dict(gridcolor=GRID_COLOR, zerolinecolor=GRID_COLOR,
                   tickfont=dict(size=10), linecolor="rgba(255,255,255,0.05)"),
        yaxis=dict(gridcolor=GRID_COLOR, zerolinecolor=GRID_COLOR,
                   tickfont=dict(size=10), linecolor="rgba(255,255,255,0.05)"),
    )
    return fig


def cc(title: str, subtitle: str = "") -> None:
    """Chart card header."""
    st.markdown(
        f'<div class="chart-title">{title}</div>'
        f'<div class="chart-subtitle">{subtitle}</div>',
        unsafe_allow_html=True,
    )


def fmt(n: float) -> str:
    if abs(n) >= 1_000_000: return f"{n/1_000_000:.2f}M"
    if abs(n) >= 1_000:     return f"{n/1_000:.1f}K"
    return f"{n:,.0f}"


# ════════════════════════════════════════════════════════════════════
# DATA PIPELINE
# ════════════════════════════════════════════════════════════════════
@st.cache_data(show_spinner=False)
def load_file(file_bytes: bytes, file_name: str) -> pd.DataFrame:
    buf = io.BytesIO(file_bytes)
    if file_name.lower().endswith(".csv"):
        for enc in ["utf-8", "latin-1", "cp1252"]:
            try:
                buf.seek(0)
                return pd.read_csv(buf, encoding=enc)
            except Exception:
                continue
    elif file_name.lower().endswith((".xlsx", ".xls")):
        return pd.read_excel(buf)
    raise ValueError(f"Unsupported: {file_name}")


def smart_merge(dfs):
    if len(dfs) == 1:
        return dfs[0], "Single dataset loaded."
    common = set(dfs[0].columns)
    for d in dfs[1:]:
        common &= set(d.columns)
    if common:
        key = sorted(common, key=lambda c: dfs[0][c].nunique())[0]
        merged = dfs[0]
        for d in dfs[1:]:
            extra = list(set(d.columns) - set(merged.columns)) + [key]
            merged = pd.merge(merged, d[extra], on=key, how="outer")
        return merged, f"✅ Merged {len(dfs)} datasets on key `{key}`."
    if all(set(d.columns) == set(dfs[0].columns) for d in dfs[1:]):
        return pd.concat(dfs, ignore_index=True), f"✅ Stacked {len(dfs)} datasets vertically."
    return dfs[0], "⚠️ Could not auto-merge — using first dataset."


@st.cache_data(show_spinner=False)
def clean_data(df: pd.DataFrame):
    logs = []
    df = df.copy()

    orig = df.columns.tolist()
    df.columns = (df.columns.str.strip().str.lower()
                  .str.replace(r"[^\w]+", "_", regex=True).str.strip("_"))
    changed = sum(o != n for o, n in zip(orig, df.columns))
    if changed:
        logs.append(f"🔤 Normalised {changed} column name(s) → lowercase_underscore.")

    n_dupes = df.duplicated().sum()
    if n_dupes:
        df.drop_duplicates(inplace=True)
        logs.append(f"🗑️ Removed {n_dupes} duplicate row(s).")

    for col in df.select_dtypes(include="object").columns:
        sample = df[col].dropna().astype(str).head(200)
        if sample.str.match(r"^\d{1,4}[\-\/\.]\d{1,2}[\-\/\.]\d{1,4}").mean() > 0.55:
            try:
                df[col] = pd.to_datetime(df[col], infer_datetime_format=True, errors="coerce")
                logs.append(f"📅 Parsed `{col}` as datetime.")
            except Exception:
                pass

    for col in df.select_dtypes(include="object").columns:
        cleaned = df[col].astype(str).str.replace(r"[\$,€£%\s]", "", regex=True)
        num = pd.to_numeric(cleaned, errors="coerce")
        if num.notna().mean() > 0.80:
            df[col] = num
            logs.append(f"🔢 Converted `{col}` to numeric.")

    total_missing = df.isnull().sum().sum()
    for col in df.columns:
        miss = df[col].isnull().mean()
        if miss == 0: continue
        if miss > 0.60:
            df.drop(columns=[col], inplace=True)
            logs.append(f"🗑️ Dropped `{col}` ({miss*100:.0f}% missing).")
        elif pd.api.types.is_numeric_dtype(df[col]):
            df[col].fillna(df[col].median(), inplace=True)
        elif pd.api.types.is_datetime64_any_dtype(df[col]):
            df[col].fillna(method="ffill", inplace=True)
        else:
            mode = df[col].mode()
            df[col].fillna(mode[0] if len(mode) else "Unknown", inplace=True)

    filled = total_missing - df.isnull().sum().sum()
    if filled:
        logs.append(f"✅ Imputed {filled} missing value(s).")
    if not logs:
        logs.append("✅ Data was already clean — no changes needed.")
    return df, logs


def classify_columns(df: pd.DataFrame) -> dict:
    numeric, categorical, date_cols, high_card = [], [], [], []
    for col in df.columns:
        if pd.api.types.is_datetime64_any_dtype(df[col]): date_cols.append(col)
        elif pd.api.types.is_numeric_dtype(df[col]):      numeric.append(col)
        elif df[col].nunique() <= 50:                      categorical.append(col)
        else:                                              high_card.append(col)
    return dict(numeric=numeric, categorical=categorical, date=date_cols, high_card=high_card)


def smart_detect(df: pd.DataFrame, col_types: dict) -> dict:
    def best(patterns, pool):
        for p in patterns:
            for c in pool:
                if p in c.lower(): return c
        return None
    num = col_types["numeric"]
    cat = col_types["categorical"]
    dt  = col_types["date"]
    return {
        "amount":       best(["amount","sales","revenue","price","total"], num),
        "quantity":     best(["qty","quantity","units","count","volume"], num),
        "profit":       best(["profit","margin","gain","net"], num),
        "category":     best(["category","cat","segment","type","dept"], cat),
        "sub_category": best(["sub_cat","subcat","sub-cat","subcategory","product","item","name"], cat),
        "state":        best(["state","region","province","location","city","area"], cat),
        "payment":      best(["payment","pay_mode","pay_method","mode","method"], cat),
        "date":         dt[0] if dt else None,
    }


# ════════════════════════════════════════════════════════════════════
# CHART BUILDERS
# ════════════════════════════════════════════════════════════════════
def chart_hbar(df, cat_col, num_col, top_n=14):
    agg = df.groupby(cat_col)[num_col].sum().sort_values().tail(top_n).reset_index()
    fig = go.Figure(go.Bar(
        x=agg[num_col], y=agg[cat_col].astype(str), orientation="h",
        marker=dict(color=agg[num_col],
                    colorscale=[[0,"#1e3a8a"],[0.4,"#2563eb"],[1,"#06b6d4"]],
                    showscale=False, line=dict(width=0)),
        text=[fmt(v) for v in agg[num_col]],
        textposition="outside", textfont=dict(size=9, color="#94a3b8"),
    ))
    fig = apply_chart_theme(fig, height=max(300, len(agg)*30+60))
    fig.update_yaxes(tickfont=dict(size=10))
    return fig


def chart_donut(df, cat_col, num_col):
    agg = df.groupby(cat_col)[num_col].sum().reset_index()
    fig = go.Figure(go.Pie(
        labels=agg[cat_col].astype(str), values=agg[num_col], hole=0.64,
        marker=dict(colors=BAR_SEQ[:len(agg)], line=dict(color="#080b18", width=2.5)),
        textinfo="percent", textfont=dict(size=10, color="#e2e8f0"),
        hovertemplate="<b>%{label}</b><br>%{value:,.0f}<br>%{percent}<extra></extra>",
    ))
    fig.add_annotation(text=f"<b>{fmt(agg[num_col].sum())}</b>",
                       x=0.5, y=0.5, font=dict(size=15, color="#f1f5f9"), showarrow=False)
    fig = apply_chart_theme(fig, height=300)
    fig.update_layout(showlegend=True,
        legend=dict(orientation="v", yanchor="middle", y=0.5, xanchor="left", x=1.02))
    return fig


def chart_vbar_profit(df, cat_col, num_col):
    agg = df.groupby(cat_col)[num_col].sum().sort_values(ascending=False).head(12).reset_index()
    colors = [C_GREEN if v >= 0 else C_RED for v in agg[num_col]]
    fig = go.Figure(go.Bar(
        x=agg[cat_col].astype(str), y=agg[num_col],
        marker=dict(color=colors, line=dict(width=0)),
        text=[fmt(v) for v in agg[num_col]],
        textposition="outside", textfont=dict(size=9, color="#94a3b8"),
    ))
    fig = apply_chart_theme(fig, height=320)
    fig.update_xaxes(tickangle=-35)
    fig.add_hline(y=0, line_color="rgba(255,255,255,0.12)", line_width=1)
    return fig


def chart_line_monthly(df, date_col, num_col):
    tmp = df.copy()
    tmp["_m"] = tmp[date_col].dt.to_period("M").astype(str)
    agg = tmp.groupby("_m")[num_col].sum().reset_index().sort_values("_m")
    bar_col = [C_GREEN if v >= 0 else C_RED for v in agg[num_col]]
    fig = make_subplots(specs=[[{"secondary_y": False}]])
    fig.add_trace(go.Bar(x=agg["_m"], y=agg[num_col],
                         marker=dict(color=bar_col, opacity=0.72, line=dict(width=0)),
                         name=num_col.replace("_"," ").title()))
    fig.add_trace(go.Scatter(x=agg["_m"], y=agg[num_col], mode="lines+markers",
                             line=dict(color=C_CYAN, width=2.5),
                             marker=dict(size=5, color=C_CYAN), name="Trend"))
    fig = apply_chart_theme(fig, height=310)
    fig.update_xaxes(tickangle=-45, tickfont=dict(size=9))
    fig.add_hline(y=0, line_color="rgba(255,255,255,0.1)", line_width=1)
    return fig


def chart_pie_payment(df, pay_col, qty_col):
    val_col = qty_col if qty_col else df.select_dtypes(include="number").columns[0]
    agg = df.groupby(pay_col)[val_col].sum().reset_index()
    fig = go.Figure(go.Pie(
        labels=agg[pay_col].astype(str), values=agg[val_col],
        marker=dict(colors=BAR_SEQ[:len(agg)], line=dict(color="#080b18", width=2)),
        textinfo="label+percent", textfont=dict(size=10),
        hole=0.0, pull=[0.04]*len(agg),
    ))
    fig = apply_chart_theme(fig, height=300)
    fig.update_layout(showlegend=False)
    return fig


def chart_scatter(df, x_col, y_col, color_col=None):
    kwargs = dict(x=x_col, y=y_col, opacity=0.6,
                  hover_data=df.columns[:5].tolist(),
                  color_discrete_sequence=BAR_SEQ)
    if color_col:
        kwargs["color"] = color_col
    fig = px.scatter(df, **kwargs, template=PLOTLY_TEMPLATE)
    return apply_chart_theme(fig, height=320)


def chart_heatmap(df, num_cols):
    corr = df[num_cols].corr().round(2)
    fig = go.Figure(go.Heatmap(
        z=corr.values, x=corr.columns.tolist(), y=corr.index.tolist(),
        colorscale="RdBu_r", zmid=0,
        text=corr.values.round(2), texttemplate="%{text}", textfont=dict(size=9),
    ))
    n = len(num_cols)
    fig = apply_chart_theme(fig, height=max(260, n*38+60))
    fig.update_xaxes(tickangle=-45)
    return fig


def chart_treemap(df, path_cols, num_col):
    fig = px.treemap(df, path=path_cols, values=num_col, color=num_col,
                     color_continuous_scale=["#1e3a8a","#2563eb","#06b6d4"],
                     template=PLOTLY_TEMPLATE)
    return apply_chart_theme(fig, height=340)


def chart_area_trend(df, date_col, num_col):
    """Area chart — cumulative trend."""
    tmp = df.copy()
    tmp["_m"] = tmp[date_col].dt.to_period("M").astype(str)
    agg = tmp.groupby("_m")[num_col].sum().reset_index().sort_values("_m")
    fig = go.Figure(go.Scatter(
        x=agg["_m"], y=agg[num_col], fill="tozeroy",
        mode="lines+markers",
        line=dict(color=C_PURPLE, width=2.5),
        fillcolor="rgba(124,58,237,0.12)",
        marker=dict(size=5, color=C_PURPLE),
    ))
    fig = apply_chart_theme(fig, height=280)
    fig.update_xaxes(tickangle=-45, tickfont=dict(size=9))
    return fig


def chart_funnel(df, cat_col, num_col):
    """Funnel chart for category breakdown."""
    agg = df.groupby(cat_col)[num_col].sum().sort_values(ascending=False).head(8).reset_index()
    fig = go.Figure(go.Funnel(
        y=agg[cat_col].astype(str), x=agg[num_col],
        textinfo="value+percent total",
        marker=dict(color=BAR_SEQ[:len(agg)], line=dict(width=1, color="#080b18")),
        connector=dict(line=dict(color="rgba(255,255,255,0.1)", width=1)),
    ))
    fig = apply_chart_theme(fig, height=320)
    return fig


def chart_bubble(df, x_col, y_col, size_col, color_col=None):
    """Bubble chart."""
    kwargs = dict(x=x_col, y=y_col, size=size_col, opacity=0.7,
                  color_discrete_sequence=BAR_SEQ)
    if color_col:
        kwargs["color"] = color_col
    fig = px.scatter(df, **kwargs, template=PLOTLY_TEMPLATE,
                     size_max=55)
    return apply_chart_theme(fig, height=320)


# ════════════════════════════════════════════════════════════════════
# AI INSIGHTS
# ════════════════════════════════════════════════════════════════════
@st.cache_data(show_spinner=False, ttl=600)
def ai_insights(sample_json: str, stats_text: str) -> str:
    prompt = f"""You are a senior business intelligence analyst. Analyze this dataset and produce a sharp report.

Format EXACTLY as:

## 🏆 Top Performers
- [3 bullet points: highest-selling/profitable items with exact numbers]

## ⚠️ Problem Areas
- [2-3 bullet points: loss-making segments, anomalies, risks]

## 📈 Trends & Patterns
- [2-3 bullet points: trends, correlations, seasonality]

## 💡 Strategic Recommendations
- [3 specific, actionable recommendations]

## 📝 Executive Summary
[4 sentences summarising the dataset in plain English with numbers. Be specific and direct.]

DATA STATISTICS:
{stats_text}

SAMPLE (5 rows JSON):
{sample_json}

Rules: Be specific with numbers. No generic advice. Focus on what data actually shows."""

    try:
        resp = requests.post(
            "https://api.anthropic.com/v1/messages",
            headers={"Content-Type": "application/json"},
            json={
                "model": "claude-sonnet-4-20250514",
                "max_tokens": 1000,
                "messages": [{"role": "user", "content": prompt}],
            },
            timeout=30,
        )
        return resp.json()["content"][0]["text"]
    except Exception:
        return f"## 📊 Auto-Generated Insights\n\n{stats_text}\n\n> _AI unavailable — showing computed stats._"


def build_stats(df, col_types, role):
    lines = [
        f"Shape: {df.shape[0]:,} rows × {df.shape[1]} cols",
        f"Numeric: {col_types['numeric']}",
        f"Categorical: {col_types['categorical']}",
        f"Dates: {col_types['date']}",
        f"Missing: {df.isnull().sum().sum()}",
    ]
    num_df = df.select_dtypes(include="number")
    if not num_df.empty:
        lines += ["\nStats:", num_df.describe().round(2).to_string()]
    if role.get("category") and role.get("amount"):
        top = df.groupby(role["category"])[role["amount"]].sum().sort_values(ascending=False).head(5)
        lines.append(f"\nTop {role['category']} by {role['amount']}:\n{top.to_string()}")
    if role.get("sub_category") and role.get("profit"):
        worst = df.groupby(role["sub_category"])[role["profit"]].sum().sort_values().head(5)
        lines.append(f"\nWorst {role['sub_category']} by {role['profit']}:\n{worst.to_string()}")
    return "\n".join(lines)


def build_report(df, logs, merge_msg, insights, role):
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    lines = [
        "=" * 68,
        "   POWER BI STYLE AI SALES DASHBOARD — ANALYSIS REPORT",
        f"   Built by  : Ankit Prajapati",
        f"   Generated : {now}",
        "=" * 68,
        "",
        "── DATASET OVERVIEW ────────────────────────────────────────────",
        f"   Rows    : {len(df):,}",
        f"   Columns : {len(df.columns)}",
        f"   Missing : {df.isnull().sum().sum()}",
        f"   Merge   : {merge_msg}",
        "",
        "── CLEANING LOG ────────────────────────────────────────────────",
    ] + [f"   {l}" for l in logs] + [
        "",
        "── DESCRIPTIVE STATISTICS ──────────────────────────────────────",
        df.describe(include="all").round(2).to_string(),
        "",
        "── AI INSIGHTS ─────────────────────────────────────────────────",
        re.sub(r"[#*`]", "", insights),
        "",
        "=" * 68,
        "   © Ankit Prajapati — AI Sales Dashboard",
        "=" * 68,
    ]
    return "\n".join(lines)


# ════════════════════════════════════════════════════════════════════
# KPI RENDERER
# ════════════════════════════════════════════════════════════════════
def kpi(label, value, icon, card_cls, glow, delta="", neg=False):
    delta_cls  = "neg" if neg else ""
    delta_html = f'<div class="kpi-delta {delta_cls}">{delta}</div>' if delta else ""
    st.markdown(f"""
    <div class="kpi-card {card_cls} {glow}">
      <span class="kpi-icon">{icon}</span>
      <div class="kpi-label">{label}</div>
      <div class="kpi-value">{value}</div>
      {delta_html}
    </div>""", unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════════
# ── SIDEBAR ──────────────────────────────────────────────────────────
# ════════════════════════════════════════════════════════════════════
with st.sidebar:

    # ── App logo + dev profile ──────────────────────────────────────
    st.markdown("""
    <div class="profile-wrap">
      <div class="profile-logo">📊 AI Dashboard</div>
      <div class="profile-tagline">Power BI Style · v2.0</div>
      <div class="profile-divider"></div>

      <!-- Developer Card -->
      <div class="dev-card">
        <div class="dev-avatar">AP</div>
        <div class="dev-name">Ankit Prajapati</div>
        <div class="dev-role">Full Stack Developer</div>
        <div style="font-size:.72rem;color:#64748b;margin:4px 0 6px;position:relative;z-index:1;">
          🛠️ Built this dashboard with Python
        </div>
        <div class="dev-skills">
          <span class="dev-skill-tag">Python</span>
          <span class="dev-skill-tag">Streamlit</span>
          <span class="dev-skill-tag">Plotly</span>
          <span class="dev-skill-tag">Pandas</span>
          <span class="dev-skill-tag">Claude AI</span>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="section-label" style="margin:14px 16px 0;">📁 Data Upload</div>',
                unsafe_allow_html=True)
    uploaded = st.file_uploader(
        "Upload CSV / Excel",
        type=["csv", "xlsx", "xls"],
        accept_multiple_files=True,
        label_visibility="collapsed",
    )

    # Filters injected here after data loads
    st.markdown('<div class="section-label" style="margin:10px 16px 4px;">🎛️ Dashboard Filters</div>',
                unsafe_allow_html=True)
    filter_area = st.container()

    # Footer
    st.markdown("""
    <div class="footer-watermark">
      Built with ❤️ by<br>
      <span class="name">Ankit Prajapati</span><br>
      Streamlit · Plotly · Claude AI
    </div>
    """, unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════════
# HEADER BANNER
# ════════════════════════════════════════════════════════════════════
st.markdown("""
<div class="dash-header">
  <span class="dash-badge">✦ AI POWERED</span>
  <div class="dash-header-title" style="margin-top:10px;">
    Sales Intelligence Dashboard
  </div>
  <div class="dash-header-sub">
    Upload data → auto-cleaned → smart slicers → AI-powered charts & insights
  </div>
  <div class="dash-by">Designed &amp; built by <span>Ankit Prajapati</span></div>
</div>
""", unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════════
# EMPTY STATE
# ════════════════════════════════════════════════════════════════════
if not uploaded:
    c1, c2, c3, c4 = st.columns(4)
    for col, icon, title, body in [
        (c1, "🔀", "Auto Merge",     "Joins multiple files on common keys"),
        (c2, "🧹", "Smart Cleaning", "Fixes types, nulls, dupes automatically"),
        (c3, "🎛️", "Slicers",        "Filter charts by category, date, state, value"),
        (c4, "🤖", "AI Insights",    "Claude generates executive-level conclusions"),
    ]:
        with col:
            st.markdown(f"""
            <div class="kpi-card blue kpi-glow-blue" style="text-align:center;padding:28px 14px;">
              <div style="font-size:2.2rem;margin-bottom:10px;">{icon}</div>
              <div style="font-weight:800;margin-bottom:6px;">{title}</div>
              <div style="color:#475569;font-size:.82rem;line-height:1.5;">{body}</div>
            </div>""", unsafe_allow_html=True)

    st.info("👈 Upload one or more CSV / Excel files from the sidebar to launch the dashboard.", icon="💡")
    st.markdown("""
    <div style="text-align:center;margin-top:32px;color:#1e293b;font-size:.8rem;">
      Dashboard by <b style="color:#4f46e5;">Ankit Prajapati</b>
    </div>
    """, unsafe_allow_html=True)
    st.stop()


# ════════════════════════════════════════════════════════════════════
# LOAD → MERGE → CLEAN → CLASSIFY
# ════════════════════════════════════════════════════════════════════
raw_dfs = []
with st.spinner("📂 Loading files…"):
    for f in uploaded:
        try:
            raw_dfs.append(load_file(f.read(), f.name))
        except Exception as e:
            st.error(f"Could not load **{f.name}**: {e}")
if not raw_dfs:
    st.stop()

merged_df, merge_msg = smart_merge(raw_dfs)
with st.spinner("🧹 Cleaning data…"):
    df, clean_logs = clean_data(merged_df)

col_types = classify_columns(df)
role      = smart_detect(df, col_types)


# ════════════════════════════════════════════════════════════════════
# SIDEBAR — SLICERS (dynamic)
# ════════════════════════════════════════════════════════════════════
with filter_area:
    filtered_df = df.copy()

    # ── Categorical slicers ─────────────────────────────────────────
    for slicer_role, emoji in [("category", "📦"), ("sub_category", "🏷️"), ("state", "🗺️"), ("payment", "💳")]:
        col_name = role.get(slicer_role)
        if col_name and col_name in filtered_df.columns:
            label = col_name.replace("_", " ").title()
            st.markdown(f'<div class="slicer-header">{emoji} {label}</div>', unsafe_allow_html=True)
            opts = sorted(df[col_name].dropna().unique().tolist())
            # show "All" checkbox first
            all_on = st.checkbox(f"All {label}", value=True, key=f"all_{slicer_role}")
            if not all_on:
                sel = st.multiselect(f"Select {label}", opts, default=opts[:3], key=f"ms_{slicer_role}",
                                     label_visibility="collapsed")
                if sel:
                    filtered_df = filtered_df[filtered_df[col_name].isin(sel)]

    # ── Date range slicer ───────────────────────────────────────────
    if role["date"] and role["date"] in filtered_df.columns:
        st.markdown('<div class="slicer-header">📅 Date Range</div>', unsafe_allow_html=True)
        min_d = df[role["date"]].dropna().min().date()
        max_d = df[role["date"]].dropna().max().date()
        dr = st.date_input("Date range", value=[min_d, max_d],
                           min_value=min_d, max_value=max_d,
                           label_visibility="collapsed")
        if len(dr) == 2:
            filtered_df = filtered_df[
                (filtered_df[role["date"]] >= pd.Timestamp(dr[0])) &
                (filtered_df[role["date"]] <= pd.Timestamp(dr[1]))
            ]

        # Quarter slicer
        st.markdown('<div class="slicer-header">🗓️ Quarter</div>', unsafe_allow_html=True)
        quarters = ["All", "Q1 (Jan–Mar)", "Q2 (Apr–Jun)", "Q3 (Jul–Sep)", "Q4 (Oct–Dec)"]
        sel_q = st.selectbox("Quarter", quarters, label_visibility="collapsed")
        if sel_q != "All":
            q_map = {"Q1 (Jan–Mar)": [1,2,3], "Q2 (Apr–Jun)": [4,5,6],
                     "Q3 (Jul–Sep)": [7,8,9],  "Q4 (Oct–Dec)": [10,11,12]}
            filtered_df = filtered_df[filtered_df[role["date"]].dt.month.isin(q_map[sel_q])]

    # ── Numeric range slicer ────────────────────────────────────────
    if role["amount"] and role["amount"] in filtered_df.columns:
        col_n = role["amount"]
        st.markdown(f'<div class="slicer-header">💰 {col_n.replace("_"," ").title()} Range</div>',
                    unsafe_allow_html=True)
        mn = float(df[col_n].min())
        mx = float(df[col_n].max())
        if mn < mx:
            rng = st.slider("Amount range", mn, mx, (mn, mx),
                            format="%.0f", label_visibility="collapsed",
                            key="slider_amount")
            filtered_df = filtered_df[
                (filtered_df[col_n] >= rng[0]) & (filtered_df[col_n] <= rng[1])
            ]

    # ── Top-N slicer ────────────────────────────────────────────────
    st.markdown('<div class="slicer-header">🔢 Top N Records</div>', unsafe_allow_html=True)
    top_n = st.select_slider("Top N", options=[50, 100, 500, 1000, 5000, 10000, "All"],
                             value="All", label_visibility="collapsed")
    if top_n != "All":
        filtered_df = filtered_df.head(int(top_n))

fdf = filtered_df


# ════════════════════════════════════════════════════════════════════
# MAIN SLICER BAR (top of dashboard — quick chips)
# ════════════════════════════════════════════════════════════════════
st.markdown(f"""
<div class="slicer-section">
  <div class="slicer-header" style="margin-bottom:6px;">⚡ Active Filters</div>
  <div style="font-size:.8rem;color:#64748b;">
    Showing <b style="color:#60a5fa;">{len(fdf):,}</b> of
    <b style="color:#a78bfa;">{len(df):,}</b> records
    &nbsp;·&nbsp;
    {len(col_types['numeric'])} numeric &nbsp;·&nbsp;
    {len(col_types['categorical'])} categorical
    {f'&nbsp;·&nbsp; 📅 date: <b style="color:#34d399;">{role["date"]}</b>' if role["date"] else ''}
  </div>
</div>
""", unsafe_allow_html=True)


# ════════════════════════════════════════════════════════════════════
# TABS
# ════════════════════════════════════════════════════════════════════
tab_dash, tab_slicer, tab_data, tab_insights = st.tabs([
    "📊 Dashboard",
    "🎛️ Advanced Slicers",
    "🗂️ Data & Cleaning",
    "🤖 AI Insights",
])


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# TAB 1 — DASHBOARD
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
with tab_dash:

    # ── KPI row ─────────────────────────────────────────────────────
    kc1, kc2, kc3, kc4 = st.columns(4)
    with kc1:
        val = fmt(fdf[role["amount"]].sum()) if role["amount"] else "N/A"
        kpi("Total Sales", val, "💰", "blue", "kpi-glow-blue", "▲ Auto-detected")
    with kc2:
        val = fmt(fdf[role["quantity"]].sum()) if role["quantity"] else "N/A"
        kpi("Total Quantity", val, "📦", "purple", "kpi-glow-purple", "▲ Sum of units")
    with kc3:
        if role["profit"]:
            pv = fdf[role["profit"]].sum()
            kpi("Total Profit", fmt(pv), "📈", "gold", "kpi-glow-gold",
                f"{'▼ Net loss' if pv < 0 else '▲ Net profit'}", neg=pv < 0)
        else:
            others = [c for c in col_types["numeric"] if c not in [role["amount"], role["quantity"]]]
            kpi(others[0].replace("_"," ").title() if others else "Metric",
                fmt(fdf[others[0]].sum()) if others else "N/A",
                "📊", "gold", "kpi-glow-gold")
    with kc4:
        ulabel = role["category"] or role["sub_category"]
        if ulabel:
            kpi(f"Unique {ulabel.replace('_',' ').title()}", str(fdf[ulabel].nunique()),
                "🏷️", "teal", "kpi-glow-teal", f"{len(fdf):,} rows filtered")
        else:
            kpi("Total Rows", f"{len(fdf):,}", "📋", "teal", "kpi-glow-teal")

    st.markdown("<div style='margin:16px 0 4px;'></div>", unsafe_allow_html=True)

    # ── Row 2: Hbar + Donut ─────────────────────────────────────────
    r2a, r2b = st.columns([1.55, 1])

    with r2a:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        if role["sub_category"] and role["amount"]:
            cc(f"Sum of {role['amount'].replace('_',' ').title()} by {role['sub_category'].replace('_',' ').title()}", "Top 14 sub-categories")
            st.plotly_chart(chart_hbar(fdf, role["sub_category"], role["amount"]),
                            use_container_width=True, config={"displayModeBar": False}, key="hbar_1")
        elif col_types["categorical"] and col_types["numeric"]:
            c, n = col_types["categorical"][0], col_types["numeric"][0]
            cc(f"Sum of {n.replace('_',' ').title()} by {c.replace('_',' ').title()}")
            st.plotly_chart(chart_hbar(fdf, c, n), use_container_width=True,
                            config={"displayModeBar": False}, key="hbar_2")
        else:
            st.info("No categorical + numeric columns for bar chart.")
        st.markdown("</div>", unsafe_allow_html=True)

    with r2b:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        if role["category"] and role["quantity"]:
            cc(f"Sum of Quantity by Category", "Category share")
            st.plotly_chart(chart_donut(fdf, role["category"], role["quantity"]),
                            use_container_width=True, config={"displayModeBar": False}, key="donut_1")
        elif role["category"] and role["amount"]:
            cc(f"Sum of Amount by Category")
            st.plotly_chart(chart_donut(fdf, role["category"], role["amount"]),
                            use_container_width=True, config={"displayModeBar": False}, key="donut_2")
        elif col_types["categorical"] and col_types["numeric"]:
            c, n = col_types["categorical"][0], col_types["numeric"][0]
            cc(f"{n.replace('_',' ').title()} by {c.replace('_',' ').title()}")
            st.plotly_chart(chart_donut(fdf, c, n), use_container_width=True,
                            config={"displayModeBar": False}, key="donut_3")
        else:
            st.info("Insufficient data for donut chart.")
        st.markdown("</div>", unsafe_allow_html=True)

    # ── Row 3: Profit vbar + Monthly line ───────────────────────────
    r3a, r3b = st.columns([1.2, 1])

    with r3a:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        if role["sub_category"] and role["profit"]:
            cc(f"Profit by {role['sub_category'].replace('_',' ').title()}", "🟢 Profit  🔴 Loss")
            st.plotly_chart(chart_vbar_profit(fdf, role["sub_category"], role["profit"]),
                            use_container_width=True, config={"displayModeBar": False}, key="vbar_1")
        elif col_types["categorical"] and col_types["numeric"]:
            c = col_types["categorical"][0]; n = col_types["numeric"][-1]
            cc(f"{n.replace('_',' ').title()} by {c.replace('_',' ').title()}")
            st.plotly_chart(chart_vbar_profit(fdf, c, n), use_container_width=True,
                            config={"displayModeBar": False}, key="vbar_2")
        else:
            st.info("No data for profit chart.")
        st.markdown("</div>", unsafe_allow_html=True)

    with r3b:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        if role["date"] and role["profit"]:
            cc("Profit by Month", "Bar + line combo trend")
            st.plotly_chart(chart_line_monthly(fdf, role["date"], role["profit"]),
                            use_container_width=True, config={"displayModeBar": False}, key="line_1")
        elif role["date"] and role["amount"]:
            cc("Sales by Month", "Monthly revenue trend")
            st.plotly_chart(chart_line_monthly(fdf, role["date"], role["amount"]),
                            use_container_width=True, config={"displayModeBar": False}, key="line_2")
        elif role["payment"]:
            cc(f"Quantity by {role['payment'].replace('_',' ').title()}", "Payment mode distribution")
            st.plotly_chart(chart_pie_payment(fdf, role["payment"], role["quantity"]),
                            use_container_width=True, config={"displayModeBar": False}, key="pie_r3")
        else:
            st.info("No date/payment column for this chart.")
        st.markdown("</div>", unsafe_allow_html=True)

    # ── Row 4: Payment pie + Area trend ─────────────────────────────
    r4a, r4b = st.columns([1, 1.2])

    with r4a:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        if role["payment"]:
            cc(f"Qty by {role['payment'].replace('_',' ').title()}", "Payment method split")
            st.plotly_chart(chart_pie_payment(fdf, role["payment"], role["quantity"]),
                            use_container_width=True, config={"displayModeBar": False}, key="pie_r4")
        elif len(col_types["numeric"]) >= 2 and col_types["categorical"]:
            x, y = col_types["numeric"][0], col_types["numeric"][1]
            cc(f"Scatter: {x} vs {y}")
            st.plotly_chart(chart_scatter(fdf, x, y, col_types["categorical"][0]),
                            use_container_width=True, config={"displayModeBar": False}, key="scatter_r4")
        else:
            st.info("No payment data available.")
        st.markdown("</div>", unsafe_allow_html=True)

    with r4b:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        if role["date"] and role["amount"]:
            cc("Cumulative Revenue Trend", "Area chart — monthly")
            st.plotly_chart(chart_area_trend(fdf, role["date"], role["amount"]),
                            use_container_width=True, config={"displayModeBar": False}, key="area_r4")
        elif len(col_types["numeric"]) >= 2:
            cc("Correlation Heatmap", "Numeric column relationships")
            st.plotly_chart(chart_heatmap(fdf, col_types["numeric"][:8]),
                            use_container_width=True, config={"displayModeBar": False}, key="heat_r4b")
        else:
            st.info("No data for area/heatmap chart.")
        st.markdown("</div>", unsafe_allow_html=True)

    # ── Row 5: Heatmap + Funnel ──────────────────────────────────────
    r5a, r5b = st.columns([1.2, 1])

    with r5a:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        if len(col_types["numeric"]) >= 2:
            cc("Correlation Heatmap", "Strength of relationships")
            st.plotly_chart(chart_heatmap(fdf, col_types["numeric"][:8]),
                            use_container_width=True, config={"displayModeBar": False}, key="heat_r5")
        else:
            st.info("Need 2+ numeric columns.")
        st.markdown("</div>", unsafe_allow_html=True)

    with r5b:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        if role["category"] and role["amount"]:
            cc(f"Funnel: {role['amount'].replace('_',' ').title()} by {role['category'].replace('_',' ').title()}", "Top-to-bottom contribution")
            st.plotly_chart(chart_funnel(fdf, role["category"], role["amount"]),
                            use_container_width=True, config={"displayModeBar": False}, key="funnel_r5")
        elif col_types["categorical"] and col_types["numeric"]:
            c, n = col_types["categorical"][0], col_types["numeric"][0]
            cc(f"Funnel: {n.replace('_',' ').title()} by {c.replace('_',' ').title()}")
            st.plotly_chart(chart_funnel(fdf, c, n), use_container_width=True,
                            config={"displayModeBar": False}, key="funnel_r5b")
        else:
            st.info("No data for funnel chart.")
        st.markdown("</div>", unsafe_allow_html=True)

    # ── Row 6: Treemap ───────────────────────────────────────────────
    if role["category"] and role["sub_category"] and role["amount"]:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        cc("Revenue Treemap", f"{role['category']} → {role['sub_category']} hierarchy")
        st.plotly_chart(
            chart_treemap(fdf, [role["category"], role["sub_category"]], role["amount"]),
            use_container_width=True, config={"displayModeBar": False}, key="treemap_r6",
        )
        st.markdown("</div>", unsafe_allow_html=True)

    # ── Row 7: Bubble (if 3 numeric) ────────────────────────────────
    num_c = col_types["numeric"]
    if len(num_c) >= 3:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        x, y, sz = num_c[0], num_c[1], num_c[2]
        cc(f"Bubble Chart: {x} vs {y} (size={sz})", "Multi-variable relationship")
        fdf_b = fdf.copy()
        fdf_b[sz] = fdf_b[sz].clip(lower=0)        # bubble size must be ≥ 0
        col_arg = role["category"] if role["category"] else None
        st.plotly_chart(chart_bubble(fdf_b, x, y, sz, col_arg),
                        use_container_width=True, config={"displayModeBar": False}, key="bubble_r7")
        st.markdown("</div>", unsafe_allow_html=True)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# TAB 2 — ADVANCED SLICERS (interactive pivot-style)
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
with tab_slicer:
    st.markdown('<p class="chart-title" style="margin-bottom:12px;">🎛️ Custom Chart Builder — Pick any columns</p>', unsafe_allow_html=True)

    sb1, sb2, sb3 = st.columns(3)
    with sb1:
        x_axis = st.selectbox("X-Axis (Category)", col_types["categorical"] + col_types["date"],
                              key="adv_x")
    with sb2:
        y_axis = st.selectbox("Y-Axis (Metric)", col_types["numeric"], key="adv_y")
    with sb3:
        chart_type = st.selectbox("Chart Type",
                                  ["Bar (Vertical)", "Bar (Horizontal)", "Donut", "Line", "Scatter", "Funnel"],
                                  key="adv_type")

    color_by = None
    if col_types["categorical"]:
        color_by = st.selectbox("Colour by (optional)",
                                ["None"] + col_types["categorical"], key="adv_color")
        color_by = None if color_by == "None" else color_by

    if x_axis and y_axis:
        st.markdown('<div class="chart-card">', unsafe_allow_html=True)
        cc(f"{chart_type}: {y_axis.replace('_',' ').title()} by {x_axis.replace('_',' ').title()}")
        if chart_type == "Bar (Vertical)":
            agg2 = fdf.groupby(x_axis)[y_axis].sum().reset_index().sort_values(y_axis, ascending=False).head(20)
            colors2 = [C_GREEN if v >= 0 else C_RED for v in agg2[y_axis]]
            f2 = go.Figure(go.Bar(x=agg2[x_axis].astype(str), y=agg2[y_axis],
                                  marker=dict(color=colors2, line=dict(width=0)),
                                  text=[fmt(v) for v in agg2[y_axis]], textposition="outside",
                                  textfont=dict(size=9, color="#94a3b8")))
            f2 = apply_chart_theme(f2)
            f2.update_xaxes(tickangle=-35)
        elif chart_type == "Bar (Horizontal)":
            f2 = chart_hbar(fdf, x_axis, y_axis)
        elif chart_type == "Donut":
            f2 = chart_donut(fdf, x_axis, y_axis)
        elif chart_type == "Line":
            agg2 = fdf.groupby(x_axis)[y_axis].sum().reset_index().sort_values(x_axis)
            f2 = go.Figure(go.Scatter(x=agg2[x_axis].astype(str), y=agg2[y_axis],
                                      mode="lines+markers",
                                      line=dict(color=C_CYAN, width=2.5),
                                      marker=dict(size=5)))
            f2 = apply_chart_theme(f2)
        elif chart_type == "Scatter":
            f2 = chart_scatter(fdf, x_axis, y_axis, color_by)
        else:  # Funnel
            f2 = chart_funnel(fdf, x_axis, y_axis)
        st.plotly_chart(f2, use_container_width=True, config={"displayModeBar": False}, key="adv_chart")
        st.markdown("</div>", unsafe_allow_html=True)

    # ── Pivot table slicer ────────────────────────────────────────
    st.markdown('<p class="chart-title" style="margin:18px 0 8px;">📐 Pivot Table</p>', unsafe_allow_html=True)
    pv1, pv2, pv3 = st.columns(3)
    with pv1:
        pivot_rows = st.selectbox("Rows", col_types["categorical"], key="pv_rows")
    with pv2:
        pivot_vals = st.selectbox("Values", col_types["numeric"], key="pv_vals")
    with pv3:
        pivot_agg = st.selectbox("Aggregation", ["Sum", "Mean", "Count", "Max", "Min"], key="pv_agg")
    if pivot_rows and pivot_vals:
        agg_fn = {"Sum": "sum","Mean": "mean","Count": "count","Max": "max","Min": "min"}[pivot_agg]
        pivot_df = fdf.groupby(pivot_rows)[pivot_vals].agg(agg_fn).round(2).reset_index()
        pivot_df.columns = [pivot_rows, f"{pivot_agg} of {pivot_vals}"]
        pivot_df = pivot_df.sort_values(f"{pivot_agg} of {pivot_vals}", ascending=False)
        st.dataframe(pivot_df, use_container_width=True, height=280)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# TAB 3 — DATA & CLEANING
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
with tab_data:
    st.markdown(f'<div class="insight-card success">🔗 {merge_msg}</div>', unsafe_allow_html=True)
    st.markdown('<p class="chart-title" style="margin-top:18px;">🧹 Cleaning Log</p>', unsafe_allow_html=True)
    for log in clean_logs:
        cls = "success" if "✅" in log else "warning" if "⚠️" in log else ""
        st.markdown(f'<div class="insight-card {cls}">{log}</div>', unsafe_allow_html=True)

    st.markdown('<p class="chart-title" style="margin-top:20px;">📋 Data Preview (first 200 rows)</p>', unsafe_allow_html=True)
    st.dataframe(fdf.head(200), use_container_width=True, height=300)

    st.markdown('<p class="chart-title" style="margin-top:20px;">📈 Descriptive Statistics</p>', unsafe_allow_html=True)
    num_df = fdf.select_dtypes(include="number")
    if not num_df.empty:
        st.dataframe(num_df.describe().round(2), use_container_width=True)
    else:
        st.info("No numeric columns.")

    st.markdown('<p class="chart-title" style="margin-top:20px;">🏷️ Column Classification</p>', unsafe_allow_html=True)
    type_rows = []
    for c in fdf.columns:
        kind = ("📅 Date" if c in col_types["date"] else
                "🔢 Numeric" if c in col_types["numeric"] else
                "🏷️ Categorical" if c in col_types["categorical"] else "📝 Text")
        type_rows.append({"Column": c, "Dtype": str(fdf[c].dtype), "Kind": kind,
                          "Unique": fdf[c].nunique(), "Missing": int(fdf[c].isnull().sum())})
    st.dataframe(pd.DataFrame(type_rows), use_container_width=True)

    st.markdown('<p class="chart-title" style="margin-top:20px;">⬇️ Export</p>', unsafe_allow_html=True)
    dc1, dc2 = st.columns(2)
    with dc1:
        st.download_button("⬇️ Cleaned Dataset (CSV)", fdf.to_csv(index=False).encode("utf-8"),
                           "cleaned_data.csv", "text/csv", use_container_width=True)
    with dc2:
        rep = build_report(fdf, clean_logs, merge_msg, "See AI Insights tab.", role)
        st.download_button("⬇️ Summary Report (.txt)", rep.encode("utf-8"),
                           "analysis_report.txt", "text/plain", use_container_width=True)


# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# TAB 4 — AI INSIGHTS
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
with tab_insights:
    pc = st.columns(4)
    for col_w, label, val in zip(pc, ["Rows","Columns","Numeric","Categories"],
                                 [f"{len(fdf):,}", str(len(fdf.columns)),
                                  str(len(col_types["numeric"])), str(len(col_types["categorical"]))]):
        with col_w:
            st.markdown(f"""
            <div class="mini-metric">
              <div class="mini-metric-label">{label}</div>
              <div class="mini-metric-val">{val}</div>
            </div>""", unsafe_allow_html=True)

    st.markdown("<div style='margin:18px 0 6px;'></div>", unsafe_allow_html=True)
    st.markdown('<p class="chart-title">🤖 Claude AI Analysis</p>', unsafe_allow_html=True)

    with st.spinner("🧠 Claude is analysing your data…"):
        stats_txt   = build_stats(fdf, col_types, role)
        sample_json = fdf.head(5).to_json(orient="records", date_format="iso", default_handler=str)
        insights    = ai_insights(sample_json, stats_txt)

    st.markdown('<div class="conclusion-box">', unsafe_allow_html=True)
    st.markdown(insights)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div style='margin-top:18px;'></div>", unsafe_allow_html=True)
    report_full = build_report(fdf, clean_logs, merge_msg, insights, role)
    st.download_button("⬇️ Download Full Report with AI Insights (.txt)",
                       report_full.encode("utf-8"), "full_report_ankit.txt",
                       "text/plain", use_container_width=True)

    # Watermark
    st.markdown("""
    <div style="text-align:center;margin-top:30px;padding:16px;
                border-top:1px solid rgba(255,255,255,0.04);">
      <div style="font-size:.78rem;color:#1e293b;">
        Dashboard designed &amp; built by
        <b style="background:linear-gradient(90deg,#60a5fa,#a78bfa);
                  -webkit-background-clip:text;-webkit-text-fill-color:transparent;
                  background-clip:text;font-size:.88rem;">Ankit Prajapati</b>
      </div>
      <div style="font-size:.68rem;color:#0f172a;margin-top:3px;">
        Streamlit · Plotly · Pandas · Claude AI
      </div>
    </div>
    """, unsafe_allow_html=True)