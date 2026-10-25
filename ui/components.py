import html
import streamlit as st

def render_header():
    """Renders the centered animated hero banner and personal name header."""
    st.markdown("""
    <div style="width: 100%; margin-bottom: 28px;">
      <div class="hero-banner-text">Student of Sir.Iqbal Gill</div>
      <div style="text-align: left; margin-top: 12px;">
        <span style="font-size: 28px; font-weight: 700; color: #EDEBFF; letter-spacing: -0.5px;">Abdul Subhan</span>
        <span style="font-size: 28px; font-weight: 400; color: #5CF0DA; letter-spacing: -0.5px;"> / ask your knowledge</span>
      </div>
    </div>
    """, unsafe_allow_html=True)

def render_empty_state():
    """Renders the CSS 3D floating pages illustration for empty state."""
    st.markdown("""
    <style>
    .empty-card {
      background: linear-gradient(135deg, rgba(255,255,255,.13), rgba(255,255,255,.04));
      border: 1px solid rgba(255,255,255,.2);
      backdrop-filter: blur(18px);
      -webkit-backdrop-filter: blur(18px);
      border-radius: 22px;
      max-width: 600px;
      padding: 40px;
      margin: 30px auto;
      text-align: center;
      box-shadow: 0 30px 60px rgba(0,0,0,.45);
    }
    .illustration-3d-wrapper {
      perspective: 1000px;
      width: 180px;
      height: 140px;
      margin: 0 auto 30px auto;
      position: relative;
    }
    .stack-3d-inner {
      width: 100%;
      height: 100%;
      position: relative;
      transform-style: preserve-3d;
      transform: rotateX(55deg) rotateZ(-30deg);
      animation: floatIllustration 6s ease-in-out infinite;
    }
    .glass-page {
      position: absolute;
      width: 120px;
      height: 140px;
      left: 30px;
      background: linear-gradient(135deg, rgba(255,255,255,.25), rgba(255,255,255,.05));
      border: 1px solid rgba(255,255,255,.4);
      border-radius: 12px;
      backdrop-filter: blur(12px);
      box-shadow: 0 10px 30px rgba(124,92,255,0.3);
    }
    .page-1 { transform: translateZ(0px); border-color: rgba(124,92,255,0.4); }
    .page-2 { transform: translateZ(30px); border-color: rgba(45,226,200,0.5); }
    .page-3 { transform: translateZ(60px); border-color: rgba(92,240,218,0.7); box-shadow: 0 15px 35px rgba(45,226,200,0.5); }
    @keyframes floatIllustration {
      0%, 100% { transform: rotateX(55deg) rotateZ(-30deg) translateY(0); }
      50% { transform: rotateX(55deg) rotateZ(-30deg) translateY(-12px); }
    }
    </style>
    
    <div class="empty-card">
      <div class="illustration-3d-wrapper" aria-hidden="true">
        <div class="stack-3d-inner">
          <div class="glass-page page-1"></div>
          <div class="glass-page page-2"></div>
          <div class="glass-page page-3"></div>
        </div>
      </div>
      <div style="display: flex; align-items: center; justify-content: center; gap: 10px; margin-bottom: 12px;">
        <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#5CF0DA" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
          <path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/>
          <polyline points="17 8 12 3 7 8"/>
          <line x1="12" y1="3" x2="12" y2="15"/>
        </svg>
        <span style="font-size: 24px; font-weight: 700; color: #5CF0DA;">Upload a Document to get started</span>
      </div>
      <p style="color: #B7B2E6; font-size: 15px; margin: 0; line-height: 1.6;">
        Upload any document (PDF, DOCX, TXT, MD, CSV, PPTX, HTML, JSON, etc.) to begin asking questions grounded directly in your knowledge base.
      </p>
    </div>
    """, unsafe_allow_html=True)

def render_indexed_pill(filename: str):
    """Renders slim glass pill showing active document status."""
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, rgba(255,255,255,.13), rgba(255,255,255,.04)); border: 1px solid rgba(45,226,200,.4); backdrop-filter: blur(18px); border-radius: 99px; padding: 10px 20px; display: inline-flex; align-items: center; gap: 10px; margin-bottom: 24px; box-shadow: 0 10px 25px rgba(0,0,0,0.3);">
      <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="#5CF0DA" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true">
        <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/>
        <polyline points="22 4 12 14.01 9 11.01"/>
      </svg>
      <span style="color: #EDEBFF; font-weight: 600; font-size: 14px;">{html.escape(filename)}</span>
      <span style="color: #5CF0DA; font-size: 12px; font-weight: 700; letter-spacing: 1px;">INDEXED</span>
    </div>
    """, unsafe_allow_html=True)

def render_user_message(content: str):
    """Renders user message bubble."""
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, #7C5CFF, #FF4FD8); border-radius: 22px 22px 6px 22px; padding: 16px 20px; max-width: 420px; font-size: 15px; color: #FFFFFF; margin-left: auto; margin-bottom: 16px; box-shadow: 0 10px 25px rgba(124,92,255,0.3); word-break: break-word;">
      {html.escape(content)}
    </div>
    """, unsafe_allow_html=True)

