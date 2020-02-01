// fazer requisiçao http para a url abaixo
// https://api.codenation.dev/v1/challenge/dev-ps/generate-data?token=5860dbfd272c62443befc9e3de1fafb87a9e3f80

// o conteúdo da requisição deve ser salvo no arquivo answer.json

let obj = require ("./answer.json"); // criação de objeto literal a partir de arquivo JSON

const {cifrado: TEXTO_CIFRADO, numero_casas: CHAVE} = obj; // extração de dados do obj com destructuring

// códigos importantes da tabela ASCII:
const LETRA_A = 97;
const LETRA_Z = 122;
const ESPACO = 32;
const PONTO = 46;

let cifradosASCII = null;
let decifradosASCII = null;
let textoDecifrado = "";

// composição do texto decifrado:
for (var i = 0; i < TEXTO_CIFRADO.length; i++) {

	cifradosASCII = TEXTO_CIFRADO [i].charCodeAt () // código ASCII representando um caractere de TEXTO_CIFRADO

	if (cifradosASCII === ESPACO || cifradosASCII === PONTO) {
		decifradosASCII = cifradosASCII;
	} 
	else if (cifradosASCII < LETRA_A + CHAVE) { // caso o uso da chave gere um caracter indesejável
		decifradosASCII = (LETRA_Z + 1) - (LETRA_A - (cifradosASCII - CHAVE));
	} 
	else {
		decifradosASCII = cifradosASCII - CHAVE;
	}

	textoDecifrado = textoDecifrado + String.fromCharCode (decifradosASCII);
}

// criação do resumo criptográfico sha1:
const crypto = require('crypto')
  , shaUm = crypto.createHash('sha1');
shaUm.update(textoDecifrado);
let resumoCriptografico = shaUm.digest('hex');

 // atualização de dados no objeto literal:
obj.resumo_criptografico  = resumoCriptografico;
obj.decifrado = textoDecifrado;

strJSON = JSON.stringify (obj); // conversão do obj para JSON string

// atualização do arquivo answer.json:
let fs = require('fs');
fs.writeFile("answerJS.json", strJSON, err => {
    if (err) {
        console.log(err);
    }
});

// este programa deve submeter o arquivo JSON final
// via POST para a API:
// https://api.codenation.dev/v1/challenge/dev-ps/submit-solution?token=5860dbfd272c62443befc9e3de1fafb87a9e3f80

// obs: o arquivo JSON deve ser enviado como multipart/form-data, 
// como se fosse enviado por um formulário HTML, 
// com um campo do tipo file com o nome answer.