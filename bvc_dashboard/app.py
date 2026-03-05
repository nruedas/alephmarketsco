import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import plotly.graph_objects as go
from pathlib import Path

BASE_DIR = Path(__file__).parent

st.set_page_config(page_title="AlephMarketsCO", page_icon="📊", layout="wide")

STYLES = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    * { font-family: 'Inter', sans-serif; box-sizing: border-box; margin: 0; padding: 0; }
    body { background: transparent; }
    .card { background: #0d1610; border-radius: 12px; padding: 20px 24px; margin-bottom: 12px; border-left: 3px solid #2ecc71; border-top: 1px solid #1a2a1e; border-right: 1px solid #1a2a1e; border-bottom: 1px solid #1a2a1e; }
    .card-miss { background: #0d1610; border-radius: 12px; padding: 20px 24px; margin-bottom: 12px; border-left: 3px solid #e74c3c; border-top: 1px solid #1a2a1e; border-right: 1px solid #1a2a1e; border-bottom: 1px solid #1a2a1e; }
    .card-estimado { background: #0d1610; border-radius: 12px; padding: 20px 24px; margin-bottom: 12px; border-left: 3px solid #f39c12; border-top: 1px solid #1a2a1e; border-right: 1px solid #1a2a1e; border-bottom: 1px solid #1a2a1e; }
    .card-header { display: flex; justify-content: space-between; align-items: flex-start; margin-bottom: 4px; }
    .empresa-nombre { font-size: 1.1rem; font-weight: 700; color: #ffffff; }
    .empresa-meta { font-size: 0.75rem; color: #3a5a40; margin-top: 3px; }
    .badge-beat { background: #0d2a14; color: #2ecc71; border: 1px solid #1a4a24; border-radius: 20px; padding: 3px 12px; font-size: 0.72rem; font-weight: 600; }
    .badge-miss { background: #2a0d0d; color: #e74c3c; border: 1px solid #4a1a1a; border-radius: 20px; padding: 3px 12px; font-size: 0.72rem; font-weight: 600; }
    .badge-est  { background: #2a1e0d; color: #f39c12; border: 1px solid #4a3a1a; border-radius: 20px; padding: 3px 12px; font-size: 0.72rem; font-weight: 600; }
    .est-banner { background: #1a1200; border: 1px solid #3a2a00; border-radius: 8px; padding: 8px 14px; margin: 10px 0; font-size: 0.77rem; color: #f39c12; line-height: 1.5; }
    .est-banner strong { color: #f5c842; }
    .metrics-row { display: flex; gap: 28px; margin-top: 16px; flex-wrap: wrap; align-items: flex-start; }
    .metric-box { display: flex; flex-direction: column; gap: 3px; min-width: 90px; }
    .metric-label { font-size: 0.64rem; color: #3a5a40; text-transform: uppercase; letter-spacing: 0.1em; }
    .metric-value { font-size: 1rem; font-weight: 600; color: #e8e8e8; }
    .yoy-pos { font-size: 0.76rem; color: #2ecc71; font-weight: 600; }
    .yoy-neg { font-size: 0.76rem; color: #e74c3c; font-weight: 600; }
    .divider-metric { width: 1px; background: #1a2a1e; align-self: stretch; min-height: 40px; margin: 0 4px; }
    .guidance-box { margin-top: 14px; padding: 9px 13px; background: #080c0e; border-radius: 7px; font-size: 0.8rem; color: #4a7050; border-left: 2px solid #1a3a20; }
    .guidance-label { color: #2ecc71; font-weight: 500; }
    .rank-item { display: flex; align-items: center; gap: 14px; padding: 11px 15px; background: #0d1610; border-radius: 9px; margin-bottom: 7px; border: 1px solid #1a2a1e; }
    .rank-gold   { font-size: 1rem; font-weight: 700; color: #f1c40f; width: 26px; }
    .rank-silver { font-size: 1rem; font-weight: 700; color: #95a5a6; width: 26px; }
    .rank-bronze { font-size: 1rem; font-weight: 700; color: #a04000; width: 26px; }
    .rank-num    { font-size: 1rem; font-weight: 700; color: #3a5a40; width: 26px; }
    .rank-empresa { font-weight: 600; color: #e8e8e8; font-size: 0.88rem; }
    .rank-sector  { font-size: 0.72rem; color: #3a5a40; }
    .rank-valor   { font-size: 0.95rem; font-weight: 700; color: #2ecc71; }
</style>
"""

st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    .stApp { background-color: #080c0e; color: #d4d4d4; }
    [data-testid="stSidebar"] { background-color: #0a0f11; border-right: 1px solid #1a2a1e; }
    .stRadio label { color: #7a9a80 !important; font-size: 0.88rem !important; }
    .logo-text { font-size: 1.6rem; font-weight: 800; letter-spacing: -0.03em; line-height: 1.1; }
    .logo-aleph { color: #2ecc71; }
    .logo-markets { color: #ffffff; }
    .logo-co { color: #2ecc71; }
    .logo-by { font-size: 0.82rem; color: #4a7050; margin-top: 5px; }
    .logo-links { margin-top: 8px; display: flex; gap: 10px; }
    .logo-link { font-size: 0.75rem; color: #2ecc71; text-decoration: none; border: 1px solid #1a3a20; border-radius: 5px; padding: 2px 8px; }
    .page-title { font-size: 1.55rem; font-weight: 700; color: #ffffff; letter-spacing: -0.02em; }
    .page-subtitle { font-size: 0.83rem; color: #3a5a40; margin-top: 3px; margin-bottom: 24px; border-bottom: 1px solid #1a2a1e; padding-bottom: 18px; }
    .summary-card { background: #0d1610; border-radius: 10px; padding: 18px 20px; text-align: center; border: 1px solid #1a2a1e; }
    .big-num { font-size: 1.9rem; font-weight: 700; color: #fff; }
    .sum-label { font-size: 0.68rem; color: #3a5a40; text-transform: uppercase; letter-spacing: 0.1em; margin-top: 5px; }
    .sum-sublabel { font-size: 0.8rem; color: #4a7050; margin-top: 1px; }
    .footer { text-align: center; color: #1a3a20; font-size: 0.73rem; padding: 20px 0 6px 0; border-top: 1px solid #1a2a1e; margin-top: 40px; }
    .footer a { color: #2ecc71; text-decoration: none; }
    .aviso { background:#1a1200; border:1px solid #3a2a00; border-radius:8px; padding:10px 16px; margin-bottom:20px; font-size:0.8rem; color:#f39c12; }
</style>
""", unsafe_allow_html=True)

ESTIMADAS = {"Grupo Aval", "Grupo Bolivar", "GEB"}

@st.cache_data
def cargar_datos():
    df = pd.read_csv(BASE_DIR / "resultados_bvc.csv")
    for c in ["Ingresos_Real","Ingresos_Est","Utilidad_Neta_Real","Utilidad_Neta_Est",
              "EBITDA_Real","EBITDA_Est","Margen_Neto_Pct","Deuda_Neta","Dividendo_COP"]:
        if c in df.columns:
            df[c] = pd.to_numeric(df[c], errors="coerce")
    return df

@st.cache_data
def cargar_2024():
    try:
        df = pd.read_csv(BASE_DIR / "resultados_bvc_2024.csv")
        for c in ["Ingresos_Real","Utilidad_Neta_Real","EBITDA_Real","Margen_Neto_Pct","Dividendo_COP"]:
            if c in df.columns:
                df[c] = pd.to_numeric(df[c], errors="coerce")
        return df
    except:
        return None

df   = cargar_datos()
df24 = cargar_2024()

def fmt(val):
    if pd.isna(val): return "---"
    return f"${val:,.0f}B"

def fmt_pct(val):
    if pd.isna(val): return "---"
    return f"{val:.1f}%"

def fmt_div(val):
    if pd.isna(val): return "---"
    return f"${val:,.0f}"

def get24(empresa, col):
    if df24 is None: return None
    r = df24[df24["Empresa"] == empresa]
    if r.empty: return None
    v = r.iloc[0][col]
    return None if pd.isna(v) else float(v)

def yoy_span(v25, v24):
    if v24 is None or pd.isna(v25) or v24 == 0: return ""
    pct = round((v25 - v24) / abs(v24) * 100, 1)
    cls = "yoy-pos" if pct >= 0 else "yoy-neg"
    sig = "+" if pct >= 0 else ""
    return f'<span class="{cls}">{sig}{pct}% YoY</span>'

def render_card(row):
    empresa  = str(row["Empresa"])
    es_est   = empresa in ESTIMADAS
    supero   = row["Supero"] == "Si"
    es_fin   = row["Sector"] == "Financiero"

    if es_est:
        card_cls  = "card-estimado"
        badge_cls = "badge-est"
        badge_txt = "&#9888; ESTIMADO"
    elif supero:
        card_cls  = "card"
        badge_cls = "badge-beat"
        badge_txt = "&#10003; SUPERÓ"
    else:
        card_cls  = "card-miss"
        badge_cls = "badge-miss"
        badge_txt = "&#10007; PERDIÓ"

    ebitda_v  = "N/A &mdash; Sector Financiero" if es_fin else fmt(row["EBITDA_Real"])
    yoy_i     = yoy_span(row["Ingresos_Real"],      get24(empresa, "Ingresos_Real"))
    yoy_u     = yoy_span(row["Utilidad_Neta_Real"], get24(empresa, "Utilidad_Neta_Real"))
    yoy_e     = yoy_span(row["EBITDA_Real"],        get24(empresa, "EBITDA_Real")) if not es_fin else ""

    est_banner = ""
    if es_est:
        est_banner = """
        <div class="est-banner">
            &#9888; <strong>DATOS ESTIMADOS &mdash; NO OFICIALES.</strong>
            Estas cifras son proyecciones basadas en resultados acumulados y analisis de mercado.
            Los resultados reales del 2025 aun no han sido publicados oficialmente.
            No tomar como informacion definitiva ni como base para decisiones de inversion.
        </div>"""

    html = f"""
    {STYLES}
    <div class="{card_cls}">
        <div class="card-header">
            <div>
                <div class="empresa-nombre">{empresa}</div>
                <div class="empresa-meta">{row['Ticker_BVC']} &nbsp;&middot;&nbsp; {row['Sector']} &nbsp;&middot;&nbsp; {row['Periodo']}</div>
            </div>
            <span class="{badge_cls}">{badge_txt}</span>
        </div>
        {est_banner}
        <div class="metrics-row">
            <div class="metric-box">
                <span class="metric-label">Ingresos</span>
                <span class="metric-value">{fmt(row['Ingresos_Real'])}</span>
                {yoy_i}
            </div>
            <div class="divider-metric"></div>
            <div class="metric-box">
                <span class="metric-label">Utilidad Neta</span>
                <span class="metric-value">{fmt(row['Utilidad_Neta_Real'])}</span>
                {yoy_u}
            </div>
            <div class="divider-metric"></div>
            <div class="metric-box">
                <span class="metric-label">EBITDA</span>
                <span class="metric-value">{ebitda_v}</span>
                {yoy_e}
            </div>
            <div class="divider-metric"></div>
            <div class="metric-box">
                <span class="metric-label">Margen Neto</span>
                <span class="metric-value">{fmt_pct(row['Margen_Neto_Pct'])}</span>
            </div>
            <div class="divider-metric"></div>
            <div class="metric-box">
                <span class="metric-label">Dividendo</span>
                <span class="metric-value">{fmt_div(row['Dividendo_COP'])} COP</span>
            </div>
        </div>
        <div class="guidance-box">
            <span class="guidance-label">Guidance &mdash;</span> {row['Guidance']}
        </div>
    </div>
    """
    card_height = 220 if not es_est else 300
    if es_fin: card_height -= 20
    components.html(html, height=card_height, scrolling=False)

def chart_layout(fig, height=360):
    fig.update_layout(
        plot_bgcolor="#080c0e", paper_bgcolor="#080c0e",
        font=dict(color="#3a5a40", family="Inter"),
        xaxis=dict(showgrid=False, showticklabels=False, zeroline=False),
        yaxis=dict(showgrid=False, tickfont=dict(color="#7a9a80", size=12)),
        margin=dict(l=10, r=110, t=10, b=10),
        height=height, showlegend=False,
    )
    return fig

# ── SIDEBAR ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="padding:12px 0 16px 0;">
        <div style="font-size:1.6rem;font-weight:800;letter-spacing:-0.03em;">
            <span style="color:#2ecc71;">Aleph</span><span style="color:#fff;">Markets</span><span style="color:#2ecc71;">CO</span>
        </div>
        <div style="font-size:0.82rem;color:#4a7050;margin-top:5px;">by Nicolas Rueda</div>
        <div style="margin-top:8px;display:flex;gap:8px;">
            <a href="https://github.com/nruedas" target="_blank"
               style="font-size:0.75rem;color:#2ecc71;text-decoration:none;border:1px solid #1a3a20;border-radius:5px;padding:2px 8px;">
               GitHub
            </a>
            <a href="https://www.linkedin.com/in/nicolas-rueda-segura-599533379/" target="_blank"
               style="font-size:0.75rem;color:#2ecc71;text-decoration:none;border:1px solid #1a3a20;border-radius:5px;padding:2px 8px;">
               LinkedIn
            </a>
        </div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("<hr style='border-color:#1a2a1e;margin-bottom:16px;'>", unsafe_allow_html=True)
    pagina = st.radio("Nav", ["Resumen","Resultados","YoY 2024 vs 2025","Rankings","Comparador"], label_visibility="collapsed")
    st.markdown("<hr style='border-color:#1a2a1e;margin-top:16px;'>", unsafe_allow_html=True)
    st.markdown("<p style='color:#1a3a20;font-size:0.72rem;line-height:1.8;'>Datos actualizados manualmente<br>Fuente: IR de cada emisor<br>Cifras en miles de millones COP<br><span style='color:#f39c12;'>&#9888; Algunas cifras son estimadas</span></p>", unsafe_allow_html=True)

# ── RESUMEN ───────────────────────────────────────────────────────────────────
if pagina == "Resumen":
    st.markdown("<div class='page-title'>Resumen de Mercado</div>", unsafe_allow_html=True)
    st.markdown("<div class='page-subtitle'>Resultados anuales 2025 &middot; Principales emisores del COLCAP</div>", unsafe_allow_html=True)
    st.markdown("<div class='aviso'>&#9888; <strong>Aviso:</strong> Las cifras de <strong>Grupo Aval, Grupo Bolívar, Ecopetrol y GEB</strong> son <strong>estimaciones basadas en análisis de mercado</strong>. No corresponden a resultados oficiales. No utilizar como base para decisiones de inversión.</div>", unsafe_allow_html=True)

    total = len(df)
    beat  = len(df[df["Supero"] == "Si"])
    miss  = len(df[df["Supero"] == "No"])
    est   = len(df[df["Empresa"].isin(ESTIMADAS)])
    pct_b = round(beat / total * 100) if total > 0 else 0

    c1,c2,c3,c4,c5 = st.columns(5)
    with c1: st.markdown(f"<div class='summary-card'><div class='big-num'>{total}</div><div class='sum-label'>Empresas</div><div class='sum-sublabel'>reportando</div></div>", unsafe_allow_html=True)
    with c2: st.markdown(f"<div class='summary-card'><div class='big-num' style='color:#2ecc71'>{beat}</div><div class='sum-label'>Superaron</div><div class='sum-sublabel'>expectativas</div></div>", unsafe_allow_html=True)
    with c3: st.markdown(f"<div class='summary-card'><div class='big-num' style='color:#e74c3c'>{miss}</div><div class='sum-label'>Por debajo</div><div class='sum-sublabel'>de expectativas</div></div>", unsafe_allow_html=True)
    with c4: st.markdown(f"<div class='summary-card'><div class='big-num' style='color:#f39c12'>{est}</div><div class='sum-label'>Estimadas</div><div class='sum-sublabel'>no oficiales</div></div>", unsafe_allow_html=True)
    with c5: st.markdown(f"<div class='summary-card'><div class='big-num'>{pct_b}%</div><div class='sum-label'>Tasa de beat</div><div class='sum-sublabel'>este periodo</div></div>", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    col_g1, col_g2 = st.columns(2)
    with col_g1:
        st.markdown("#### Ingresos Totales")
        df_s = df.dropna(subset=["Ingresos_Real"]).sort_values("Ingresos_Real", ascending=True)
        colors = ["#f39c12" if r["Empresa"] in ESTIMADAS else ("#2ecc71" if r["Supero"]=="Si" else "#e74c3c") for _,r in df_s.iterrows()]
        fig = go.Figure(go.Bar(x=df_s["Ingresos_Real"], y=df_s["Empresa"], orientation="h", marker_color=colors, marker_line_width=0,
            text=[f"${v:,.0f}B" for v in df_s["Ingresos_Real"]], textposition="outside", textfont=dict(color="#4a7050", size=11)))
        st.plotly_chart(chart_layout(fig), use_container_width=True)
    with col_g2:
        st.markdown("#### Utilidad Neta")
        df_s2 = df.dropna(subset=["Utilidad_Neta_Real"]).sort_values("Utilidad_Neta_Real", ascending=True)
        colors2 = ["#f39c12" if r["Empresa"] in ESTIMADAS else ("#2ecc71" if r["Supero"]=="Si" else "#e74c3c") for _,r in df_s2.iterrows()]
        fig2 = go.Figure(go.Bar(x=df_s2["Utilidad_Neta_Real"], y=df_s2["Empresa"], orientation="h", marker_color=colors2, marker_line_width=0,
            text=[f"${v:,.0f}B" for v in df_s2["Utilidad_Neta_Real"]], textposition="outside", textfont=dict(color="#4a7050", size=11)))
        st.plotly_chart(chart_layout(fig2), use_container_width=True)

    st.markdown("#### Vista rápida")
    df_t = df[["Empresa","Sector","Ingresos_Real","Utilidad_Neta_Real","EBITDA_Real","Margen_Neto_Pct","Dividendo_COP","Supero"]].copy()
    df_t["Datos"] = df_t["Empresa"].apply(lambda x: "⚠ Estimado" if x in ESTIMADAS else "✓ Oficial")
    df_t.columns = ["Empresa","Sector","Ingresos (B)","Utilidad (B)","EBITDA (B)","Margen %","Dividendo COP","Superó","Datos"]
    st.dataframe(df_t, use_container_width=True, hide_index=True)

# ── RESULTADOS ────────────────────────────────────────────────────────────────
elif pagina == "Resultados":
    st.markdown("<div class='page-title'>Resultados por Empresa</div>", unsafe_allow_html=True)
    st.markdown("<div class='page-subtitle'>Tarjetas en naranja = datos estimados no oficiales</div>", unsafe_allow_html=True)

    col_f1, col_f2, col_f3 = st.columns(3)
    with col_f1:
        sector_sel = st.selectbox("Sector", ["Todos"] + sorted(df["Sector"].unique().tolist()))
    with col_f2:
        resultado_sel = st.selectbox("Resultado", ["Todos","Supero expectativas","Por debajo","Solo estimados"])
    with col_f3:
        orden_sel = st.selectbox("Ordenar por", ["Empresa","Ingresos","Utilidad Neta","Margen"])

    df_f = df.copy()
    if sector_sel != "Todos": df_f = df_f[df_f["Sector"] == sector_sel]
    if resultado_sel == "Supero expectativas": df_f = df_f[df_f["Supero"] == "Si"]
    elif resultado_sel == "Por debajo":        df_f = df_f[df_f["Supero"] == "No"]
    elif resultado_sel == "Solo estimados":    df_f = df_f[df_f["Empresa"].isin(ESTIMADAS)]
    orden_map = {"Empresa":"Empresa","Ingresos":"Ingresos_Real","Utilidad Neta":"Utilidad_Neta_Real","Margen":"Margen_Neto_Pct"}
    df_f = df_f.sort_values(orden_map[orden_sel], ascending=(orden_sel=="Empresa"))

    st.markdown(f"<p style='color:#3a5a40;font-size:0.8rem;margin-bottom:16px;'>{len(df_f)} empresa(s)</p>", unsafe_allow_html=True)
    for _, row in df_f.iterrows():
        render_card(row)

# ── YoY ───────────────────────────────────────────────────────────────────────
elif pagina == "YoY 2024 vs 2025":
    st.markdown("<div class='page-title'>Comparacion YoY · 2024 vs 2025</div>", unsafe_allow_html=True)
    st.markdown("<div class='page-subtitle'>Evolucion año a año · Naranja = cifras estimadas no oficiales</div>", unsafe_allow_html=True)
    if df24 is None:
        st.warning("Agrega resultados_bvc_2024.csv para ver esta seccion.")
    else:
        metrica_sel = st.selectbox("Metrica", ["Ingresos_Real","Utilidad_Neta_Real","EBITDA_Real","Margen_Neto_Pct"])
        label_map = {"Ingresos_Real":"Ingresos (B COP)","Utilidad_Neta_Real":"Utilidad Neta (B COP)","EBITDA_Real":"EBITDA (B COP)","Margen_Neto_Pct":"Margen Neto (%)"}
        emps,v24s,v25s = [],[],[]
        for emp in df[df["Empresa"].isin(df24["Empresa"])]["Empresa"].tolist():
            v24 = get24(emp, metrica_sel)
            arr = df[df["Empresa"]==emp][metrica_sel].values
            v25 = float(arr[0]) if len(arr)>0 and not pd.isna(arr[0]) else None
            if v24 is not None and v25 is not None:
                emps.append(emp); v24s.append(v24); v25s.append(v25)
        bar_colors_25 = ["#f39c12" if e in ESTIMADAS else "#2ecc71" for e in emps]
        fig = go.Figure()
        fig.add_trace(go.Bar(name="2024", x=emps, y=v24s, marker_color="#1a3a20", marker_line_width=0,
            text=[f"{v:,.0f}" for v in v24s], textposition="outside", textfont=dict(color="#3a5a40", size=10)))
        fig.add_trace(go.Bar(name="2025", x=emps, y=v25s, marker_color=bar_colors_25, marker_line_width=0,
            text=[f"{v:,.0f}" for v in v25s], textposition="outside", textfont=dict(color="#7a9a80", size=10)))
        fig.update_layout(barmode="group", plot_bgcolor="#080c0e", paper_bgcolor="#080c0e",
            font=dict(color="#3a5a40"), xaxis=dict(showgrid=False, tickfont=dict(color="#7a9a80", size=11)),
            yaxis=dict(showgrid=False, showticklabels=False),
            legend=dict(bgcolor="#0d1610", bordercolor="#1a2a1e", borderwidth=1, font=dict(color="#7a9a80")),
            margin=dict(l=10,r=10,t=30,b=10), height=420)
        st.markdown(f"#### {label_map[metrica_sel]}")
        st.plotly_chart(fig, use_container_width=True)
        rows_yoy = [{"Empresa":e,"2024":round(v24,1),"2025":round(v25,1),
                     "Variacion %":round((v25-v24)/abs(v24)*100,1) if v24!=0 else 0,
                     "Tipo":"⚠ Estimado" if e in ESTIMADAS else "✓ Oficial"}
                    for e,v24,v25 in zip(emps,v24s,v25s)]
        st.markdown("#### Variacion por empresa")
        st.dataframe(pd.DataFrame(rows_yoy).sort_values("Variacion %",ascending=False), use_container_width=True, hide_index=True)

# ── RANKINGS ──────────────────────────────────────────────────────────────────
elif pagina == "Rankings":
    st.markdown("<div class='page-title'>Rankings 2025</div>", unsafe_allow_html=True)
    st.markdown("<div class='page-subtitle'>Las empresas mejor posicionadas · ⚠ = datos estimados no oficiales</div>", unsafe_allow_html=True)

    def render_ranking(col, titulo, es_pct=False):
        df_r = df.dropna(subset=[col]).sort_values(col, ascending=False).head(5).reset_index(drop=True)
        st.markdown(f"**{titulo}**")
        medal_cls = ["rank-gold","rank-silver","rank-bronze","rank-num","rank-num"]
        for i, row in df_r.iterrows():
            val   = row[col]
            label = f"{val:.1f}%" if es_pct else f"${val:,.0f}B"
            mcls  = medal_cls[i] if i < 5 else "rank-num"
            v24   = get24(row["Empresa"], col)
            yoy_t = ""
            if v24 and v24 != 0:
                pct = round((val-v24)/abs(v24)*100,1)
                sig = "+" if pct>=0 else ""
                cy  = "#2ecc71" if pct>=0 else "#e74c3c"
                yoy_t = f"<span style='font-size:0.72rem;color:{cy};'>{sig}{pct}% YoY</span>"
            est_tag = " <span style='font-size:0.65rem;color:#f39c12;'>⚠ est.</span>" if row["Empresa"] in ESTIMADAS else ""
            st.markdown(f"""
            <div class="rank-item">
                <span class="{mcls}">#{i+1}</span>
                <div style="flex:1"><div class="rank-empresa">{row['Empresa']}{est_tag}</div>
                <div class="rank-sector">{row['Sector']}</div></div>
                <div style="text-align:right"><div class="rank-valor">{label}</div>{yoy_t}</div>
            </div>""", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        render_ranking("Utilidad_Neta_Real","Utilidad Neta")
        render_ranking("Margen_Neto_Pct","Margen Neto",es_pct=True)
    with col2:
        render_ranking("Ingresos_Real","Ingresos Totales")
        render_ranking("Dividendo_COP","Dividendo por Accion")

# ── COMPARADOR ────────────────────────────────────────────────────────────────
elif pagina == "Comparador":
    st.markdown("<div class='page-title'>Comparador de Empresas</div>", unsafe_allow_html=True)
    st.markdown("<div class='page-subtitle'>Selecciona hasta 4 empresas · ⚠ = cifras estimadas no oficiales</div>", unsafe_allow_html=True)
    seleccion = st.multiselect("Selecciona empresas", df["Empresa"].tolist(), default=df["Empresa"].tolist()[:3], max_selections=4)
    if len(seleccion) < 2:
        st.info("Selecciona al menos 2 empresas para comparar.")
    else:
        if any(e in ESTIMADAS for e in seleccion):
            st.markdown("<div class='aviso'>⚠ Una o más empresas tienen <strong>datos estimados no oficiales</strong>. Las celdas marcadas con ⚠ no corresponden a resultados definitivos.</div>", unsafe_allow_html=True)
        df_comp = df[df["Empresa"].isin(seleccion)].reset_index(drop=True)
        metricas = {"Ingresos (B COP)":"Ingresos_Real","Utilidad Neta (B COP)":"Utilidad_Neta_Real",
                    "EBITDA (B COP)":"EBITDA_Real","Margen Neto %":"Margen_Neto_Pct","Dividendo COP":"Dividendo_COP"}
        rows_html = ""
        for label, col in metricas.items():
            vals = df_comp[col].tolist()
            nums = [v for v in vals if not pd.isna(v)]
            max_val = max(nums) if nums else None
            celdas = ""
            for idx, v in enumerate(vals):
                emp = df_comp.iloc[idx]["Empresa"]
                if pd.isna(v):
                    celdas += "<td style='padding:11px 16px;color:#1a3a20;text-align:center;'>---</td>"
                else:
                    es_pct = "%" in label
                    txt    = f"{v:.1f}%" if es_pct else f"${v:,.0f}"
                    color  = "#2ecc71" if v == max_val else "#e8e8e8"
                    mk     = " ⚠" if emp in ESTIMADAS else ""
                    celdas += f"<td style='padding:11px 16px;font-weight:600;color:{color};text-align:center;'>{txt}{mk}</td>"
            rows_html += f"<tr style='border-bottom:1px solid #1a2a1e;'><td style='padding:11px 16px;color:#3a5a40;font-size:0.75rem;text-transform:uppercase;'>{label}</td>{celdas}</tr>"
        headers = "".join([f"<th style='padding:12px 16px;color:#e8e8e8;font-weight:600;text-align:center;'>{e}</th>" for e in df_comp["Empresa"].tolist()])
        st.markdown(f"<div style='overflow-x:auto;'><table style='width:100%;border-collapse:collapse;background:#0d1610;border-radius:12px;overflow:hidden;border:1px solid #1a2a1e;'><thead><tr style='border-bottom:1px solid #1a3a20;'><th style='padding:12px 16px;color:#3a5a40;font-size:0.72rem;text-align:left;'>METRICA</th>{headers}</tr></thead><tbody>{rows_html}</tbody></table></div>", unsafe_allow_html=True)
        st.markdown("<br>**Comparacion visual**", unsafe_allow_html=True)
        metrica_graf = st.selectbox("Metrica a graficar", list(metricas.keys()))
        col_graf = metricas[metrica_graf]
        df_g = df_comp.dropna(subset=[col_graf])
        colores = ["#f39c12" if e in ESTIMADAS else c for e,c in zip(df_g["Empresa"],["#2ecc71","#3498db","#9b59b6","#1abc9c"])]
        fig = go.Figure(go.Bar(x=df_g["Empresa"], y=df_g[col_graf], marker_color=colores, marker_line_width=0,
            text=[f"{v:.1f}%" if "%" in metrica_graf else f"${v:,.0f}B" for v in df_g[col_graf]],
            textposition="outside", textfont=dict(color="#4a7050", size=11)))
        fig.update_layout(plot_bgcolor="#080c0e", paper_bgcolor="#080c0e", font=dict(color="#3a5a40"),
            xaxis=dict(showgrid=False, tickfont=dict(color="#7a9a80", size=12)),
            yaxis=dict(showgrid=False, showticklabels=False),
            margin=dict(l=10,r=10,t=30,b=10), height=340, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

st.markdown("""
<div class="footer">
    <span>AlephMarketsCO</span> · by Nicolas Rueda ·
    <a href="https://github.com/nruedas" target="_blank">GitHub</a> ·
    <a href="https://www.linkedin.com/in/nicolas-rueda-segura-599533379/" target="_blank">LinkedIn</a> ·
    Cifras en miles de millones COP · Fuente: IR de cada emisor ·
    <span style="color:#f39c12;">⚠ Algunas cifras son estimadas, no oficiales</span>
</div>
""", unsafe_allow_html=True)
