import PySimpleGUI as sg
import pandas as pd
import bancodados as bd
from datetime import datetime
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import seaborn as sns


w, h = sg.Window.get_screen_size()
my_new_theme = {'BACKGROUND': 'white',
                'TEXT': 'black',
                'INPUT': 'white',
                'TEXT_INPUT': 'black',
                'SCROLL': 'white',
                'BUTTON': ('white', '#AB1717'),
                'PROGRESS': ('#0091ff', '#D0D0D0'),
                'BORDER': 1,
                'SLIDER_DEPTH': 0,
                'PROGRESS_DEPTH': 0}

sg.theme_add_new('my_custom_theme', my_new_theme)
sg.theme('my_custom_theme')
kpi_dashboard = 'All'
var_aux = False

def gera_relatorio(visao_tabela, caminho):
    data_hora = datetime.now().strftime("%d-%m-%Y-%H-%M-%S")
    df = pd.DataFrame(visao_tabela, columns=['DATE', 'SITE', 'KPI', 'TARGET', 'VALUE', 'USERNAME'])
    df.to_csv(caminho + '/kpi_report_' + data_hora + '.csv', encoding='UTF-8', index=False)
    return f'Saved in {caminho}'


def preenche_listbox():
    conexao = bd.retornar_conexao()  # alterar esta função para retornar a conexão e não o cursor
    usuarios = 'SELECT USERNAME, REGISTRATION_NUMBER, EMAIL, ACCESS_TYPE FROM USUARIOS'
    # df = pd.read_csv('dados_indicadores.csv', encoding='utf-8', sep=';')
    df = pd.read_sql(usuarios, conexao)
    data = df.values.tolist()  # read everything else into a list of rows
    header_list = ['Username', 'Registration Number', 'Email', 'Acess type']
    return header_list, data


# Capturar os dados de site e username quando o login for feito
def carrega_KPI(site, username):
    conexao = bd.retornar_conexao()  # alterar esta função para retornar a conexão e não o cursor
    inst_sql = 'SELECT _DATE, _SITE, _KPI, _TARGET, _VALUE, _USERNAME FROM TB_KPI'
    dfKPI = pd.read_sql(inst_sql, conexao)
    dfKPI = dfKPI.loc[dfKPI['_SITE'] == site]
    combo_list = dfKPI['_KPI'].drop_duplicates()
    combo_list = combo_list.tolist()
    combo_list.insert(0, 'All')
    data = dfKPI.values.tolist()  # read everything else into a list of rows
    header_list = ['DATE', 'SITE', 'KPI', 'TARGET', 'VALUE', 'USERNAME']
    return header_list, data, combo_list


def filtra_KPI(kpi, site):
    conexao = bd.retornar_conexao()  # alterar esta função para retornar a conexão e não o cursor
    inst_sql = 'SELECT _DATE, _SITE, _KPI, _TARGET, _VALUE, _USERNAME FROM TB_KPI'
    dfKPI = pd.read_sql(inst_sql, conexao)
    if kpi == 'All':
        dfKPI = dfKPI.loc[dfKPI['_SITE'] == site]
        data = dfKPI.values.tolist()
    else:
        dfKPI = dfKPI.loc[dfKPI['_SITE'] == site]
        dfKPI = dfKPI.loc[dfKPI['_KPI'] == kpi]
        data = dfKPI.values.tolist()  # read everything else into a list of rows
    return data


