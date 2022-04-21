# Extração da Situação cadastral do CNPJ na Receita

## Scrapping de CNPJ na Receita

Realiza o Scrapping automatizado das situações de CNPJ direto da Receita, formatando o resultado e gerando uma planilha com os documentos consultados!

## O que o projeto contém
- Request em Python
- Uso da biblioteca BeautifulSoup
- Uso da biblioteca Pandas para gerenciar planilhas de Excel
- Integração com a API do Guru Captcha

## Instalação
Para rodar o projeto faça essas configurações:
- Clone o projeto (utilizando comando git ou baixando em zip)
- Instale o Python (recomendado versão 3.8)
- Instale a biblioteca que se encontra em requirements
```
python -m pip install -U pip setuptools
python -m pip install --upgrade pip
pip install -r requirements.txt
```
Para alimentar a aplicação com documentos basta colocar um arquivo em formato Excel (.xlsx) na pasta **Planilhas** (a pasta é criada automaticamente ao executar a aplicação), nesse arquivo basta preencher os documentos na Coluna 'A' como no exemplo abaixo
```
00360305000104
00000000000191
```
![excel1](https://user-images.githubusercontent.com/19514153/164362213-cfa90056-6b11-4164-a9b7-805e549c37b3.png)

## Endpoints
Arquivo com os documentos inseridos preenchidos com a informação da Receita! Os arquivos gerados se encontram na pasta **Finalizado** com o mesmo nome do arquivo inicial com o cabeçalho do arquivo da seguinte maneira:
```
Documento | Número de Inscrição	| Tipo de Número de Inscrição	| Data de Abertura	| Nome Empresarial	| Título do Estabelicimento (Nome Fantasia) |	Porte	Código e Descrição de Atividade Econômica Principal	| Código e Descrição das Atividades Econômicas Secundárias (1) | Código e Descrição das Atividades Econômicas Secundárias (2) |	Código e Descrição das Atividades Econômicas Secundárias (3) | Código e Descrição das Atividades Econômicas Secundárias (4) | Código e Descrição da natureza Jurídica | Logradouro | Número | Complemento | CEP |	Bairro/Distrito |	Município |	UF | E-mail | Telefone | Ente Federativo Responsável (EFR) | Situação Cadastral | Data da Situação Cadastral | Motivo de Situação Cadastral | Situação Especial |	Data da Situação Especial
```
![image](https://user-images.githubusercontent.com/19514153/164363366-b0051788-8251-4d24-835e-8a875bbe18bd.png)
<br>
**No Console irar imprimir a situação do processo da execuçao da aplicacao!**
<br>
![excel2](https://user-images.githubusercontent.com/19514153/164363942-a34b7e0c-bb79-447c-bfcb-06fd23953ce6.png)
