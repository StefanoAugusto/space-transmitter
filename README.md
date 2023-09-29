<h1 align="center">Space Transmitter</h1>
<h4 align="center"> :white_check_mark: Projeto Finalizado :white_check_mark:</h4>
O projeto Space Transmitter faz parte do processo avaliativo da disciplina de Cyber Security de Ciências da Computação - Atitus 2023/02, que é inclusa no bloco de Arquitetura de soluções em Cloud do curso. O projeto consiste em aplicar todos as metodologias ensinadas em sala de aula, buscando a melhora do algoritmo, devendo observar indicações da avaliação para o funcionamento<br><br>

<h2 align="center">
    <a>Instruções do Projeto</a>
</h2>
A aplicação é separada em dois pontos: cliente e servidor. O cliente é utilizado para o cadastro de Sondas e dados de localidades, bem como para o envio da chave pública da Sonda e assinatura de dados para o servidor. Enquanto o servidor é utilizado para receber os dados da Sonda e verificar a assinatura utilizando a chave pública da sonda enviada pelo cliente.
<h2 align="center"><a>Funcionalidades</a></h2>
<ul>
	<li> Menu de escolha entre as opções; </li>
	<li> Cadastro de Sondas; </li>
	<li> Listagem de Sondas cadastradas; </li>
	<li> Envio da chave pública para o servidor;</li>
	<li> Cadastro de dados em um arquivo criptografado (nome do local, temperatura e radiações); </li>
	<li> Assinatura dos dados; </li>
  <li> Envio dos dados assinados ao servidor; </li>
	<li> Verificação se assinatura é válida. </li>
</ul>
<br>
<h2 align="center">
	<a>Como executar o projeto</a>
</h2>
A aplicação deve ser executada baixando os arquivos do repositório e executar via prompt de comando. Para isso, é necessário ter a linguagem Python 3 e as bibliotecas pycryptodome, rsa instaladas. Para download da linguagem, <a href=https://www.python.org/>clique aqui</a>. Para instalar a biblioteca pycryptodome e rsa, é necessário ter o PIP instalado, sua instalação é feita junto com a linguagem Python. Além disso, é necessário executar o seguinte comando no prompt de comando:
<br><br>

```
 pip install pycryptodome
```
```
 pip install rsa
```
Para executar o projeto, é necessário abrir o prompt de comando dentro da pasta principal do projeto e executar os seguintes comandos:
<br>
```
 py mainServer.py
```
```
 py mainClient.py
```
<h2 align="center"><a>Autor</a></h2>
A solução foi criada por: <b>Stefano Augusto Mossi (Registro Acadêmico: 1131685)</b>.<br>
<br>
	
[![linkedin](https://img.shields.io/badge/linkedin-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://br.linkedin.com/in/stefano-augusto-mossi-6525aa217)