def login():
  
    part2 = [

        [sg.Image('Images/user.PNG', size=(80, 77), background_color='#FFFFFF', pad=(7, (80, 25)))],
        [sg.Text('Username', font='Helvetica 12 italic', size=(9, 1), background_color='#FFFFFF', pad=(7, (3, 5)))],
        [sg.InputText('', font='Helvetica 12', size=(35, 4), background_color='#FFFFFF', border_width=1, key='-user-')],
        [sg.Text('Password', font='Helvetica 12 italic', enable_events=True, size=(9, 1), background_color='#FFFFFF',
                 pad=(7, (7, 5)), key='-LOGIN-')],
        [sg.InputText('', font='Helvetica 12', enable_events=True, size=(35, 4), password_char='*',
                      background_color='#FFFFFF', border_width=1, key='-senha-')],
        [sg.Button('Login', size=(7, 1), font='Helvetica 12 bold italic', button_color='#B11919', pad=(7, (25, 20)))],
        [sg.Text('Register', font='Helvetica 9 bold italic', size=(9, 1), background_color='#FFFFFF', text_color='blue',
                 justification='center', enable_events=True, click_submits=True)],
        [sg.Button('Submit', visible=False, bind_return_key=True)]
    ]
    # Cria a janela
    part1 = [
        [sg.Image('Images/logo.PNG', size=(80, 76), background_color='#FFFFFF')]
    ]

    layout = [
        [sg.Column(part1, justification='left', background_color='#FFFFFF'), ],
        [sg.Column(part2, background_color='#FFFFFF', element_justification='center', pad=(20, 3))]
    ]
    return sg.Window("User Login", layout, size=(w, h), return_keyboard_events=True, element_justification='center',
                     resizable=True, finalize=True, background_color='#FFFFFF', icon='Images/user_icon.ico')


def cadastro():
    kpi_value = ''
    part1 = [
        [sg.Image('Images/logo.PNG', size=(80, 77), background_color='#FFFFFF')]
    ]
    # Todas as coisas dentro de sua janela.
    part2 = [
        [sg.Image('Images/user.PNG', size=(60, 60), background_color='#FFFFFF', pad=((180, 20), (45, 20)))],
        [sg.Text('Username:', font='Helvetica 12 italic', size=(18, 1), background_color='#FFFFFF', pad=(2, 5)),
         sg.InputText('', font='Helvetica 12', size=(35, 4), background_color='#FFFFFF', border_width=1, key='-user-')],
        [sg.Text('Registration Number:', font='Helvetica 12 italic', size=(18, 1), background_color='#FFFFFF',
                 pad=(2, 5)),
         sg.InputText('', font='Helvetica 12', size=(35, 4), background_color='#FFFFFF', border_width=1, key='-rg-')],
        [sg.Text('Email:', font='Helvetica 12 italic', size=(18, 1), background_color='#FFFFFF', pad=(2, 5)),
         sg.InputText('', font='Helvetica 12', size=(35, 4), background_color='#FFFFFF', border_width=1,
                      key='-email-')],
        [sg.Text('Industrial Site:', font='Helvetica 12 italic', size=(18, 1), pad=(2, 5), background_color='#FFFFFF'),
         sg.Combo(['CAJICA', 'ITATIAIA', 'RECIFE', 'RIO NEGRO'], default_value='', font='Helvetica 12', key='-SITE-',
                  size=(34, 4), background_color='#FFFFFF')],

        [sg.Text('Password:', font='Helvetica 12 italic', size=(18, 1), background_color='#FFFFFF', pad=(2, 5)),
         sg.InputText('', font='Helvetica 12', size=(35, 4), background_color='#FFFFFF', border_width=1,
                      password_char='*', key='-pass-')],
        [sg.Text('Confirm Password:', font='Helvetica 12 italic', size=(18, 1), background_color='#FFFFFF', pad=(2, 5)),
         sg.InputText('', font='Helvetica 12', size=(35, 4), background_color='#FFFFFF', border_width=1,
                      password_char='*', key='-confirm_pass-')],
        [sg.Button('Register', button_color='#AB1717', font='Helvetica 12 bold italic', pad=((180, 20), (20, 20)),
                   size=(10, 1), key='-register-')],
        [sg.Text('', background_color='#FFFFFF', text_color='#AB1717', key='-error-', auto_size_text=True,
                 pad=((180, 20), (3, 3)), justification='center')],
        [sg.Text('Login', background_color='#FFFFFF', size=(9, 1), pad=((180, 20), (10, 20)),
                 font='Helvetica 9 bold italic', text_color='blue', enable_events=True, click_submits=True,
                 key='-login-', justification='center', )]
    ]

    layout = [
        [sg.Column(part1, justification='left', background_color='#FFFFFF'), ],
        [sg.Column(part2, background_color='#FFFFFF', element_justification='center', pad=(20, 3))]
    ]

    return sg.Window("User Registration", layout, size=(w, h), element_justification='center', resizable=True,
                     finalize=True, background_color='#FFFFFF', icon='Images/user_icon.ico')


