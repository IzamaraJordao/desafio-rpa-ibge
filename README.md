# Desafio RPA — SIDRA/IBGE

Automação para extrair a população de 60 anos ou mais por Unidade da Federação da tabela 1209 do SIDRA/IBGE. Inclui uma API para executar o robô e uma dashboard para visualizar os dados.

[![Assistir à apresentação do projeto no YouTube](https://img.youtube.com/vi/vKQyV7TydxY/hqdefault.jpg)](https://youtu.be/vKQyV7TydxY)

Clique para assistir à apresentação.

## Dependências necessárias

- **Ambiente:** Windows, Python 3 e acesso à internet. Para API e dashboard, Node.js 22.12 ou superior e npm.
- **Automação:** Playwright e Chromium. A dependência Python está em `requirements.txt`.
- **API:** Express, CORS, TypeScript e tsx.
- **Dashboard:** React, TypeScript, Vite, Papa Parse, Recharts e React Toastify.

As dependências da API e da dashboard estão nos respectivos arquivos `package.json` e são instaladas com `npm ci`.

## Passo a passo de execução

### 1. Preparar o ambiente Python

No terminal, na raiz do projeto:

```terminal
python -m venv .venv
.venv/Scripts/python.exe -m pip install -r requirements.txt
.venv/Scripts/python.exe -m playwright install chromium
```

### 2. Executar a automação

```terminal
.venv/Scripts/python.exe desafio_ibge_1209.py
```

Acrescente `--headless` para executar sem janela. O CSV é salvo em `dados/populacao_60mais_1209.csv`. A pasta é criada automaticamente e uma nova coleta substitui o arquivo anterior.

### 3. Executar os testes automatizados (opcional)

Após gerar o CSV pelo menos uma vez (passo 2), valide o arquivo com os testes de `tests/test_csv.py`:

```terminal
.venv/Scripts/python.exe -m unittest discover -s tests
```

### 4. Iniciar a API e a dashboard (opcional)

Em um novo terminal, a partir da raiz do projeto, inicie a API:

```terminal
cd api
npm ci
npm start
```

A API fica disponível em `http://localhost:3333`. Em outro terminal, também a partir da raiz, inicie a dashboard:

```terminal
cd dashboard
npm ci
npm run dev
```

Abra o endereço exibido pelo Vite. O botão **Atualizar dados do IBGE** executa a automação e recarrega os dados. Mantenha os dois terminais abertos e execute uma coleta por vez.

## Estratégia adotada

A automação inicia em `https://sidra.ibge.gov.br/`, abre a busca interna e acessa a tabela 1209 pelo resultado. Seleciona exclusivamente as faixas **60 a 69 anos** e **70 anos ou mais**, o ano mais recente listado e as **27 UFs**, desmarcando o agregado Brasil.

A coleta usa cliques e esperas explícitas do Playwright, sem consultar a API REST do SIDRA, abrir diretamente a URL da tabela ou alterar o DOM manualmente. O download é solicitado pela interface e o CSV é validado quanto ao ano, às faixas etárias, aos valores e aos territórios.

A dashboard lê o CSV, soma as duas faixas por UF e apresenta os totais em cartões, gráfico e ranking com busca. A API local apenas inicia o processo Python e retorna o resultado da execução.

## Principais desafios encontrados

- **Localizar os elementos do SIDRA:**: a tabela precisava ser descoberta pela interface. Foram usados textos, atributos e papéis de acessibilidade para identificar a pesquisa e seus resultados, evitando coordenadas fixas na tela.consulta `aria-selected`, mantém as opções desejadas e remove as demais da mesma lista, conferindo o estado final
- **Garantir filtros exclusivos:**: clicar em uma opção já selecionada pode desmarcá-la. A automação consulta `aria-selected`, mantém as opções desejadas e remove as demais da mesma lista, conferindo o estado final.
- **Separar e validar os dados:**: o CSV inclui títulos, cabeçalhos, fonte e notas. A validação identifica o bloco das UFs e rejeita valores inválidos, duplicatas, territórios extras ou unidades ausentes. Os testes automatizados cobrem esses cenários.
