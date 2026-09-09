import re
from pathlib import Path
import csv

from playwright.sync_api import (
    sync_playwright,
    TimeoutError as PlaywrightTimeoutError,
)


URL_INICIAL = "https://sidra.ibge.gov.br/"


def abrir_sidra(page):
    print("Abrindo SIDRA...")

    page.goto(
        URL_INICIAL,
        wait_until="domcontentloaded",
        timeout=30000,
    )

    try:
        page.wait_for_load_state(
            "networkidle",
            timeout=15000,
        )
    except PlaywrightTimeoutError:
        print("Página ainda possui carregamentos ativos.")

    print("SIDRA carregado com sucesso.")


def abrir_campo_busca(page):
    print("Procurando ícone de pesquisa...")

    lupa = page.locator(
        'a[title="Pesquisa Tabela"]'
        '[data-target="#sidra-pesquisa-lg"]'
    )

    lupa.wait_for(
        state="visible",
        timeout=10000,
    )

    print("Ícone de pesquisa encontrado.")

    lupa.click()

    print("Pesquisa aberta.")


def encontrar_campo_busca(page):
    print("Procurando campo de busca...")

    abrir_campo_busca(page)

    area_pesquisa = page.locator(
        "#sidra-pesquisa-lg"
    )

    area_pesquisa.wait_for(
        state="visible",
        timeout=10000,
    )

    estrategias = [
        area_pesquisa.locator("input[type='text']"),
        area_pesquisa.locator("input[type='search']"),
        area_pesquisa.get_by_role("textbox"),
        area_pesquisa.locator("input"),
    ]

    for campo in estrategias:
        try:
            if campo.count() > 0:
                primeiro = campo.first

                primeiro.wait_for(
                    state="visible",
                    timeout=5000,
                )

                print("Campo de busca encontrado.")

                return primeiro

        except Exception:
            continue

    raise Exception(
        "A área de pesquisa abriu, "
        "mas o campo de pesquisa não foi localizado."
    )


def pesquisar_tabela_1209(page):
    campo = encontrar_campo_busca(page)

    print("Pesquisando pela tabela 1209...")

    campo.click()
    campo.fill("1209")
    campo.press("Enter")

    try:
        page.wait_for_load_state(
            "networkidle",
            timeout=15000,
        )
    except PlaywrightTimeoutError:
        print(
            "Página ainda possui carregamentos ativos, "
            "continuando..."
        )

    print("Pesquisa enviada.")


def localizar_resultado_tabela(page):
    print("Procurando resultado da tabela 1209...")

    estrategias = [
        page.get_by_role(
            "link",
            name=re.compile(
                r"1209",
                re.IGNORECASE,
            ),
        ),

        page.locator("a").filter(
            has_text=re.compile(
                r"1209",
                re.IGNORECASE,
            )
        ),

        page.get_by_text(
            "População, por grupos de idade",
            exact=False,
        ),

        page.get_by_text(
            "1209",
            exact=False,
        ),
    ]

    for resultado in estrategias:
        try:
            if resultado.count() > 0:
                primeiro = resultado.first

                primeiro.wait_for(
                    state="visible",
                    timeout=5000,
                )

                if primeiro.is_visible():
                    print("Tabela 1209 encontrada.")

                    return primeiro

        except Exception:
            continue

    raise Exception(
        "Tabela 1209 não encontrada nos resultados."
    )


def acessar_tabela_1209(page):
    pesquisar_tabela_1209(page)

    resultado = localizar_resultado_tabela(page)

    print("Abrindo tabela 1209...")

    resultado.click()

    try:
        page.wait_for_load_state(
            "domcontentloaded",
            timeout=15000,
        )
    except PlaywrightTimeoutError:
        pass

    print("Tabela aberta.")
    print("URL atual:", page.url)


def localizar_item_por_texto(page, texto):
    item = page.locator(
        "div.item-lista"
    ).filter(
        has=page.get_by_text(
            texto,
            exact=True,
        )
    )

    if item.count() == 0:
        raise Exception(
            f"Item '{texto}' não encontrado."
        )

    item = item.first

    item.scroll_into_view_if_needed()

    return item


def selecionar_item_por_texto(page, texto):
    print(f"Selecionando: {texto}")

    item = localizar_item_por_texto(
        page,
        texto,
    )

    botao = item.locator(
        "button.sidra-toggle"
    )

    botao.wait_for(
        state="visible",
        timeout=10000,
    )

    selecionado = botao.get_attribute(
        "aria-selected"
    )

    if selecionado != "true":
        botao.click()

    print(f"{texto} selecionado.")


def desmarcar_item_por_texto(page, texto):
    print(f"Desmarcando: {texto}")

    item = localizar_item_por_texto(
        page,
        texto,
    )

    botao = item.locator(
        "button.sidra-toggle"
    )

    botao.wait_for(
        state="visible",
        timeout=10000,
    )

    selecionado = botao.get_attribute(
        "aria-selected"
    )

    if selecionado == "true":
        botao.click()

    print(f"{texto} desmarcado.")


