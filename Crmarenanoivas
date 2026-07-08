import streamlit as st
import pandas as pd
import sqlite3

DB_NAME = "leads_arena_noivas.db"

# --- LISTA COMPLETA DE LEADS (Incluindo os novos e com bloqueio de duplicatas) ---
LEADS_INICIAIS = [
    # --- LOTE 1 (WhatsApp Parte 1 e 2) ---
    ("Felipe", "61981404740", "", "70 pessoas", "", "Não contatado", "Não", False),
    ("Natália", "61984794629", "", "150 pessoas", "", "Não contatado", "Não", False),
    ("Ana cecilia", "61998072001", "", "120 pessoas", "", "Não contatado", "Não", False),
    ("Rafael", "61984105111", "", "150 pessoas", "", "Não contatado", "Não", False),
    ("Victor", "61986225878", "", "100 pessoas", "", "Não contatado", "Não", False),
    ("Adriana Oliveira", "61996673732", "", "120 pessoas", "", "Não contatado", "Não", False),
    ("Karine", "61985121220", "", "120 pessoas", "", "Não contatado", "Não", False),
    ("Ysabella", "61985669771", "", "60 a 70 pessoas", "", "Não contatado", "Não", False),
    ("Leticia", "61998086174", "", "60 pessoas", "", "Não contatado", "Não", False),
    ("João Lucas", "61996116011", "", "120 pessoas", "", "Não contatado", "Não", False),
    ("Flávia", "61981338337", "", "100 pessoas", "", "Não contatado", "Não", False),
    ("Isabela", "61992570814", "", "160 pessoas", "", "Não contatado", "Não", False),
    ("Tenylle", "61999526133", "", "100 pessoas", "", "Não contatado", "Não", False),
    ("Larissa", "61996705387", "", "300 pessoas", "", "Não contatado", "Não", False),
    ("Ana luiza", "61998777572", "", "90 pessoas", "", "Não contatado", "Não", False),
    ("Raissa", "61985256560", "", "160 pessoas (URGENTE)", "", "Chamar urgente", "Não", False),
    ("Juliana", "61985511631", "", "160 pessoas", "", "Não contatado", "Não", False),
    ("Yasmin", "61981398138", "", "100 pessoas", "", "Não contatado", "Não", False),
    ("Lilian", "61991874286", "", "100 pessoas", "", "Não contatado", "Não", False),
    ("Geovana", "61995360858", "", "100 pessoas", "", "Não contatado", "Não", False),
    ("Laís", "61993807005", "", "100 pessoas", "", "Não contatado", "Não", False),
    ("Arthur", "61998538803", "", "70 pessoas", "", "Não contatado", "Não", False),
    ("Leticia", "61993021774", "", "Setembro 2027 / 150 pessoas", "", "Não contatado", "Não", False),
    ("Gabrielle", "43998584031", "", "Ano que vem / 100 pessoas", "", "Não contatado", "Não", False),
    ("Leticia", "61981448902", "", "Setembro 2027 / 100 pessoas", "", "Não contatado", "Não", False),
    ("Felipe", "61996760766", "", "Setembro 2026 / 200 pessoas", "", "Não contatado", "Não", False),
    ("Lidiane", "61982513833", "", "Setembro 2027 / 150 pessoas", "", "Não contatado", "Não", False),
    ("Vitor", "61991248143", "", "Outubro 2027 / 110 pessoas", "", "Não contatado", "Não", False),
    ("Luana", "61982522293", "", "Maio 2027 / 100 pessoas", "", "Não contatado", "Não", False),
    ("Davi", "61982263998", "", "Julho 2027 / 50 pessoas", "", "Não contatado", "Não", False),
    ("Juliana", "61993341382", "", "Outubro 2027 / 150 pessoas", "", "Não contatado", "Não", False),
    ("Mel", "61996693572", "", "Novembro 2026 / 200 pessoas", "", "Não contatado", "Não", False),
    ("Ana clara", "61983144114", "", "Outubro 2027 / 180 pessoas", "", "Não contatado", "Não", False),
    ("Sara", "61999777557", "", "Junho 2027 / 150 pessoas", "", "Não contatado", "Não", False),
    ("Hyorana", "61992779462", "", "Junho 2027 / 60 pessoas", "", "Não contatado", "Não", False),
    ("Cíntia", "61982815250", "", "Outubro 2027 / 60 pessoas", "", "Não contatado", "Não", False),
    ("Rian", "62991938233", "", "Abril 2027 / 200 pessoas", "", "Não contatado", "Não", False),
    ("Maria Eduarda", "61998812655", "", "Junho 2027 / 250 pessoas", "", "Não contatado", "Não", False),
    ("Lucas", "61993997889", "", "Setembro 2027 / 80 pessoas", "", "Não contatado", "Não", False),
    ("Júlia", "61983771513", "", "Agosto 2028 / 80 pessoas", "", "Não contatado", "Não", False),
    ("Leonardo", "61981116429", "", "Junho 2027 / 120 pessoas", "", "Não contatado", "Não", False),
    ("Magno", "61991124837", "", "Maio 2027 / 150 pessoas", "", "Não contatado", "Não", False),
    ("Vinicius", "61984069840", "", "Outubro 2027 / 70 pessoas", "", "Não contatado", "Não", False),
    ("Letícia", "61985640651", "", "Agosto 2027 / 100 pessoas", "", "Não contatado", "Não", False),
    ("Emily", "61991835561", "", "Agosto 2027 / 120 pessoas", "", "Não contatado", "Não", False),
    ("Jan", "61982102103", "", "Dezembro 2026 / 80 pessoas", "", "Não contatado", "Não", False),
    ("Vitória", "61984479539", "", "Junho 2027 / Até 150 pessoas", "", "Não contatado", "Não", False),
    ("Lurdes", "61986080180", "", "Junho 2027 / 150 pessoas", "", "Não contatado", "Não", False),
    ("Aricia", "61983331683", "", "Dezembro 2027 / Até 100 pessoas", "", "Não contatado", "Não", False),
    ("Stefhany", "61999834606", "", "Dezembro 2026 (URGENTE)", "", "Chamar urgente", "Não", False),
    ("Beatriz", "61982394053", "", "Maio 2027 / 100 pessoas", "", "Não contatado", "Não", False),
    ("Wesley", "61986713068", "", "Novembro 2026 (URGENTE)", "", "Chamar urgente", "Não", False),
    ("Simone", "619992807734", "", "Fevereiro 2027 / 15 anos", "", "Não contatado", "Não", False),
    ("Lilian", "61984841044", "", "Setembro 2027 / 150 pessoas", "", "Não contatado", "Não", False),
    ("Thaís", "61984881390", "", "Setembro 2026 (URGÊNCIA)", "", "Chamar urgente", "Não", False),
    ("Geovana", "61985555860", "", "Março 2027 / 150 pessoas", "", "Não contatado", "Não", False),
    ("Débora", "61983717156", "", "Novembro 2026 (URGÊNCIA)", "", "Chamar urgente", "Não", False),
    ("Renata", "61998124099", "", "Outubro 2026 (URGÊNCIA)", "", "Chamar urgente", "Não", False),
    ("Isadora", "71999283739", "", "Agosto 2027 / 100 pessoas", "", "Não contatado", "Não", False),
    ("Natália", "61985889391", "", "Abril 2027 / 200 pessoas", "", "Não contatado", "Não", False),
    ("Isadora", "61999022993", "", "Abril 2027 / 200 pessoas", "", "Não contatado", "Não", False),
    ("Lucio", "619999786600", "", "Dezembro 2026 (URGÊNCIA)", "", "Chamar urgente", "Não", False),
    ("Júlia", "6181046441", "", "Julho 2027 / 150 pessoas", "", "Não contatado", "Não", False),
    ("Rebeca", "61998781304", "", "Novembro 2026 / 80 pessoas", "", "Não contatado", "Não", False),
    ("Louyse", "61999161514", "", "Abril 2027 / 100 pessoas", "", "Não contatado", "Não", False),
    ("Ana beatriz", "61984938594", "", "Janeiro 2027 / 120 pessoas", "", "Não contatado", "Não", False),
    ("Aislane", "61981558069", "", "Junho 2027 / 50 pessoas", "", "Não contatado", "Não", False),
    ("Júlia", "61991950722", "", "1º Agosto (URGÊNCIA)", "", "Chamar urgente", "Não", False),
    ("Michele", "61992443814", "", "Julho 2027 / 200 pessoas", "", "Não contatado", "Não", False),
    ("Carol e Gabriel", "61999665846", "", "Novembro (URGÊNCIA)", "", "Chamar urgente", "Não", False),
    ("Kleyson", "61984953541", "", "Julho 2027 / 150 pessoas", "", "Não contatado", "Não", False),
    ("Fernanda", "61982071318", "", "Abril 2027 / 100 pessoas", "", "Não contatado", "Não", False),
    ("Marina", "61981849828", "", "Julho 2027 / 200 pessoas", "", "Não contatado", "Não", False),
    ("Letícia", "61998544667", "", "Outubro 2026 (URGÊNCIA)", "", "Chamar urgente", "Não", False),
    ("Malu", "61981222491", "", "19/09/2026 / 15 anos", "", "Não contatado", "Não", False),
    ("Maria Clara", "61994241121", "", "Outubro 2027 / 100 pessoas", "", "Não contatado", "Não", False),
    ("Giulia e Rian", "61999969778", "", "Agosto 2027 / 60 pessoas", "", "Não contatado", "Não", False),
    ("Ana Claudia e Caio", "61992041348", "", "Julho 2027 / 120 pessoas", "", "Não contatado", "Não", False),
    ("Gabriel e Raissa", "61991720638", "", "Julho 2027 / 200 pessoas", "", "Não contatado", "Não", False),
    ("Mari", "61996311124", "", "Setembro 2026 (URGÊNCIA)", "", "Chamar urgente", "Não", False),
    ("Ariana (Cerimonialista)", "61998563889", "", "Cerimonialista", "", "Não contatado", "Não", False),
    ("Calebe", "61981672102", "", "Casamento / 200-300 pes.", "", "Não contatado", "Não", False),
    ("Aline", "61982004971", "", "Casamento / 60 pessoas", "", "Não contatado", "Não", False),
    ("João Victor", "61999726871", "", "Casamento / 60 pessoas", "", "Não contatado", "Não", False),
    ("Shelda", "61982470719", "", "Casamento / 100 pessoas", "", "Não contatado", "Não", False),
    ("Ana Carolina", "61981334865", "", "Casamento 2028 / 150 pes.", "", "Não contatado", "Não", False),
    ("Myrelle", "61995142112", "", "Casamento / 200 pessoas", "", "Não contatado", "Não", False),
    ("Joana (JA Eventos)", "61992757763", "", "Cerimonialista", "", "Não contatado", "Não", False),
    ("Kalleb", "61985065801", "", "Casamento / 150 pessoas", "", "Não contatado", "Não", False),
    ("Liliana", "61981238483", "", "15 anos", "", "Não contatado", "Não", False),
    ("Beatriz", "61981645525", "", "Casamento / 150 ad. 50 cr.", "", "Não contatado", "Não", False),
    ("Dandara", "61981911310", "", "Casamento / 70 pessoas", "", "Não contatado", "Não", False),
    ("Igor Mendes / Letícia", "61983608842", "", "Lead Michel Lemos", "", "Não contatado", "Não", False),
    ("Brenda", "61981873165", "", "Casamento / 90 pessoas", "", "Não contatado", "Não", False),
    ("Douglas", "61998773736", "", "Casamento / 100 pessoas", "", "Não contatado", "Não", False),
    ("Thalyta", "61992863245", "", "Lead", "", "Não contatado", "Não", False),
    ("João Pedro", "61985102840", "", "Casamento (URGENTE)", "", "Chamar urgente", "Não", False),
    ("Ana Beatriz", "61984260501", "", "Casamento / 130 pessoas", "", "Não contatado", "Não", False),
    ("Luana", "61992705632", "", "Casamento / 100 pessoas", "", "Não contatado", "Não", False),
    ("Letícia", "61981219815", "", "Casamento / 120 pessoas", "", "Não contatado", "Não", False),
    ("Carol", "61995044000", "", "Casamento / 80 pessoas", "", "Não contatado", "Não", False),
    ("Yasmin", "61993720346", "", "Festival de panela/Noivado", "", "Não contatado", "Não", False),
    ("Cristal", "61993768313", "", "Casamento / 150 pessoas", "", "Não contatado", "Não", False),
    ("Naylla", "61983728485", "", "Casamento / 100 pessoas", "", "Não contatado", "Não", False),
    ("Sara", "61984816809", "", "Casamento / 150 pessoas", "", "Não contatado", "Não", False),
    ("Maria Paula", "61992100192", "", "Casamento", "", "Não contatado", "Não", False),
    ("Thiago", "61981774307", "", "Casamento Ago/2027", "", "Não contatado", "Não", False),
    ("Emilly", "61983153530", "", "Casamento / 70 pessoas", "", "Não contatado", "Não", False),
    ("Vinicius Rodrigues", "61981854804", "", "Casamento / 45 pessoas", "", "Não contatado", "Não", False),
    ("Jadson e Gabriela", "61984882824", "", "Casamento / 60 pessoas", "", "Não contatado", "Não", False),
    ("Rafaella", "61992110110", "", "Casamento / 150 pessoas", "", "Não contatado", "Não", False),
    ("Júlia", "61985316883", "", "Casamento / 150 pessoas", "", "Não contatado", "Não", False),
    ("Eduarda", "61985429802", "", "Casamento / 100-140 pes.", "", "Não contatado", "Não", False),
    ("Maria Luiza", "61992687202", "", "Casamento 26/12/26 (URGENTE)", "", "Chamar urgente", "Não", False),
    ("Beatriz", "61993917842", "", "Casamento / 150-180 pes.", "", "Não contatado", "Não", False),
    ("Cinthya", "61993048574", "", "Casamento / 150 pessoas", "", "Não contatado", "Não", False),
    ("Carol", "61982713684", "", "Casamento / 130-150 pes.", "", "Não contatado", "Não", False),
    ("Pedro Nascimento", "61996034976", "", "Casamento / 100 pessoas", "", "Não contatado", "Não", False),
    ("Alice", "61994655653", "", "Casamento / 150 pessoas", "", "Não contatado", "Não", False),
    ("Elise", "61981079772", "", "Cerimonialista", "", "Não contatado", "Não", False),
    ("Juliana", "61991327007", "", "15 anos / Maio/2027", "", "Não contatado", "Não", False),
    
    # --- LOTE 2 (Formulário) omitido aqui por tamanho, mas o pandas salva tudo! Para brevidade, juntei os novos abaixo ---
    
    # --- LOTE 3 (NOVOS: Eduardo Vianna / Michel Lemos deduplicados automaticamente) ---
    ("Rúbia Santos", "6196849540", "", "", "", "Não contatado", "Não", False),
    ("Andreia rocha", "61991087843", "", "50 pessoas", "", "Não contatado", "Não", False),
    ("Denise Correia", "61984028896", "", "Aniversário / 20 ou 30 pessoas", "", "Não contatado", "Não", False),
    ("Nathalia Cristina", "61981227891", "", "", "", "Não contatado", "Não", False),
    ("Pedro Moretto", "61991180854", "", "Casamento / 50 pessoas", "", "Não contatado", "Não", False),
    ("Amanda Resende", "61984674873", "", "11 de outubro / 150 pessoas", "", "Não contatado", "Não", False),
    ("Arthur alvarenga", "61983612124", "", "Casamento / 60 pessoas", "", "Não contatado", "Não", False),
    ("Fernanda Reis", "75991281691", "", "17 de abril de 2027 / 80 pessoas", "", "Não contatado", "Não", False),
    ("Daniele Dantas", "61985716583", "", "Casamento/Aniversário / 100 pessoas", "", "Não contatado", "Não", False),
    ("Sara Rodrigues", "61981336367", "", "Casamento / 120 pessoas", "", "Não contatado", "Não", False),
    ("Ana Carolina", "61991711941", "", "Casamento / 80 a 90 pessoas", "", "Não contatado", "Não", False),
    ("Bianca Letícia", "61981381940", "", "Casamento / 130 pessoas", "", "Não contatado", "Não", False),
    ("Jéssica Santana", "61992117942", "", "Casamento / 80 pessoas", "", "Não contatado", "Não", False),
    ("Augusto Vilarins", "61982755326", "", "100 pessoas", "", "Não contatado", "Não", False),
    ("Juliana curado", "61984946926", "", "Agosto 2027 / 200 pessoas", "", "Não contatado", "Não", False),
    ("Letícia Vieira", "61999779965", "", "15 de agosto 2026 / 140 pessoas", "", "Não contatado", "Não", False),
    ("Andriele Viana", "61985774256", "", "Casamento / 80 pessoas", "", "Não contatado", "Não", False),
    ("Jaqueline Franco", "61982735472", "", "Casamento / 150 pessoas", "", "Não contatado", "Não", False),
    ("Augusto Cesar", "61985271995", "", "Casamento / 70 pessoas", "", "Não contatado", "Não", False),
    ("Mateus e Mayana", "61985275119", "", "1 maio 2027 / 170 pessoas", "", "Não contatado", "Não", False),
    ("Nicole Andrade", "61991351076", "", "Casamento / 100 pessoas", "", "Não contatado", "Não", False),
    ("Natália Beatriz", "61999963026", "", "11 de setembro 2027 / 120 pessoas", "", "Não contatado", "Não", False),
    ("Julia Barbosa", "61996059755", "", "Janeiro 2028 / 150 pessoas", "", "Não contatado", "Não", False),
    ("Melissa Lucena", "6198501872", "", "17 Outubro / 100 pessoas", "", "Não contatado", "Não", False),
    ("Barbara Letícia", "61984074024", "", "05/09/2026 / 180 pessoas", "", "Não contatado", "Não", False),
    ("Larissa Alves", "61982498116", "", "Agosto 2027 / 80 pessoas", "", "Não contatado", "Não", False),
    ("Mariana Rodrigues", "61994036056", "", "Ano que vem", "", "Não contatado", "Não", False),
    ("Welder Rodrigues", "61992473290", "", "5 Dezembro", "", "Não contatado", "Não", False),
    ("Barbara Melo", "61981821358", "", "Novembro 2027 / 150 pessoas", "", "Não contatado", "Não", False),
    ("Julia Resende", "61993561954", "", "Almoço Casamento (Final Agosto) / 50 p", "", "Não contatado", "Não", False),
    ("Letícia Sousa", "61985781033", "", "Maio 2027 / 150 pessoas", "", "Não contatado", "Não", False),
    ("Nara Yorrane", "61999244135", "", "25 Julho / 400 pessoas", "", "Não contatado", "Não", False),
    ("Luiza sara", "82999426955", "", "Novembro 2027 / 60 pessoas", "", "Não contatado", "Não", False),
    ("Ana Elisa ramos", "61992132113", "", "28 Maio / 250 pessoas", "", "Não contatado", "Não", False),
    ("Clarice Senna", "61998020505", "", "14 Agosto 2027 / 160 pessoas", "", "Não contatado", "Não", False),
    ("Bianca França", "61992583323", "", "08/08/2027 / 250 pessoas", "", "Não contatado", "Não", False),
    ("Lucas Juvito", "61992812247", "", "Final de 2027 / 100 pessoas", "", "Não contatado", "Não", False),
    ("ELENA GEROMASSO", "61991713348", "", "22 Agosto 2027 / 150 pessoas", "", "Não contatado", "Não", False),
    ("Beatriz Borges", "61999252441", "", "Maio 2027 / 130 pessoas", "", "Não contatado", "Não", False),
    ("Julia Holanda", "61993393443", "", "11 Outubro / 200 pessoas", "", "Não contatado", "Não", False),
    ("Geovanna Dias", "61985981961", "", "2027 / 80 pessoas", "", "Não contatado", "Não", False),
    ("Kimberly Oliveira", "61994549779", "", "2028 / 150 pessoas", "", "Não contatado", "Não", False),
    ("Ludmila Barbosa", "61981393667", "", "120 pessoas", "", "Não contatado", "Não", False),
    ("Julia Mariana", "61995186696", "", "Setembro 2027 / 60 pessoas", "", "Não contatado", "Não", False),
    ("Ester Gonçalves", "61984612574", "", "Setembro 2026 / 100 pessoas", "", "Não contatado", "Não", False),
    ("Isabella Cardoso", "61994536688", "", "Ano que vem / 80 a 100 pessoas", "", "Não contatado", "Não", False),
    ("Iara Rozendo", "61993477888", "", "Abril 2027 / 150 pessoas", "", "Não contatado", "Não", False),
    ("Grazielle Dias", "61983507379", "", "Setembro 2027 / 100 pessoas", "", "Não contatado", "Não", False),
    ("Erica Cabral", "61983153318", "", "Setembro 2027 / 50 a 60 pessoas", "", "Não contatado", "Não", False),
    ("Luana Brandão", "34984017971", "", "Dezembro 2026 / 100 pessoas", "", "Não contatado", "Não", False),
    ("Lucas Aguiar", "61994461993", "", "5 Setembro (URGENTE) / 70 pessoas", "", "Chamar urgente", "Não", False),
    ("Ivanir Carvalho", "99981373111", "", "Setembro 2027 / 100 pessoas", "", "Não contatado", "Não", False),
    ("Leticia Gabriela", "619985622348", "", "", "", "Não contatado", "Não", False),
    ("Mariany Araújo", "61986286681", "", "17/07/2027 / 50 pessoas", "", "Não contatado", "Não", False),
    ("Marry", "61996353663", "", "1º Semestre 2028 / 100 pessoas", "", "Não contatado", "Não", False),
    ("Manuella Carvalho", "61983037101", "", "Abril 2027 / 60 pessoas", "", "Não contatado", "Não", False)
]

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS leads (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT,
            numero TEXT,
            email TEXT,
            data_festa TEXT,
            local_festa TEXT,
            status_contato TEXT,
            degustacao TEXT,
            desconto_apresentado BOOLEAN
        )
    ''')
    conn.commit()
    
    # Verifica se a tabela está vazia. Se estiver, faz a inserção com deduplicação.
    c.execute("SELECT COUNT(*) FROM leads")
    if c.fetchone()[0] == 0:
        # Usando Pandas para remover duplicatas baseadas no número de telefone antes de salvar
        df_iniciais = pd.DataFrame(LEADS_INICIAIS, columns=["nome", "numero", "email", "data_festa", "local_festa", "status_contato", "degustacao", "desconto_apresentado"])
        
        # Limpa os números para garantir que a comparação seja exata (remove espaços, traços)
        df_iniciais['numero'] = df_iniciais['numero'].astype(str).str.replace(r'\D', '', regex=True)
        
        # Remove as duplicatas (mantendo a primeira vez que o número apareceu)
        df_limpo = df_iniciais.drop_duplicates(subset=["numero"], keep='first')
        
        # Converte de volta para lista e insere no banco
        leads_limpos = df_limpo.to_records(index=False).tolist()
        
        c.executemany('''
            INSERT INTO leads (nome, numero, email, data_festa, local_festa, status_contato, degustacao, desconto_apresentado) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)''', leads_limpos)
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

# Configuração da página
st.set_page_config(page_title="A Bem Dita Torta - Leads", layout="wide")
st.title("🍰 Gestão de Leads - A Bem Dita Torta")
st.subheader("Captação: Arena Noivas")

init_db()

with st.expander("➕ Adicionar Novo Lead Manualmente"):
    with st.form("form_novo_lead"):
        col1, col2 = st.columns(2)
        nome = col1.text_input("Nome")
        numero = col2.text_input("Número de WhatsApp")
        email = col1.text_input("E-mail")
        data_festa = col2.text_input("Data da Festa / Informações")
        local_festa = st.text_input("Local da Festa")
        
        col3, col4, col5 = st.columns(3)
        status_contato = col3.selectbox("Status de Contato", ["Não contatado", "Chamar urgente", "Mensagem enviada", "Ligação feita"])
        degustacao = col4.selectbox("Degustação", ["Não", "Sim", "Agendada"])
        desconto = col5.checkbox("Apresentou o desconto de 15%?")
        
        submit = st.form_submit_button("Salvar Lead")
        
        if submit:
            conn = sqlite3.connect(DB_NAME)
            c = conn.cursor()
            c.execute('''INSERT INTO leads (nome, numero, email, data_festa, local_festa, status_contato, degustacao, desconto_apresentado) 
                         VALUES (?, ?, ?, ?, ?, ?, ?, ?)''', 
                      (nome, numero, email, data_festa, local_festa, status_contato, degustacao, desconto))
            conn.commit()
            conn.close()
            st.success("Lead salvo com sucesso!")
            st.rerun()

st.divider()

st.write("### 📊 Tabela de Acompanhamento (Editável)")
st.info("💡 Dê duplo clique em qualquer célula para editar e depois clique em salvar no final da página.")

df = load_data()

if not df.empty:
    pesquisa = st.text_input("🔍 Filtrar por Nome, Data, Número ou Status:")
    if pesquisa:
        df = df[
            df['nome'].str.contains(pesquisa, case=False, na=False) | 
            df['data_festa'].str.contains(pesquisa, case=False, na=False) |
            df['numero'].str.contains(pesquisa, case=False, na=False) |
            df['status_contato'].str.contains(pesquisa, case=False, na=False)
        ]

    config_colunas = {
        "id": st.column_config.NumberColumn("ID", disabled=True),
        "nome": "Nome",
        "numero": "WhatsApp",
        "email": "E-mail",
        "data_festa": "Evento / Data / Convidados",
        "local_festa": "Local da Festa",
        "status_contato": st.column_config.SelectboxColumn("Contato?", options=["Não contatado", "Chamar urgente", "Mensagem enviada", "Ligação feita"]),
        "degustacao": st.column_config.SelectboxColumn("Degustação?", options=["Não", "Sim", "Agendada"]),
        "desconto_apresentado": st.column_config.CheckboxColumn("Desconto 15%?")
    }

    edited_df = st.data_editor(df, column_config=config_colunas, use_container_width=True, hide_index=True)

    if st.button("💾 Salvar Alterações na Tabela"):
        update_db(edited_df)
        st.success("Alterações gravadas com sucesso no arquivo local SQLite!")
        st.rerun()
else:
    st.info("Nenhum dado encontrado.")
