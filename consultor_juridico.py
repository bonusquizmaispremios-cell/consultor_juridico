import streamlit as st
from groq import Groq
from datetime import datetime
import json
import re

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="CONSULTOR JURÍDICO", layout="wide")

# --- ESTILO CSS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    .stApp { background-color:#F6FBF4; font-family:'Inter',sans-serif; }
    [data-testid="stSidebar"] { display:none; }

    .stTextInput>div>div>input, .stTextArea>div>textarea,
    .stSelectbox>div>div>div, .stNumberInput>div>div>input {
        background-color:#FFFFFF !important; color:#1A1A2E !important;
        border:1px solid #CED4DA !important; font-family:'Inter',sans-serif !important;
    }

    .stButton>button {
        width:100%; border-radius:10px; height:3.2em;
        background:linear-gradient(135deg,#16A34A,#15803D) !important; color:white !important;
        font-weight:600; border:none; box-shadow:2px 2px 8px rgba(0,0,0,0.1);
        font-family:'Inter',sans-serif !important; transition:all 0.2s ease;
    }
    .stButton>button:hover { background:linear-gradient(135deg,#15803D,#166534) !important; transform:translateY(-1px); }
    .stApp .stButton>button, .stApp .stButton>button p,
    .stApp .stButton>button span, .stApp .stButton>button div { color:white !important; }

    .stApp h1, .stApp h2, .stApp h3 { color:#14532D !important; font-family:'Inter',sans-serif !important; font-weight:700 !important; }

    .card { background:linear-gradient(135deg,#F0FDF4,#DCFCE7); padding:20px; border-radius:14px; border:1px solid #86EFAC; margin-bottom:14px; white-space:normal; word-wrap:break-word; }
    .stApp .card, .stApp .card p, .stApp .card span, .stApp .card div, .stApp .card strong, .stApp .card em { color:#14532D !important; }

    .card-dark { background:linear-gradient(135deg,#DCFCE7,#D1FAE5); padding:20px; border-radius:14px; border:1px solid #6EE7B7; margin-bottom:14px; white-space:normal; word-wrap:break-word; }
    .stApp .card-dark, .stApp .card-dark p, .stApp .card-dark span, .stApp .card-dark div, .stApp .card-dark strong { color:#14532D !important; }

    .card-green { background:linear-gradient(135deg,#DCFCE7,#BBF7D0); padding:20px; border-radius:14px; border:1px solid #4ADE80; margin-bottom:14px; white-space:normal; word-wrap:break-word; }
    .stApp .card-green, .stApp .card-green p, .stApp .card-green span, .stApp .card-green div { color:#14532D !important; }

    .card-blue { background:linear-gradient(135deg,#EFF6FF,#DBEAFE); padding:20px; border-radius:14px; border:1px solid #93C5FD; margin-bottom:14px; white-space:normal; word-wrap:break-word; }
    .stApp .card-blue, .stApp .card-blue p, .stApp .card-blue span, .stApp .card-blue div { color:#1E3A8A !important; }

    .card-red { background:linear-gradient(135deg,#FFF5F5,#FEE2E2); padding:20px; border-radius:14px; border:1px solid #FECACA; margin-bottom:14px; white-space:normal; word-wrap:break-word; }
    .stApp .card-red, .stApp .card-red p, .stApp .card-red span, .stApp .card-red div { color:#7F1D1D !important; }

    .card-yellow { background:linear-gradient(135deg,#FFFBEB,#FEF3C7); padding:18px; border-radius:12px; border:1px solid #FCD34D; margin-bottom:12px; white-space:normal; word-wrap:break-word; }
    .stApp .card-yellow, .stApp .card-yellow p, .stApp .card-yellow span, .stApp .card-yellow div { color:#78350F !important; }

    .stat-box { background:#FFFFFF; border-radius:12px; padding:16px; text-align:center; border:1px solid #86EFAC; }
    .stApp .stat-box div, .stApp .stat-box span, .stApp .stat-box p { color:#14532D !important; }
    .stApp .stat-numero, .stat-numero { font-size:2em; font-weight:700; color:#166534 !important; }

    .hist-item { background:#FFFFFF; border-radius:10px; padding:12px 16px; margin-bottom:8px; border-left:4px solid #86EFAC; }
    .stApp .hist-item, .stApp .hist-item p, .stApp .hist-item span, .stApp .hist-item div, .stApp .hist-item small { color:#14532D !important; }

    .badge { background:#166534; color:white !important; padding:4px 12px; border-radius:20px; font-size:0.78em; font-weight:600; display:inline-block; margin:2px; }
    .badge-verde { background:#059669; color:white !important; padding:4px 12px; border-radius:20px; font-size:0.78em; font-weight:600; display:inline-block; margin:2px; }
    .badge-amarelo { background:#B45309; color:white !important; padding:4px 12px; border-radius:20px; font-size:0.78em; font-weight:600; display:inline-block; margin:2px; }
    .badge-azul { background:#1D4ED8; color:white !important; padding:4px 12px; border-radius:20px; font-size:0.78em; font-weight:600; display:inline-block; margin:2px; }
    .badge-roxo { background:#6D28D9; color:white !important; padding:4px 12px; border-radius:20px; font-size:0.78em; font-weight:600; display:inline-block; margin:2px; }

    .divider { border:none; height:1px; background:linear-gradient(to right,transparent,#86EFAC,transparent); margin:18px 0; }

    .chat-user { background:#FFFFFF; border:1px solid #86EFAC; border-radius:12px 12px 4px 12px; padding:12px 16px; margin:8px 0; }
    .stApp .chat-user, .stApp .chat-user p, .stApp .chat-user span, .stApp .chat-user div { color:#14532D !important; }

    .chat-persona { background:#F6FBF4; border:1px solid #86EFAC; border-radius:4px 12px 12px 12px; padding:12px 16px; margin:8px 0; }
    .stApp .chat-persona, .stApp .chat-persona p, .stApp .chat-persona span, .stApp .chat-persona div { color:#14532D !important; }

    .questao-box { background:#FFFFFF; border:2px solid #86EFAC; border-radius:12px; padding:18px; margin-bottom:14px; }
    .stApp .questao-box, .stApp .questao-box p, .stApp .questao-box span, .stApp .questao-box div { color:#14532D !important; }

    .avaliacao-box { background:#FFFFFF; border:2px solid #86EFAC; border-radius:14px; padding:18px; margin-bottom:12px; }
    .stApp .avaliacao-box, .stApp .avaliacao-box p, .stApp .avaliacao-box span, .stApp .avaliacao-box div { color:#14532D !important; }

    .meta-box { background:#FFFFFF; border:2px solid #86EFAC; border-radius:12px; padding:16px; text-align:center; margin:10px 0; }
    .stApp .meta-box, .stApp .meta-box div, .stApp .meta-box span { color:#14532D !important; }
    .stApp .meta-numero { font-size:2em; font-weight:700; color:#166534 !important; }

    .chat-scroll-container { max-height:40vh; overflow-y:auto; display:flex; flex-direction:column; scroll-behavior:smooth; padding-bottom:4px; }
    .chat-scroll-container > * { flex-shrink:0; }
    

    </style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# CACHE
# ─────────────────────────────────────────────
@st.cache_resource
def get_cache_juridico():
    return {"perfis": {}}

_cache = get_cache_juridico()

# ─────────────────────────────────────────────
# PERSISTÊNCIA LOCAL (JSON)
# ─────────────────────────────────────────────
CHAVES_SALVAR = [
    'usuario', 'historico_consultas', 'consultas_salvas', 'estado_padrao',
]

def gerar_json_sessao() -> str:
    dados = {k: st.session_state.get(k) for k in CHAVES_SALVAR}
    dados['salvo_em'] = datetime.now().strftime('%d/%m/%Y %H:%M')
    return json.dumps(dados, ensure_ascii=False, indent=2, default=str)

def carregar_json_sessao(dados):
    _bloq = {'api_key','etapa','nome_login','chave_login','upload_login','btn_entrar_login'}
    _pref = (
        'btn_','sel_','ul_','dl_','cad_','_sub','_sm','_tab','_bsc',
        'ativo_','rem_','sel_pet_','ev_','prof_','hig_','prev_',
        'vac_','sint_','comp_','trad_','subs_','amb_','viag_','chat_',
        'duvida_','emerg_','peso_','data_','obs_','tipo_','vet_','desc_',
        'local_','prox_','alim','sit_emerg_','tc_','oraf','siau','agmag',
        'lv','mv','pt','pi','sh','wc','rv','rp','rc',
    )
    import re as _re
    for k, v in dados.items():
        if k in _bloq: continue
        if any(k.startswith(p) for p in _pref): continue
        if _re.match(r'.+_\d+$', k): continue
        st.session_state[k] = v

def salvar_perfil_cache(usuario: str):
    _cache["perfis"][usuario] = {k: st.session_state.get(k) for k in CHAVES_SALVAR}

def perfis_salvos() -> list:
    return list(_cache["perfis"].keys())

def carregar_perfil_cache(usuario: str) -> dict | None:
    return _cache["perfis"].get(usuario)

def salvar_consulta(modulo: str, pergunta: str, conteudo: str):
    st.session_state.historico_consultas.append({
        'data':     datetime.now().strftime('%d/%m %H:%M'),
        'modulo':   modulo,
        'pergunta': pergunta,
        'conteudo': conteudo,
    })

# --- INICIALIZAÇÃO DE ESTADO ---
defaults = {
    'etapa':              "Login",
    'usuario':            "",
    'api_key':            "",
    'pagina':              "Home",
    'historico_consultas': [],
    'consultas_salvas':    [],
    'estado_padrao':       "",
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# --- PRINCÍPIO ÉTICO COMPARTILHADO ---
PRINCIPIO_JURIDICO = """
PRINCÍPIO OBRIGATÓRIO — siga isso em TODA resposta:
- Você fornece ORIENTAÇÃO JURÍDICA GERAL E EDUCATIVA baseada na legislação brasileira — você NÃO é advogado e isso NÃO é
  aconselhamento jurídico definitivo para o caso específico da pessoa
- NUNCA afirme com certeza absoluta o resultado de um caso ("você vai ganhar", "isso é ilegal com certeza") —
  use linguagem como "em geral, a legislação prevê...", "esse tipo de situação costuma se enquadrar em...", "isso pode configurar..."
- Sempre cite a lei/norma relevante de forma geral (ex: Código de Defesa do Consumidor, CLT, Código Civil) quando souber,
  mas deixe claro que a aplicação exata depende dos detalhes do caso
- SEMPRE recomende buscar um advogado, a Defensoria Pública (gratuita) ou o órgão competente para casos que precisem de
  ação judicial, são complexos, ou envolvam valores/riscos altos
- Para crimes contra a honra e discriminação (racismo, injúria racial, difamação, calúnia, ameaças), seja especialmente
  cuidadoso: explique a diferença entre os conceitos de forma clara, mas sempre oriente a registrar Boletim de Ocorrência
  e buscar a Defensoria Pública ou Ministério Público — nunca minimize a gravidade nem garanta desfecho
- Tom: didático, acolhedor e claro — sem jargão jurídico excessivo, traduza termos técnicos quando usá-los
- Português do Brasil
"""

DISCLAIMER_PADRAO = """
<div class="disclaimer">
⚠️ <strong>Importante:</strong> esta é uma orientação jurídica geral e educativa gerada por IA, baseada na legislação brasileira —
não substitui a consulta com um advogado, que pode analisar as particularidades do seu caso. Para casos que envolvam valores
altos, urgência ou processo judicial, busque um advogado ou a Defensoria Pública (gratuita, para quem não pode pagar).
</div>
"""

# --- MOTOR DE IA ---
def juridico_ia(prompt: str, modulo: str, system_extra: str = "") -> str:
    try:
        client = Groq(api_key=st.session_state.api_key)
        contexto_estado = f"\nEstado/região do usuário (se relevante para legislação local): {st.session_state.estado_padrao}." if st.session_state.estado_padrao else ""
        system = f"""Você é um consultor de orientação jurídica geral, especialista em {modulo}, com conhecimento da legislação brasileira.
Usuário: {st.session_state.usuario}.{contexto_estado}
{PRINCIPIO_JURIDICO}
{system_extra}"""
        response = client.chat.completions.create(
            messages=[
                {"role": "system", "content": system},
                {"role": "user", "content": prompt},
            ],
            model="openai/gpt-oss-120b",
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"⚠️ Erro na API: {e}"

# --- BARRA DE SALVAR ---
def barra_salvar():
    salvar_perfil_cache(st.session_state.usuario)
    nome_usuario = st.session_state.usuario.lower().replace(' ', '_') or 'minha_sessao'
    total  = len(st.session_state.historico_consultas)
    salvos = len(st.session_state.consultas_salvas)

    col_info, col_btn = st.columns([4, 2])
    with col_info:
        st.markdown(
            f"<div style='background:#F5F3FF;border:1px solid #7C3AED;border-radius:10px;"
            f"padding:10px 14px;font-size:0.84em;color:#1A1A2E;line-height:1.6;'>"
            f"💾 <strong>Antes de sair, salve seus dados no computador.</strong><br>"
            f"<span style='color:#888;font-size:0.88em;'>{total} consultas geradas · {salvos} salvas</span>"
            f"</div>",
            unsafe_allow_html=True
        )
    with col_btn:
        st.download_button(
            label="💾 SALVAR MEUS DADOS (.json)",
            data=gerar_json_sessao(),
            file_name=f"consultor_juridico_{nome_usuario}.json",
            mime="application/json",
            use_container_width=True,
            key="consulto9"
        )
    st.markdown("<hr class='divider'>", unsafe_allow_html=True)
    st.markdown("""<style>
    .dica-nav{font-size:0.72em;color:#94A3B8;text-align:center;padding:2px 0 6px;}
    .dica-mobile{display:none;}
    .dica-desktop{display:block;}
    @media(max-width:768px){.dica-mobile{display:block;}.dica-desktop{display:none;}}
    </style>
    <div class='dica-nav dica-mobile'>👆 Deslize o dedo para navegar entre as abas</div>
    <div class='dica-nav dica-desktop'>📋 Clique no ícone acima para abrir o menu completo</div>
    """, unsafe_allow_html=True)

# Estrutura dos módulos
MODULOS = {
    "Consumidor":      {"emoji": "⚖️", "titulo": "Direito do Consumidor", "cor": "card"},
    "Trabalho":        {"emoji": "💼", "titulo": "Direito do Trabalho", "cor": "card-blue"},
    "Moradia":         {"emoji": "🏠", "titulo": "Moradia e Aluguel", "cor": "card-orange"},
    "Contratos":       {"emoji": "📜", "titulo": "Contratos em Geral", "cor": "card"},
    "Transito":        {"emoji": "🚗", "titulo": "Trânsito", "cor": "card-blue"},
    "Familia":         {"emoji": "👨‍👩‍👧", "titulo": "Direito de Família", "cor": "card-orange"},
    "GolpesDigitais":  {"emoji": "📱", "titulo": "Golpes e Fraudes Digitais", "cor": "card-red"},
    "Crimes":          {"emoji": "👮", "titulo": "Crimes em Geral", "cor": "card-red"},
    "Condominio":      {"emoji": "🏢", "titulo": "Condomínio", "cor": "card"},
    "MEI":             {"emoji": "📄", "titulo": "MEI e Pequenos Negócios", "cor": "card-green"},
    "CrimesHonra":      {"emoji": "🛡️", "titulo": "Racismo, Injúria, Difamação, Calúnia e Ameaças", "cor": "card-red"},
}

# ============================================================
# TELA: LOGIN
# ============================================================
if 'consultas_salvas' not in st.session_state: st.session_state['consultas_salvas'] = []
if 'estado_padrao' not in st.session_state: st.session_state['estado_padrao'] = None
if 'historico_consultas' not in st.session_state: st.session_state['historico_consultas'] = []

if st.session_state.etapa == "Login":
    st.markdown("# 🤖 CONSULTOR JURÍDICO")
    st.markdown("<div class=\'card\'><b>🔒 ACESSO RESTRITO A CLIENTES DO QUIZ COM PRÊMIOS</b><br>🔗 <a href='https://quizcompremios.com.br' target='_blank' style='color:#4F46E5;font-weight:700;text-decoration:underline;'>quizcompremios.com.br</a></div>", unsafe_allow_html=True)
    st.info("💻 **Dica:** Pela complexidade dos agentes, no computador a experiência é mais agradável.")
    with st.container():
        nome  = st.text_input("Seu Nome:", key="nome_login")
        chave = st.text_input("🔑 Sua Chave API da Groq:", type="password", key="chave_login")
        arq_j = st.file_uploader("📂 Carregar dados salvos (.json):", type=["json"], key="upload_login")
        dados_login = json.load(arq_j) if arq_j else None
        if st.button("✨ ENTRAR", key="btn_entrar_login"):
            if len(nome.strip()) < 2:
                st.warning("Digite um nome com pelo menos 2 caracteres.")
            elif chave.strip():
                st.session_state.usuario = nome.strip()
                st.session_state.api_key = chave
                if dados_login: carregar_json_sessao(dados_login)
                st.session_state.etapa = "App"
                st.rerun()
            else:
                st.warning("Preencha nome e chave API.")

elif st.session_state.etapa == "App":


    st.markdown("""<div class="disclaimer-topo">
    ⚖️ <strong>Este consultor oferece orientação jurídica geral e educativa</strong> — não substitui um advogado.
    Para casos urgentes, com valores altos ou que exijam ação judicial, consulte um advogado ou a <strong>Defensoria Pública</strong> (gratuita).
    </div>""", unsafe_allow_html=True)


    # TABS — navegação nativa
    (_tab_Home, _tab_Consumidor, _tab_Trabalho, _tab_Moradia, _tab_Contratos, _tab_Transito, _tab_Familia, _tab_GolpesDigitais, _tab_Crimes, _tab_Condominio, _tab_MEI, _tab_CrimesHonra, _tab_Provas, _tab_Ajuda, _tab_Biblioteca) = st.tabs(['🏠 Painel', '⚖️ Consumidor', '💼 Trabalho', '🏠 Moradia', '📜 Contratos', '🚗 Trânsito', '👨\u200d👩\u200d👧 Família', '📱 Golpes Digitais', '👮 Crimes', '🏢 Condomínio', '🏪 MEI', '😤 Crimes Honra', '📂 Provas', '❓ Ajuda', '📚 Biblioteca'])

    # ── BARRA SALVAR — aparece em todas as abas ──
    with st.expander("💾 Salvar / Carregar meus dados", expanded=False):
        _bsc1, _bsc2 = st.columns(2)
        with _bsc1:
            import json as _jsv
            _dsv = {k: st.session_state.get(k) for k in list(st.session_state.keys()) if not k.startswith('_') and k not in ('api_key',)}
            st.download_button("💾 Baixar meus dados (.json)",
                data=_jsv.dumps(_dsv, ensure_ascii=False, indent=2, default=str),
                file_name=f"dados_{st.session_state.get('usuario','user')}.json",
                mime="application/json", key="dl_barra_sv_consulto")
        with _bsc2:
            _fupsv = st.file_uploader("📂 Carregar dados salvos:", type=["json"], key="ul_barra_sv_consulto", label_visibility="collapsed")
            if _fupsv:
                try:
                    import json as _jld
                    for _k2,_v2 in _jld.loads(_fupsv.read().decode()).items():
                        if _k2 not in ('api_key','etapa'): st.session_state[_k2] = _v2
                    st.success("✅ Dados restaurados!"); st.rerun()
                except: st.error("Arquivo inválido.")


    with _tab_Home:
        col_u, col_r = st.columns([3, 1])
        with col_u:
            st.title(f"Olá, {st.session_state.usuario}! ⚖️")
            st.markdown("<span class='badge'>Orientação Jurídica</span>", unsafe_allow_html=True)
        with col_r:
            if st.button("🚪 Sair", key="consulto3"):
                for k in list(st.session_state.keys()):
                    del st.session_state[k]
                st.rerun()

        if len(st.session_state.historico_consultas) == 0:
            st.markdown("""<div style="background:#FEF3C7;border:2px solid #F59E0B;border-radius:12px;
            padding:12px 18px;margin-bottom:4px;color:#000;font-size:0.9em;font-weight:600;">
            ⚠️ Seus dados não estão mais no servidor.
            </div>""", unsafe_allow_html=True)
            arq_home = st.file_uploader("Carregar meus dados salvos (.json):", type=["json"], key="upload_home")
            if arq_home is not None:
                try:
                    dados_home = json.load(arq_home)
                    carregar_json_sessao(dados_home)
                    salvar_perfil_cache(st.session_state.usuario)
                    st.success("✅ Dados recuperados!")
                    st.rerun()
                except Exception:
                    st.error("Arquivo inválido.")

        st.session_state.estado_padrao = st.text_input("📍 Seu estado (opcional, ajuda em questões regionais):", value=st.session_state.estado_padrao, placeholder="ex: São Paulo, Minas Gerais...", key="consulto4")


        modulos_count = {}
        for c in st.session_state.historico_consultas:
            modulos_count[c['modulo']] = modulos_count.get(c['modulo'], 0) + 1

        c1, c2, c3, c4 = st.columns(4)
        c1.markdown(f"<div class='stat-box'><div class='stat-numero'>{len(st.session_state.historico_consultas)}</div><div>Consultas geradas</div></div>", unsafe_allow_html=True)
        c2.markdown(f"<div class='stat-box'><div class='stat-numero'>{len(st.session_state.consultas_salvas)}</div><div>Salvas</div></div>", unsafe_allow_html=True)
        c3.markdown(f"<div class='stat-box'><div class='stat-numero'>{len(modulos_count)}</div><div>Áreas consultadas</div></div>", unsafe_allow_html=True)
        c4.markdown(f"<div class='stat-box'><div class='stat-numero'>{modulos_count.get('Consumidor',0)}</div><div>Direito do Consumidor</div></div>", unsafe_allow_html=True)

        st.markdown("<div class='card'>💡 <em>'Conhecer seus direitos é o primeiro passo para exercê-los. O segundo é saber quando buscar ajuda profissional.'</em></div>", unsafe_allow_html=True)

        st.markdown("### 🗺️ Módulos disponíveis")
        st.markdown("Clique nos ícones acima para acessar cada área:")
        guia = {
            "⚖️ Consumidor":        "Trocas, devoluções, garantia, propaganda enganosa, cobrança indevida",
            "💼 Trabalho":          "Demissão, horas extras, férias, rescisão, assédio, carteira assinada",
            "🏠 Moradia":           "Aluguel, despejo, condições do imóvel, fiador, depósito caução",
            "📜 Contratos":         "Cláusulas abusivas, rescisão, multas, o que verificar antes de assinar",
            "🚗 Trânsito":          "Multas, acidentes, CNH, seguro, direitos em caso de colisão",
            "👨‍👩‍👧 Família":           "Pensão alimentícia, guarda, divórcio, herança, união estável",
            "📱 Golpes Digitais":   "Pix, cartão clonado, compras online, como agir e se proteger",
            "👮 Crimes":            "Furto, roubo, estelionato, o que fazer e como denunciar",
            "🏢 Condomínio":        "Taxa condominial, regras, animais, barulho, vagas de garagem",
            "📄 MEI":               "Abertura, obrigações, impostos, direitos do microempreendedor",
            "🛡️ Crimes contra Honra":"Racismo, injúria racial, difamação, calúnia, ameaças — diferenças e como agir",
            "📂 Provas":            "O que reunir e como documentar qualquer situação jurídica",
            "🏛️ Onde Buscar Ajuda": "Defensoria, Procon, sindicatos, delegacias — endereços e como acessar",
        }
        for aba, desc in guia.items():
            st.markdown(f"**{aba}** — {desc}")

    with _tab_Consumidor:
        st.header("⚖️ Direito do Consumidor")
        st.markdown("*Tire suas dúvidas sobre direitos do consumidor.*")
        _prompt_consumidor = st.text_area("Descreva sua situação ou dúvida:", height=120, key="consul_consumidor_in", placeholder="Digite aqui...")
        if st.button("🤖 GERAR COM IA", key="consul_consumidor_btn", use_container_width=True):
            if _prompt_consumidor.strip():
                with st.spinner("Analisando..."):
                    try:
                        from groq import Groq as _GrT
                        _cli = _GrT(api_key=st.session_state.api_key)
                        _r = _cli.chat.completions.create(
                            model="openai/gpt-oss-120b",
                            messages=[{"role":"user","content":_prompt_consumidor}],
                            max_tokens=2048
                        )
                        st.markdown(f"<div class='card'>{_r.choices[0].message.content}</div>", unsafe_allow_html=True)
                    except Exception as _e:
                        st.error(f"Erro: {_e}")
            else:
                st.warning("Preencha o campo acima.")


    with _tab_Trabalho:
        st.header("💼 Direito do Trabalho")
        st.markdown("*Entenda seus direitos trabalhistas.*")
        _prompt_trabalho = st.text_area("Descreva sua situação ou dúvida:", height=120, key="consul_trabalho_in", placeholder="Digite aqui...")
        if st.button("🤖 GERAR COM IA", key="consul_trabalho_btn", use_container_width=True):
            if _prompt_trabalho.strip():
                with st.spinner("Analisando..."):
                    try:
                        from groq import Groq as _GrT
                        _cli = _GrT(api_key=st.session_state.api_key)
                        _r = _cli.chat.completions.create(
                            model="openai/gpt-oss-120b",
                            messages=[{"role":"user","content":_prompt_trabalho}],
                            max_tokens=2048
                        )
                        st.markdown(f"<div class='card'>{_r.choices[0].message.content}</div>", unsafe_allow_html=True)
                    except Exception as _e:
                        st.error(f"Erro: {_e}")
            else:
                st.warning("Preencha o campo acima.")


    with _tab_Moradia:
        st.header("🏠 Moradia e Aluguel")
        st.markdown("*Dúvidas sobre contratos de locação e moradia.*")
        _prompt_moradia = st.text_area("Descreva sua situação ou dúvida:", height=120, key="consul_moradia_in", placeholder="Digite aqui...")
        if st.button("🤖 GERAR COM IA", key="consul_moradia_btn", use_container_width=True):
            if _prompt_moradia.strip():
                with st.spinner("Analisando..."):
                    try:
                        from groq import Groq as _GrT
                        _cli = _GrT(api_key=st.session_state.api_key)
                        _r = _cli.chat.completions.create(
                            model="openai/gpt-oss-120b",
                            messages=[{"role":"user","content":_prompt_moradia}],
                            max_tokens=2048
                        )
                        st.markdown(f"<div class='card'>{_r.choices[0].message.content}</div>", unsafe_allow_html=True)
                    except Exception as _e:
                        st.error(f"Erro: {_e}")
            else:
                st.warning("Preencha o campo acima.")


    with _tab_Contratos:
        st.header("📜 Contratos em Geral")
        st.markdown("*Análise e dúvidas sobre contratos.*")
        _prompt_contratos = st.text_area("Descreva sua situação ou dúvida:", height=120, key="consul_contratos_in", placeholder="Digite aqui...")
        if st.button("🤖 GERAR COM IA", key="consul_contratos_btn", use_container_width=True):
            if _prompt_contratos.strip():
                with st.spinner("Analisando..."):
                    try:
                        from groq import Groq as _GrT
                        _cli = _GrT(api_key=st.session_state.api_key)
                        _r = _cli.chat.completions.create(
                            model="openai/gpt-oss-120b",
                            messages=[{"role":"user","content":_prompt_contratos}],
                            max_tokens=2048
                        )
                        st.markdown(f"<div class='card'>{_r.choices[0].message.content}</div>", unsafe_allow_html=True)
                    except Exception as _e:
                        st.error(f"Erro: {_e}")
            else:
                st.warning("Preencha o campo acima.")


    with _tab_Transito:
        st.header("🚗 Direito de Trânsito")
        st.markdown("*Multas, acidentes e questões de trânsito.*")
        _prompt_transito = st.text_area("Descreva sua situação ou dúvida:", height=120, key="consul_transito_in", placeholder="Digite aqui...")
        if st.button("🤖 GERAR COM IA", key="consul_transito_btn", use_container_width=True):
            if _prompt_transito.strip():
                with st.spinner("Analisando..."):
                    try:
                        from groq import Groq as _GrT
                        _cli = _GrT(api_key=st.session_state.api_key)
                        _r = _cli.chat.completions.create(
                            model="openai/gpt-oss-120b",
                            messages=[{"role":"user","content":_prompt_transito}],
                            max_tokens=2048
                        )
                        st.markdown(f"<div class='card'>{_r.choices[0].message.content}</div>", unsafe_allow_html=True)
                    except Exception as _e:
                        st.error(f"Erro: {_e}")
            else:
                st.warning("Preencha o campo acima.")


    with _tab_Familia:
        st.header("👨‍👩‍👧 Direito de Família")
        st.markdown("*Divórcio, guarda, pensão e família.*")
        _prompt_familia = st.text_area("Descreva sua situação ou dúvida:", height=120, key="consul_familia_in", placeholder="Digite aqui...")
        if st.button("🤖 GERAR COM IA", key="consul_familia_btn", use_container_width=True):
            if _prompt_familia.strip():
                with st.spinner("Analisando..."):
                    try:
                        from groq import Groq as _GrT
                        _cli = _GrT(api_key=st.session_state.api_key)
                        _r = _cli.chat.completions.create(
                            model="openai/gpt-oss-120b",
                            messages=[{"role":"user","content":_prompt_familia}],
                            max_tokens=2048
                        )
                        st.markdown(f"<div class='card'>{_r.choices[0].message.content}</div>", unsafe_allow_html=True)
                    except Exception as _e:
                        st.error(f"Erro: {_e}")
            else:
                st.warning("Preencha o campo acima.")


    with _tab_GolpesDigitais:
        m = MODULOS["GolpesDigitais"]
        st.header(f"{m['emoji']} {m['titulo']}")
        st.markdown("Caiu em um golpe ou suspeita de fraude? Veja seus direitos e o que fazer.")

        tipo_golpe = st.selectbox("Tipo de situação:", key="select_tipo_golpe", options=[
            "Pix enviado por engano ou golpe", "Compra online que não chegou", "Cartão de crédito clonado",
            "Cobrança que não reconheço na fatura", "Conta bancária invadida", "Golpe do falso boleto",
            "Compra com produto não entregue/diferente", "Outro tipo de fraude digital",
        ])
        detalhes_golpe = st.text_area("Detalhes da situação:", height=100,
            placeholder="ex: Transferi R$500 via Pix para uma pessoa que se identificou como funcionário do banco...", key="consulto8")

        if st.button("⚖️ OBTER ORIENTAÇÃO", key="consulto5"):
            if detalhes_golpe.strip():
                with st.spinner("Analisando..."):
                    prompt = (
                        f"Situação: {tipo_golpe}. Detalhes: {detalhes_golpe}\n\n"
                        f"FORMATO:\n\n"
                        f"📋 RESUMO DA SITUAÇÃO:\n[confirmação do entendimento]\n\n"
                        f"⚖️ SEUS DIREITOS NESTE CASO:\n[o que a legislação (CDC, normas do Banco Central) prevê para esse tipo de fraude]\n\n"
                        f"⚡ AÇÕES IMEDIATAS (faça AGORA):\n"
                        f"1. [ação mais urgente — geralmente contatar o banco]\n2. [ação 2]\n3. [ação 3]\n\n"
                        f"📂 PROVAS A REUNIR:\n[prints, comprovantes, registros de conversa, etc]\n\n"
                        f"🏛️ ONDE REGISTRAR:\n[Boletim de Ocorrência online, Banco Central via SR, Procon, etc]\n\n"
                        f"💰 CHANCE DE REAVER O VALOR:\n[explicação geral e honesta sobre o que costuma ser possível ou não nesse tipo de caso]"
                    )
                    res = juridico_ia(prompt, "Golpes Digitais")
                    if res: st.session_state['res_golpesdigita_consul2'] = str(res)
                    salvar_consulta("GolpesDigitais", f"{tipo_golpe}: {detalhes_golpe[:60]}", res)
                    st.session_state['resposta_golpes'] = res
            else:
                st.warning("Descreva os detalhes da situação.")

        if st.session_state.get('resposta_golpes'):
            st.markdown(f"<div class='card-red'>{st.session_state['resposta_golpes']}</div>", unsafe_allow_html=True)
            st.markdown(DISCLAIMER_PADRAO, unsafe_allow_html=True)
            col_dl, col_sv = st.columns(2)
            with col_dl:
                st.download_button("📋 Baixar (.txt)", data=st.session_state['resposta_golpes'],
                    file_name="orientacao_golpe.txt", mime="text/plain", use_container_width=True, key="consulto7")
            with col_sv:
                if st.button("❤️ Salvar", key="sv_golpes", use_container_width=True):
                    st.session_state.consultas_salvas.append({
                        'modulo': 'GolpesDigitais', 'pergunta': tipo_golpe,
                        'conteudo': st.session_state['resposta_golpes'],
                        'data': datetime.now().strftime('%d/%m %H:%M'),
                    })
                    st.success("❤️ Salvo!")

        # ========================
        # CRIMES EM GERAL
        # ========================

    with _tab_Crimes:
        m = MODULOS["Crimes"]
        st.header(f"{m['emoji']} {m['titulo']}")
        st.markdown("Foi vítima de um crime? Entenda seus direitos e os próximos passos.")

        tipo_crime = st.selectbox("Tipo de situação:", key="select_tipo_crime", options=[
            "Furto (sem violência)", "Roubo (com violência ou ameaça)", "Estelionato/fraude",
            "Invasão de domicílio", "Dano ao patrimônio", "Perda de documentos",
            "Vizinho/conhecido cometeu um crime contra mim", "Outra situação",
        ])
        detalhes_crime = st.text_area("Descreva o que aconteceu:", height=100,
            placeholder="ex: Meu celular foi furtado dentro do ônibus, sem que eu percebesse...", key="consulto6")

        if st.button("⚖️ OBTER ORIENTAÇÃO", key="consulto6_d2"):
            if detalhes_crime.strip():
                with st.spinner("Analisando..."):
                    prompt = (
                        f"Tipo de situação: {tipo_crime}. Detalhes: {detalhes_crime}\n\n"
                        f"FORMATO:\n\n"
                        f"📋 RESUMO E CLASSIFICAÇÃO GERAL:\n[explique de forma geral em qual tipo de situação isso se enquadra no Código Penal, sem certeza absoluta]\n\n"
                        f"⚡ O QUE FAZER IMEDIATAMENTE:\n[passos práticos — segurança pessoal primeiro, depois burocrático]\n\n"
                        f"📝 COMO REGISTRAR O BOLETIM DE OCORRÊNCIA:\n[onde e como — presencial ou online, dependendo do tipo]\n\n"
                        f"📂 PROVAS E INFORMAÇÕES A REUNIR:\n[o que documentar para esse caso]\n\n"
                        f"🏛️ PRÓXIMOS PASSOS APÓS O BO:\n[o que normalmente acontece depois — investigação, possível indenização civil, etc]"
                    )
                    res = juridico_ia(prompt, "Crimes")
                    if res: st.session_state['res_crimes_consul3'] = str(res)
                    salvar_consulta("Crimes", f"{tipo_crime}: {detalhes_crime[:60]}", res)
                    st.session_state['resposta_crimes'] = res
            else:
                st.warning("Descreva o que aconteceu.")

        if st.session_state.get('resposta_crimes'):
            st.markdown(f"<div class='card-red'>{st.session_state['resposta_crimes']}</div>", unsafe_allow_html=True)
            st.markdown(DISCLAIMER_PADRAO, unsafe_allow_html=True)
            col_dl, col_sv = st.columns(2)
            with col_dl:
                st.download_button("📋 Baixar (.txt)", data=st.session_state['resposta_crimes'],
                    file_name="orientacao_crime.txt", mime="text/plain", use_container_width=True, key="consulto5_d2")
            with col_sv:
                if st.button("❤️ Salvar", key="sv_crimes", use_container_width=True):
                    st.session_state.consultas_salvas.append({
                        'modulo': 'Crimes', 'pergunta': tipo_crime,
                        'conteudo': st.session_state['resposta_crimes'],
                        'data': datetime.now().strftime('%d/%m %H:%M'),
                    })
                    st.success("❤️ Salvo!")

        # ========================
        # CRIMES CONTRA A HONRA / DISCRIMINAÇÃO
        # ========================

    with _tab_Condominio:
        st.header("🏢 Condomínio")
        st.markdown("*Regras, conflitos e direitos em condomínio.*")
        _prompt_condominio = st.text_area("Descreva sua situação ou dúvida:", height=120, key="consul_condominio_in", placeholder="Digite aqui...")
        if st.button("🤖 GERAR COM IA", key="consul_condominio_btn", use_container_width=True):
            if _prompt_condominio.strip():
                with st.spinner("Analisando..."):
                    try:
                        from groq import Groq as _GrT
                        _cli = _GrT(api_key=st.session_state.api_key)
                        _r = _cli.chat.completions.create(
                            model="openai/gpt-oss-120b",
                            messages=[{"role":"user","content":_prompt_condominio}],
                            max_tokens=2048
                        )
                        st.markdown(f"<div class='card'>{_r.choices[0].message.content}</div>", unsafe_allow_html=True)
                    except Exception as _e:
                        st.error(f"Erro: {_e}")
            else:
                st.warning("Preencha o campo acima.")


    with _tab_MEI:
        st.header("🏪 MEI e Microempresa")
        st.markdown("*Questões jurídicas para pequenos empreendedores.*")
        _prompt_mei = st.text_area("Descreva sua situação ou dúvida:", height=120, key="consul_mei_in", placeholder="Digite aqui...")
        if st.button("🤖 GERAR COM IA", key="consul_mei_btn", use_container_width=True):
            if _prompt_mei.strip():
                with st.spinner("Analisando..."):
                    try:
                        from groq import Groq as _GrT
                        _cli = _GrT(api_key=st.session_state.api_key)
                        _r = _cli.chat.completions.create(
                            model="openai/gpt-oss-120b",
                            messages=[{"role":"user","content":_prompt_mei}],
                            max_tokens=2048
                        )
                        st.markdown(f"<div class='card'>{_r.choices[0].message.content}</div>", unsafe_allow_html=True)
                    except Exception as _e:
                        st.error(f"Erro: {_e}")
            else:
                st.warning("Preencha o campo acima.")


    with _tab_CrimesHonra:
        m = MODULOS["CrimesHonra"]
        st.header(f"{m['emoji']} {m['titulo']}")

        st.markdown("""<div class="disclaimer-topo">
        Estes são crimes previstos em lei e levados muito a sério pelo sistema de justiça brasileiro.
        Esta seção explica as diferenças entre os conceitos para te ajudar a entender e documentar a situação —
        mas a orientação mais importante em todos os casos é: <strong>registre Boletim de Ocorrência e busque a
        Defensoria Pública ou o Ministério Público</strong>.
        </div>""", unsafe_allow_html=True)

        tab1, tab2 = st.tabs(["📖 Entenda as Diferenças", "📝 Descrever Minha Situação"])

        with tab1:
            st.markdown("#### Entendendo cada conceito:")
            conceitos = {
                "🛡️ Racismo": "Discriminação ou preconceito em razão de raça, cor, etnia, religião ou procedência nacional. É crime previsto na Lei 7.716/1989 (Lei do Racismo) e considerado **inafiançável e imprescritível** pela Constituição Federal.",
                "🛡️ Injúria Racial": "Ofender a honra de alguém usando elementos raciais/étnicos como insulto direcionado à pessoa (diferente do racismo, que é mais genérico). Prevista no Código Penal, art. 140, §3º.",
                "🛡️ Difamação": "Atribuir a alguém um fato ofensivo à sua reputação, mesmo que verdadeiro, perante terceiros. Código Penal, art. 139.",
                "🛡️ Calúnia": "Atribuir falsamente a alguém um fato definido como crime, sabendo que é falso. Código Penal, art. 138.",
                "🛡️ Ameaça": "Prometer causar mal injusto e grave a alguém, por palavra, escrito, gesto ou outro meio simbólico. Código Penal, art. 147.",
            }
            for nome, desc in conceitos.items():
                st.markdown(f"<div class='card'><strong>{nome}</strong><br><br>{desc}</div>", unsafe_allow_html=True)

        with tab2:
            situacao_honra = st.text_area("📝 Descreva o que aconteceu:", height=140,
                placeholder="ex: Um colega de trabalho me chamou de um nome racista na frente de outras pessoas...", key="consulto4_d2")
            onde_aconteceu = st.selectbox("Onde aconteceu:", ["Presencialmente", "Redes sociais", "WhatsApp/mensagem", "Por telefone", "E-mail", "Outro"], key="consulto7_d2")
            tem_testemunhas = st.radio("Havia testemunhas?", ["Sim", "Não", "Não tenho certeza"], horizontal=True, key="consulto8_d2")

            if st.button("⚖️ OBTER ORIENTAÇÃO SOBRE ESTA SITUAÇÃO", key="consulto9_d2"):
                if situacao_honra.strip():
                    with st.spinner("Analisando..."):
                        prompt = (
                            f"Situação relatada: {situacao_honra}\n"
                            f"Onde aconteceu: {onde_aconteceu}. Testemunhas: {tem_testemunhas}.\n\n"
                            f"FORMATO:\n\n"
                            f"📋 RESUMO DA SITUAÇÃO:\n[confirmação do entendimento]\n\n"
                            f"⚖️ EM QUAL CONCEITO ISSO PODE SE ENQUADRAR:\n"
                            f"[Explique, com cautela, se isso parece se aproximar de racismo, injúria racial, difamação, calúnia e/ou ameaça —"
                            f" SEMPRE deixando claro que a classificação exata depende de análise do Ministério Público/juiz]\n\n"
                            f"📂 PROVAS ESSENCIAIS PARA ESTE CASO:\n"
                            f"[específico para o canal informado: {onde_aconteceu} — prints, gravações, testemunhas, etc]\n\n"
                            f"📝 COMO REGISTRAR O BOLETIM DE OCORRÊNCIA:\n[orientação prática]\n\n"
                            f"🏛️ ONDE BUSCAR APOIO ESPECÍFICO:\n"
                            f"[Defensoria Pública, Ministério Público, Disque 100/Disque Direitos Humanos, "
                            f"delegacias especializadas em crimes raciais se aplicável]\n\n"
                            f"💪 VOCÊ NÃO ESTÁ SOZINHO(A):\n[1-2 frases de acolhimento — sem minimizar a gravidade da situação]"
                        )
                        res = juridico_ia(prompt, "Crimes contra a Honra e Discriminação",
                            "Trate com máxima seriedade e acolhimento. Nunca minimize. Nunca garanta desfecho judicial.")
                        salvar_consulta("CrimesHonra", situacao_honra[:60], res)
                        st.session_state['resposta_honra'] = res
                else:
                    st.warning("Descreva a situação.")

            if st.session_state.get('resposta_honra'):
                st.markdown(f"<div class='card-red'>{st.session_state['resposta_honra']}</div>", unsafe_allow_html=True)
                st.markdown(DISCLAIMER_PADRAO, unsafe_allow_html=True)
                col_dl, col_sv = st.columns(2)
                with col_dl:
                    st.download_button("📋 Baixar (.txt)", data=st.session_state['resposta_honra'],
                        file_name="orientacao_crimes_honra.txt", mime="text/plain", use_container_width=True, key="consulto3_d2")
                with col_sv:
                    if st.button("❤️ Salvar", key="sv_honra", use_container_width=True):
                        st.session_state.consultas_salvas.append({
                            'modulo': 'CrimesHonra', 'pergunta': situacao_honra[:60],
                            'conteudo': st.session_state['resposta_honra'],
                            'data': datetime.now().strftime('%d/%m %H:%M'),
                        })
                        st.success("❤️ Salvo!")

        # ========================
        # QUAIS PROVAS REUNIR
        # ========================

    with _tab_Provas:
        st.header("📂 Quais Provas Reunir")
        st.markdown("Cada tipo de situação exige provas diferentes. Selecione o caso para saber o que documentar.")

        area_provas = st.selectbox("Tipo de situação:", key="select_area_provas", options=[
            "Problema com produto/loja (consumidor)", "Problema no trabalho/demissão",
            "Problema com aluguel/moradia", "Contrato descumprido", "Acidente de trânsito",
            "Disputa de família/pensão", "Golpe digital/fraude", "Crime contra a honra (racismo, injúria, etc)",
            "Conflito com vizinho/condomínio", "Outra situação",
        ])

        if st.button("📂 VER LISTA DE PROVAS NECESSÁRIAS", key="consulto10"):
            with st.spinner("Preparando lista..."):
                prompt = (
                    f"Para a situação: {area_provas}\n\n"
                    f"Liste de forma prática e organizada quais provas e documentos a pessoa deveria reunir.\n\n"
                    f"FORMATO:\n\n"
                    f"📂 PROVAS PARA: {area_provas.upper()}\n\n"
                    f"📄 DOCUMENTOS ESSENCIAIS:\n[lista]\n\n"
                    f"📸 REGISTROS VISUAIS:\n[fotos, prints, vídeos relevantes para esse caso]\n\n"
                    f"💬 COMUNICAÇÕES:\n[mensagens, e-mails, gravações de chamada que podem ajudar]\n\n"
                    f"👥 TESTEMUNHAS:\n[que tipo de testemunha é relevante e como documentar o relato dela]\n\n"
                    f"⏰ PRAZO PARA AGIR:\n[se há urgência ou prazo legal típico para esse tipo de caso]\n\n"
                    f"💡 DICA PRÁTICA:\n[1 dica específica de como organizar essas provas para não perder nada]"
                )
                res = juridico_ia(prompt, "Provas")
                if res: st.session_state['res_provas_consul4'] = str(res)
                salvar_consulta("Provas", area_provas, res)
                st.session_state['resposta_provas'] = res

        if st.session_state.get('resposta_provas'):
            st.markdown(f"<div class='card-green'>{st.session_state['resposta_provas']}</div>", unsafe_allow_html=True)
            col_dl, col_sv = st.columns(2)
            with col_dl:
                st.download_button("📋 Baixar (.txt)", data=st.session_state['resposta_provas'],
                    file_name="lista_provas.txt", mime="text/plain", use_container_width=True, key="consulto2")
            with col_sv:
                if st.button("❤️ Salvar", key="sv_provas", use_container_width=True):
                    st.session_state.consultas_salvas.append({
                        'modulo': 'Provas', 'pergunta': area_provas,
                        'conteudo': st.session_state['resposta_provas'],
                        'data': datetime.now().strftime('%d/%m %H:%M'),
                    })
                    st.success("❤️ Salvo!")

        # ========================
        # ONDE BUSCAR AJUDA
        # ========================

    with _tab_Ajuda:
        st.header("❓ Ajuda Rápida")
        st.markdown("*Qual é sua dúvida jurídica hoje?*")
        _prompt_ajuda = st.text_area("Descreva sua situação ou dúvida:", height=120, key="consul_ajuda_in", placeholder="Digite aqui...")
        if st.button("🤖 GERAR COM IA", key="consul_ajuda_btn", use_container_width=True):
            if _prompt_ajuda.strip():
                with st.spinner("Analisando..."):
                    try:
                        from groq import Groq as _GrT
                        _cli = _GrT(api_key=st.session_state.api_key)
                        _r = _cli.chat.completions.create(
                            model="openai/gpt-oss-120b",
                            messages=[{"role":"user","content":_prompt_ajuda}],
                            max_tokens=2048
                        )
                        st.markdown(f"<div class='card'>{_r.choices[0].message.content}</div>", unsafe_allow_html=True)
                    except Exception as _e:
                        st.error(f"Erro: {_e}")
            else:
                st.warning("Preencha o campo acima.")


    with _tab_Biblioteca:
        st.header("📚 Biblioteca de Consultas")
        st.markdown("Todas as suas consultas salvas, organizadas por área.")

        if not st.session_state.consultas_salvas:
            st.info("Biblioteca vazia. Gere consultas nos módulos e salve as importantes aqui!")
        else:
            modulos_bib = list(set(c['modulo'] for c in st.session_state.consultas_salvas))
            filtro = st.selectbox("Filtrar por módulo:", ["Todos"] + modulos_bib, key="consulto11")

            consultas_f = [
                c for c in st.session_state.consultas_salvas
                if filtro == "Todos" or c['modulo'] == filtro
            ]

            st.markdown(f"**{len(consultas_f)} consulta(s) encontrada(s)**")

            for i, item in enumerate(reversed(consultas_f)):
                idx_real = len(st.session_state.consultas_salvas) - 1 - i
                emoji_mod = MODULOS.get(item.get('modulo', ''), {}).get('emoji', '📋')
                with st.expander(f"{emoji_mod} [{item.get('modulo', '')}] {item.get('pergunta', '')[:60]} — {item['data']}"):
                    st.markdown(f"<div class='card'>{item['conteudo']}</div>", unsafe_allow_html=True)
                    col_dl, col_del = st.columns([3, 1])
                    with col_dl:
                        st.download_button("📋 Baixar", data=item['conteudo'],
                            file_name=f"{item.get('modulo', '').lower()}.txt", mime="text/plain", key=f"dl_bib_{i}")
                    with col_del:
                        if st.button("🗑️ Remover", key=f"del_bib_{i}"):
                            st.session_state.consultas_salvas.pop(idx_real)
                            st.rerun()

        if st.session_state.historico_consultas:
            st.markdown("<hr class='divider'>", unsafe_allow_html=True)
            historico_txt = "\n\n".join(
                f"[{c['data']}] {c['modulo']} — {c['pergunta']}\n{c['conteudo']}\n{'─'*40}"
                for c in st.session_state.historico_consultas
            )
            st.download_button("⬇️ Exportar todo o histórico (.txt)", data=historico_txt,
                file_name="historico_juridico.txt", mime="text/plain", key="consulto1")

            if st.button("🗑️ Limpar Todo o Histórico", key="consulto12"):
                st.session_state.historico_consultas = []
                st.rerun()

        # --- RODAPÉ ---
        st.markdown(
        "<div style='text-align:center;color:#999;font-size:0.8em;margin-top:60px;'>"
        "© 2026 Consultor Jurídico — Orientação Jurídica Geral com IA · Quiz Com Prêmios"
        "</div>", unsafe_allow_html=True
        )

# --- RODAPÉ ---
st.markdown(
    "<div style='text-align:center;color:#999;font-size:0.8em;margin-top:60px;'>"
    "© 2026 Consultor Jurídico — Orientação Jurídica Geral com IA · Quiz Com Prêmios"
    "</div>", unsafe_allow_html=True
)
