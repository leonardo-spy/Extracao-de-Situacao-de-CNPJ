import pandas as pd
import extracao.guru as guru
import extracao.receita as receita

from threading import Lock, Thread
from time import sleep,time
import os
import sys
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)



''' tipo de captcha 0 = Google, 1 = hCaptcha, 2 = IMG captcha'''
tipo_cap = 2

''' Chave de autentificação da API do Guru '''
key_guru = ""

''' Quantidade maxima de requisicoes de documentos no site da guru e da receita '''
numero_instancia_max = 135 

numero_instancia = 0

''' numero de tentativas maxima em um documento que falhou '''
tentativa_maxima = 3 

''' segundos que espera para poder processar o documento denovo '''
tempo_espera = 90

documentos_list=[]
documentos_dados = []

def consulta_direto():
    for arquivo in os.listdir('./planilhas'):
        if not arquivo.startswith("ID") and not arquivo.startswith("$RECYCLE.BIN") and not arquivo.endswith(".csv"):
            try:
                print(f"Preparando arquivo: {arquivo} ...")
                documentos_excel = pd.read_excel("./planilhas/"+arquivo,header=None,usecols=[0])
                print(f"Arquivo: {arquivo} sendo processado!")
                documentos_excel = documentos_excel.drop_duplicates(subset =0, keep='first')
                documentos_para_processar = []
                for linha in documentos_excel.values:
                    if  linha[0] != "" and linha[0] != None and linha[0] == linha[0]:
                        documentos_para_processar.append(linha[0])
                if len(documentos_para_processar)>0:
                    print(f"Processando {str(len(documentos_para_processar))} documento(s) !")
                    dados_receita = gerenciar_macros(documentos_para_processar,True)
                    print(f"Finalizando o arquivo {arquivo} !")
                    planilha_dados = pd.DataFrame(dados_receita)
                    documentos_excel = documentos_excel.rename(columns={0:'documento'})
                    planilha_dados = planilha_dados.rename(columns={0:'documento'})
                    planilha_novo_dados = documentos_excel[['documento']].merge(planilha_dados[['documento',1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27]],on = 'documento', how = "left")
                    planilha_novo_dados.to_excel("./finalizado/"+arquivo,index = False,header =["Documento","Número de Inscrição","Tipo de Número de Inscrição","Data de Abertura","Nome Empresarial","Título do Estabelecimento (Nome Fantasia)","Porte","Código e Descrição de Atividade Econômica Principal","Código e Descrição das Atividades Econômicas Secundárias (1)","Código e Descrição das Atividades Econômicas Secundárias (2)","Código e Descrição das Atividades Econômicas Secundárias (3)","Código e Descrição das Atividades Econômicas Secundárias (4)","Código e Descrição da natureza Jurídica","Logradouro","Número","Complemento","CEP","Bairro/Distrito","Município","UF","E-mail","Telefone","Ente Federativo Responsável (EFR)","Situação Cadastral","Data da Situação Cadastral","Motivo de Situação Cadastral","Situação Especial","Data da Situação Especial"])
                    os.remove("./planilhas/"+arquivo)
                    print(f"Todos os {str(len(documentos_para_processar))} documento(s) do arquivo {arquivo} foram processado!")
                else:
                    print("Não há documento para processar no arquivo "+str(arquivo)) 
            except Exception as e:
                    print("Arquivo "+str(arquivo)+" invalido! Erro: "+str(e)) 


def gerenciar_macros(documentos=[],completo=False):
    #colocar um for para adicionar um espaço no array de cada documento como None q ser usado para o tempo
    # verificar se o tempo é none ou se ja faz 1 min com o lock para verificao e lock para adicao de tempo no array tmb
    global numero_instancia_max 
    global documentos_list

    for documento in documentos:
        documentos_list.append([documento,None,0])

    atualizar_contagem()

    while (True in [True if y[0]!="" and y[2]<tentativa_maxima else False for y in documentos_list]):
        for i,documento in enumerate(documentos_list):
            with Lock():
                global numero_instancia            
                if (numero_instancia < numero_instancia_max):
                    if ((documento[1] == None or time() -documento[1]>=tempo_espera) and documento[0]!="" and documento[2]<tentativa_maxima):
                        documentos_list[i][1] = time()
                        numero_instancia+= 1
                        Thread(target=gerenciar_documento,name="doc"+str(documento)+' key:'+str(i), args=(i,documento[0],completo)).start()
                else:
                    sleep(5)
        if not(True in [True if y[0]!="" and y[2]<tentativa_maxima else False for y in documentos_list]):
            break

        if not(False in [True if y[1] != None and time() -y[1]>=tempo_espera and numero_instancia < numero_instancia_max else False for y in documentos_list]):
            sleep(5)
        elif numero_instancia >= numero_instancia_max:
            sleep(1)
    return documentos_dados

def gerenciar_documento(key,documento,completo):
    id_captcha = None
    if tipo_cap == 0:
        id_guru = guru.aquisicao("&method=userrecaptcha&googlekey=6LcT2zQUAAAAABRp8qIQR2R0Y2LWYTafR0A8WFbr&pageurl=",receita.url_receita)
    elif tipo_cap == 1:
        id_guru = guru.aquisicao("&method=hcaptcha&sitekey=af4fc5a3-1ac5-4e6d-819d-324d412a5e9d&pageurl=",receita.url_receita)
    if tipo_cap != 2:
        id_captcha = guru.verificao(id_guru) 

    if id_captcha != None or tipo_cap == 2:
        dados = receita.gerenciamento_receita(documento,id_captcha,completo)
    with Lock():
        global documentos_list
        if (id_captcha != None or tipo_cap == 2) and dados != None:
            documentos_list[key][0] = ""
            global documentos_dados
            documentos_dados.append(dados)
            atualizar_contagem()
        else:            
            documentos_list[key][2]+= 1
            if documentos_list[key][2] == tentativa_maxima:
                if completo == True:
                    documentos_dados.append([documento,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None,None])
                else:
                    documentos_dados.append([documento,None,None,None,None,None])
        global numero_instancia
        numero_instancia-= 1

def atualizar_contagem():
    processados = sum([True if y[0]=="" or y[2]>=(tentativa_maxima-1) else False for y in documentos_list])
    sys.stdout.write ("Documentos Processados %s/%s \r" % (str(processados),str(len(documentos_list))))
    sys.stdout.flush()

def main():
    print("Inicializando...")
    
    consulta_direto()

    sys.exit()
                

'''Main do código'''
if __name__ == "__main__":
    pd.set_option('max_row', None)
    if not os.path.exists("./planilhas/"):
        os.makedirs("./planilhas/")
    if not os.path.exists("./finalizado/"):
        os.makedirs("./finalizado/")
    main()

