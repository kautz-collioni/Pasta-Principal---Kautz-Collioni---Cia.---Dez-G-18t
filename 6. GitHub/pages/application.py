import streamlit as st
import base64
import streamlit.components.v1 as components
from streamlit.components.v1 import html
import time
import Conector as con

# ========================= 1. PAGE CONFIGURATION AND STYLE LOADING =========================
st.set_page_config(
    page_title = "Relatório Integrado | Kautz-Collioni & Cia.",
    layout = "wide",
    initial_sidebar_state = "expanded",
)

hide_st_style = '''
<style>
    div[class^="_hostedName"] {
        visibility: hidden;
    }
</style>
'''
st.markdown(hide_st_style, unsafe_allow_html = True)

def load_css(file_name):
    try:
        with open(file_name, encoding = 'utf-8') as f:
            st.markdown(f'''<style>{f.read()}</style>''', unsafe_allow_html = True)
    except FileNotFoundError:
        pass

# ======================== 2. SESSION STATE INITIALIZATION ========================

# Controls the user's login state
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
    st.switch_page("login.py")

# Controls the current section in the main application
if 'current_section' not in st.session_state:
    st.session_state.current_section = "Área Inicial"

# ======================== 3. LOGOUT FUNCTION ========================

def back_to_login():
    keys_to_preserve = ['logged_in', 'current_section']
    keys_to_delete = [key for key in st.session_state.keys() if key not in keys_to_preserve]
    for key in keys_to_delete:
        del st.session_state[key]
    st.session_state.logged_in = False
    st.switch_page("login.py")

# ======================== 4. GO TO HOMEPAGE APPLICATION ========================

def go_to_homepage():
    st.session_state.nav_radio = "Área Inicial"

# ======================== 5. MAIN APPLICATION ========================