def configurar_grupo_idade(page):
    print("\nConfigurando grupo de idade...")

    desmarcar_item_por_texto(
        page,
        "Total",
    )

    selecionar_item_por_texto(
        page,
        "60 a 69 anos",
    )

    selecionar_item_por_texto(
        page,
        "70 anos ou mais",
    )

    print(
        "Grupo de idade configurado "
        "para população com 60 anos ou mais."
    )


def encontrar_ano_mais_recente(page):
    print("Identificando o ano mais recente disponível...")

    # Procura os nomes dos itens da lista
    nomes = page.locator(
        "div.item-lista div.sidra-check span.nome"
    )

    anos = []

    for i in range(nomes.count()):
        nome = nomes.nth(i)

        try:
            texto = nome.inner_text().strip()

            # Só considera texto que seja exatamente um ano
            if re.fullmatch(r"\d{4}", texto):
                anos.append(int(texto))

        except Exception:
            continue

    if not anos:
        raise Exception(
            "Nenhum ano encontrado na lista de filtros."
        )

    ano_mais_recente = max(anos)

    print("Anos encontrados:", sorted(set(anos)))
    print(
        "Ano mais recente encontrado:",
        ano_mais_recente
    )

    return str(ano_mais_recente)



def configurar_ano(page):
    print("\nConfigurando ano...")

    ano_mais_recente = encontrar_ano_mais_recente(
        page
    )

    item_ano = localizar_item_por_texto(
        page,
        ano_mais_recente,
    )

    botao = item_ano.locator(
        "button.sidra-toggle"
    )

    botao.wait_for(
        state="visible",
        timeout=10000,
    )

    selecionado = botao.get_attribute(
        "aria-selected"
    )

    if selecionado != "true":
        botao.click()

    print(
        f"Ano {ano_mais_recente} selecionado."
    )

def configurar_unidade_federacao(page):
    print("\nConfigurando Unidade da Federação...")

    brasil = page.locator(
        'li[id^="arvore-"]'
    ).filter(
        has=page.get_by_text(
            "Brasil",
            exact=False,
        )
    ).first

    brasil.wait_for(
        state="visible",
        timeout=10000,
    )

    botao_brasil = brasil.locator(
        ":scope > div.item-arvore "
        "> div.nome-arvore "
        "> div.sidra-check "
        "> button.sidra-toggle"
    )

    botao_brasil.wait_for(
        state="visible",
        timeout=10000,
    )

    selecionado_brasil = (
        botao_brasil.get_attribute(
            "aria-selected"
        )
    )

    if selecionado_brasil == "true":
        print("Desmarcando Brasil...")
        botao_brasil.click()

    print("Brasil desmarcado.")

    uf = page.locator(
        'li[id^="arvore-"]'
    ).filter(
        has=page.get_by_text(
            "Unidade da Federação",
            exact=False,
        )
    ).first

    uf.wait_for(
        state="visible",
        timeout=10000,
    )

    uf.scroll_into_view_if_needed()

    print("Unidade da Federação encontrada.")

    botao_uf = uf.locator(
        ":scope > div.item-arvore "
        "> div.nome-arvore "
        "> div.sidra-check "
        "> button.sidra-toggle"
    )

    botao_uf.wait_for(
        state="visible",
        timeout=10000,
    )

    selecionado_uf = botao_uf.get_attribute(
        "aria-selected"
    )

    if selecionado_uf != "true":
        print("Selecionando todas as UFs...")
        botao_uf.click()

    print("Unidades da Federação selecionadas.")


def baixar_csv(page):
    print("\nIniciando download do CSV...")

    botao_download = page.get_by_role(
        "button",
        name="Download",
        exact=True,
    ).first

    botao_download.scroll_into_view_if_needed()
    botao_download.click()

    print("Janela de download aberta.")

    formulario = page.locator("#download-form")

    formulario.wait_for(
        state="visible",
        timeout=10000,
    )

    print("Formulário de download carregado.")

    formato = formulario.locator(
        'select[name="formato-arquivo"]'
    )

    formato.wait_for(
        state="visible",
        timeout=10000,
    )

    formato.select_option(value="br.csv")

    print(
        "Formato selecionado:",
        formato.input_value(),
    )

    nome_arquivo = formulario.locator(
        'input[name="nome-arquivo"]'
    )

    nome_arquivo.fill(
        "populacao_60mais_1209"
    )

    print("Nome do arquivo configurado.")

    pasta_dados = Path("dados")
    pasta_dados.mkdir(
        parents=True,
        exist_ok=True,
    )

    destino = (
        pasta_dados
        / "populacao_60mais_1209.csv"
    )

    print("Procurando link final de Download...")

    links_download = page.locator(
        "a"
    ).filter(
        has_text=re.compile(
            r"^\s*Download\s*$",
            re.IGNORECASE,
        )
    )

    confirmar_download = None

    for i in range(links_download.count()):

        link = links_download.nth(i)

        try:
            if link.is_visible():
                confirmar_download = link

                print(
                    "Link de Download encontrado."
                )

                print(
                    "href:",
                    link.get_attribute("href"),
                )

                print(
                    "class:",
                    link.get_attribute("class"),
                )

                break

        except Exception:
            continue

    if confirmar_download is None:
        raise Exception(
            "Não encontrei uma tag <a> visível "
            "com o texto Download."
        )

    print("Solicitando arquivo ao SIDRA...")

    with page.expect_download(
        timeout=60000,
    ) as download_info:

        confirmar_download.click()

    download = download_info.value

    download.save_as(
        str(destino)
    )

    if not destino.exists():
        raise Exception(
            "O arquivo não foi encontrado "
            "depois do download."
        )

    tamanho = destino.stat().st_size

    if tamanho == 0:
        raise Exception(
            "O arquivo foi criado, mas está vazio."
        )

    print("\n=================================")
    print("DOWNLOAD CONCLUÍDO COM SUCESSO!")
    print("=================================")

    print(
        "Arquivo:",
        destino.resolve(),
    )

    print(
        "Tamanho:",
        tamanho,
        "bytes",
    )