def registro_KPI():
    header_list, dados, combo_list = carrega_KPI(site, user)

    # Todas as coisas dentro de sua janela.
    coluna1_KPI = [[sg.Image('Images/logo.PNG', size=(80, 77), background_color='#FFFFFF', pad=(7, (3, 40))),
                    sg.Text('Data Factory', font='Helvetica 24 bold italic', text_color='#7E7364',
                            background_color='#FFFFFF', pad=(7, (3, 40)))],
                   [sg.Text('KPI Name:', size=(9, 1), background_color='#FFFFFF'),
                    sg.Combo(combo_list, default_value='All', key='-KPI_NAME-',
                             size=(29, 6), background_color='#FFFFFF', enable_events=True),
                    sg.Text('Owner:', size=(9, 1), pad=((35, 2), 3), background_color='#FFFFFF'),
                    sg.InputText(user, size=(30, 6), background_color='#FFFFFF', border_width=1)],
                   [sg.Text('KPI Value:', size=(9, 1), background_color='#FFFFFF'),
                    sg.InputText('', size=(30, 6), background_color='#FFFFFF', border_width=1, key='-KPI_VALUE-'),
                    sg.Text('KPI Target: ', pad=((39, 2), 3), size=(9, 1), background_color='#FFFFFF'),
                    sg.InputText('', size=(30, 6), background_color='#FFFFFF', border_width=1, key='-KPI_TARGET-')],
                   [sg.Text('Date:', size=(9, 1), background_color='#FFFFFF'),
                    sg.InputText(size=(30, 6), background_color='#FFFFFF', border_width=1, key='-DATE-',
                                 enable_events=True, disabled=True),
                    sg.CalendarButton(' ', close_when_date_chosen=True, button_color='#FFFFFF', target='-DATE-',
                                      location=(900, 100), no_titlebar=False, image_filename='Images/calendar.png',
                                      image_size=(16, 16), format=('%Y-%m-%d'), key='mes'),
                    sg.Text('Comments: ', pad=((9, 2), 3), size=(9, 1), background_color='#FFFFFF'),
                    sg.InputText('', size=(30, 6), background_color='#FFFFFF', border_width=1)
                    ],
                   [sg.Text('Monthly Review about the selected KPI', size=(40, 1), background_color='#FFFFFF',pad=(7, (35, 3)))],
                   [sg.Table(values=dados, headings=header_list, vertical_scroll_only=True, display_row_numbers=True,
                             col_widths=[10, 10, 20, 10, 10, 10], auto_size_columns=None, num_rows=min(17, 15),
                             size=(120, 15), header_background_color='#AB1717', header_text_color='#FFFFFF',
                             justification='left', enable_events=True, selected_row_colors=('#FFFFFF','#339A99'), key='-Table-'), sg.Image(size=(24, 24),pad=(1,(0,270)), filename='Images/download.png', key='-download-', enable_events=True)],
                   [sg.Button('Save', font='Helvetica 12 bold italic', button_color='#AB1717', size=(10, 1)),
                    sg.Button('Edit', button_color='#AB1717', size=(10, 1), font='Helvetica 12 bold italic',
                              pad=(7, 15))]
                   ]

    coluna2_KPI = [
        [sg.Text('Welcome ' + user.lower(), auto_size_text=True, background_color='#FFFFFF', text_color='#000000',
                 key='-USER-',
                 pad=((140, 0), 10)),
         sg.Image('Images/usuario.png', size=(32, 32), pad=((2, 0), 10), background_color='#FFFFFF')]
    ]
    # Cria a janela

    layout = [[sg.Column(coluna1_KPI, background_color='#FFFFFF', size=(w - (w * (1 / 3)), h), pad=(30, 3)),
               sg.Column(coluna2_KPI, size=(w * (1 / 3), h), background_color='#FFFFFF',
                         element_justification='center')]
              ]
    return sg.Window("Registration of Industrial KPI's", layout, size=(w, h), font='Helvetica 12',
                     element_justification='left', resizable=True, finalize=True, background_color='#FFFFFF',
                     icon='Images/bar_icon.ico')


