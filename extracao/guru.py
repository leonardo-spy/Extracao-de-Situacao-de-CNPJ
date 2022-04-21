import requests
from time import sleep
from main import key_guru

'''
Variaveis Globais do Guru
'''

#url_guru_requisicao = "https://api.captcha.guru/in.php?key="+key_guru
def url_guru_requisicao():
    return "https://api.captcha.guru/in.php?key="+key_guru
#url_guru_resposta = "https://api.captcha.guru/res.php?key="+key_guru+"&action=get&id="
def url_guru_resposta():
    return "https://api.captcha.guru/res.php?key="+key_guru+"&action=get&id="
'''
Metodos do Guru
Aquisicao e Verificao
'''

'''
Funcao Que envia uma aquisicao para o Guru responder o captcha
'''
def aquisicao(metodo,url_receita):
    id_guru = ""
    with requests.get(url = url_guru_requisicao()+metodo+url_receita,timeout=30) as r:
        if(r.status_code == 200):            
            resultado = r.text.split('|')
            if resultado[0] == 'OK':
                id_guru = resultado[1]
            else:
                print("Erro: "+str(r.text)) 
    return id_guru

'''
Funcao Que envia uma aquisicao para verificar a solucao do captcha do Guru
'''
def verificao(id_guru):
    id_captcha = ""
    if id_guru != "":
        while True:
                id_captcha = ""
                with requests.get(url = url_guru_resposta()+id_guru, timeout=30) as r:
                    if(r.status_code == 200):
                        if(r.text != "CAPCHA_NOT_READY"):
                            resultado = r.text.split('|')
                            if resultado[0] == 'OK':
                                id_captcha = resultado[1]
                            #print(r.text)
                            break
                sleep(3)
    return id_captcha

def resolveCaptchaImg(img_bytes):
    #img_bytes = img_bytes.decode()
    files = {'file': img_bytes}
    data = {'key': key_guru, 'method': 'post'}
    r = requests.post('http://api.captcha.guru/in.php', files=files, data=data)
    if r.ok and r.text.find('OK') > -1:
        reqid = r.text[r.text.find('|')+1:]
        for timeout in range(40):
            r = requests.get('http://api.captcha.guru/res.php?key='+key_guru+'&action=get&id='+reqid)
            if r.text.find('CAPCHA_NOT_READY') > -1:
                sleep(3)
            if r.text.find('ERROR') > -1:
                return [False,r.text]
            if r.text.find('OK') > -1:
                txt_captcha = r.text[r.text.find('|')+1:]
                if len(txt_captcha) == 6:
                    return [True,txt_captcha]
                else:
                    return [False,'Captcha não completo: '+txt_captcha]
    return [False,'']