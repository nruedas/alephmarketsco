import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from pathlib import Path

st.set_page_config(page_title="AlephMarketsCO", page_icon="📊", layout="wide")

BASE_DIR = Path(__file__).parent

# ──────────────────────────────────────────────────────────────────────────────
# ESTILOS
# ──────────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    .stApp { background-color: #080c0e; color: #d4d4d4; }
    [data-testid="stSidebar"] { background-color: #0a0f11; border-right: 1px solid #1a2a1e; }
    .stRadio label { color: #7a9a80 !important; font-size: 0.88rem !important; }

    .logo-text  { font-size: 1.6rem; font-weight: 800; letter-spacing: -0.03em; line-height: 1.1; }
    .logo-aleph { color: #2ecc71; }
    .logo-co    { color: #2ecc71; }
    .logo-by    { font-size: 0.78rem; color: #4a7050; margin-top: 4px; }

    .page-title    { font-size: 1.55rem; font-weight: 700; color: #ffffff; letter-spacing: -0.02em; }
    .page-subtitle { font-size: 0.83rem; color: #3a5a40; margin-top: 3px; margin-bottom: 16px;
                     border-bottom: 1px solid #1a2a1e; padding-bottom: 14px; }

    .banner-estimado {
        background: #0f130f; border: 1px solid #2a3a2a; border-left: 3px solid #4a7050;
        border-radius: 8px; padding: 10px 16px; margin-bottom: 20px;
        font-size: 0.78rem; color: #6a8a6a; line-height: 1.6;
    }
    .banner-estimado strong { color: #8ab08a; }

    .card       { background:#0d1610; border-radius:12px; padding:20px 24px; margin-bottom:10px;
                  border-left:3px solid #2ecc71; border-top:1px solid #1a2a1e;
                  border-right:1px solid #1a2a1e; border-bottom:1px solid #1a2a1e; }
    .card-miss  { background:#0d1610; border-radius:12px; padding:20px 24px; margin-bottom:10px;
                  border-left:3px solid #e74c3c; border-top:1px solid #1a2a1e;
                  border-right:1px solid #1a2a1e; border-bottom:1px solid #1a2a1e; }
    .card-neutral { background:#0d1610; border-radius:12px; padding:20px 24px; margin-bottom:10px;
                  border-left:3px solid #4a7050; border-top:1px solid #1a2a1e;
                  border-right:1px solid #1a2a1e; border-bottom:1px solid #1a2a1e; }

    .card-header  { display:flex; justify-content:space-between; align-items:flex-start; margin-bottom:4px; }
    .empresa-nombre { font-size:1.1rem; font-weight:700; color:#ffffff; }
    .empresa-meta   { font-size:0.73rem; color:#3a5a40; margin-top:2px; }

    .badge-beat { background:#0d2a14; color:#2ecc71; border:1px solid #1a4a24;
                  border-radius:20px; padding:3px 12px; font-size:0.72rem; font-weight:600; }
    .badge-miss { background:#2a0d0d; color:#e74c3c; border:1px solid #4a1a1a;
                  border-radius:20px; padding:3px 12px; font-size:0.72rem; font-weight:600; }
    .badge-linea{ background:#0d1a20; color:#5a9abf; border:1px solid #1a3a4a;
                  border-radius:20px; padding:3px 12px; font-size:0.72rem; font-weight:600; }
    .badge-na   { background:#141414; color:#4a4a4a; border:1px solid #2a2a2a;
                  border-radius:20px; padding:3px 12px; font-size:0.72rem; font-weight:600; }

    .metrics-row  { display:flex; gap:28px; margin-top:14px; flex-wrap:wrap; align-items:flex-start; }
    .metric-box   { display:flex; flex-direction:column; gap:3px; min-width:88px; }
    .metric-label { font-size:0.63rem; color:#3a5a40; text-transform:uppercase; letter-spacing:0.1em; }
    .metric-value { font-size:1rem; font-weight:600; color:#e8e8e8; }
    .yoy-pos { font-size:0.76rem; color:#2ecc71; font-weight:600; }
    .yoy-neg { font-size:0.76rem; color:#e74c3c; font-weight:600; }
    .yoy-neu { font-size:0.76rem; color:#5a9abf; font-weight:600; }
    .divider-metric { width:1px; background:#1a2a1e; align-self:stretch; min-height:40px; margin:0 4px; }

    .nr-box { margin-top:10px; padding:8px 12px; background:#0a1008; border-radius:6px;
              font-size:0.76rem; color:#4a6a4a; border-left:2px solid #2a3a2a; }
    .nr-label { color:#6a9a6a; font-weight:600; }

    .guidance-box   { margin-top:12px; padding:8px 12px; background:#080c0e; border-radius:6px;
                      font-size:0.79rem; color:#4a7050; border-left:2px solid #1a3a20; }
    .guidance-label { color:#2ecc71; font-weight:500; }

    .summary-card { background:#0d1610; border-radius:10px; padding:18px 20px; text-align:center;
                    border:1px solid #1a2a1e; }
    .big-num   { font-size:1.9rem; font-weight:700; color:#fff; }
    .sum-label { font-size:0.68rem; color:#3a5a40; text-transform:uppercase; letter-spacing:0.1em; margin-top:5px; }

    .rank-item   { display:flex; align-items:center; gap:14px; padding:11px 15px;
                   background:#0d1610; border-radius:9px; margin-bottom:7px; border:1px solid #1a2a1e; }
    .rank-gold   { font-size:1rem; font-weight:700; color:#f1c40f; width:26px; }
    .rank-silver { font-size:1rem; font-weight:700; color:#95a5a6; width:26px; }
    .rank-bronze { font-size:1rem; font-weight:700; color:#a04000; width:26px; }
    .rank-num    { font-size:1rem; font-weight:700; color:#3a5a40; width:26px; }
    .rank-empresa { font-weight:600; color:#e8e8e8; font-size:0.88rem; }
    .rank-sector  { font-size:0.72rem; color:#3a5a40; }
    .rank-valor   { font-size:0.95rem; font-weight:700; color:#2ecc71; margin-left:auto; }

    .footer { text-align:center; color:#1a3a20; font-size:0.73rem;
              padding:20px 0 6px 0; border-top:1px solid #1a2a1e; margin-top:40px; }
    .footer a { color:#2ecc71; text-decoration:none; }
</style>
""", unsafe_allow_html=True)

# ──────────────────────────────────────────────────────────────────────────────
# CARGA DE DATOS
# ──────────────────────────────────────────────────────────────────────────────
NUM_COLS = ["Ingresos_Real","Utilidad_Neta_Real","EBITDA_Real",
            "Margen_EBITDA_Pct","Margen_Neto_Pct","Utilidad_Ajustada"]

@st.cache_data
def cargar_2025():
    df = pd.read_csv(BASE_DIR / "resultados_bvc_2025.csv")
    for c in NUM_COLS:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors="coerce")
    return df

@st.cache_data
def cargar_2024():
    try:
        df = pd.read_csv(BASE_DIR / "resultados_bvc_2024.csv")
        for c in NUM_COLS:
            if c in df.columns:
                df[c] = pd.to_numeric(df[c], errors="coerce")
        return df
    except:
        return None

df   = cargar_2025()
df24 = cargar_2024()

# ──────────────────────────────────────────────────────────────────────────────
# HELPERS
# ──────────────────────────────────────────────────────────────────────────────
def fmt(val, suffix="B"):
    if pd.isna(val): return "N/D"
    return f"${val:,.2f}{suffix}"

def fmt_pct(val):
    if pd.isna(val): return "N/D"
    return f"{val:.1f}%"

def yoy_class(s):
    if not isinstance(s, str): return "yoy-neu"
    s = s.strip()
    if s.startswith("+"): return "yoy-pos"
    if s.startswith("-"): return "yoy-neg"
    return "yoy-neu"

def badge_html(supero):
    s = str(supero).strip() if pd.notna(supero) else ""
    if s.lower() in ["sí","si","yes","true"]:
        return '<span class="badge-beat">✓ Superó expectativas</span>'
    elif s.lower() in ["no","false"]:
        return '<span class="badge-miss">✗ No superó</span>'
    elif "línea" in s.lower() or "linea" in s.lower():
        return '<span class="badge-linea">~ En línea</span>'
    return '<span class="badge-na">Sin datos</span>'

def card_class(supero):
    s = str(supero).strip() if pd.notna(supero) else ""
    if s.lower() in ["sí","si","yes","true"]: return "card"
    if s.lower() in ["no","false"]:           return "card-miss"
    return "card-neutral"

# ──────────────────────────────────────────────────────────────────────────────
# SIDEBAR
# ──────────────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div class="logo-text">
        <span class="logo-aleph">Aleph</span><span style="color:#fff">Markets</span><span class="logo-co">CO</span>
    </div>
    <div class="logo-by">by Nicolas Rueda</div>
    <div style="margin-top:10px; display:flex; gap:8px;">
        <a href="https://github.com/nruedas" target="_blank"
           style="font-size:0.73rem;color:#2ecc71;text-decoration:none;border:1px solid #1a3a20;border-radius:5px;padding:2px 8px;">GitHub</a>
        <a href="https://linkedin.com/in/nicolas-rueda-segura-599533379" target="_blank"
           style="font-size:0.73rem;color:#2ecc71;text-decoration:none;border:1px solid #1a3a20;border-radius:5px;padding:2px 8px;">LinkedIn</a>
    </div>
    <hr style="border-color:#1a2a1e; margin:18px 0 14px 0;">
    """, unsafe_allow_html=True)

    pagina = st.radio("Navegación", [
        "📋 Resumen",
        "🏢 Resultados 2025",
        "📊 Resultados 2024",
        "📈 Comparativo YoY",
        "🏆 Rankings",
        "⚔️ Comparador",
    ])

# Banner general estimados — aparece en todas las páginas
BANNER = """
<div class="banner-estimado">
    <strong>⚠ Datos estimados / compilados</strong> — Las cifras provienen de comunicados oficiales,
    estimaciones de analistas y cálculo propio. Algunas empresas no han publicado resultados completos
    al corte (<strong>5 mar 2026</strong>). Este dashboard es un <strong>proyecto en construcción</strong>;
    los datos se actualizarán a medida que las empresas reporten oficialmente.
    No constituye asesoría de inversión. <strong>N/D</strong> = no disponible · <strong>*</strong> = contiene eventos no recurrentes.
</div>
"""

# ──────────────────────────────────────────────────────────────────────────────
# PÁGINA: RESUMEN
# ──────────────────────────────────────────────────────────────────────────────
if pagina == "📋 Resumen":
    st.markdown('<div class="page-title">Resumen del Mercado</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">COLCAP · Principales emisores · Resultados 2025</div>', unsafe_allow_html=True)
    st.markdown(BANNER, unsafe_allow_html=True)

    beat  = df[df["Supero"].astype(str).str.lower().isin(["sí","si","yes","true"])]
    miss  = df[df["Supero"].astype(str).str.lower() == "no"]

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(f'<div class="summary-card"><div class="big-num">{len(df)}</div><div class="sum-label">Emisores monitoreados</div></div>', unsafe_allow_html=True)
    with c2:
        st.markdown(f'<div class="summary-card"><div class="big-num" style="color:#2ecc71">{len(beat)}</div><div class="sum-label">Superaron expectativas</div></div>', unsafe_allow_html=True)
    with c3:
        st.markdown(f'<div class="summary-card"><div class="big-num" style="color:#e74c3c">{len(miss)}</div><div class="sum-label">No superaron</div></div>', unsafe_allow_html=True)
    with c4:
        util_total = df["Utilidad_Neta_Real"].sum()
        st.markdown(f'<div class="summary-card"><div class="big-num">{fmt(util_total)}</div><div class="sum-label">Utilidad neta total (COP bn)</div></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    resumen_data = []
    for _, r in df.iterrows():
        s = str(r.get("Supero","")).strip().lower()
        emoji = "✅" if s in ["sí","si"] else "❌" if s == "no" else "〰️" if "línea" in s else "—"
        resumen_data.append({
            "Empresa":       r["Empresa"],
            "Sector":        r["Sector"],
            "Utilidad 2025": fmt(r.get("Utilidad_Neta_Real")),
            "Var. Utilidad": r.get("Variacion_Utilidad_Pct","N/D"),
            "Margen Neto":   fmt_pct(r.get("Margen_Neto_Pct")),
            "Expectativas":  emoji,
        })
    st.dataframe(pd.DataFrame(resumen_data), use_container_width=True, hide_index=True)

    df_plot = df.dropna(subset=["Utilidad_Neta_Real"]).sort_values("Utilidad_Neta_Real", ascending=True)
    colors  = ["#2ecc71" if str(r).lower() in ["sí","si"] else
               "#e74c3c" if str(r).lower() == "no" else "#5a9abf"
               for r in df_plot["Supero"]]
    fig = go.Figure(go.Bar(
        x=df_plot["Utilidad_Neta_Real"], y=df_plot["Empresa"],
        orientation="h", marker_color=colors,
        text=[fmt(v) for v in df_plot["Utilidad_Neta_Real"]],
        textposition="outside", textfont=dict(color="#8a9a88", size=11),
    ))
    fig.update_layout(
        title="Utilidad Neta 2025 (COP bn)", title_font_color="#7a9a80",
        paper_bgcolor="#080c0e", plot_bgcolor="#0d1610",
        font_color="#8a9a88", height=380,
        xaxis=dict(gridcolor="#1a2a1e", zerolinecolor="#1a2a1e"),
        yaxis=dict(gridcolor="#1a2a1e"),
        margin=dict(l=10, r=90, t=40, b=20),
    )
    st.plotly_chart(fig, use_container_width=True)

# ──────────────────────────────────────────────────────────────────────────────
# PÁGINA: RESULTADOS 2025
# ──────────────────────────────────────────────────────────────────────────────
elif pagina == "🏢 Resultados 2025":
    st.markdown('<div class="page-title">Resultados 2025</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Resultados anuales por empresa · COLCAP Top 9</div>', unsafe_allow_html=True)
    st.markdown(BANNER, unsafe_allow_html=True)

    for _, r in df.iterrows():
        tiene_nr = str(r.get("Tiene_No_Recurrentes","")).strip().lower() in ["sí","si","true","1"]
        cc    = card_class(r.get("Supero"))
        badge = badge_html(r.get("Supero"))
        var_u = str(r.get("Variacion_Utilidad_Pct","")).strip()
        vcls  = yoy_class(var_u)

        ingresos = fmt(r.get("Ingresos_Real")) if pd.notna(r.get("Ingresos_Real")) else "N/A (banco)"
        ebitda   = fmt(r.get("EBITDA_Real"))   if pd.notna(r.get("EBITDA_Real"))   else "N/A (banco)"
        div_val  = r.get("Dividendo_COP","")
        div_str  = f"COP {float(div_val):,.0f}" if pd.notna(div_val) and str(div_val).strip() not in ["","nan"] else "N/D"

        nrn   = r.get("Nota_No_Recurrente","")
        notas = r.get("Notas","")

        st.markdown(f"""
        <div class="{cc}">
            <div class="card-header">
                <div>
                    <div class="empresa-nombre">{r['Empresa']}</div>
                    <div class="empresa-meta">{r['Sector']} · {r.get('Ticker_BVC','')}</div>
                </div>
                {badge}
            </div>
            <div class="metrics-row">
                <div class="metric-box">
                    <div class="metric-label">Ingresos</div>
                    <div class="metric-value">{ingresos}</div>
                </div>
                <div class="divider-metric"></div>
                <div class="metric-box">
                    <div class="metric-label">Utilidad Neta</div>
                    <div class="metric-value">{fmt(r.get('Utilidad_Neta_Real'))}</div>
                    <div class="{vcls}">{var_u} vs 2024</div>
                </div>
                <div class="divider-metric"></div>
                <div class="metric-box">
                    <div class="metric-label">EBITDA</div>
                    <div class="metric-value">{ebitda}</div>
                </div>
                <div class="divider-metric"></div>
                <div class="metric-box">
                    <div class="metric-label">Margen EBITDA</div>
                    <div class="metric-value">{fmt_pct(r.get('Margen_EBITDA_Pct'))}</div>
                </div>
                <div class="divider-metric"></div>
                <div class="metric-box">
                    <div class="metric-label">Margen Neto</div>
                    <div class="metric-value">{fmt_pct(r.get('Margen_Neto_Pct'))}</div>
                </div>
                <div class="divider-metric"></div>
                <div class="metric-box">
                    <div class="metric-label">Dividendo</div>
                    <div class="metric-value">{div_str}</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        if tiene_nr and pd.notna(nrn) and str(nrn).strip():
            st.markdown(f'<div class="nr-box" style="margin-top:-8px;margin-bottom:4px"><span class="nr-label">* Evento no recurrente:</span> {nrn}</div>', unsafe_allow_html=True)
        if pd.notna(notas) and str(notas).strip():
            st.markdown(f'<div class="guidance-box" style="margin-top:2px;margin-bottom:10px"><span class="guidance-label">Notas: </span>{notas}</div>', unsafe_allow_html=True)

# ──────────────────────────────────────────────────────────────────────────────
# PÁGINA: RESULTADOS 2024
# ──────────────────────────────────────────────────────────────────────────────
elif pagina == "📊 Resultados 2024":
    st.markdown('<div class="page-title">Resultados 2024</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Resultados anuales por empresa · Referencia histórica</div>', unsafe_allow_html=True)
    st.markdown(BANNER, unsafe_allow_html=True)

    if df24 is None:
        st.warning("No se encontró el archivo de datos 2024.")
    else:
        for _, r in df24.iterrows():
            cc    = card_class(r.get("Supero"))
            badge = badge_html(r.get("Supero"))
            var_u = str(r.get("Variacion_Utilidad_Pct","")).strip()
            vcls  = yoy_class(var_u)
            ingresos = fmt(r.get("Ingresos_Real")) if pd.notna(r.get("Ingresos_Real")) else "N/A (banco)"
            ebitda   = fmt(r.get("EBITDA_Real"))   if pd.notna(r.get("EBITDA_Real"))   else "N/A (banco)"
            div_val  = r.get("Dividendo_COP","")
            div_str  = f"COP {float(div_val):,.0f}" if pd.notna(div_val) and str(div_val).strip() not in ["","nan"] else "N/D"
            notas    = r.get("Notas","")

            st.markdown(f"""
            <div class="{cc}">
                <div class="card-header">
                    <div>
                        <div class="empresa-nombre">{r['Empresa']}</div>
                        <div class="empresa-meta">{r['Sector']} · {r.get('Ticker_BVC','')}</div>
                    </div>
                    {badge}
                </div>
                <div class="metrics-row">
                    <div class="metric-box">
                        <div class="metric-label">Ingresos</div>
                        <div class="metric-value">{ingresos}</div>
                    </div>
                    <div class="divider-metric"></div>
                    <div class="metric-box">
                        <div class="metric-label">Utilidad Neta</div>
                        <div class="metric-value">{fmt(r.get('Utilidad_Neta_Real'))}</div>
                        <div class="{vcls}">{var_u} vs 2023</div>
                    </div>
                    <div class="divider-metric"></div>
                    <div class="metric-box">
                        <div class="metric-label">EBITDA</div>
                        <div class="metric-value">{ebitda}</div>
                    </div>
                    <div class="divider-metric"></div>
                    <div class="metric-box">
                        <div class="metric-label">Margen Neto</div>
                        <div class="metric-value">{fmt_pct(r.get('Margen_Neto_Pct'))}</div>
                    </div>
                    <div class="divider-metric"></div>
                    <div class="metric-box">
                        <div class="metric-label">Dividendo</div>
                        <div class="metric-value">{div_str}</div>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
            if pd.notna(notas) and str(notas).strip():
                st.markdown(f'<div class="guidance-box" style="margin-top:2px;margin-bottom:10px"><span class="guidance-label">Notas: </span>{notas}</div>', unsafe_allow_html=True)

# ──────────────────────────────────────────────────────────────────────────────
# PÁGINA: COMPARATIVO YOY
# ──────────────────────────────────────────────────────────────────────────────
elif pagina == "📈 Comparativo YoY":
    st.markdown('<div class="page-title">Comparativo 2024 vs 2025</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Evolución año a año de los principales indicadores</div>', unsafe_allow_html=True)
    st.markdown(BANNER, unsafe_allow_html=True)

    if df24 is None:
        st.warning("No se encontró el archivo de datos 2024.")
    else:
        merged = pd.merge(
            df24[["Empresa","Utilidad_Neta_Real","EBITDA_Real","Margen_Neto_Pct"]].rename(
                columns={"Utilidad_Neta_Real":"Util_24","EBITDA_Real":"EBIT_24","Margen_Neto_Pct":"Mrg_24"}),
            df[["Empresa","Utilidad_Neta_Real","EBITDA_Real","Margen_Neto_Pct","Variacion_Utilidad_Pct","Supero"]].rename(
                columns={"Utilidad_Neta_Real":"Util_25","EBITDA_Real":"EBIT_25","Margen_Neto_Pct":"Mrg_25"}),
            on="Empresa", how="inner"
        )

        tab1, tab2, tab3 = st.tabs(["Utilidad Neta", "EBITDA", "Margen Neto"])

        with tab1:
            df_u = merged.dropna(subset=["Util_24","Util_25"]).sort_values("Util_25", ascending=False)
            fig = go.Figure()
            fig.add_trace(go.Bar(name="2024", x=df_u["Empresa"], y=df_u["Util_24"],
                                 marker_color="#1a5a30", text=[fmt(v) for v in df_u["Util_24"]], textposition="outside"))
            fig.add_trace(go.Bar(name="2025", x=df_u["Empresa"], y=df_u["Util_25"],
                                 marker_color="#2ecc71", text=[fmt(v) for v in df_u["Util_25"]], textposition="outside"))
            fig.update_layout(barmode="group", paper_bgcolor="#080c0e", plot_bgcolor="#0d1610",
                              font_color="#8a9a88", height=400, legend=dict(bgcolor="#0d1610"),
                              xaxis=dict(gridcolor="#1a2a1e"), yaxis=dict(gridcolor="#1a2a1e", title="COP bn"),
                              margin=dict(l=10, r=10, t=20, b=20))
            st.plotly_chart(fig, use_container_width=True)

            rows = []
            for _, r in df_u.iterrows():
                delta = r["Util_25"] - r["Util_24"]
                pct   = (delta / r["Util_24"] * 100) if r["Util_24"] else None
                rows.append({"Empresa": r["Empresa"], "2024": fmt(r["Util_24"]), "2025": fmt(r["Util_25"]),
                             "Δ COP bn": f"{delta:+.2f}", "Δ %": f"{pct:+.1f}%" if pct else "N/D",
                             "Var. Reportada": r.get("Variacion_Utilidad_Pct","")})
            st.dataframe(pd.DataFrame(rows), use_container_width=True, hide_index=True)

        with tab2:
            df_e = merged.dropna(subset=["EBIT_24","EBIT_25"]).sort_values("EBIT_25", ascending=False)
            if df_e.empty:
                st.info("No hay datos EBITDA comparables (bancos no reportan EBITDA).")
            else:
                fig2 = go.Figure()
                fig2.add_trace(go.Bar(name="2024", x=df_e["Empresa"], y=df_e["EBIT_24"], marker_color="#1a5a30"))
                fig2.add_trace(go.Bar(name="2025", x=df_e["Empresa"], y=df_e["EBIT_25"], marker_color="#2ecc71"))
                fig2.update_layout(barmode="group", paper_bgcolor="#080c0e", plot_bgcolor="#0d1610",
                                   font_color="#8a9a88", height=380, legend=dict(bgcolor="#0d1610"),
                                   xaxis=dict(gridcolor="#1a2a1e"), yaxis=dict(gridcolor="#1a2a1e", title="COP bn"),
                                   margin=dict(l=10, r=10, t=20, b=20))
                st.plotly_chart(fig2, use_container_width=True)

        with tab3:
            df_m = merged.dropna(subset=["Mrg_24","Mrg_25"]).sort_values("Mrg_25", ascending=False)
            if df_m.empty:
                st.info("No hay datos de margen comparables.")
            else:
                fig3 = go.Figure()
                fig3.add_trace(go.Bar(name="2024", x=df_m["Empresa"], y=df_m["Mrg_24"], marker_color="#1a5a30"))
                fig3.add_trace(go.Bar(name="2025", x=df_m["Empresa"], y=df_m["Mrg_25"], marker_color="#2ecc71"))
                fig3.update_layout(barmode="group", paper_bgcolor="#080c0e", plot_bgcolor="#0d1610",
                                   font_color="#8a9a88", height=380, legend=dict(bgcolor="#0d1610"),
                                   xaxis=dict(gridcolor="#1a2a1e"), yaxis=dict(gridcolor="#1a2a1e", title="%"),
                                   margin=dict(l=10, r=10, t=20, b=20))
                st.plotly_chart(fig3, use_container_width=True)

# ──────────────────────────────────────────────────────────────────────────────
# PÁGINA: RANKINGS
# ──────────────────────────────────────────────────────────────────────────────
elif pagina == "🏆 Rankings":
    st.markdown('<div class="page-title">Rankings 2025</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">¿Quién ganó más, quién creció más, quién es más eficiente?</div>', unsafe_allow_html=True)
    st.markdown(BANNER, unsafe_allow_html=True)

    medals = ["rank-gold","rank-silver","rank-bronze"]

    def render_ranking(titulo, df_rank, col_val, fmt_fn, subtitulo=""):
        st.markdown(f"**{titulo}**")
        if subtitulo:
            st.markdown(f"<div style='font-size:0.75rem;color:#3a5a40;margin-bottom:8px'>{subtitulo}</div>", unsafe_allow_html=True)
        dr = df_rank.dropna(subset=[col_val]).sort_values(col_val, ascending=False).head(9)
        for i, (_, r) in enumerate(dr.iterrows()):
            mc    = medals[i] if i < 3 else "rank-num"
            medal = ["🥇","🥈","🥉"][i] if i < 3 else f"{i+1}."
            st.markdown(f"""
            <div class="rank-item">
                <div class="{mc}">{medal}</div>
                <div>
                    <div class="rank-empresa">{r['Empresa']}</div>
                    <div class="rank-sector">{r['Sector']}</div>
                </div>
                <div class="rank-valor">{fmt_fn(r[col_val])}</div>
            </div>""", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        render_ranking("Mayor Utilidad Neta", df, "Utilidad_Neta_Real", fmt)
        st.markdown("<br>", unsafe_allow_html=True)
        render_ranking("Mayor EBITDA", df, "EBITDA_Real", fmt, "Bancos excluidos (N/A)")
    with col2:
        render_ranking("Mayor Margen Neto %", df, "Margen_Neto_Pct", fmt_pct)
        st.markdown("<br>", unsafe_allow_html=True)
        render_ranking("Mayor Margen EBITDA %", df, "Margen_EBITDA_Pct", fmt_pct)

# ──────────────────────────────────────────────────────────────────────────────
# PÁGINA: COMPARADOR
# ──────────────────────────────────────────────────────────────────────────────
elif pagina == "⚔️ Comparador":
    st.markdown('<div class="page-title">Comparador de Empresas</div>', unsafe_allow_html=True)
    st.markdown('<div class="page-subtitle">Selecciona dos o más empresas y compara sus métricas</div>', unsafe_allow_html=True)
    st.markdown(BANNER, unsafe_allow_html=True)

    seleccion = st.multiselect("Selecciona empresas:", df["Empresa"].tolist(),
                                default=df["Empresa"].tolist()[:3])

    if len(seleccion) < 2:
        st.info("Selecciona al menos 2 empresas para comparar.")
    else:
        df_sel  = df[df["Empresa"].isin(seleccion)]
        metrica = st.selectbox("Métrica principal:", [
            "Utilidad_Neta_Real","EBITDA_Real","Ingresos_Real","Margen_Neto_Pct","Margen_EBITDA_Pct"
        ], format_func=lambda x: {
            "Utilidad_Neta_Real": "Utilidad Neta (COP bn)",
            "EBITDA_Real":        "EBITDA (COP bn)",
            "Ingresos_Real":      "Ingresos (COP bn)",
            "Margen_Neto_Pct":    "Margen Neto %",
            "Margen_EBITDA_Pct":  "Margen EBITDA %",
        }[x])

        df_plot = df_sel.dropna(subset=[metrica]).sort_values(metrica, ascending=False)
        colors  = ["#2ecc71" if str(r).lower() in ["sí","si"] else
                   "#e74c3c" if str(r).lower() == "no" else "#5a9abf"
                   for r in df_plot["Supero"]]

        fig = go.Figure(go.Bar(
            x=df_plot["Empresa"], y=df_plot[metrica], marker_color=colors,
            text=[fmt(v) if "Pct" not in metrica else fmt_pct(v) for v in df_plot[metrica]],
            textposition="outside",
        ))
        fig.update_layout(
            paper_bgcolor="#080c0e", plot_bgcolor="#0d1610", font_color="#8a9a88",
            height=400, xaxis=dict(gridcolor="#1a2a1e"), yaxis=dict(gridcolor="#1a2a1e"),
            margin=dict(l=10, r=10, t=20, b=20),
        )
        st.plotly_chart(fig, use_container_width=True)

        tabla = df_sel[["Empresa","Sector","Ingresos_Real","Utilidad_Neta_Real",
                         "EBITDA_Real","Margen_Neto_Pct","Variacion_Utilidad_Pct","Supero"]].copy()
        tabla.columns = ["Empresa","Sector","Ingresos","Utilidad Neta","EBITDA","Mrg Neto %","Var Utilidad","Expectativas"]
        for c in ["Ingresos","Utilidad Neta","EBITDA"]:
            tabla[c] = tabla[c].apply(lambda v: fmt(v) if pd.notna(v) else "N/A")
        tabla["Mrg Neto %"] = tabla["Mrg Neto %"].apply(lambda v: fmt_pct(v) if pd.notna(v) else "N/A")
        st.dataframe(tabla, use_container_width=True, hide_index=True)

# ──────────────────────────────────────────────────────────────────────────────
# FOOTER
# ──────────────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="footer">
    AlephMarketsCO · by <strong>Nicolas Rueda</strong> ·
    <a href="https://github.com/nruedas" target="_blank">GitHub</a> ·
    <a href="https://linkedin.com/in/nicolas-rueda-segura-599533379" target="_blank">LinkedIn</a>
    · Datos estimados al 5 mar 2026 · No constituye asesoría de inversión
</div>
""", unsafe_allow_html=True)