def win_administrador():
    header_list, dados, combo_list = carrega_KPI(site, user)


    coluna1_KPI = [[sg.Image('Images/logo.PNG', size=(80, 77), background_color='#FFFFFF', pad=(7, (3, 40))),
                    sg.Text('Data Factory', font='Helvetica 24 bold italic', text_color='#7E7364',
                            background_color='#FFFFFF',  pad=(7, (3, 40)))],
                   [sg.Text('KPI Name:', size=(9, 1), background_color='#FFFFFF'),
                    sg.Combo(combo_list, default_value='All', key='-KPI_NAME-',
                             size=(29, 6), background_color='#FFFFFF', enable_events=True),
                    sg.Text('Owner:', size=(9, 1), pad=((35, 2), 3), background_color='#FFFFFF'),
                    sg.InputText(user, size=(30, 6), background_color='#FFFFFF', border_width=1)],
                   [sg.Text('KPI Value:', size=(9, 1), background_color='#FFFFFF'),
                    sg.InputText('', size=(30, 6), background_color='#FFFFFF', border_width=1, key='-KPI_VALUE-'),
                    sg.Text('KPI Target: ', pad=((39, 2), 3), size=(9, 1), background_color='#FFFFFF'),
                    sg.InputText('', size=(30, 6), background_color='#FFFFFF', border_width=1, key='-KPI_TARGET-')],
                   [sg.Text('Date:', size=(9, 1), background_color='#FFFFFF'),
                    sg.InputText(size=(30, 6), background_color='#FFFFFF', border_width=1, key='-DATE-',
                                 enable_events=True, disabled=True),
                    sg.CalendarButton(' ', close_when_date_chosen=True, button_color='#FFFFFF', target='-DATE-',
                                      location=(900, 100), no_titlebar=False, image_filename='Images/calendar.png',
                                      image_size=(16, 16), format=('%Y-%m-%d'), key='mes'),
                    sg.Text('Comments: ', pad=((9, 2), 3), size=(9, 1), background_color='#FFFFFF'),
                    sg.InputText('', size=(30, 6), background_color='#FFFFFF', border_width=1)
                    ],
                   [sg.Text('Monthly Review about the selected KPI', size=(40, 1), background_color='#FFFFFF',pad=(7, (35, 3)))],
                   [sg.Table(values=dados, headings=header_list, vertical_scroll_only=True, display_row_numbers=True,
                             col_widths=[10, 10, 20, 10, 10, 10], auto_size_columns=None, num_rows=min(17, 15),
                             size=(120, 15), header_background_color='#AB1717', header_text_color='#FFFFFF',
                             justification='left', enable_events=True, selected_row_colors=('#FFFFFF','#339A99'), key='-Table-'), sg.Image(size=(24, 24),pad=(1,(0,270)), filename='Images/download.png', key='-download-', enable_events=True)],
                   [sg.Button('Save', font='Helvetica 12 bold italic', button_color='#AB1717', size=(10, 1)),
                    sg.Button('Edit', button_color='#AB1717', size=(10, 1), font='Helvetica 12 bold italic',
                              pad=(7, 15))]
                   ]

    coluna2_KPI = [
        [sg.Text('Welcome ' + user.lower(), auto_size_text=True, background_color='#FFFFFF', text_color='#000000',
                 pad=((160, 0), 10), justification='right'),
         sg.Image('Images/usuario.png', size=(32, 32), pad=((2, 0), 10), background_color='#FFFFFF')],
        [sg.Text('', pad=((0, 2), 225), size=(40, 15), background_color='#FFFFFF', justification='left',)]
    ]

    tab1_layout = [[sg.Column(coluna1_KPI, background_color='#FFFFFF', size=(w - (w * (1 / 3)), h), pad=((30,0), 3)),
                    sg.Column(coluna2_KPI, size=(w * (1 / 3), h), background_color='#FFFFFF', pad=(0,0))]
                   ]

    header, data = preenche_listbox()
    coluna1_Users = [
        [sg.Image('Images/logo.PNG', size=(80, 77), background_color='#FFFFFF', pad=(7, (3, 40))),
         sg.Text('Data Factory', font='Helvetica 24 bold italic', text_color='#7E7364', background_color='#FFFFFF', pad=(7, (3, 40)))],
        [sg.Text('Registration Number:', size=(16, 1), text_color='#000000', background_color='#FFFFFF'),
         sg.InputText('', size=(30, 6), background_color='#FFFFFF', border_width=1, key='-registration_number-'),
         sg.Image('Images/search.png', size=(16, 16), background_color='#FFFFFF', enable_events=True, key='-search-'),
         sg.Text('Acess Type:', size=(12, 1), background_color='#FFFFFF'),
         sg.Combo(['Common user', 'Admin'], key='-access_type-', size=(28, 6), background_color='#FFFFFF')],
        [sg.Text('Username:', size=(16, 1), text_color='#000000', background_color='#FFFFFF'),
         sg.InputText('', size=(30, 6), background_color='#FFFFFF', border_width=1, key='-username-'),
         sg.Text('Email:', size=(10, 1), text_color='#000000', background_color='#FFFFFF', pad=((31, 25), 3)),
         sg.InputText('', size=(30, 6), background_color='#FFFFFF', border_width=1, key='-email-')],
        [sg.Text('Industrial Site:', size=(16, 1), background_color='#FFFFFF'),
         sg.Combo(['CAJICA', 'ITATIAIA', 'RECIFE', 'RIO NEGRO'], default_value='', key='-SITE-', size=(29, 6),
                  background_color='#FFFFFF')],
        [sg.Text('Last modifications', size=(16, 1), text_color='#000000', background_color='#FFFFFF',
                 pad=(7, (35, 3)))],
        [sg.Table(values=data, headings=header, vertical_scroll_only=True, display_row_numbers=True,
                  col_widths=[15, 20, 20, 20], auto_size_columns=None, num_rows=min(17, 15),
                  size=(120, 15), header_background_color='#AB1717', header_text_color='#FFFFFF',
                  justification='left')],
        [sg.Button('Save', button_color='#AB1717', size=(10, 1), font='Helvetica 12 bold italic', pad=(7, 15))],
    ]

    coluna2_Users = [
        [sg.Text('Welcome ' + user.lower(), auto_size_text=True, background_color='#FFFFFF', text_color='#000000',
                 pad=((140, 0), 10)),
         sg.Image('Images/usuario.png', size=(32, 32), pad=((2, 0), 10), background_color='#FFFFFF')]
    ]

    tab2_layout = [[sg.Column(coluna1_Users, background_color='#FFFFFF', size=(w - (w * (1 / 3)), h), pad=(30, 3)),
                    sg.Column(coluna2_Users, size=(w * (1 / 3), h), background_color='#FFFFFF',
                              element_justification='right')]
                   ]


    tab3_layout = [[sg.Image('Images/logo.PNG', size=(80, 77), background_color='#FFFFFF', pad=((0,7),(10, 40))),
                    sg.Text('Data Factory', font='Helvetica 24 bold italic', text_color='#7E7364',
                            background_color='#FFFFFF',  pad=((7,590),(10, 40))),
                    sg.Text('KPI Name:', size=(9, 1), background_color='#FFFFFF'),
                    sg.Combo(combo_list, default_value='All', key='-KPI_NAME_DASHBOARD-',
                             size=(29, 6), background_color='#FFFFFF', enable_events=True)],
                   [sg.Text('', background_color='#FFFFFF')],
                   [sg.Canvas(key='-CANVAS-')],
                   ]

    layout = [[sg.TabGroup([[sg.Tab('Register KPI', tab1_layout, background_color='#FFFFFF', title_color='red'),
                             sg.Tab('Users', tab2_layout, background_color='#FFFFFF'),
                             sg.Tab('Dashboard', tab3_layout, background_color='#FFFFFF',
                                    element_justification='center')]], size=(w, h), border_width=0,
                           selected_background_color='#AB1717', selected_title_color='#FFFFFF')]]


    # Cria a janela
    return sg.Window('Administrator View', layout, size=(w, h), element_justification='left', font='Helvetica 12',
                     resizable=True, finalize=True, background_color='#FFFFFF', icon='Images/bar_icon.ico', margins=(0, 0))


