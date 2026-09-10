# Desafio RPA — SIDRA/IBGE — Tabela 1209

Automação em Python com Playwright que navega pela interface do SIDRA, encontra a tabela 1209 e baixa a população de 60 anos ou mais por Unidade da Federação. A API e a dashboard são complementos opcionais; a entrega principal funciona pela linha de comando.

## Requisitos e instalação

- Python 3 e dependências de `requirements.txt`.
- Chromium instalado pelo Playwright e acesso à internet.
- Para API e dashboard: Node.js 22.12 ou superior e npm. A API está configurada para Windows, usando `.venv/Scripts/python.exe`.

No PowerShell, na raiz do projeto:

```powershell
py -m venv .venv
.venv/Scripts/python.exe -m pip install -r requirements.txt
.venv/Scripts/python.exe -m playwright install chromium
```

## Execução da automação

Na raiz do projeto:

```powershell
.venv/Scripts/python.exe desafio_ibge_1209.py
```

Para executar sem janela do navegador:

```powershell
.venv/Scripts/python.exe desafio_ibge_1209.py --headless
```

Com um ambiente virtual ativado, também é possível usar `python desafio_ibge_1209.py`. O navegador fecha ao concluir ou falhar; erros são exibidos no terminal e resultam em código de saída diferente de zero.

O arquivo é salvo em `dados/populacao_60mais_1209.csv`, relativo à pasta do script. A pasta é criada automaticamente. Uma nova execução substitui o arquivo anterior.

## Estratégia adotada

1. Abrir a página inicial `https://sidra.ibge.gov.br/`.
2. Abrir a pesquisa do SIDRA, buscar `1209` e clicar no resultado da tabela.
3. Selecionar exclusivamente `60 a 69 anos` e `70 anos ou mais`, verificando o estado dos botões após os cliques.
4. Identificar o maior ano exibido na lista e manter somente esse ano selecionado. O CSV incluído utiliza 2022; esse valor não está fixado no código.
5. Desmarcar Brasil e selecionar todas as Unidades da Federação.
6. Solicitar CSV (BR) pelo formulário de download e capturar o arquivo com `expect_download()`.
7. Validar o cabeçalho, o ano selecionado, os valores e a presença das 27 UFs, sem duplicatas ou territórios extras.

As duas faixas etárias juntas representam a população de 60 anos ou mais. A dashboard soma as duas colunas para calcular os totais.

A coleta não utiliza a API REST do SIDRA, acesso direto à URL da tabela ou alteração manual do DOM. Todas as mudanças de filtros são feitas por cliques na interface. Os seletores usam nomes, atributos e a estrutura das listas; as esperas explícitas aguardam os elementos relevantes, inclusive em carregamentos lentos.

## Principais desafios encontrados

- **Descobrir a tabela pela interface:** abrir a pesquisa e aguardar o resultado, mantendo a navegação a partir da página inicial.
- **Selecionar filtros sem inverter estados:** os botões usam `aria-selected`. A automação verifica o estado antes e depois do clique e remove seleções adicionais dentro da lista correspondente.
- **Representar a população 60+:** a tabela separa esse público em duas faixas, que precisam ser selecionadas juntas.
- **Lidar com carregamento assíncrono:** uma consulta imediata pode retornar zero elementos antes de o resultado aparecer. As buscas aguardam explicitamente sua disponibilidade.
- **Capturar o download:** o nome interno do arquivo pode diferir do solicitado. O arquivo é salvo explicitamente no caminho exigido.
- **Validar o CSV do SIDRA:** há metadados, fonte e notas além dos dados. A validação identifica o cabeçalho e verifica apenas o bloco de UFs, rejeitando filtros ou valores inesperados.

Mudanças futuras na interface do SIDRA podem exigir atualização dos seletores. Se a tabela mudar de formato, a validação falhará para evitar aceitar silenciosamente um arquivo diferente do esperado.

## API e dashboard opcionais

Prepare o ambiente Python acima. Em um terminal na raiz:

```powershell
cd api
npm.cmd ci
npm.cmd start
```

A API inicia em `http://localhost:3333`. `GET /health` verifica sua disponibilidade; `POST /executar-rpa` inicia o script Python e responde ao terminar. Essa API local apenas executa o robô; ela não consulta a API REST do SIDRA.

Em outro terminal, na raiz:

```powershell
cd dashboard
npm.cmd ci
npm.cmd run dev
```

Abra o endereço exibido pelo Vite. A dashboard lê o CSV de `dados/`, configurado como diretório público. O botão **Atualizar dados do IBGE** executa o robô pela API e recarrega o CSV ao concluir. Mantenha ambos os terminais em execução e use a automação por vez, pois as execuções escrevem no mesmo arquivo.

O build estático copia o CSV disponível naquele momento; para visualizar atualizações feitas pelo robô, utilize o servidor de desenvolvimento. Um build já gerado precisa ser reconstruído para incluir um CSV novo.

## Verificações

```powershell
.venv/Scripts/python.exe -B -c "from desafio_ibge_1209 import validar_csv; validar_csv()"
.venv/Scripts/python.exe -B -m unittest discover -s tests
cd api
npm.cmd run typecheck
cd ../dashboard
npm.cmd run lint
npm.cmd run build
```

## Estrutura e entrega

```text
desafio-rpa-ibge/
|-- desafio_ibge_1209.py
|-- requirements.txt
|-- README.md
|-- .gitignore
|-- tests/
|-- dados/
|   `-- populacao_60mais_1209.csv
|-- api/
|   |-- server.ts
|   |-- tsconfig.json
|   `-- package.json
`-- dashboard/
    |-- src/
    |-- vite.config.ts
    `-- package.json
```

A entrega no GitHub deve incluir o código, os arquivos de configuração, os `package-lock.json`, este README e o CSV gerado. Ambientes virtuais, dependências instaladas, caches e builds são ignorados pelo Git.