def render_assistant_message(content: str, sources: list):
    """Renders assistant message panel with citation chips."""
    num_sources = len(sources)
    
    chips_list = []
    for idx, s in enumerate(sources):
        doc_name = html.escape(str(s.get("doc_name", "document")))
        page = html.escape(str(s.get("page", "?")))
        chip = f'<span style="display:inline-block; padding:4px 10px; border-radius:99px; background:rgba(45,226,200,.18); color:#5CF0DA; font-size:12px; font-weight:600; margin-right:6px; margin-top:8px;">{idx+1} {doc_name} p.{page}</span>'
        chips_list.append(chip)
        
    chips_html = "".join(chips_list)

    st.markdown(f'''<div style="background: linear-gradient(135deg, rgba(255,255,255,.13), rgba(255,255,255,.04)); border: 1px solid rgba(255,255,255,.2); backdrop-filter: blur(18px); -webkit-backdrop-filter: blur(18px); border-radius: 22px; padding: 24px; max-width: 600px; font-size: 15px; line-height: 1.7; color: #EDEBFF; margin-bottom: 24px; box-shadow: 0 20px 40px rgba(0,0,0,0.3);"><div style="color: #5CF0DA; font-size: 12px; letter-spacing: 2px; font-weight: 700; margin-bottom: 12px; text-transform: uppercase;">ANSWER &middot; {num_sources} SOURCES</div><div>{content}</div><div style="margin-top: 14px;">{chips_html}</div></div>''', unsafe_allow_html=True)

def render_thinking():
    """Renders 3 pulsing teal dots inside a glass pill."""
    st.markdown("""
    <style>
    @keyframes pulseDot {
      0%, 100% { opacity: 0.3; transform: scale(0.8); }
      50% { opacity: 1; transform: scale(1.2); }
    }
    .dot-1 { animation: pulseDot 1.4s infinite 0s; }
    .dot-2 { animation: pulseDot 1.4s infinite 0.2s; }
    .dot-3 { animation: pulseDot 1.4s infinite 0.4s; }
    </style>
    
    <div style="background: linear-gradient(135deg, rgba(255,255,255,.13), rgba(255,255,255,.04)); border: 1px solid rgba(255,255,255,.2); backdrop-filter: blur(18px); border-radius: 99px; padding: 12px 24px; display: inline-flex; align-items: center; gap: 8px; margin-bottom: 20px;">
      <span style="color: #5CF0DA; font-size: 13px; font-weight: 600; margin-right: 4px;">Thinking</span>
      <span class="dot-1" style="width: 8px; height: 8px; background: #5CF0DA; border-radius: 50%;"></span>
      <span class="dot-2" style="width: 8px; height: 8px; background: #5CF0DA; border-radius: 50%;"></span>
      <span class="dot-3" style="width: 8px; height: 8px; background: #5CF0DA; border-radius: 50%;"></span>
    </div>
    """, unsafe_allow_html=True)

def render_indexing_progress():
    """Renders progress bar for indexing."""
    st.markdown("""
    <div style="background: linear-gradient(135deg, rgba(255,255,255,.13), rgba(255,255,255,.04)); border: 1px solid rgba(255,255,255,.2); backdrop-filter: blur(18px); border-radius: 22px; padding: 20px; margin-bottom: 20px;">
      <div style="color: #5CF0DA; font-weight: 600; font-size: 14px; margin-bottom: 10px;">
        Reading and indexing document...
      </div>
      <div style="width: 100%; height: 8px; background: rgba(255,255,255,.1); border-radius: 99px; overflow: hidden;">
        <div style="width: 100%; height: 100%; background: linear-gradient(135deg, #2DE2C8, #7C5CFF); animation: pulseDot 2s infinite;"></div>
      </div>
    </div>
    """, unsafe_allow_html=True)

def render_error(error_msg: str):
    """Renders plain-language glass error card."""
    st.markdown(f"""
    <div style="background: linear-gradient(135deg, rgba(255,255,255,.13), rgba(255,255,255,.04)); border-left: 4px solid #FF4FD8; border-top: 1px solid rgba(255,255,255,.2); border-right: 1px solid rgba(255,255,255,.2); border-bottom: 1px solid rgba(255,255,255,.2); backdrop-filter: blur(18px); border-radius: 16px; padding: 20px; color: #EDEBFF; margin-bottom: 20px;">
      <div style="color: #FF4FD8; font-weight: 700; font-size: 15px; margin-bottom: 6px;">Action Needed</div>
      <div style="font-size: 14px; line-height: 1.5; color: #B7B2E6;">{html.escape(error_msg)}</div>
      <div style="font-size: 12px; color: #5CF0DA; margin-top: 10px;">Hint: Check your API key or document upload and try again.</div>
    </div>
    """, unsafe_allow_html=True)

def render_no_sources():
    """Renders muted card when no relevant sources exist."""
    st.markdown("""
    <div style="background: linear-gradient(135deg, rgba(255,255,255,.13), rgba(255,255,255,.04)); border: 1px solid rgba(255,255,255,.2); backdrop-filter: blur(18px); border-radius: 22px; padding: 30px 20px; text-align: center; color: #B7B2E6; font-size: 14px;">
      Retrieved source context chunks will appear here as 3D glass cards once you ask a question.
    </div>
    """, unsafe_allow_html=True)

