import json
import requests

URL = 'https://api.codenation.dev/v1/challenge/dev-ps/generate-data'
MEU_TOKEN = '5860dbfd272c62443befc9e3de1fafb87a9e3f80'
PARAMS = {'token': MEU_TOKEN}

# requisição http dos dados necessários:
resposta = requests.get (url = URL, params = PARAMS) # enviando GET e salvando objeto do tipo Response
dicionario = resposta.json () # convertendo Response em dicionário

# extração de dados do dicionário:
TEXTO_CIFRADO = dicionario ['cifrado']
CHAVE = dicionario ['numero_casas']

# códigos importantes da tabela ASCII:
LETRA_A = 97
LETRA_Z = 122
ESPACO = 32
PONTO = 46

cifradosASCII = None
decifradosASCII = None
textoDecifrado = ''

# composição do texto decifrado:
for i in TEXTO_CIFRADO:

    cifradosASCII = ord (i) # código ASCII representando um caractere de TEXTO_CIFRADO

    if cifradosASCII == ESPACO or cifradosASCII == PONTO:
        decifradosASCII = cifradosASCII

    elif cifradosASCII < LETRA_A + CHAVE:
        decifradosASCII = (LETRA_Z + 1) - (LETRA_A - (cifradosASCII - CHAVE))

    else:
        decifradosASCII = cifradosASCII - CHAVE
    
    textoDecifrado = textoDecifrado + chr (decifradosASCII)

# criação do resumo criptográfico sha1:
from hashlib import sha1
resumoCriptografico = sha1 (textoDecifrado.encode ('utf-8')).hexdigest ()

# atualização de dados no dicionário:
dicionario ['resumo_criptografico'] = resumoCriptografico
dicionario ['decifrado'] = textoDecifrado

strJSON = json.dumps (dicionario) # conversão de dict para JSON string

# criação do arquivo answer.json:
with open ('answer.json', 'w') as arquivoJson:
    arquivoJson.write (strJSON)

# envio do arquivo multipart/form-data (como se enviado por formulário HTML)
# com um campo do tipo file com o nome answer:
ARQUIVO = {'answer': open('answer.json', 'rb')}
URL_PARA_ENVIO = "https://api.codenation.dev/v1/challenge/dev-ps/submit-solution"

r = requests.post (url = URL_PARA_ENVIO, params = PARAMS, files = ARQUIVO) # dando POST e salvando objeto do tipo Response

# extracting response text  
pastebin_url = r.text 
print("The pastebin URL is:%s"%pastebin_url)
print (r)