# Desafio RPA – SIDRA/IBGE – Tabela 1209

Automação desenvolvida em Python com Playwright para acessar o SIDRA/IBGE pela interface do site, localizar a Tabela 1209 e baixar os dados de população com 60 anos ou mais por Unidade da Federação.

## Objetivo

A automação:

- acessa `https://sidra.ibge.gov.br/`;
- utiliza a pesquisa do próprio SIDRA para localizar a tabela 1209;
- abre a tabela por meio da interface;
- seleciona as faixas etárias `60 a 69 anos` e `70 anos ou mais`;
- seleciona o ano de 2022;
- remove a seleção agregada de Brasil;
- seleciona todas as Unidades da Federação;
- escolhe o formato CSV (BR);
- realiza o download;
- cria automaticamente a pasta `dados`;
- salva o arquivo como:

```text
dados/populacao_60mais_1209.csv
```

## Tecnologias

- Python 3
- Playwright
- Chromium

## Instalação

### 1. Criar ambiente virtual

No Windows:

```bash
py -m venv .venv
```

### 2. Ativar o ambiente virtual

Git Bash:

```bash
source .venv/Scripts/activate
```

PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 3. Instalar dependências

```bash
pip install -r requirements.txt
```

### 4. Instalar o Chromium utilizado pelo Playwright

```bash
python -m playwright install chromium
```

## Execução

Com o ambiente virtual ativo:

```bash
python desafio_ibge_1209.py
```

Ao finalizar, o arquivo será salvo em:

```text
dados/populacao_60mais_1209.csv
```

## Estratégia da automação

A solução não acessa diretamente a URL da tabela 1209. A automação inicia na página principal do SIDRA e utiliza o mecanismo de pesquisa disponibilizado pela própria interface.

Os elementos são localizados principalmente por atributos estáveis, textos e estados de acessibilidade, evitando seletores dependentes de posições fixas na página.

Para os controles de seleção do SIDRA, a automação verifica o atributo `aria-selected` antes de clicar. Dessa forma, evita alternar acidentalmente uma opção que já esteja no estado desejado.

O download é capturado pelo Playwright com `expect_download()`. O SIDRA pode entregar o arquivo com um nome interno em formato UUID; por isso, após a captura, o arquivo é salvo explicitamente como `dados/populacao_60mais_1209.csv`.

## População com 60 anos ou mais

Na Tabela 1209, a população com 60 anos ou mais é apresentada em duas faixas:

```text
60 a 69 anos
70 anos ou mais
```

Por esse motivo, a automação seleciona ambas para representar a população de 60 anos ou mais.

## Ano utilizado

Foi utilizado o ano de 2022, disponível na tabela 1209 como período recente.

## Tratamento de erros

A automação possui:

- esperas explícitas para carregamento e visibilidade dos elementos;
- validação de estados antes de selecionar ou desmarcar filtros;
- tratamento de timeout;
- validação do download;
- criação automática da pasta de saída;
- verificação de existência e tamanho do CSV gerado.

## Estrutura do projeto

```text
desafio-ibge-1209/
├── desafio_ibge_1209.py
├── requirements.txt
├── README.md
├── .gitignore
└── dados/
    └── populacao_60mais_1209.csv
```

## Observações

A automação utiliza apenas interações com a interface web do SIDRA/IBGE. Não é utilizada API REST para obtenção dos dados e a tabela não é acessada diretamente por URL.