def render_3d_source_stack(sources: list):
    """Renders 3D Source Stack iframe with generous padding and margins to eliminate hover clipping."""
    n = len(sources)
    if n == 0:
        render_no_sources()
        return

    component_height = 80 + n * 155
    z_offsets = [30, 20, 10, 5, 0, 0]
    
    cards_html = []
    for i, src in enumerate(sources):
        z = z_offsets[i % len(z_offsets)]
        top = 25 + i * 150
        z_index = 50 - i
        
        delay_float = f"-{0.5 + i * 0.8:.1f}s"
        delay_entry = f"{i * 0.12:.2f}s"
        
        doc_name = html.escape(str(src.get("doc_name", "document")))
        page_str = html.escape(str(src.get("page", "?")))
        snippet = html.escape(str(src.get("snippet", ""))[:130])
        score = src.get("score", None)
        
        score_html = ""
        if score is not None:
            score_html = f'<span class="score-chip">{score:.2f}</span>'

        card_code = f"""
        <div class="source-card" style="
          top: {top}px;
          left: 18px;
          --z: {z}px;
          z-index: {z_index};
          animation-delay: {delay_float}, {delay_entry};
        ">
          <div class="card-header">
            <div class="card-title-group">
              <span class="chip-num">{i+1}</span>
              <span class="card-title">{doc_name} &middot; p.{page_str}</span>
            </div>
            {score_html}
          </div>
          <div class="card-snippet">{snippet}...</div>
        </div>
        """
        cards_html.append(card_code)

    full_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
    <meta charset="utf-8">
    <style>
      @import url('https://fonts.googleapis.com/css2?family=Sora:wght@400;600;700&display=swap');
      * {{ box-sizing: border-box; }}
      body {{
        margin: 0; padding: 25px 20px 20px 20px;
        background: transparent;
        font-family: 'Sora', sans-serif;
        color: #EDEBFF;
        overflow: hidden;
      }}
      .stack-container {{
        perspective: 1000px;
        position: relative;
        width: 100%;
        height: {component_height}px;
        transform-style: preserve-3d;
      }}
      .source-card {{
        position: absolute;
        width: calc(100% - 36px);
        max-width: 310px;
        padding: 14px 16px;
        background: linear-gradient(135deg, rgba(255,255,255,.14), rgba(255,255,255,.04));
        border: 1px solid rgba(255,255,255,.22);
        backdrop-filter: blur(18px);
        -webkit-backdrop-filter: blur(18px);
        border-radius: 18px;
        box-shadow: 0 15px 35px rgba(0,0,0,.45), 0 0 20px rgba(124,92,255,.2);
        transition: transform 0.3s cubic-bezier(0.175, 0.885, 0.32, 1.275), box-shadow 0.3s ease, border-color 0.3s ease;
        transform: translateZ(var(--z)) rotateY(-4deg) rotateX(2deg);
        animation: cardFloat 6s ease-in-out infinite, cardSlideIn 0.5s ease forwards;
        pointer-events: auto !important;
        cursor: pointer;
      }}
      .source-card:hover {{
        transform: translateZ(50px) scale(1.02) rotateY(0deg) rotateX(0deg) !important;
        border-color: rgba(45,226,200,0.85) !important;
        box-shadow: 0 25px 50px rgba(0,0,0,.7), 0 0 35px rgba(45,226,200,.5) !important;
        z-index: 99999 !important;
      }}
      .card-header {{ display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px; }}
      .card-title-group {{ display: flex; align-items: center; gap: 8px; overflow: hidden; }}
      .chip-num {{ background: rgba(45, 226, 200, 0.25); color: #5CF0DA; font-size: 11px; font-weight: 700; padding: 2px 7px; border-radius: 99px; flex-shrink: 0; }}
      .card-title {{ font-size: 12px; font-weight: 700; color: #EDEBFF; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }}
      .score-chip {{ background: rgba(45,226,200,.18); color: #5CF0DA; font-size: 10px; font-weight: 600; padding: 2px 6px; border-radius: 99px; flex-shrink: 0; }}
      .card-snippet {{ font-size: 12px; line-height: 1.4; color: #B7B2E6; display: -webkit-box; -webkit-line-clamp: 3; -webkit-box-orient: vertical; overflow: hidden; }}
      @keyframes cardFloat {{
        0%, 100% {{ transform: translateZ(var(--z)) rotateY(-4deg) rotateX(2deg); }}
        50% {{ transform: translateZ(var(--z)) rotateY(-4deg) rotateX(2deg) translateY(-6px); }}
      }}
      @keyframes cardSlideIn {{
        from {{ opacity: 0; transform: translateZ(var(--z)) translateX(30px); }}
        to {{ opacity: 1; }}
      }}
    </style>
    </head>
    <body>
      <div class="stack-container">
        {"".join(cards_html)}
      </div>
    </body>
    </html>
    """
    st.components.v1.html(full_html, height=component_height)
