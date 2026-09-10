# Desafio RPA — SIDRA/IBGE

Automação em Python e Playwright para extrair a população de 60 anos ou mais por UF da tabela 1209. Inclui uma API Express para executar o robô e uma dashboard React para visualizar os dados.

## Instalação e execução

Requisitos: Windows, Python 3. Para a API e a dashboard, Node.js 22.12 ou superior e npm.

No PowerShell, na raiz do projeto:

```powershell
py -m venv .venv
.venv/Scripts/python.exe -m pip install -r requirements.txt
.venv/Scripts/python.exe -m playwright install chromium
.venv/Scripts/python.exe desafio_ibge_1209.py
```

Use `--headless` para executar sem janela. O resultado é salvo em `dados/populacao_60mais_1209.csv`; a pasta é criada automaticamente e o arquivo é substituído a cada execução.

## API e dashboard opcionais

Após preparar o Python, execute em dois terminais na raiz do projeto:

**API** — disponível em `http://localhost:3333`:

```powershell
npm.cmd --prefix api ci
npm.cmd --prefix api start
```

**Dashboard** — abra o endereço exibido pelo Vite:

```powershell
npm.cmd --prefix dashboard ci
npm.cmd --prefix dashboard run dev
```

O botão **Atualizar dados do IBGE** executa o robô e recarrega o CSV. Mantenha a API ativa e execute uma coleta por vez. O build estático inclui uma cópia do CSV e precisa ser reconstruído após novas coletas.

## Estratégia

O robô parte da página inicial do SIDRA, encontra a tabela pela busca interna e seleciona as faixas **60 a 69 anos** e **70 anos ou mais**, o ano mais recente listado e as **27 UFs**. Baixa o CSV pela interface e valida ano, faixas, valores e territórios.

A coleta utiliza cliques e esperas explícitas, sem consultar a API REST do SIDRA ou abrir diretamente a URL da tabela.
Apos a coleta os dados sao tratados e enviados a dashboard para analise detalhada.

## Principais desafios

- **Localizar os elementos pela interface:**: A automação identifica o botão de pesquisa, o campo de busca e o resultado por textos, atributos e papéis de acessibilidade, evitando depender de coordenadas na tela.
- **Lidar com carregamentos assíncronos:**: os resultados e filtros nem sempre aparecem assim que a página abre. Foram usadas esperas explícitas para aguardar os elementos antes de interagir, com limites de tempo para sinalizar falhas de carregamento.
- **Garantir os filtros corretos:** :clicar em uma opção já selecionada pode desmarcá-la. O robô consulta `aria-selected`, seleciona as opções desejadas e remove as demais da mesma lista, verificando o estado final
- **Validar o conteúdo do CSV:** :o arquivo inclui título, cabeçalhos, fonte e notas além dos dados, foi uma dificuldade para separar cada um.

## Verificações

Na raiz do projeto:

```powershell
.venv/Scripts/python.exe -B -m unittest discover -s tests
npm.cmd --prefix api run typecheck
npm.cmd --prefix dashboard run lint
npm.cmd --prefix dashboard run build
```