def main_app():
    # Load main application CSS
    load_css("styles/common_style.css")
    load_css("styles/sidebar_style.css")

    # Main application title
    st.markdown("""<div class="app-title">Porsche Brasil</div>""", unsafe_allow_html = True)

    st.markdown("---")

    with st.sidebar:

        # Loading the sidebar header logo
        try:
            with open("media/dark_header.png", "rb") as f:
                image_base64 = base64.b64encode(f.read()).decode()
            st.markdown(
                f"""
                <div class="logo-container" style='text-align: center; margin-bottom: -15rem; position: relative;z-index: 1; margin-top: -4rem;'>
                    <img src='data:image/png;base64,{image_base64}' style='width: 100%; height: 60%; pointer-events: none; user-select: none; -webkit-user-drag: none;' draggable='false; margin-bottom: -15rem; top: -4rem; position: relative; padding-bottom: 0rem; z-index: 1;'>
                </div>
                """,
                unsafe_allow_html = True
            )
        except Exception as e:
            st.error(f"Erro ao carregar a imagem: {e}")
            st.markdown("<h4>Kautz-Collioni & Cia.</h4>", unsafe_allow_html = True)

        st.button("Botão Invisível", key="stButton-invisible_btn", on_click=go_to_homepage)

        # User greeting
        first_name = st.session_state.username.split()[0]
        st.markdown(f'<div class="user-greeting">Olá, {first_name}!</div>', unsafe_allow_html = True)
        
        # Navigation menu - Sidebar buttons
        sidebar_options = ["Área Inicial", "Análise Exploratória", "Forecasting", "Fluxo de Caixa", "Avaliação", "Contato"]
        
        try:
            current_index = sidebar_options.index(st.session_state.current_section)
        except ValueError:
            current_index = 0

        section = st.radio(
            "Navegação", 
            sidebar_options, 
            index = current_index,
            key = "nav_radio", 
            label_visibility = "collapsed"
        )

        if section != st.session_state.current_section:
            st.session_state.current_section = section
            st.rerun()
    
        # Exit button - Logout
        st.button("Sair", key = "logout_btn", on_click = back_to_login, use_container_width = True)

        # Sidebar footer
        st.markdown(
            '<div class="sidebar-footer">Todos os direitos reservados © 2025 | Kautz-Collioni & Cia.</div>',
            unsafe_allow_html = True
        )

    database = con.database_revenue

    # ======================== PRINT BUTTON ========================

    print_button = """
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css">
    <style>
    button[class="print-button"] {
        padding: 10px 15px;
        font-size: 16px;
        font-weight: bold;
        cursor: pointer;
        background-color: transparent;
        color: #212529;
        border: none;
        border-radius: 0.25rem;
        font-family: Source Sans Pro, sans-serif;
        text-decoration: none;
        transition: background-color 0.15s ease-in-out, border-color 0.15s ease-in-out, box-shadow 0.15s ease-in-out;
        outline: none;
    }

    button[class="print-button"]:hover {
        background-color: #e9ecef;
        border-color: #ced4da;
    }

    button[class="print-button"]:active {
        background-color: #a6a5a5;
        border-color: #ced4da; /* Ajusta a cor da borda */
        color: #212529;
        box-shadow: inset 0 3px 5px rgba(0, 0, 0, 0.125);
    }

    @media print {
        button[class="print-button"] {
            display: none !important;
        }

        .svg-container {
            page-break-inside: avoid !important;
            break-inside: avoid-page !important;
            display: block !important;
        }
    }
    </style>

    <script>
        function printReport() {
            const expandedSidebar = window.parent.document.querySelector('section[data-testid="stSidebar"][aria-expanded="true"]');

            const sidebarToggle = window.parent.document.querySelector('div[data-testid="stSidebarCollapseButton"] > button');

            if (expandedSidebar && sidebarToggle) {
                sidebarToggle.closest('button').click();
            }
            
            setTimeout(() => {
                top.window.print();
            }, 500);
        }
    </script>

    <button 
        onclick="printReport();" 
        class="print-button"
    >
    <i class="fa-solid fa-print"; style="font-size: 30px;"></i>

    </button>
    """

    if st.session_state.current_section not in ["Área Inicial", "Contato"]:

        components.html(print_button, height = 80)

    load_css("styles/print_button_style.css")

    # ======================== APP SECTIONS ========================

    # Section: Área Inicial
    if st.session_state.current_section == "Área Inicial":

        st.markdown('<div class="graph-container">', unsafe_allow_html = True)

        st.caption(f"Database do relatório: :blue[10/10/2025].")

        st.subheader("Quadro Geral")
        m1, m2, m3 = st.columns(3)
        with m1:
            st.metric(label="Lojas Ativas", value="50", delta_color="normal", delta="+5")
        with m2:
            st.metric(label="Colaboradores", value="2.000", delta="+100", delta_color="normal")
        with m3:
            st.metric(label="Target de Receita", value="R$ 2B - 5B", delta="+300M", delta_color="normal")

        st.divider()

        col1, col2 = st.columns([1.2, 0.8], gap="large")

        with col1:
            st.subheader("🎯 Objetivos")
            
            with st.container(border=True):
                st.markdown("**Performance Financeira**")
                st.progress(0.15, text="**Meta:** +15% receita líquida")
                st.progress(0.05, text="**Meta:** +5pp margem líquida")
                
            with st.container(border=True):
                st.markdown("**Operações e Eficiência**")
                st.info("Reduzir custos operacionais em 10% através de iniciativas de eficiência.")
                
            with st.container(border=True):
                st.markdown("**Histórico de Reuniões**")
                tab1, tab2, tab3, tab4, tab5 = st.tabs(["20/10/2025", "20/09/2025", "20/08/2025", "20/07/2025", "20/06/2025"])
                with tab1:
                    st.write("""
                            • Análise da evolução recente dos principais indicadores contábeis.\n
                            • Identificação de desvios relevantes em relação ao planejamento estratégico.\n
                            • Discussão sobre margens operacionais e estrutura de custos.\n
                            • Avaliação da sustentabilidade do fluxo de caixa no curto prazo.\n
                            • Definição de recomendações para ajuste de metas financeiras.\n
                            """)
                with tab2:
                    st.write("""
                            • Exame da composição atual do passivo financeiro.\n
                            • Avaliação do perfil de vencimentos e custos da dívida.\n
                            • Discussão sobre riscos associados à alavancagem.\n
                            • Análise de alternativas de refinanciamento.\n
                            • Deliberação sobre diretrizes para otimização da estrutura de capital.\n
                            """)
                with tab3:
                    st.write("""
                            • Apresentação de cenários macroeconômicos prospectivos.\n
                            • Avaliação dos efeitos esperados sobre o setor de atuação.\n
                            • Discussão sobre sensibilidade a variáveis externas relevantes.\n
                            • Identificação de riscos e oportunidades conjunturais.\n
                            • Alinhamento das premissas para planejamento financeiro.\n
                            """)
                with tab4:
                    st.write("""
                            • Revisão das premissas econômicas dos projetos em estudo.\n
                            • Avaliação de retornos esperados e riscos associados.\n
                            • Comparação entre alternativas de alocação de recursos.\n
                            • Discussão sobre impactos no caixa e no endividamento.\n
                            • Emissão de parecer técnico para suporte à decisão.\n
                            """)
                with tab5:
                    st.write("""
                            • Avaliação dos processos atuais de controle financeiro.\n
                            • Identificação de fragilidades operacionais relevantes.\n
                            • Discussão sobre aderência a boas práticas de governança.\n
                            • Proposição de melhorias nos mecanismos de monitoramento.\n
                            • Definição de encaminhamentos para implementação gradual.\n
                            """)                

        with col2:
            st.subheader("🏢 Perfil Institucional")
            
            with st.status("Detalhes da Empresa", expanded=True):
                st.write("**Segmento:** indústria automotiva.")
                st.write("**Sede:** São Paulo, Brasil.")
                
            st.markdown("---")

            st.markdown("### Presença Estratégica")
            st.scatter_chart(
                {"Norte": [10], "Sul": [15], "Sudeste": [25]}
            )
        st.markdown('</div>', unsafe_allow_html = True)

    # Section: Análise Exploratória
    elif st.session_state.current_section == "Análise Exploratória":

        st.markdown('<div class="graph-container">', unsafe_allow_html = True)
        st.plotly_chart(con.figure1, use_container_width = True)
        st.markdown(f"<p id='description-text'>{con.description1}</p>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html = True)

        st.markdown("---")

        st.markdown('<div class="graph-container">', unsafe_allow_html = True)
        st.plotly_chart(con.figure2, use_container_width = True)
        st.markdown(f"<p id='description-text'>{con.description2}</p>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html = True)

        st.markdown("---")

        st.markdown('<div class="graph-container">', unsafe_allow_html = True)
        st.plotly_chart(con.figure3, use_container_width = True)
        st.markdown(f"<p id='description-text'>{con.description3}</p>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html = True)

        st.markdown("---")

        st.markdown('<div class="graph-container">', unsafe_allow_html = True)
        st.plotly_chart(con.figure4, use_container_width = True)
        st.markdown(f"<p id='description-text'>{con.description4}</p>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html = True)

        st.markdown("---")

        st.markdown('<div class="graph-container">', unsafe_allow_html = True)
        st.plotly_chart(con.figure5, use_container_width = True)
        st.markdown(f"<p id='description-text'>{con.description5}</p>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html = True)

        st.markdown("---")

        st.markdown('<div class="graph-container">', unsafe_allow_html = True)
        st.plotly_chart(con.figure6, use_container_width = True)
        st.markdown(f"<p id='description-text'>{con.description6}</p>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html = True)

        st.markdown("---")

        st.markdown('<div class="graph-container">', unsafe_allow_html = True)
        st.plotly_chart(con.figure7, use_container_width = True)
        st.markdown(f"<p id='description-text'>{con.description7}</p>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html = True)

        st.markdown("---")
        
        st.markdown('<div class="graph-container">', unsafe_allow_html = True)
        st.plotly_chart(con.figure8, use_container_width = True)
        st.markdown(f"<p id='description-text'>{con.description8}</p>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html = True)        

    # Section: Forecasting e Relacionados
    elif st.session_state.current_section == "Forecasting":

        st.markdown('<div class="graph-container">', unsafe_allow_html = True)
        st.plotly_chart(con.figure9, use_container_width = True)
        st.markdown(f"<p id='description-text'>{con.description9}</p>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html = True)

        st.markdown("---")

        st.markdown('<div class="graph-container">', unsafe_allow_html = True)
        st.plotly_chart(con.figure10, use_container_width = True)
        st.markdown(f"<p id='description-text'>{con.description10}</p>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html = True)

        st.markdown("---")
        
        st.markdown('<div class="graph-container">', unsafe_allow_html = True)
        st.plotly_chart(con.figure11, use_container_width = True)
        st.markdown(f"<p id='description-text'>{con.description11}</p>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html = True)

        st.markdown("---")
        
        st.markdown('<div class="graph-container">', unsafe_allow_html = True)
        st.dataframe(con.comparison_table, hide_index = True, use_container_width = True)
        st.markdown('</div>', unsafe_allow_html = True)
        col1, col2 = st.columns([8,1])
        with col2:
            st.download_button(
                label = "Baixar",
                data = con.buffer_excel_formatted(con.comparison_table),
                file_name = "Estimativas.xlsx",
                mime = "text/csv",
                )

    # Section: Fluxo de Caixa e Estoque
    elif st.session_state.current_section == "Fluxo de Caixa":

        st.markdown('<div class="graph-container">', unsafe_allow_html = True)
        st.plotly_chart(con.figure12, use_container_width = True)
        st.markdown(f"<p id='description-text'>{con.description12}</p>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html = True)

        st.markdown("---")
        
        st.markdown('<div class="graph-container">', unsafe_allow_html = True)
        st.plotly_chart(con.figure13, use_container_width = True)
        st.markdown(f"<p id='description-text'>{con.description13}</p>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html = True)

        st.markdown("---")

        st.markdown('<div class="graph-container">', unsafe_allow_html = True)
        st.plotly_chart(con.figure14, use_container_width = True)
        st.markdown(f"<p id='description-text'>{con.description14}</p>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html = True)

    # Section: Avaliação de Desempenho
    elif st.session_state.current_section == "Avaliação":

        st.markdown('<div class="graph-container">', unsafe_allow_html = True)
        st.plotly_chart(con.figure15, use_container_width = True)
        st.markdown(f"<p id='description-text'>{con.description15}</p>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html = True)

        st.markdown("---")

        st.markdown('<div class="graph-container">', unsafe_allow_html = True)
        st.plotly_chart(con.figure16, use_container_width = True)
        st.markdown(f"<p id='description-text'>{con.description16}</p>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html = True)


    # Section: Contato
    elif st.session_state.current_section == "Contato":

        st.markdown("""
                <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.0/css/all.min.css">
                <style> 
                    [data-testid="stImage"] img {
                        width: 50% !important;
                        height: auto;
                        display: block;
                        border-radius: 50%;
                        object-fit: cover;
                        aspect-ratio: 1 / 1;}
                    a {
                        color: inherit !important; 
                        text-decoration: none !important;
                    }

                    a:hover {
                        color: inherit !important;
                        text-decoration: none !important; 
                    }

                    .social-icon {
                        font-size: 1.5rem;
                        color: inherit;
                        text-decoration: none;
                        transition: color 0.3s ease;
                        margin-right: 0.5rem;
                    }

                    .social-text {
                        font-size: 0.8rem;
                        margin-left: 0.5rem;
                    }

                    .social-icon:hover {
                        color: #0077b5;
                    }
                </style>
            """, unsafe_allow_html = True)
        
        col1, col2 = st.columns(2)

        with col1:
            st.markdown("#### Bernardo Kautz")
            st.image("media/bernardo_kautz_profile_picture.jpg", use_container_width = True)
            st.markdown("Consultor &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Economista")
            st.text("Financista, mestrando em Economia Aplicada na Universidade de São Paulo (USP), com experiência profissional em captação de recursos à inovação e pesquisa acadêmica.")
            icon_col1, icon_col2, icon_col3, icon_col4 = st.columns(4)
            
            with icon_col1:
                st.markdown("""
                            <a class="social-icon" href="https://wa.me/555496781573" target="_blank">
                                <i class="fa-brands fa-whatsapp"></i>
                            <span class="social-text"> WhatsApp </span></a>""", unsafe_allow_html = True)
                
            with icon_col2:
                st.markdown(f"""
                            <a class="social-icon" href="mailto:bernardo@kautz-collioni.com.br">
                                <i class="fa-solid fa-at"></i>
                            <span class="social-text"> Email </span> </a>""", unsafe_allow_html = True)
                
            with icon_col3:
                st.markdown("""
                            <a class="social-icon" href="https://www.linkedin.com/in/bernardo-kautz" target="_blank">
                                <i class="fa-brands fa-linkedin"></i>
                            <span class="social-text"> LinkedIn </span> </a>""", unsafe_allow_html = True)
            with icon_col4:
                st.markdown(" ")

        with col2:
            st.markdown("#### Gustavo Collioni")
            st.image("media/gustavo_a_collioni_profile_picture.jpg", use_container_width = True)
            st.markdown("Consultor &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Economista")
            st.text("Financista, mestrando em Desenvolvimento Regional na Pontifícia Universidade Católica do Rio Grande do Sul (PUCRS), certificado como especialista em investimentos, com experiência profissional em gestão de patrimônio.")

            icon_col5, icon_col6, icon_col7, icon_col8 = st.columns(4)

            with icon_col5:
                st.markdown("""
                            <a class="social-icon" href="https://wa.me/5551982765730" target="_blank">
                                <i class="fa-brands fa-whatsapp"></i>
                            <span class="social-text"> WhatsApp </span></a>""", unsafe_allow_html = True)
                
            with icon_col6:
                st.markdown(f"""
                            <a class="social-icon" href="mailto:gustavo@kautz-collioni.com.br">
                                <i class="fa-solid fa-at"></i>
                            <span class="social-text"> Email </span> </a>""", unsafe_allow_html = True)
                
            with icon_col7:
                st.markdown("""
                            <a class="social-icon" href="https://www.linkedin.com/in/gustavo-collioni" target="_blank">
                                <i class="fa-brands fa-linkedin"></i>
                            <span class="social-text"> LinkedIn </span> </a>""", unsafe_allow_html = True)
            with icon_col8:
                st.markdown(" ")

    st.markdown("---")

    # Footer
    st.markdown(
        """
        <div style="width:100%; text-align:center; font-size:12px; color:#999999; margin-top:1rem; padding:1rem 0;">
        E-mail: suporte@kautz.collioni_cia.com.br. | Telefone: (51) 9 8276-5730.
        </div>
        """,
        unsafe_allow_html = True
    )

# ======================== 5. MAIN CONTROLLER ========================

if st.session_state.get('logged_in', False):
    main_app()
else:
    st.switch_page("login.py")
