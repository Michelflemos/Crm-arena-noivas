import streamlit as st
import pandas as pd
import sqlite3

DB_NAME = "leads_arena_noivas.db"

# --- LISTA DE OPÇÕES PARA OS MENUS ---
STATUS_OPCOES = [
    "Não contatado", 
    "Chamar urgente",
    "Mensagem enviada", 
    "Ligação feita (Não atendeu)", 
    "Em atendimento / Negociação", 
    "Orçamento enviado", 
    "Fechado / Contrato Assinado", 
    "Perdido / Sem interesse"
]

# --- DADOS TRATADOS, SEPARADOS E LIMPOS ---
# Ordem das colunas: Nome, WhatsApp, E-mail, Tipo Evento, Data Evento, Qtd Convidados, Local, 
# Status 1, Obs 1, Status 2, Obs 2, Status 3, Obs 3, Degustacao, Desconto
LEADS_INICIAIS = [
    # Lote 1 - WhatsApp Limpo
    ("Felipe", "61981404740", "", "", "", "70", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Natália", "61984794629", "", "", "", "150", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Ana cecilia", "61998072001", "", "", "", "120", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Rafael", "61984105111", "", "", "", "150", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Victor", "61986225878", "", "", "", "100", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Adriana Oliveira", "61996673732", "", "", "", "120", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Karine", "61985121220", "", "", "", "120", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Ysabella", "61985669771", "", "", "", "60 a 70", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Leticia", "61998086174", "", "", "", "60", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("João Lucas", "61996116011", "", "", "", "120", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Raissa", "61985256560", "", "", "", "160", "", "Chamar urgente", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Juliana", "61985511631", "", "", "", "160", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Leticia", "61993021774", "", "", "Setembro 2027", "150", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Gabrielle", "43998584031", "", "", "2027", "100", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Felipe", "61996760766", "", "", "Setembro 2026", "200", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Mel", "61996693572", "", "", "Novembro 2026", "200", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Rian", "62991938233", "", "", "Abril 2027", "200", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Maria Eduarda", "61998812655", "", "", "Junho 2027", "250", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Júlia", "61983771513", "", "", "Agosto 2028", "80", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Stefhany", "61999834606", "", "", "Dezembro 2026", "150", "", "Chamar urgente", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Simone", "619992807734", "", "15 anos", "Fevereiro 2027", "150", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Thaís", "61984881390", "", "", "Setembro 2026", "130", "", "Chamar urgente", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Renata", "61998124099", "", "", "Outubro 2026", "150", "", "Chamar urgente", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Júlia", "61991950722", "", "", "1º Agosto", "150", "", "Chamar urgente", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Malu", "61981222491", "", "15 anos", "19/09/2026", "150", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    
    # Lote 2 - Formulário PDF (Tratado e com colunas específicas)
    ("Natasha Montenegro", "", "montenegro.nfo@gmail.com", "Casamento", "19/08/2026", "", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Sara Linhares", "61985173768", "saralinharesouza@gmail.com", "Casamento", "03/04/2027", "", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Júlia Morais", "51996721214", "julia.moraisap@gmail.com", "Casamento", "24/05/2028", "", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Karina Lira", "61984277735", "karinalira@gmail.com", "15 anos", "27/05/2027", "", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Sabrina Peres", "61998601202", "cereja.sabrina@gmail.com", "15 anos", "05/02/2027", "", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Thiago Braz", "61992922122", "thiago.vinciti@gmail.com", "Casamento", "28/11/2026", "", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Taynáh Sampaio", "61991959343", "taynnah.62@gmail.com", "Casamento", "06/09/2026", "", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Adriana Cardoso", "61983458562", "drimakelooku@gmail.com", "Casamento", "09/01/2027", "", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Analice", "61996862586", "erciliaats85@gmail.com", "15 anos", "12/09/2026", "", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Priscila Gonçalves", "", "priscilagoncalvesoc@gmail.com", "Debutante", "30/07/2026", "", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Alanna Carolina", "71996427787", "carol.franca.bio@gmail.com", "Festa", "14/07/2026", "", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    
    # Lote 3 - Novos Leads WhatsApp (Tratados minuciosamente)
    ("Andreia rocha", "61991087843", "", "", "", "50", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Denise Correia", "61984028896", "", "Aniversário", "", "20 a 30", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Pedro Moretto", "61991180854", "", "Casamento", "", "50", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Amanda Resende", "61984674873", "", "", "11/10", "150", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Arthur alvarenga", "61983612124", "", "Casamento", "", "60", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Fernanda Reis", "75991281691", "", "", "17/04/2027", "80", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Daniele Dantas", "61985716583", "", "Casamento/Aniv.", "", "100", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Sara Rodrigues", "61981336367", "", "Casamento", "", "120", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Ana Carolina", "61991711941", "", "Casamento", "", "80 a 90", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Juliana curado", "61984946926", "", "", "Agosto 2027", "200", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Letícia Vieira", "61999779965", "", "", "15/08", "140", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Mateus e Mayana", "61985275119", "", "", "01/05/2027", "170", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Natália Beatriz", "61999963026", "", "", "11/09/2027", "120", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Julia Barbosa", "61996059755", "", "Casamento", "Janeiro 2028", "150", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Barbara Letícia", "61984074024", "", "", "05/09/2026", "180", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Welder Rodrigues", "61992473290", "", "", "05/12", "", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Nara Yorrane", "61999244135", "", "", "25/07", "400", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Ana Elisa ramos", "61992132113", "", "", "28/05", "250", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Clarice Senna", "61998020505", "", "", "14/08/2027", "160", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Lucas Aguiar", "61994461993", "", "", "05/09", "70", "", "Chamar urgente", "", "Não contatado", "", "Não contatado", "", "Não", False)
]

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    # Criando a tabela com as colunas separadas
    c.execute('''
        CREATE TABLE IF NOT EXISTS leads (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT,
            numero TEXT,
            email TEXT,
            tipo_evento TEXT,
            data_evento TEXT,
            qtd_convidados TEXT,
            local_festa TEXT,
            status_1 TEXT,
            obs_1 TEXT,
            status_2 TEXT,
            obs_2 TEXT,
            status_3 TEXT,
            obs_3 TEXT,
            degustacao TEXT,
            desconto_apresentado BOOLEAN
        )
    ''')
    conn.commit()
    
    # Inserção inicial com verificação e limpeza
    c.execute("SELECT COUNT(*) FROM leads")
    if c.fetchone()[0] == 0:
        df_iniciais = pd.DataFrame(LEADS_INICIAIS, columns=[
            "nome", "numero", "email", "tipo_evento", "data_evento", "qtd_convidados", "local_festa", 
            "status_1", "obs_1", "status_2", "obs_2", "status_3", "obs_3", "degustacao", "desconto_apresentado"
        ])
        
        # Filtro inteligente de duplicatas
        df_iniciais['numero_limpo'] = df_iniciais['numero'].astype(str).str.replace(r'\D', '', regex=True)
        df_limpo = df_iniciais.drop_duplicates(subset=["numero_limpo"], keep='first').drop(columns=["numero_limpo"])
        leads_limpos = df_limpo.to_records(index=False).tolist()
        
        c.executemany('''
            INSERT INTO leads (nome, numero, email, tipo_evento, data_evento, qtd_convidados, local_festa, 
                               status_1, obs_1, status_2, obs_2, status_3, obs_3, degustacao, desconto_apresentado) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', leads_limpos)
        conn.commit()
    conn.close()

def load_data():
    conn = sqlite3.connect(DB_NAME)
    df = pd.read_sql_query("SELECT * FROM leads", conn)
    conn.close()
    return df

def update_db(edited_df):
    conn = sqlite3.connect(DB_NAME)
    edited_df.to_sql('leads', conn, if_exists='replace', index=False)
    conn.close()

# --- INTERFACE DO STREAMLIT ---
st.set_page_config(page_title="A Bem Dita Torta - CRM", layout="wide")
st.title("🍰 Gestão de Leads - A Bem Dita Torta")
st.subheader("CRM Profissional")

init_db()

with st.expander("➕ Adicionar Novo Lead Manualmente"):
    with st.form("form_novo_lead"):
        col1, col2, col3 = st.columns(3)
        nome = col1.text_input("Nome")
        numero = col2.text_input("WhatsApp")
        email = col3.text_input("E-mail")
        
        col4, col5, col6 = st.columns(3)
        tipo_evento = col4.text_input("Tipo de Evento (Ex: Casamento, 15 anos)")
        data_evento = col5.text_input("Data do Evento")
        qtd_convidados = col6.text_input("Nº de Convidados")
        
        local_festa = st.text_input("Local da Festa")
        
        col7, col8 = st.columns(2)
        degustacao = col7.selectbox("Degustação", ["Não", "Sim", "Agendada"])
        desconto = col8.checkbox("Apresentou o desconto de 15%?")
        
        submit = st.form_submit_button("Salvar Lead")
        
        if submit:
            conn = sqlite3.connect(DB_NAME)
            c = conn.cursor()
            c.execute('''INSERT INTO leads (nome, numero, email, tipo_evento, data_evento, qtd_convidados, local_festa, 
                                            status_1, obs_1, status_2, obs_2, status_3, obs_3, degustacao, desconto_apresentado) 
                         VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', 
                      (nome, numero, email, tipo_evento, data_evento, qtd_convidados, local_festa, 
                       "Não contatado", "", "Não contatado", "", "Não contatado", "", degustacao, desconto))
            conn.commit()
            conn.close()
            st.success("Lead adicionado com sucesso!")
            st.rerun()

st.divider()
st.write("### 📊 Funil de Contatos (Editável)")
st.info("💡 Dê duplo clique em qualquer célula para digitar observações (como datas de retorno) ou alterar os menus.")

df = load_data()

if not df.empty:
    pesquisa = st.text_input("🔍 Filtrar por Nome, WhatsApp, Status ou Tipo de Evento:")
    if pesquisa:
        df = df[
            df['nome'].str.contains(pesquisa, case=False, na=False) | 
            df['numero'].str.contains(pesquisa, case=False, na=False) |
            df['tipo_evento'].str.contains(pesquisa, case=False, na=False) |
            df['status_1'].str.contains(pesquisa, case=False, na=False)
        ]

    # Configuração de todas as colunas para edição
    config_colunas = {
        "id": st.column_config.NumberColumn("ID", disabled=True),
        "nome": "Nome",
        "numero": "WhatsApp",
        "email": "E-mail",
        "tipo_evento": "Evento",
        "data_evento": "Data",
        "qtd_convidados": "Convidados",
        "local_festa": "Local",
        "status_1": st.column_config.SelectboxColumn("1º Contato (Status)", options=STATUS_OPCOES),
        "obs_1": "1º Contato (Obs)",
        "status_2": st.column_config.SelectboxColumn("2º Contato (Status)", options=STATUS_OPCOES),
        "obs_2": "2º Contato (Obs)",
        "status_3": st.column_config.SelectboxColumn("3º Contato (Status)", options=STATUS_OPCOES),
        "obs_3": "3º Contato (Obs)",
        "degustacao": st.column_config.SelectboxColumn("Degustação?", options=["Não", "Sim", "Agendada"]),
        "desconto_apresentado": st.column_config.CheckboxColumn("Desconto 15%?")
    }

    edited_df = st.data_editor(df, column_config=config_colunas, use_container_width=True, hide_index=True)

    if st.button("💾 Salvar Alterações no Funil"):
        update_db(edited_df)
        st.success("Todas as observações e status foram atualizados com sucesso!")
        st.rerun()
else:
    st.info("Nenhum dado encontrado.")
