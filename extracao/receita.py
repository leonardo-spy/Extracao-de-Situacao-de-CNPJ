import requests
from bs4 import BeautifulSoup

'''
Variaveis Globais do Guru
'''
headers_receita = {
    "Content-Type": "application/x-www-form-urlencoded",
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36 Edg/91.0.864.59",
    "content-length":None
}
url_receita = "http://servicos.receita.fazenda.gov.br/Servicos/cnpjreva/Cnpjreva_Solicitacao.asp"
url_receita_valida = "http://servicos.receita.fazenda.gov.br/Servicos/cnpjreva/valida_recaptcha.asp"

'''
Metodos do Guru
Acessar Receita e Validação na Receita
'''

'''
Funcao Que acessa a pagina da Receita para a captura do cookie
'''
def acessar_receita(s):
    cookies_receita = None
    try:
        with s.get(url = url_receita, headers=headers_receita,verify=False,timeout=30) as r:
            cookies_receita = r.cookies
    except Exception as e:
        print("Erro ao Acessa a Receita! Erro: "+str(e))
    return cookies_receita

'''
Funcao Que acessa a pagina de validação da Receita para prosseguir com a requisição e capturar os dados
'''
def validacao_receita(s,cookies_receita,documento,id_captcha,completo):
    from main import tipo_cap
    resultado = None
    #cnpj = str(str(documento).split('.')[0])
    #if len(cnpj) < 14:
        #cnpj = cnpj.zfill(14)
    #cnpj = '{}.{}.{}/{}-{}'.format(cnpj[:2], cnpj[2:5], cnpj[5:8], cnpj[8:12],cnpj[12:])
    cnpj = documento
    if tipo_cap==0:
        myobj = {'origem':'comprovante','cnpj': cnpj,'g-recaptcha-response':id_captcha,'search_type':'cnpj'}
    elif tipo_cap==1:
        myobj = {'origem':'comprovante','cnpj': cnpj,'h-captcha-response':id_captcha,'search_type':'cnpj'}
    #TODO: Fazer uma funcao para substitui os codigos abaixo
    try:
        with s.post(url = url_receita_valida,data = myobj, headers=headers_receita,verify=False,allow_redirects=True,cookies=cookies_receita,timeout=30) as r:
            soup = BeautifulSoup(r.text, 'lxml')
            div_principal = soup.find("div", {'id': 'principal'})
            if completo == True:
                try:
                    div_filhos = div_principal.find_all('table',recursive = False)[0].find('tr',recursive = False).find('td',recursive = False)
                except (IndexError,AttributeError) as ee :
                    print("Não foi possivel localizar o parametro principal da pagina da receita no documento "+str(cnpj)+" ! código do erro:"+str(ee))
                    return resultado
                try:
                    numero_inscricao = div_filhos.find_all('table',recursive = False)[1].find('tr',recursive = False).find_all('td',recursive = False)[0].find_all('font',recursive = False)[1].find_all('b',recursive = False)[0].text
                    numero_inscricao = numero_inscricao.replace('\n', '').replace('\r', '').replace('\t', '')
                except (IndexError,AttributeError) as eee :
                    numero_inscricao = None
                    pass
                try:
                    numero_inscricao_tipo = div_filhos.find_all('table',recursive = False)[1].find('tr',recursive = False).find_all('td',recursive = False)[0].find_all('font',recursive = False)[1].find_all('b',recursive = False)[1].text
                    numero_inscricao_tipo = numero_inscricao_tipo.replace('\n', '').replace('\r', '').replace('\t', '')
                except (IndexError,AttributeError) as eee :
                    numero_inscricao_tipo = None
                    pass
                try:
                    data_abertura = div_filhos.find_all('table',recursive = False)[1].find('tr',recursive = False).find_all('td',recursive = False)[2].find_all('font',recursive = False)[1].find('b',recursive = False).text
                    data_abertura = data_abertura.replace('\n', '').replace('\r', '').replace('\t', '')
                except (IndexError,AttributeError) as eee :
                    data_abertura = None
                    pass
                try:
                    nome_empresarial = div_filhos.find_all('table',recursive = False)[2].find('tr',recursive = False).find('td',recursive = False).find_all('font',recursive = False)[1].find('b',recursive = False).text
                    nome_empresarial = nome_empresarial.replace('\n', '').replace('\r', '').replace('\t', '')
                except (IndexError,AttributeError) as eee :
                    nome_empresarial = None
                    pass
                try:
                    nome_fantasia = div_filhos.find_all('table',recursive = False)[3].find('tr',recursive = False).find_all('td',recursive = False)[0].find_all('font',recursive = False)[1].find('b',recursive = False).text
                    nome_fantasia = nome_fantasia.replace('\n', '').replace('\r', '').replace('\t', '')
                except (IndexError,AttributeError) as eee :
                    nome_fantasia = None
                    pass
                try:
                    porte = div_filhos.find_all('table',recursive = False)[3].find('tr',recursive = False).find_all('td',recursive = False)[2].find_all('font',recursive = False)[1].find('b',recursive = False).text
                    porte = porte.replace('\n', '').replace('\r', '').replace('\t', '')
                except (IndexError,AttributeError) as eee :
                    porte = None
                    pass
                try:
                    codigo_atividade_principal = div_filhos.find_all('table',recursive = False)[4].find('tr',recursive = False).find('td',recursive = False).find_all('font',recursive = False)[1].find('b',recursive = False).text
                    codigo_atividade_principal = codigo_atividade_principal.replace('\n', '').replace('\r', '').replace('\t', '')
                except (IndexError,AttributeError) as eee :
                    codigo_atividade_principal = None
                    pass
                try:
                    codigo_atividade_secundaria_1 = div_filhos.find_all('table',recursive = False)[5].find('tr',recursive = False).find('td',recursive = False).find_all('font',recursive = False)[1].find('b',recursive = False).text
                    codigo_atividade_secundaria_1 = codigo_atividade_secundaria_1.replace('\n', '').replace('\r', '').replace('\t', '')
                except (IndexError,AttributeError) as eee :
                    codigo_atividade_secundaria_1 = None
                    pass
                try:
                    codigo_atividade_secundaria_2 = div_filhos.find_all('table',recursive = False)[5].find('tr',recursive = False).find('td',recursive = False).find_all('font',recursive = False)[2].find('b',recursive = False).text
                    codigo_atividade_secundaria_2 = codigo_atividade_secundaria_2.replace('\n', '').replace('\r', '').replace('\t', '')
                except (IndexError,AttributeError) as eee :
                    codigo_atividade_secundaria_2 = None
                    pass
                try:
                    codigo_atividade_secundaria_3 = div_filhos.find_all('table',recursive = False)[5].find('tr',recursive = False).find('td',recursive = False).find_all('font',recursive = False)[3].find('b',recursive = False).text
                    codigo_atividade_secundaria_3 = codigo_atividade_secundaria_3.replace('\n', '').replace('\r', '').replace('\t', '')
                except (IndexError,AttributeError) as eee :
                    codigo_atividade_secundaria_3 = None
                    pass
                try:
                    codigo_atividade_secundaria_4 = div_filhos.find_all('table',recursive = False)[5].find('tr',recursive = False).find('td',recursive = False).find_all('font',recursive = False)[4].find('b',recursive = False).text
                    codigo_atividade_secundaria_4 = codigo_atividade_secundaria_4.replace('\n', '').replace('\r', '').replace('\t', '')
                except (IndexError,AttributeError) as eee :
                    codigo_atividade_secundaria_4 = None
                    pass
                try:
                    codigo_natureza  = div_filhos.find_all('table',recursive = False)[6].find('tr',recursive = False).find('td',recursive = False).find_all('font',recursive = False)[1].find('b',recursive = False).text
                    codigo_natureza = codigo_natureza.replace('\n', '').replace('\r', '').replace('\t', '')
                except (IndexError,AttributeError) as eee :
                    codigo_natureza = None
                    pass
                try:
                    logradouro = div_filhos.find_all('table',recursive = False)[7].find('tr',recursive = False).find_all('td',recursive = False)[0].find_all('font',recursive = False)[1].find('b',recursive = False).text
                    logradouro = logradouro.replace('\n', '').replace('\r', '').replace('\t', '')
                except (IndexError,AttributeError) as eee :
                    logradouro = None
                    pass
                try:
                    numero = div_filhos.find_all('table',recursive = False)[7].find('tr',recursive = False).find_all('td',recursive = False)[2].find_all('font',recursive = False)[1].find('b',recursive = False).text
                    numero = numero.replace('\n', '').replace('\r', '').replace('\t', '')
                except (IndexError,AttributeError) as eee :
                    numero = None
                    pass
                try:
                    complemento = div_filhos.find_all('table',recursive = False)[7].find('tr',recursive = False).find_all('td',recursive = False)[4].find_all('font',recursive = False)[1].find('b',recursive = False).text
                    complemento = complemento.replace('\n', '').replace('\r', '').replace('\t', '')
                except (IndexError,AttributeError) as eee :
                    complemento = None
                    pass
                try:
                    cep = div_filhos.find_all('table',recursive = False)[8].find('tr',recursive = False).find_all('td',recursive = False)[0].find_all('font',recursive = False)[1].find('b',recursive = False).text
                    cep = cep.replace('\n', '').replace('\r', '').replace('\t', '')
                except (IndexError,AttributeError) as eee :
                    cep = None
                    pass
                try:
                    bairro = div_filhos.find_all('table',recursive = False)[8].find('tr',recursive = False).find_all('td',recursive = False)[2].find_all('font',recursive = False)[1].find('b',recursive = False).text
                    bairro = bairro.replace('\n', '').replace('\r', '').replace('\t', '')
                except (IndexError,AttributeError) as eee :
                    bairro = None
                    pass
                try:
                    municipio = div_filhos.find_all('table',recursive = False)[8].find('tr',recursive = False).find_all('td',recursive = False)[4].find_all('font',recursive = False)[1].find('b',recursive = False).text
                    municipio = municipio.replace('\n', '').replace('\r', '').replace('\t', '')
                except (IndexError,AttributeError) as eee :
                    municipio = None
                    pass
                try:
                    uf = div_filhos.find_all('table',recursive = False)[8].find('tr',recursive = False).find_all('td',recursive = False)[6].find_all('font',recursive = False)[1].find('b',recursive = False).text
                    uf = uf.replace('\n', '').replace('\r', '').replace('\t', '')
                except (IndexError,AttributeError) as eee :
                    uf = None
                    pass
                try:
                    email = div_filhos.find_all('table',recursive = False)[9].find('tr',recursive = False).find_all('td',recursive = False)[0].find_all('font',recursive = False)[1].find('b',recursive = False).text
                    email = email.replace('\n', '').replace('\r', '').replace('\t', '')
                except (IndexError,AttributeError) as eee :
                    email = None
                    pass
                try:
                    telefone = div_filhos.find_all('table',recursive = False)[9].find('tr',recursive = False).find_all('td',recursive = False)[2].find_all('font',recursive = False)[1].find('b',recursive = False).text
                    telefone = telefone.replace('\n', '').replace('\r', '').replace('\t', '')
                except (IndexError,AttributeError) as eee :
                    telefone = None
                    pass
                try:
                    efr = div_filhos.find_all('table',recursive = False)[10].find('tr',recursive = False).find('td',recursive = False).find_all('font',recursive = False)[1].find('b',recursive = False).text
                    efr = efr.replace('\n', '').replace('\r', '').replace('\t', '')
                except (IndexError,AttributeError) as eee :
                    efr = None
                    pass
                try:
                    situacao_cadastral = div_filhos.find_all('table',recursive = False)[11].find('tr',recursive = False).find_all('td',recursive = False)[0].find_all('font',recursive = False)[1].find('b',recursive = False).text
                    situacao_cadastral = situacao_cadastral.replace('\n', '').replace('\r', '').replace('\t', '')
                except (IndexError,AttributeError) as eee :
                    situacao_cadastral = None
                    pass
                try:
                    data_situacao_cadastral = div_filhos.find_all('table',recursive = False)[11].find('tr',recursive = False).find_all('td',recursive = False)[2].find_all('font',recursive = False)[1].find('b',recursive = False).text
                    data_situacao_cadastral = data_situacao_cadastral.replace('\n', '').replace('\r', '').replace('\t', '')
                except (IndexError,AttributeError) as eee :
                    data_situacao_cadastral = None
                    pass
                try:
                    motivo_situacao_cadastral = div_filhos.find_all('table',recursive = False)[12].find('tr',recursive = False).find('td',recursive = False).find_all('font',recursive = False)[1].find('b',recursive = False).text
                    motivo_situacao_cadastral = motivo_situacao_cadastral.replace('\n', '').replace('\r', '').replace('\t', '')
                except (IndexError,AttributeError) as eee :
                    motivo_situacao_cadastral = None
                    pass
                try:
                    situacao_especial = div_filhos.find_all('table',recursive = False)[13].find('tr',recursive = False).find_all('td',recursive = False)[0].find_all('font',recursive = False)[1].find('b',recursive = False).text
                    situacao_especial = situacao_especial.replace('\n', '').replace('\r', '').replace('\t', '')
                except (IndexError,AttributeError) as eee :
                    situacao_especial = None
                    pass
                try:
                    data_situacao_especial = div_filhos.find_all('table',recursive = False)[13].find('tr',recursive = False).find_all('td',recursive = False)[2].find_all('font',recursive = False)[1].find('b',recursive = False).text
                    data_situacao_especial = data_situacao_especial.replace('\n', '').replace('\r', '').replace('\t', '')
                except (IndexError,AttributeError) as eee :
                    data_situacao_especial = None
                    pass
                resultado = [documento,numero_inscricao,numero_inscricao_tipo,data_abertura,nome_empresarial,nome_fantasia,porte,codigo_atividade_principal,codigo_atividade_secundaria_1,codigo_atividade_secundaria_2,codigo_atividade_secundaria_3,codigo_atividade_secundaria_4,codigo_natureza,logradouro,numero,complemento,cep,bairro,municipio,uf,email,telefone,efr,situacao_cadastral,data_situacao_cadastral,motivo_situacao_cadastral,situacao_especial,data_situacao_especial]
            else:
                try:
                    div_filhos = div_principal.find_all('table',recursive = False)[0].find('tr',recursive = False).find('td',recursive = False)
                except (IndexError,AttributeError) as ee :
                    print("Não foi possivel localizar o parametro principal da pagina da receita no documento "+str(cnpj)+" ! código do erro:"+str(ee))
                    return resultado
                try:
                    nome_empresarial = div_filhos.find_all('table',recursive = False)[2].find('tr',recursive = False).find('td',recursive = False).find_all('font',recursive = False)[1].find('b',recursive = False).text
                    nome_empresarial = nome_empresarial.replace('\n', '').replace('\r', '').replace('\t', '')
                except (IndexError,AttributeError) as eee :
                    nome_empresarial = None
                    pass
                try:
                    nome_fantasia = div_filhos.find_all('table',recursive = False)[3].find('tr',recursive = False).find_all('td',recursive = False)[0].find_all('font',recursive = False)[1].find('b',recursive = False).text
                    nome_fantasia = nome_fantasia.replace('\n', '').replace('\r', '').replace('\t', '')
                except (IndexError,AttributeError) as eee :
                    nome_fantasia = None
                    pass
                try:
                    natureza_juridica = div_filhos.find_all('table',recursive = False)[6].find('tr',recursive = False).find('td',recursive = False).find_all('font',recursive = False)[1].find('b',recursive = False).text
                    natureza_juridica = natureza_juridica.replace('\n', '').replace('\r', '').replace('\t', '')
                except (IndexError,AttributeError) as eee :
                    natureza_juridica = None
                    pass
                try:
                    email = div_filhos.find_all('table',recursive = False)[9].find('tr',recursive = False).find_all('td',recursive = False)[0].find_all('font',recursive = False)[1].find('b',recursive = False).text
                    email = email.replace('\n', '').replace('\r', '').replace('\t', '')
                except (IndexError,AttributeError) as eee :
                    email = None
                    pass
                try:
                    telefone = div_filhos.find_all('table',recursive = False)[9].find('tr',recursive = False).find_all('td',recursive = False)[2].find_all('font',recursive = False)[1].find('b',recursive = False).text
                    telefone = telefone.replace('\n', '').replace('\r', '').replace('\t', '')
                except (IndexError,AttributeError) as eee :
                    telefone = None
                    pass
                #nomes.append([documento,nome_empresarial,nome_fantasia,natureza_juridica,email,telefone])
                resultado = [documento,nome_empresarial,nome_fantasia,natureza_juridica,email,telefone]
    except Exception as e:
        print("Erro ao Capturar os dados na Receita! Erro: "+str(e)) 
    return resultado

def gerenciamento_receita(documento,id_captcha,completo):
    resultado_dados= None
    s = requests.Session()
    s.headers.update(headers_receita)
    cookies_receita = acessar_receita(s)
    if cookies_receita != None:
        resultado_dados = validacao_receita(s,cookies_receita,documento,id_captcha,completo)
    return resultado_dados