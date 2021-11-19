import pyodbc

def retornar_conexao_sql():
    
    server = "YOUR SERVER HERE"
    database = "YOUR DATA BASE"
    username = "YOUR USER NAME"
    password = "YOUR PASSWORD"
    string_conexao = 'Driver={SQL Server Native Client 11.0};Server='+server+';Database='+database+';UID='+username+';PWD='+ password
    #string_conexao = 'Driver={SQL Server Native Client 11.0};Server='+server+';Database='+database+';Trusted_Connection=yes;'
    try:
        conexao = pyodbc.connect(string_conexao, autocommit=True)
        return conexao.cursor()
    except:
        return "Erro de conexão ao banco de dados!"


def retornar_conexao():
    server = "YOUR SERVER HERE"
    database = "YOUR DATA BASE"
    username = "YOUR USER NAME"
    password = "YOUR PASSWORD"
    string_conexao = 'Driver={SQL Server Native Client 11.0};Server=' + server + ';Database=' + database + ';UID=' + username + ';PWD=' + password
    # string_conexao = 'Driver={SQL Server Native Client 11.0};Server='+server+';Database='+database+';Trusted_Connection=yes;'
    try:
        conexao = pyodbc.connect(string_conexao, autocommit=True)
        return conexao
    except:
        return "Erro de conexão ao banco de dados!"


def insert_user(username, registration_number, email, senha, access_type, site):
    cursor = retornar_conexao_sql()
    try:
        row = cursor.execute("SELECT USERNAME, EMAIL FROM USUARIOS where REGISTRATION_NUMBER=?",
                            registration_number).fetchone()
        if row == None:
            cursor.execute("INSERT INTO USUARIOS(username, registration_number, email, senha, access_type, _site) VALUES (?, ?, ?, ?, ?, ?)",username, registration_number, email, senha, access_type, site)
            row2 = cursor.execute("SELECT USERNAME, EMAIL FROM USUARIOS where REGISTRATION_NUMBER=?", registration_number).fetchone()
            return f' Usuário cadastrados: {row2.USERNAME} Email: {row2.EMAIL}'
        else:
            return f'O usuário {row.USERNAME} já possui cadastro.'
    except:
        return "Erro de conexão ao banco de dados!"


def login(username, password):
    try:
        cursor = retornar_conexao_sql()
        row = cursor.execute("SELECT USERNAME, SENHA, ACCESS_TYPE, _SITE FROM USUARIOS where USERNAME=?",username).fetchone()
    except:
        return ['Erro de conexão ao banco de dados!', 'No conection']

    try:    
        if row.USERNAME == username and row.SENHA == password:
            if row.ACCESS_TYPE == 'ADMIN':
                return ['ADMIN', row._SITE]
            else:
                return ['COMMON USER', row._SITE]
        else:
            return ['Usuário ou senha incorretos', 'No site']
    except:
        return ['Usuário ou senha incorretos', 'No site']


def busca_usuario(registration_number):
    cursor = retornar_conexao_sql()
    try:
        row = cursor.execute('SELECT USERNAME, _SITE, ACCESS_TYPE, EMAIL FROM USUARIOS WHERE REGISTRATION_NUMBER=?', registration_number).fetchone()
        return row
    except:
        return 'User not found!'


def retorna_KPI():
    cursor = retornar_conexao_sql()

    rows = cursor.execute('''if not exists (select * from TB_KPI)

    create table TB_KPI (

        _DATE DATE NOT NULL,
		_KPI VARCHAR(200) NOT NULL,
		_TARGET FLOAT NOT NULL,
		_VALUE FLOAT NOT NULL,
		_SITE VARCHAR(200) NOT NULL,
		_COMMENTS TEXT,
		_USERNAME VARCHAR(200) NOT NULL

    )''')
    return rows


def insert_KPI(_DATE, _KPI, _TARGET, _VALUE, _SITE, _COMMENTS, _USERNAME):
    cursor = retornar_conexao_sql()
    cursor.execute("BULK INSERT TB_KPI FROM 'indicadores_recife.csv' WITH (FORMAT='CSV');")
    print('Dados importados com sucesso')


def modica_usuario():
    pass
