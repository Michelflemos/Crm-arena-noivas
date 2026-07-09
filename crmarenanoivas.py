import streamlit as st
import pandas as pd
import sqlite3
import re

DB_NAME = "leads_arena_noivas.db"

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

# --- DADOS TRATADOS (WhatsApp + Tabela) ---
# Todos os 208+ contatos tratados e formatados 
LEADS_INICIAIS = [
    # ---- Leads da Tabela (E-mail, Nome, Evento, Data) ----
    ("Mayra da Silva do Vale", "", "mayrasdv@gmail.com", "Arena Noivas", "03/07/2026", "", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Natasha Montenegro", "", "montenegro.nfo@gmail.com", "Casamento", "19/08/2026", "", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Sara Linhares", "61985173768", "saralinharesouza@gmail", "Casamento", "03/04/2027", "", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Júlia", "51996721214", "julia.moraisap@gmail.cor", "Casamento", "24/05/2028", "", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Andressa Gonçalves", "", "andressa jornalistabsb@gmail.com", "Casamento", "11/07/2027", "", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Beatriz", "61999199291", "beatriz pinheiro811@gmt", "Casamento", "16/10/2027", "", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("elisa Amorim boaventura", "", "arethafe@gmail.com", "Casamento", "29/05/2027", "", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Laya lustosa", "61991878744", "Jaisinha206@gmail.com", "Casamento", "14/08/2027", "", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Karina Lira", "61984277735", "karinalira@gmail.com", "15 anos", "27/05/2027", "", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Hannah Rodrigues", "982088554", "hannahrsocialmedia@gm", "Casamento", "07/07/2027", "", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Sabrina Peres", "998601202", "cereja sabrina@gmail.cor", "15 anos", "05/02/2027", "", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Thiago Braz", "61992922122", "thiago.vinciti@gmail.com", "Casamento", "28/11/2026", "", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Jéssica Santana Carvalho", "61992117942", "1novodia@gmail.com", "Casamento", "28/11/2026", "", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Mylena Araujo do Carmo", "61999726579", "mylenaadc@hotmail.com", "Casamento", "17/09/2027", "", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Taynáh Sampaio", "61991959343", "taynnah.62@gmail.com", "Casamento", "06/09/2026", "", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("André Luiz Nery de Oliveira", "61992021534", "bsbandre75@gmail.com", "Casamento", "10/07/2027", "", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Rebeca Moreira", "61984883098", "moreirarebeca12@gmail", "Casamento", "22/08/2026", "", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Nilva Maria Pignata Curado", "61984457511", "nilvartes@gmail.com", "Casamento", "21/08/2027", "", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Marcela Nunes Mesquita Ribas Lopes", "61991945751", "adm.marcelamesquita", "Casamento", "10/07/2027", "", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Adriana Cardoso Ramos", "61983458562", "drimakelooku@gmail.com", "Casamento", "09/01/2027", "", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Milena", "61993752690", "milenaaraujonunestwdiny", "Casamento", "18/02/2027", "", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Andressa Fonseca", "61995532991", "andressa fonsecall25@gi", "Casamento", "27/11/2027", "", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Rafaella Zanetti", "61998489765", "rafamourazanetti@gmail.", "Casamento", "26/08/2028", "", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Ana Clara Rodrigues de Abreu", "61992442222", "onaclara99@gmail.com", "Casamento", "11/07/2027", "", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("André Josias Gonçalves de Oliveira", "61998210539", "andrejosias20@gmail.cor", "Casamento", "21/11/2026", "", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Patrick calque", "48999912559", "ownedspk@gmail.com", "Casamento", "20/08/2027", "", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Leticia", "61993395792", "leh brunna@gmail.com", "Casamento", "20/07/2005", "", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Gabriela", "61984975756", "gabirezende02@gmail.co", "Casamento", "10/07/2027", "", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Kalleb Damacena", "", "kallebadrielferreira@gmar", "Casamento", "05/06/2027", "", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Hellen Cristina Ribeiro Bastos", "61992357636", "hellenctbastos@gmail.co", "Casamento", "16/10/2027", "", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Analice", "61996862586", "erciliaats85@gmail.com", "15 anos", "12/09/2026", "", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Patrícia", "", "patilotti@gmail.com", "Casamento", "12/08/2028", "", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Mariana Junia de Oliveira", "61983205925", "marianajunia01@gmail.ex", "Casamento", "29/08/2026", "", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Joana Nascimento", "61981930432", "joanabercott@gmail.com", "Casamento", "14/01/2028", "", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Matheus Dias de Almeida", "61993788100", "jerrydezoa@gmail.com", "Casamento", "14/01/2028", "", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("César Augusto Ribeiro Cândido", "61999692792", "cesarcandidobm@gmail", "Casamento", "25/09/2026", "", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Camile Cardoso", "61996064302", "carnile22sales@gmail.co", "Casamento", "21/11/2026", "", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Natalia Sousa Baptista", "", "natisoub@gmail.com", "Casamento", "02/07/2027", "", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Isabela Pereira Chianca", "61982909891", "chiancaisabela@gmail.co", "Casamento", "05/09/2027", "", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Mana Eduarda Crispim de Sousa", "61994167495", "eduardacrispimmaria11@", "Casamento", "03/07/2026", "", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Ranyel Gomes Lemes", "61981502533", "gomesranyel247@gmail", "Casamento", "02/04/2028", "", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Emanuelle da rocha", "", "emanuelle@gmail.com", "Casamento", "07/09/2027", "", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Thais Carolina de Paula Martins", "61984450506", "thais marttins7030@gma", "Casamento", "19/02/2027", "", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Dandara", "61981911310", "fono dandarafarias@gma", "Casamento", "26/09/2026", "", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Rai Manano Soares", "", "raimariano@gmail.com", "Casamento", "06/06/2027", "", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Mayra", "", "maytriss97@gmail.com", "Casamento", "29/07/2027", "", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Wendy Carmo de Souza", "61998336732", "afiliadoswendy@gmail.cc", "Casamento", "26/06/2027", "", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Gabrielle", "61986641607", "gabrielleect03@gmail.cor", "Casamento", "21/04/2026", "", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Bruna Felix Tavares", "61999704300", "brunafelutavares@gmail", "Casamento", "24/04/2027", "", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Jaqueline Lima da Silva", "61986213991", "jaquelimapsico@gmail.ct", "Casamento", "12/09/2026", "", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Fernanda", "61999963638", "femandalagom@gmail.cc", "Casamento", "26/06/2027", "", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Karen Rodrigues", "61982914396", "karenvictoria2011@gmail", "Casamento", "07/08/2027", "", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Raisa", "", "raisa.frv@gmail.com", "Casamento", "24/07/2027", "", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Claudia Gornes Assunção", "61996564552", "claudinhagomas@gmail.c", "Casamento", "28/08/2027", "", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Késia", "61998450097", "kesiinharelis@gmail.com", "Casamento", "03/04/2027", "", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Sofia", "61984190457", "sofiaferreira02s@gmail.", "Casamento", "22/08/2027", "", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Sanddy", "", "lets sanddy@gmail.com", "Casamento", "16/01/2027", "", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Emilia Alves", "61984740356", "emiliaalves2013@gmail.c", "Casamento", "24/01/2027", "", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Isadora Moreira Assunção Rosa", "61999037572", "isinha06mar@gmail.com", "Casamento", "06/02/2027", "", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Izabel Cristina Lopes", "61994107390", "leboris2013@gmail.com", "Casamento", "20/07/2027", "", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Francisca das chagas pontes", "", "pontesedilene966@gmail", "Casamento", "16/01/2027", "", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Cláudio Batista Pereis", "", "batistapereitaclaudio", "Casamento", "16/02/2027", "", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Mariana Batista Nogueira Teles da Sih", "61984653194", "mananabatistabüibgmail", "Casamento", "11/09/2027", "", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Isabela", "61994256886", "isabelafandi@gmail.com", "Casamento", "18/09/2027", "", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Matheus", "", "matheusgalo201157@gmail.com", "Casamento", "28/05/2027", "", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Wendi", "61981319984", "1 wendilk@gmail.com", "Casamento", "07/09/2026", "", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Marina Santos Monteiro Cardoso", "61996858065", "marina15smcardoso@gn", "Casamento", "12/12/2027", "", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("lule", "61985318582", "rulesilvaviana@gmail.com", "Casamento", "03/05/2028", "", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Hélien Aparecida Ferreira", "61993678244", "hellenaparecida903@gm", "Casamento", "16/01/2027", "", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Fernanda Gomes de Oliveira Matos", "61981319194", "nandaccesar@gmail.com", "Casamento", "06/03/2027", "", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Augusto Cesar Nascimento Damiano", "61985271995", "augustooct5@gmail.com", "Casamento", "17/07/2027", "", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Caio César de Oliveira Matos", "61995519083", "calcoliver0404@gmail.co", "Casamento", "08/08/2026", "", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Rayssa", "", "rayssa8608@gmail.com", "Casamento", "19/09/2026", "", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Layane Monteiro", "", "Layanelmds@gmail.com", "Aniversário e casamento", "03/07/2026", "", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Diego Girão", "61998622303", "giraodoidao@gmail.com", "Casamento", "22/01/2028", "", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Júlia Oliveira Barbosa", "61996059755", "jubsoliba@gmail.com", "Casamento", "22/01/2028", "", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Priscila Gonçalves de Oliveira Cruz", "", "priscilagoncalvesoc@gmail.com", "Debutante", "30/07/2026", "", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Nicole Andrade", "61992185555", "ap gross87@gmail.com", "Casamento", "31/07/2027", "", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Natália Sereno", "61999963026", "nataliabaserenos@gmail.c", "Casamento", "11/09/2027", "", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Júlia Alves da Silva de Sousa", "61993142882", "alvesjulia217@gmail.com", "Casamento", "01/11/2026", "", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Camila", "61991657030", "camipratesf@gmail.com", "Casamento", "03/07/2027", "", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Francisca Lima", "61982538592", "Ideuzilene084@gmail.cor", "Casamento", "05/05/2028", "", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Talita Erika Resende de Jesus", "", "talita erika@gmail.com", "Casamento", "03/04/2027", "", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Kariny Beatriz da Silva Sousa", "61981845248", "beatriz sousa3264@gmar", "Casamento", "28/08/2027", "", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Gabriel Soares de Moura e Silva", "61996566180", "gabriels moura soares@", "Casamento", "28/08/2027", "", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Lais Barros", "61993807007", "burrosleief@gmail.com", "Casamento", "24/07/2027", "", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Alanna Carolina França", "71996427787", "carol franca bio@gmail.o", "Festa", "14/07/2026", "", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Jackeline Rocha", "61999023756", "jer jackeline@gmail.com", "Casamento", "06/12/2026", "", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Bruna", "", "bruna bud@hotmail.com", "Casamento", "07/07/2027", "", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Larissa Carvalho", "", "larissacarvalho176@gma", "Casamento Religioso", "17/07/2027", "", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Rodrigo Macedo de Toledo", "", "toledo.m.rodrigo@gmail.com", "Casamento", "31/10/2026", "", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Gabriel Argolo Wanderlei", "", "gwanderlei01@gmail.com", "Casamento", "07/08/2027", "", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("ANDRYELLE VIANA DA COSTA E SILVA", "61985774256", "andryelle1993@gmail.cor", "Casamento", "07/08/2027", "", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Thamires patisos", "61986526271", "thamireshagata302@gmi", "Casamento", "21/04/2027", "", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Pamela Amorim", "61981366716", "pamelavictoriana@gmail.", "Casamento", "13/11/2027", "", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Matheus Lobo Leite Ferreira", "61992166363", "matheusllf26@gmail.com", "Casamento", "04/09/2027", "", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Larissa Alves", "", "larissaalm1309@gmail.or", "Casamento", "14/08/2027", "", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Luana", "61994578973", "Juanabarrosoliveiraaa@gr", "Casamento", "20/11/2026", "", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Yasmin Ana Carolina", "61991249676", "yasminana70@gmail.com", "Casamento", "22/08/2026", "", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Vivianne Gusmao", "", "Vigusmao@hotmail.com", "Casamento", "11/06/2027", "", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Anna Beatriz", "", "annabeatrizrodrigue@gm", "Casamento", "06/11/2026", "", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Leticia Brandão Ribeiro", "61983610525", "letybrandao14@gmail.cor", "Casamento", "22/08/2027", "", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Luanny Aragão", "61992976819", "luannyalmeida30@gmail", "Casamento", "23/10/2027", "", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Jefferson Dourado", "61995682491", "jeffin.dourado@gmail.cor", "Arena noivas", "11/10/2026", "", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Mariana de Oliveira dos Santos", "61994036056", "marymadinha@gmail.com", "Casamento", "01/08/2027", "", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Dayene", "61985395787", "dayeneadriana@gmail.co", "Casamento", "04/10/2027", "", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Welder Medeiros", "", "Welder60@gmail.com", "Casamento", "05/12/2026", "", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Barbara Borges", "61983329048", "barbara borges93@gmail", "Casamento", "05/12/2026", "", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Nara", "", "starnara@gmail.com", "Aniversário 15 anot", "25/09/2027", "", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Rebeka Nerés", "61999724068", "rebekaneresi@gmail.com", "Casamento", "03/04/2027", "", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Dionni Gomes da Silva", "61991314128", "dionni87@gmail.com", "Casamento", "19/06/2027", "", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Beatriz", "61981816882", "biagomesct@gmail.com", "Casamento", "18/07/2026", "", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Gleiciane Medeiros de Araújo", "61991725391", "gleiciane eryck@hotmail", "Casamento", "04/07/2026", "", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Marilia Ima", "61981460689", "n manilialima@gmail.com", "Casamento", "29/08/2026", "", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Cecilia Porto", "61996710253", "ceportto@gmail.com", "Casamento", "17/10/2026", "", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Amanda Brandão", "61993697816", "amanda brandao02@gmi", "Casamento", "08/08/2026", "", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Jessica Lima Santos", "61981808353", "jessie mor470@gmail.cor", "Casamento", "17/10/2026", "", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Camilla", "61993573592", "thavennacamilla@gmail.c", "Casamento", "01/05/2027", "", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Luana Sthefane", "61982522293", "luanasthefane@gmail.com", "Casamento", "16/05/2027", "", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Gabriel", "61998847432", "ge soares147@gmail.con", "Casamento", "19/09/2026", "", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Bianca Soder", "", "blancasoder@gmail.com", "Casamento", "27/08/2027", "", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Patricia Caetano", "61982020447", "patycaetano36@gmail.co", "Casamento", "13/09/2026", "", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Luana Farias", "", "luanasfarias2@gmail.com", "Casamento", "12/12/2026", "", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Ellen Cristina", "61999982216", "lilianefsrodrigues11@gm", "Casamento", "12/09/2026", "", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("lane Brito Leal", "61991830307", "ianebl@hotmail.com", "Casamento", "18/12/2026", "", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Lucas Kelvyn Leite da silva", "87981430022", "lucasskelvyn@gmail.com", "Casamento", "18/12/2026", "", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Kucia", "61983418199", "kliciabl@gmail.com", "Casamento", "26/09/2027", "", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Malu Cardoso dos Santos", "61996519972", "malucardoso adv@gmail.", "Casamento", "25/09/2027", "", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Krystal Costa", "61993768313", "costa krystal@gmail.com", "Casamento", "04/06/2027", "", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Naylla e Jonatas", "61983728485", "olokojonatas@gmail.com", "Arena Norva", "16/01/2027", "", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Anna Beatriz", "61991848662", "aleltecamilo@gmail.com", "Casamento", "09/09/2028", "", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Monica Mota", "61081412219", "monicarnota18@gmail.oc", "Casamento", "17/12/2026", "", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Amanda Caroline Ramos", "61996502509", "amndorinrma@gmail.com", "Casamento", "26/03/2027", "", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("João Pedro Ortega", "61991489053", "joaortega18@gmail.com", "Casamento", "18/06/2027", "", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Hyorana Figueiredo Diniz", "61992779462", "hyorana figueiredoligma", "Casamento", "18/06/2027", "", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Suyany", "", "suyyanyy@gmail.com", "Casamento", "04/09/2027", "", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Marcus", "", "cavalcantemarcus5@gmail.com", "Casamento", "17/09/2027", "", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Eduardo guarnier", "61999643033", "eduardoquarnieria@gmail.c", "Casamento", "16/05/2027", "", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("João", "61994237132", "joaobnas@sempreceub.c", "Casamento", "16/05/2027", "", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Emilly Zica.", "61983153530", "emillydasilva110@gmail", "Casamento", "16/05/2027", "", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Mana Eduarda", "92991780266", "mamaed97@gmail.com", "Casamento", "16/05/2027", "", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Daniel", "61982077772", "daniel montartoyos silver", "Casamento", "04/07/2028", "", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Jeissiany Sousa", "61995477979", "jeissy marketing@gmail.c", "Casamento", "10/04/2027", "", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Kailany Ramos", "61994134462", "kailanyramoam@gmail.cz", "Casamento", "18/07/2027", "", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Kamyla Lima", "61996384210", "silvakamyla600@gmail.cx", "Casamento", "30/10/2027", "", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Sofia Jabber de Souza", "61981552631", "sofiajabber4@gmail.com", "Casamento", "04/09/2027", "", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Eduarda Barbirato", "", "eduarda.barbirato@gmail.com", "Casamento", "06/09/2026", "", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Sarah amorim", "61985010699", "arq sarahac@gmail.com", "Casamento", "05/08/2027", "", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Glaucia Rodrigues de Lima", "61996846394", "glaucia1967.gd@gmail.er", "Arenas noivas", "04/07/2026", "", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Larissa Caddah", "", "lalacaddah@gmail.com", "Casamento", "04/09/2027", "", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Adenilton", "", "Adenilton,junior014@gmail.com", "Casamento", "22/09/2027", "", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Leticia Nishiyama", "611984600889", "leticia augusta.n.a@gmai", "Casamento", "22/10/2026", "", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Armanda", "992152472", "amanda.spaulondy@gma", "Casamento", "20/11/2026", "", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Karine Antunes Coelho", "", "karine a coelho@gmail.com", "Casamento", "10/09/2026", "", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Karen Oliveira", "61981380615", "ka.oliveira254@gmail.cor", "Casamento", "21/11/2026", "", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Ludimilla", "21982279636", "Judimillarodrigues95@gm", "Casamento", "18/07/2027", "", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Ana Cláudia de Azevedo Ferreira", "61984429073", "anaferreira2108@gmail.c", "Casamento", "26/09/2026", "", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Gabrielle", "61983719729", "gabriellebertoly@gmail.cr", "Casamento", "05/12/2026", "", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Pedro Hennque", "61982368222", "sophiaelida9@gmail.com", "Casamento", "10/07/2027", "", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Isa Monteiro", "5561999055015", "lisliraservicos@gmail.con", "Casamento", "07/11/2026", "", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Catarine", "62984028298", "dra catarinelealdentista", "Casamento", "12/06/2027", "", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Mayara Ayres", "61993071414", "mayaraayresadv@gmail.c", "Casamento", "04/09/2027", "", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Heitor", "61991087742", "heitor711n@gmail.com", "Casamento", "03/07/2026", "", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Maria Eduarda", "61985429384", "eduardalimahatista gn", "Casamento", "12/09/2026", "", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Raizza Cristina", "61983076377", "ralzzabaptistauribi@gmall", "Casamento", "19/07/2028", "", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Julia Vargas Larangote Rodrigues", "61985316893", "juliav.conexao@gmail.cor", "Casamento", "07/08/2027", "", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Marcos", "61981286897", "marcosdabateriasomall", "Casamento", "14/08/2027", "", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Thalsa", "61991770577", "thaisasilvafonseca15 or.", "Casamento", "14/08/2027", "", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Vitória Regia da Silva", "61993140631", "vitoria.regiav21@gmail.cz", "Casamento", "04/09/2027", "", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Giovanna Fregapani", "61996399955", "g fregapani.barreto@gma", "Casamento", "19/12/2027", "", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Alcides", "6120316052", "aldacforte@gmail.com", "Casamento", "10/10/2026", "", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Fabiano Ramos", "61991981518", "makisilva16@gmail.com", "Arena Noivas", "04/07/2026", "", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Déborah Alves", "", "deborahzozimo@gmail.com", "Casamento", "04/07/2028", "", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Gabriel Soares de Moura e Silva", "61996566180", "gabriel s moura soares", "Casamento", "28/08/2027", "", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Gabriela Sousa Pinheiro", "61999777458", "gahisptj@gmail.com", "Casamento", "11/09/2027", "", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Karolline e Pedro", "61981916932", "karollinematos@gmail.co", "Casamento", "15/07/2027", "", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Maria Luiza Santiago Siqueira", "", "Maria Luiza", "Casamento", "16/07/2027", "", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Mariana Oliveira", "61995881657", "maariioli51@gmail.com", "Casamento", "28/05/2027", "", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Igor Meireles Games", "61998561390", "engigorgomes2@gmail.", "Casamento", "06/09/2026", "", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Leonardo", "61984783470", "leonardolonde@gmail.cor", "Casamento", "14/08/2027", "", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Gabriel Delfino", "61982511519", "gabrieldelfinoucb@gmail.", "Casamento", "26/09/2026", "", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Cintia", "", "cintiarodrigues490@gmail.com", "Casamento", "28/05/2027", "", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Giovanna", "61985363715", "giovannabatistamonteiro:", "Casamento", "17/07/2027", "", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Sofia Elizabeth Alves Martins de Carve", "61986425164", "sofia eam99@gmail.com", "Casamento", "11/12/2026", "", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Ricardo", "61991550301", "ricardoviannaneto@gmail", "Casamento", "20/05/0027", "", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Dara", "61983422626", "dara paulino26@gmail.co", "Casamento", "17/10/2026", "", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Maria Fabiane Soares", "", "fabianerhema@gmail.cor", "Casamento", "24/07/2027", "", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Amanda dos Santos Souma", "61993111764", "amandassousa3454@gm", "Casamento", "27/03/2027", "", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Rafaella e vitor", "61981382667", "rafaellarochadecarvalho", "Casamento", "15/08/2027", "", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Ana Carolina Bezerra Araujo", "61999665846", "carolegabriel2026@gmall", "Casamento", "20/11/2026", "", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Danna Gomes", "61998722228", "dannagomesm@gmail.co", "Casamento", "02/10/2027", "", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("André Gomes da Silva", "61993583798", "andre gds.ag@gmail.com", "Casamento", "03/04/2027", "", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    
    # ---- Leads do WhatsApp Adicionais Tratados ----
    ("Felipe", "61981404740", "", "", "", "70 pessoas", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Natália", "61984794629", "", "", "", "150 pessoas", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Ana cecilia", "61998072001", "", "", "", "120 pessoas", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Rafael", "61984105111", "", "", "", "150 pessoas", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Victor", "61986225878", "", "", "", "100 pessoas", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Adriana Oliveira", "61996673732", "", "", "", "120 pessoas", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Karine", "61985121220", "", "", "", "120 pessoas", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Ysabella", "61985669771", "", "", "", "60 a 70 pessoas", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Leticia", "61998086174", "", "", "", "60 pessoas", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("João Lucas", "61996116011", "", "", "", "120 pessoas", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Flávia", "61981338337", "", "", "", "100 pessoas", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Isabela", "61992570814", "", "", "", "160 pessoas", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Tenylle", "61999526133", "", "", "", "100 pessoas", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Larissa", "61996705387", "", "", "", "300", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Ana luiza", "61998777572", "", "", "", "90 pessoas", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Raissa", "61985256560", "", "", "", "160 pessoas", "", "Chamar urgente", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Juliana", "61985511631", "", "", "", "160 pessoas", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Yasmin", "61981398138", "", "", "", "100 pessoas", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Lilian", "61991874286", "", "", "", "100 pessoas", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Geovana", "61995360858", "", "", "", "100 pessoas", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Laís", "61993807005", "", "", "", "100 pessoas", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Arthur", "61998538803", "", "", "", "70 pessoas", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Leticia", "61993021774", "", "", "Setembro 2027", "150 pessoas", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Gabrielle", "43998584031", "", "", "ano que vem", "100 pessoas", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Leticia", "61981448902", "", "", "setembro 2027", "100 pessoas", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Felipe", "61996760766", "", "", "setembro 2026", "200 pessoas", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Lidiane,", "61982513833", "", "", "setembro 2027", "150 pessoas", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Vitor", "61991248143", "", "", "outubro 2027", "110 pessoas", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Luana", "61982522293", "", "", "maio 2027", "100 pessoas", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Davi", "61982263998", "", "", "Julho 2027", "50 pessoas", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Juliana", "61993341382", "", "", "Outubro 2027", "150 pessoas", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Mel", "61996693572", "", "", "Novembro 2026", "200 pessoas", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Ana clara", "61983144114", "", "", "Outubro 2027", "180 pessoas", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Sara", "61999777557", "", "", "junho 2027", "150 pessoas", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Hyorana", "61992779462", "", "", "junho 2027", "60 pessoas", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Cíntia", "61982815250", "", "", "outubro 2027", "60 pessoas", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Rian", "62991938233", "", "", "abril 2027", "200 pessoas", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Maria Eduarda", "61998812655", "", "", "junho 2027", "250 pessoas", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Lucas", "61993997889", "", "", "setembro 2027", "80 pessoas", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Júlia", "61983771513", "", "", "agosto 2028", "80 pessoas", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Leonardo", "61981116429", "", "", "junho 2027", "120 pessoas", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Magno", "61991124837", "", "", "maio 2027", "150 pessoas", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Vinicius", "61984069840", "", "", "outubro 2027", "70 pessoas", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Letícia", "61985640651", "", "", "agosto 2027", "100 pessoas", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Emily", "61991835561", "", "", "agosto 2027", "120 pessoas", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Jan", "61982102103", "", "", "Dezembro 2026", "80 pessoas", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Vitória", "61984479539", "", "", "junho 2027", "150 pessoas", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Lurdes", "61986080180", "", "", "Junho 2027", "150 pessoas", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Aricia", "61983331683", "", "", "dezembro 2027", "100 pessoas", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Stefhany", "61999834606", "", "", "dezembro 2026", "150 pessoas", "", "Chamar urgente", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Beatriz", "61982394053", "", "", "Maio 2027", "100 pessoas", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Wesley", "61986713068", "", "", "novembro 2026", "40 pessoas", "", "Chamar urgente", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Simone", "619992807734", "", "15 anos", "fevereiro 2027", "150 pessoas", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Lilian", "61984841044", "", "", "setembro 2027", "150 pessoas", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Thaís", "61984881390", "", "", "setembro 2026", "130 pessoas", "", "Chamar urgente", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Geovana", "61985555860", "", "", "março 2027", "150 pessoas", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Débora", "61983717156", "", "", "novembro 2026", "150 pessoas", "", "Chamar urgente", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Renata", "61998124099", "", "", "outubro 2026", "150 pessoas", "", "Chamar urgente", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Isadora", "71999283739", "", "", "agosto 2027", "100 pessoas", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Natália", "61985889391", "", "", "abril 2027", "200 pessoas", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Isadora", "61999022993", "", "", "abril 2027", "200 pessoas", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Lucio", "619999786600", "", "", "dezembro 2026", "100 pessoas", "", "Chamar urgente", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Júlia", "61981046441", "", "", "julho 2027", "150 pessoas", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Rebeca", "61998781304", "", "", "novembro 2026", "80 pessoas", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Louyse", "61999161514", "", "", "abril 2027", "100 pessoas", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Ana beatriz", "61984938594", "", "", "janeiro 2027", "120 pessoas", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Aislane", "61981558069", "", "", "junho 2027", "50 pessoas", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Júlia", "61991950722", "", "", "1 agosto", "150 pessoas", "", "Chamar urgente", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Michele", "61992443814", "", "", "julho 2027", "200 pessoas", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Carol é Gabriel", "61999665846", "", "", "novembro", "80 pessoas", "", "Chamar urgente", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Kleyson", "61984953541", "", "", "julho 2027", "150 pessoas", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Fernanda", "61982071318", "", "", "abril 2027", "100 pessoas", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Marina", "61981849828", "", "", "julho 2027", "200 pessoas", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Letícia", "61998544667", "", "", "outubro 2026", "50 pessoas", "", "Chamar urgente", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Malu", "61981222491", "", "15 anos", "19/09/2026", "150 pessoas", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Maria Clara", "61994241121", "", "", "outubro 2027", "100 pessoas", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Giulia e rian", "61999969778", "", "", "agosto 2027", "60 pessoas", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Ana Claudia e Caio", "61992041348", "", "", "Julho 2027", "120 pessoas", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Gabriel raissa", "61991720638", "", "", "julho 2027", "200 pessoas", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Mari", "61996311124", "", "", "setembro 2026", "100 pessoas", "", "Chamar urgente", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Ariana", "61998563889", "", "Cerimonialista", "", "", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Calebe -", "61981672102", "", "Casamento", "", "200 a 300 pessoas", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Aline -", "61982004971", "", "Casamento", "", "60 pessoas", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("João Victor -", "61999726871", "", "Casamento", "", "60 pessoas", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Shelda -", "61982470719", "", "Casamento", "", "100 pessoas", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Ana Carolina -", "61981334865", "", "Casamento", "2028", "150", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Myrelle -", "61995142112", "", "Casamento", "", "200 pessoas", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Joana - JA Eventos", "61992757763", "", "Cerimonialista", "", "", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Kalleb -", "61985065801", "", "Casamento", "", "150", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Liliana -", "61981238483", "", "15 anos", "", "", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Beatriz -", "61981645525", "", "Casamento", "", "150 adultos", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Dandara -", "61981911310", "", "Casamento", "", "70 pessoas", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Igor Mendes Letícia", "61983608842", "", "", "", "", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Brenda -", "61981873165", "", "Casamento", "", "90 Pessoas", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Douglas -", "61998773736", "", "Casamento", "", "100 pessoas", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Thalyta", "61992863245", "", "", "", "", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("João Pedro -", "61985102840", "", "Casamento", "em 20 dias", "170 pessoas", "", "Chamar urgente", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Ana Beatriz -", "61984260501", "", "Casamento", "", "130 pessoas", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Luana -", "61992705632", "", "Casamento", "", "100 pessoas", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Letícia -", "61981219815", "", "Casamento", "", "120 pessoas", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Carol -", "61995044000", "", "Casamento", "", "80 pessoas", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Yasmin - Festival de", "61993720346", "", "", "", "", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Cristal -", "61993768313", "", "Casamento", "", "150", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Naylla -", "61983728485", "", "Casamento", "", "100 pessoas", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Sara -", "61984816809", "", "Casamento", "", "150 pessoas", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Maria Paula -", "61992100192", "", "Casamento", "", "", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Thiago -", "61981774307", "", "Casamento", "ago/27", "120 pessoas", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Emilly -", "61983153530", "", "Casamento", "", "70 pessoas", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Vinicius Rodrigues -", "61981854804", "", "Casamento", "", "45 pessoas", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Jadson e Gabriela -", "61984882824", "", "Casamento", "", "60 pessoas", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Rafaella -", "61992110110", "", "Casamento", "", "150 pessoas", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Júlia -", "61985316883", "", "Casamento", "", "150 pessoas", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Eduarda -", "61985429802", "", "Casamento", "", "100", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Maria Luiza -", "61992687202", "", "Casamento", "26/12/26", "80 a 100", "", "Chamar urgente", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Beatriz -", "61993917842", "", "Casamento", "", "150", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Cinthya -", "61993048574", "", "Casamento", "", "150 pessoas", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Carol -", "61982713684", "", "Casamento", "", "130", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Pedro Nascimento -", "61996034976", "", "Casamento", "", "100 pessoas", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Alice -", "61994655653", "", "Casamento", "", "150 pessoas", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Elise -", "61981079772", "", "Cerimonialista", "", "", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False),
    ("Juliana - Festa", "61991327007", "", "15 anos", "Maio/2027", "", "", "Não contatado", "", "Não contatado", "", "Não contatado", "", "Não", False)
]

def clean_phone(phone_str):
    if not phone_str:
        return ""
    return re.sub(r'\D', '', phone_str)

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    # Criando a tabela com a estrutura exata solicitada
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
    
    # Inserção massiva da carga total de dados com bloqueio de repetidos
    c.execute("SELECT COUNT(*) FROM leads")
    if c.fetchone()[0] == 0:
        df_iniciais = pd.DataFrame(LEADS_INICIAIS, columns=[
            "nome", "numero", "email", "tipo_evento", "data_evento", "qtd_convidados", "local_festa", 
            "status_1", "obs_1", "status_2", "obs_2", "status_3", "obs_3", "degustacao", "desconto_apresentado"
        ])
        
        # Filtro de duplicatas (apenas um contato por número de WhatsApp/E-mail)
        df_iniciais['numero_limpo'] = df_iniciais['numero'].apply(clean_phone)
        
        # Remover duplicados onde o numero não for vazio
        mask_com_numero = df_iniciais['numero_limpo'] != ""
        df_com_num = df_iniciais[mask_com_numero].drop_duplicates(subset=["numero_limpo"], keep='first')
        df_sem_num = df_iniciais[~mask_com_numero]
        
        df_limpo = pd.concat([df_com_num, df_sem_num]).drop(columns=["numero_limpo"])
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

# --- INTERFACE ---
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
        tipo_evento = col4.text_input("Tipo de Evento (Ex: Casamento)")
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
st.info("💡 Dê duplo clique em qualquer célula para digitar observações ou alterar os menus.")

df = load_data()

if not df.empty:
    pesquisa = st.text_input("🔍 Filtrar por Nome, WhatsApp ou Status:")
    if pesquisa:
        df = df[
            df['nome'].str.contains(pesquisa, case=False, na=False) | 
            df['numero'].str.contains(pesquisa, case=False, na=False) |
            df['status_1'].str.contains(pesquisa, case=False, na=False)
        ]

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
        st.success("Alterações gravadas com sucesso!")
        st.rerun()
else:
    st.info("Nenhum dado encontrado.")