def validar_csv():
    print("\nValidando arquivo CSV...")

    caminho = Path(
        "dados/populacao_60mais_1209.csv"
    )

    if not caminho.exists():
        raise Exception(
            "CSV não encontrado para validação."
        )

    ufs_esperadas = {
        "Rondônia",
        "Acre",
        "Amazonas",
        "Roraima",
        "Pará",
        "Amapá",
        "Tocantins",
        "Maranhão",
        "Piauí",
        "Ceará",
        "Rio Grande do Norte",
        "Paraíba",
        "Pernambuco",
        "Alagoas",
        "Sergipe",
        "Bahia",
        "Minas Gerais",
        "Espírito Santo",
        "Rio de Janeiro",
        "São Paulo",
        "Paraná",
        "Santa Catarina",
        "Rio Grande do Sul",
        "Mato Grosso do Sul",
        "Mato Grosso",
        "Goiás",
        "Distrito Federal",
    }

    ufs_encontradas = set()

    with open(
        caminho,
        "r",
        encoding="utf-8-sig",
        newline="",
    ) as arquivo:

        leitor = csv.reader(
            arquivo,
            delimiter=";",
        )

        linhas = list(leitor)

    # Verifica as faixas etárias
    conteudo = str(linhas)

    if "60 a 69 anos" not in conteudo:
        raise Exception(
            "Faixa '60 a 69 anos' não encontrada."
        )

    if "70 anos ou mais" not in conteudo:
        raise Exception(
            "Faixa '70 anos ou mais' não encontrada."
        )

    # Procura as UFs
    for linha in linhas:

        if not linha:
            continue

        nome = linha[0].strip()

        if nome in ufs_esperadas:
            ufs_encontradas.add(nome)

    if len(ufs_encontradas) != 27:
        faltantes = (
            ufs_esperadas
            - ufs_encontradas
        )

        raise Exception(
            "CSV incompleto. "
            f"UFs encontradas: "
            f"{len(ufs_encontradas)}. "
            f"Faltantes: {faltantes}"
        )

    print("CSV validado com sucesso.")
    print(
        "UFs encontradas:",
        len(ufs_encontradas),
    )

    print(
        "Faixa 60 a 69 anos: OK"
    )

    print(
        "Faixa 70 anos ou mais: OK"
    )

def executar():

    with sync_playwright() as p:

        browser = p.chromium.launch(
            headless=False,
            slow_mo=250,
        )

        page = browser.new_page(
            viewport={
                "width": 1440,
                "height": 900,
            }
        )

        try:

            abrir_sidra(page)

            acessar_tabela_1209(page)

            print(
                "\nAguardando carregamento "
                "dos filtros da tabela..."
            )

            page.wait_for_selector(
                "div.item-lista",
                timeout=15000,
            )

            configurar_grupo_idade(page)

            configurar_ano(page)

            configurar_unidade_federacao(page)

            print(
                "\nFiltros configurados com sucesso."
            )

            baixar_csv(page)
            validar_csv()
            print(
                "\n================================="
            )

            print(
                "AUTOMAÇÃO CONCLUÍDA COM SUCESSO!"
            )

            print(
                "================================="
            )

            input(
                "\nPressione ENTER "
                "para fechar o navegador..."
            )

        except Exception as erro:

            print(
                "\n================================="
            )

            print(
                "ERRO NA AUTOMAÇÃO"
            )

            print(
                "================================="
            )

            print(erro)

            print(
                "\nO navegador ficará aberto "
                "para facilitar a análise."
            )

            input(
                "\nPressione ENTER "
                "para fechar..."
            )

        finally:

            browser.close()


if __name__ == "__main__":
    executar()