<div align="center">

**FACULDADE ESTADUAL DO PIAÚI INSTITUTO DE TECNOLOGIA - PIT**

</div>

                                                            
-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
Professora: Evelyn Karinne

Aluno: Joabe Carvalho Neco e Silva 

Aluno: Pedro Rodrigues de Amorim Neto 

Aluno: Luis Carlos Barbosa de Almeida

<div align="center">
  
  **Projeto em Python + Streamlit relativo a 4ª avaliação da disciplina de Algoritmos e Lógica de Programação**
</div


Projeto de controle de estoque usando a metodologia CRUD: 

Create (Criar);

Read (Ler);

Update (Atualizar);

Delete (Deletar) 

e o framework Streamlit para interface do usuário.  



**Linguagem e ferramentas utilizadas:**


Python

JSON

Git/GitHub

Streamlit

Claude(Antrophic)

**------estoque.py---------**

Criamos a função mostrar 'mostrar_estoque', utilizada para receber os dados do estoque.padrao e, com eles, chamar no arquivo principal(main.py).

As funções 'salvar_estoque', 'carregar_estoque' são usadas para salvar os dados do estoque disposto no 'estoque_padrao' e, caso não existir o arquivo.json no diretório, ele cria um arquivo com o estoque padrão.

A função 'adicionar_item' serve para adicionar e atualizar, caso o item já existida.

Por fim, a função 'remover_item' é empregada para remover items do estoque.json.

**------main.py------**

O arquivo 'main.py' é responsável por chamar todas funções definidas no arquivo 'estoque.py'. Além disso, foi criado uma interface intuitiva, amigável e organizada, utilizando técnicas de estilização como '<20' para centralizar a direita e 'center:' para centralizar.

**------estoque.json------** O estoque.json é criado a partir da execução do programa, servindo para armazenar. de forma permanente, os dados recebido pelo programa. É usado, como um banco de dados, sendo útil para inserir, visualizar, atualizar e deletar dados de um programa CRUD, por exemplo.


**Streamlit Interface:**

Usamos a Inteligência Artificial da Antrophic, **Claude** para transformar o sistema de controle de estoque, que antes era um sistema de linha de comando, em uma interface intuitiva, utilizando ícones da biblioteca Material Symbols(Biblioteca externa do Google de ícones).

**Prompt 01:** 

"Quero transformar meu sistema de gerenciamento de estoque feito em Python (terminal) em uma aplicação web usando Streamlit.

Atualmente o projeto possui dois arquivos:

* `estoque.py` → contém as funções de manipulação dos dados e salvamento em JSON.
* `main.py` → contém o menu interativo do terminal.

### O que deve ser feito

#### 1. Migrar a interface para Streamlit

Remova todas as interações de terminal, como:

* `input()`
* `print()`
* `sleep()`
* códigos de cores ANSI (`\033`)

Substitua por componentes do Streamlit, como:

* `st.sidebar`
* `st.dataframe`
* `st.selectbox`
* `st.text_input`
* `st.number_input`
* `st.button`
* `st.success`
* `st.warning`

---

#### 2. Utilizar IDs únicos para os produtos

Atualmente os produtos são armazenados usando o nome como chave.

Altere para utilizar IDs automáticos, seguindo o formato:

```json
{
    "1": {
        "nome": "arroz",
        "preco": 25.9,
        "quantidade": 50
    },
    "2": {
        "nome": "feijão",
        "preco": 8.5,
        "quantidade": 80
    }
}
```

Quando um novo produto for criado:

* descobrir o maior ID existente;
* gerar o próximo ID automaticamente.

---

#### 3. Criar alerta de estoque baixo

Sempre que um produto tiver menos de 10 unidades em estoque, exibir um aviso visual utilizando `st.warning()`.

Esse aviso deve aparecer na tela de visualização do estoque.

---

#### 4. Utilizar Session State

Use `st.session_state` para manter os dados carregados do JSON durante a navegação da aplicação.

---

### Estrutura esperada

#### Arquivo `estoque.py`

Criar ou adaptar as funções:

* `carregar_estoque()`
* `salvar_estoque()`
* `adicionar_item(nome, preco, quantidade)`
* `remover_item(id_produto)`

Regras:

* Se o JSON não existir, criar um estoque inicial com IDs.
* Se o produto já existir, atualizar seus dados.
* Se for um produto novo, criar um novo ID automaticamente.
* A remoção deve ser feita pelo ID.

---

#### Arquivo `app.py`

Criar uma interface Streamlit com menu lateral contendo:

*  Visualizar Estoque
*  Adicionar/Atualizar Produto
*  Remover Produto

##### Tela: Visualizar Estoque

* Mostrar todos os produtos em uma tabela.
* Mostrar avisos de estoque baixo.

##### Tela: Adicionar/Atualizar Produto

* Permitir selecionar um produto existente para edição.
* Ter a opção "[Novo Produto]" para cadastrar um novo item.
* Preencher os campos automaticamente ao editar.

##### Tela: Remover Produto

* Mostrar os produtos em um `selectbox`.
* Exibir os produtos no formato:

```
ID - Nome
```

* Solicitar confirmação antes da exclusão.

---

Forneça o código completo e organizado dos arquivos `estoque.py` e `app.py`, prontos."



**Prompt 02:**

*"Para estilização do sistema coloque alguns elementos visuais, criando um padrão visual usando a biblioteca Material Design do Google"*

**Features adicionadas**

-Aplicação Web

-Produtos com estoque baixo

-Menu interativo com ícones

-Diferentemente do nosso código que quando adicionava um novo produto, o novo item ficava em uma posição alfabética na tabela, o novo código agora é por ID e não por nome do produto, o novo produto vai para o final da tabela e não fica em ordem alfabética.



**Referência Bibliográfica:**

PYTHON SOFTWARE FOUNDATION - Codificador e decodificador JSON. Python 3 Documentation 2024 Disponível em: https://docs.python.org/pt-br/3/library/json.html#module-json.

Manipulação de Arquivo JSON em Python Disponível em: https://www.youtube.com/watch?v=Cp3tWEXwrTc&t=90s.

PYTHON SOFTWARE FOUNDATION. os.path — Manipulações comuns de nomes de caminho. Python 3 Documentation, 2024. Disponível em: https://docs.python.org/pt-br/3/library/os.path.html#module-os.path.

CRUD: o que é e como funciona?: https://blog.geekhunter.com.br/crud/

Inteligência Artificial da Antropich - Claude em: claude.ai

Cores no Terminal https://www.youtube.com/watch?v=0hBIhkcA8O8