def win_csv_file():
    left_col = [[sg.Text('Folder'), sg.In(size=(25,1), enable_events=True ,key='-FOLDER-'), sg.FolderBrowse('Browse')],
    [sg.Button('Save file', key='-salvar_local-')],
    [sg.Text('',text_color='blue', auto_size_text=True, key = '-confirm_save-')]]
    layout = [[sg.Column(left_col, element_justification='r')]]

    return sg.Window('Save csv file', layout, resizable=True, finalize=True)


def create_dashboard(kpi_dashboard, site, window):

    conexao = bd.retornar_conexao()  # alterar esta função para retornar a conexão e não o cursor
    inst_sql = 'SELECT _DATE, _SITE, _KPI, _TARGET, _VALUE, _USERNAME FROM TB_KPI'
    dfKPI = pd.read_sql(inst_sql, conexao)
    dfKPI['_VALUE'] = pd.to_numeric(dfKPI['_VALUE'], errors='coerce')

    if kpi_dashboard == 'All':
        dfKPI = dfKPI.loc[dfKPI['_SITE'] == site]
        data = dfKPI
    else:
        dfKPI = dfKPI.loc[dfKPI['_SITE'] == site]
        dfKPI = dfKPI.loc[dfKPI['_KPI'] == kpi_dashboard]
        data = dfKPI


    matplotlib.use('TkAgg')
    fig = plt.figure(figsize=(15,7))
    ax = sns.barplot(x=data['_DATE'], y=data['_VALUE'], palette='cool_r')
    ax.set_title('\n' + kpi_dashboard + '\n', fontdict={'fontsize':15})
    ax.set_ylabel('\n' +'KPI Value'+ '\n', fontdict={'fontsize':15})
    ax.set_xlabel('\n' + '' + '\n', fontdict={'fontsize': 15})
    y = [round(data['_VALUE'][x], 3)  if data['_VALUE'][x] < 0.9999 else round(data['_VALUE'][x], 1) for x in data.index]
    for i in range(len(y)):
        ax.text(i, y[i] + (y[i] * 0.01), str(y[i]),
                fontdict={'color': 'black', 'fontsize': 13},
                horizontalalignment='center')

    figure_canvas_agg = FigureCanvasTkAgg(fig,window['-CANVAS-'].TKCanvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
    return figure_canvas_agg


def main():
    win_login, win_cadastro, win_registro, win_admin, win_download = login(), None, None, None, None
    win_login.Maximize()

    while True:
        window, event, values = sg.read_all_windows()

        # Tratamento da tela de login

        if window == win_login:

            if event == sg.WIN_CLOSED or event == 'Cancel':
                win_login = None
                break

            elif event == 'Login' or event == 'Submit':

                # condição de admin ou usuário comum para fazer o desvio para a tela certa
                global user, site
                user = values['-user-'].upper()
                senha = values['-senha-']
                validacao_usuario = bd.login(user, senha)
                site = validacao_usuario[1]
                if (user and senha) != '':
                    if validacao_usuario[0] == 'ADMIN':
                        win_admin = win_administrador()
                        win_admin.Maximize()
                        win_login.close()
                        win_login = None

                    if validacao_usuario[0] == 'COMMON USER':
                        win_registro = registro_KPI()
                        win_registro.Maximize()
                        win_login.close()
                        win_login = None

                    if validacao_usuario[0] != 'ADMIN' and validacao_usuario[0] != 'COMMON USER':
                        sg.popup('Error', validacao_usuario[0], button_color='#AB1717', icon='Images/user_icon.ico')
                else:
                    sg.popup('Error', 'Verifique se os campos de "Login" e "Senha" foram preenchidos corretamente.',
                             button_color='#AB1717', icon='Images/user_icon.ico')

            elif event == 'Register':
                win_cadastro = cadastro()
                win_cadastro.Maximize()
                win_login.close()
                win_login = None

        # _______________________________________________________________________________________________________________________

        # Tratamento da tela de Cadastro

        if window == win_cadastro:
            if event == sg.WIN_CLOSED:
                win_cadastro = None
                break

            if event == '-register-':
                site_cad = values['-SITE-']
                user = values['-user-']
                pwd = values['-pass-']
                confirm_pwd = values['-confirm_pass-']
                rg = values['-rg-']
                email = values['-email-']
                dados_cadastro = [user, pwd, confirm_pwd, rg, email, site_cad]
                access_type = 'COMMON USER'
                count = 0
                if pwd != confirm_pwd:
                    window['-error-'].Update('* As senhas inseridas são diferentes. Tente novamente.')
                else:
                    for dado in dados_cadastro:
                        if dado == '':
                            count += 1

                    if count == 1:
                        window['-error-'].Update(f'* Resta {count} campo a ser preenchido')
                    if count > 1:
                        window['-error-'].Update(f'* Restam {count} campos a serem preenchidos')
                    elif count == 0:
                        cad = bd.insert_user(user, rg, email, pwd, access_type, site_cad)
                        sg.popup('ATENÇÂO', cad, button_color='#AB1717', icon='Images/user_icon.ico')
                        window['-error-'].Update('')

            if event == '-login-':
                win_cadastro.close()
                win_cadastro = None
                win_login = login()
                win_login.Maximize()
        # _______________________________________________________________________________________________________________________

        # Tratamento da tela de registro_KPI
        if window == win_registro:
            if event in (None, sg.WIN_CLOSED):
                win_cadastro = None
                break

            if event == '-KPI_NAME-':
                kpi = values['-KPI_NAME-']
                dados = filtra_KPI(kpi, site)
                win_registro['-Table-'].Update(dados)
                win_registro['-DATE-'].Update('')
                win_registro['-KPI_TARGET-'].Update('')
                win_registro['-KPI_VALUE-'].Update('')

            if event == 'mes':  # Usar isto para construir o calendário
                try:
                    my_date1 = sg.popup_get_date(location=(1080, 135))
                    my_date2 = f'{my_date1[2]}-{my_date1[0]}-{my_date1[1]}'
                    my_date3 = datetime.strptime(my_date2, '%Y-%m-%d').date()
                    win_registro['-DATE-'].Update(my_date3)
                except:
                    pass

            if event == '-download-':
                tabela = win_registro['-Table-'].Get()
                win_download = win_csv_file()
                janela = True
                folder = ''
                while janela == True:
                    event, values = win_download.read()

                    if event == '-FOLDER-':
                        folder = values['-FOLDER-']
                    if event == '-salvar_local-':
                        if folder in (None, '', 'Folder'):
                            win_download['-confirm_save-'].Update('Please, click on button "Browse" to chose a folder.')
                        else:
                            salvar = gera_relatorio(tabela, folder)
                            win_download['-confirm_save-'].Update(salvar)

                    if event in (None, sg.WIN_CLOSED):
                        win_download.close()
                        win_download = None
                        janela = False


        # Tratamento da tela de administrador

        if window == win_admin:
            if event in (None, sg.WIN_CLOSED):
                win_admin = None
                break

            if event == '-KPI_NAME-':
                kpi_table = values['-KPI_NAME-']
                dados = filtra_KPI(kpi_table, site)
                win_admin['-Table-'].Update(dados)
                win_admin['-DATE-'].Update('')
                win_admin['-KPI_TARGET-'].Update('')
                win_admin['-KPI_VALUE-'].Update('')

            if event == '-KPI_NAME_DASHBOARD-':
                global var_aux
                if not var_aux:
                    kpi_dashboard = values['-KPI_NAME_DASHBOARD-']
                    fig_canvas_agg = create_dashboard(kpi_dashboard, site, win_admin)
                    var_aux = True
                else:
                    kpi_dashboard = values['-KPI_NAME_DASHBOARD-']
                    fig_canvas_agg.get_tk_widget().forget()
                    fig_canvas_agg = create_dashboard(kpi_dashboard, site, win_admin)

            if event == '-search-':
                try:
                    retorno = list(bd.busca_usuario(values['-registration_number-']))
                    win_admin['-username-'].Update(retorno[0])
                    win_admin['-SITE-'].Update(retorno[1])
                    win_admin['-access_type-'].Update(retorno[2])
                    win_admin['-email-'].Update(retorno[3])
                except:
                    sg.popup('Not Found', 'Usuário não encontrado. Tente novamente!', button_color='#AB1717', icon='Images/user_icon.ico')

            if event == 'mes':  # Usar isto para construir o calendário
                try:
                    my_date1 = sg.popup_get_date(location=(1080, 135))
                    my_date2 = f'{my_date1[2]}-{my_date1[0]}-{my_date1[1]}'
                    my_date3 = datetime.strptime(my_date2, '%Y-%m-%d').date()
                    win_admin['-DATE-'].Update(my_date3)
                except:
                    pass
            ###############-PRECISO FAZER ESSA PARTE PARA O USUÁRIO SIMPLES-#################
            if event == '-download-':
                tabela = win_admin['-Table-'].Get()
                win_download = win_csv_file()
                janela = True
                folder = ''
                while janela == True:
                    event, values = win_download.read()

                    if event == '-FOLDER-':
                        folder = values['-FOLDER-']
                    if event == '-salvar_local-':
                        if folder in (None, '', 'Folder'):
                            win_download['-confirm_save-'].Update('Please, click on button "Browse" to chose a folder.')
                        else:
                            salvar = gera_relatorio(tabela, folder)
                            win_download['-confirm_save-'].Update(salvar)

                    if event in (None, sg.WIN_CLOSED):
                        win_download.close()
                        win_download = None
                        janela = False
            
            if event == '-Table-':
                data = win_admin[event].Get()
                data_selected = [data[row] for row in values[event]]
                win_admin['-DATE-'].Update(data_selected[0][0])
                win_admin['-KPI_NAME-'].Update(data_selected[0][2])
                win_admin['-KPI_TARGET-'].Update(data_selected[0][3])
                win_admin['-KPI_VALUE-'].Update(data_selected[0][4])

if __name__ == '__main__':
    main()
