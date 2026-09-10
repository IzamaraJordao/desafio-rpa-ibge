import re
from pathlib import Path
import csv

from playwright.sync_api import (
    sync_playwright,
    expect,
    TimeoutError as PlaywrightTimeoutError,
)


URL_INICIAL = "https://sidra.ibge.gov.br/"
PASTA_DADOS = Path(__file__).resolve().parent / "dados"


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
    abrir_campo_busca(page)
    campo = page.locator(
        "#sidra-pesquisa-lg input[type='text']:visible, "
        "#sidra-pesquisa-lg input[type='search']:visible"
    ).first
    campo.wait_for(state="visible", timeout=15000)
    return campo


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
    resultado = page.get_by_role("link", name=re.compile(r"\b1209\b"))
    resultado = resultado.or_(page.get_by_role(
        "link", name=re.compile("População, por grupos de idade", re.IGNORECASE)
    )).or_(page.get_by_text("População, por grupos de idade", exact=False)).or_(
        page.get_by_text("1209", exact=True)
    ).filter(visible=True).first
    resultado.wait_for(state="visible", timeout=30000)
    return resultado


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
    item = page.locator("div.item-lista").filter(
        has=page.get_by_text(texto, exact=True)
    ).first
    item.wait_for(state="attached", timeout=15000)
    item.scroll_into_view_if_needed()
    return item


def itens_do_filtro(page, texto):
    item = localizar_item_por_texto(page, texto)
    lista = item.locator(
        'xpath=ancestor::*[count(.//div[contains(concat(" ", normalize-space(@class), " "), " item-lista ")]) > 1][1]'
    )
    return lista.locator("div.item-lista")


def selecionar_exclusivamente(itens, desejados):
    nomes = [nome.strip() for nome in itens.locator("span.nome").all_text_contents()]
    faltantes = set(desejados) - set(nomes)
    if faltantes:
        raise ValueError(f"Opções não encontradas: {sorted(faltantes)}")

    for selecionar in (True, False):
        for i, nome in enumerate(nomes):
            desejado = nome in desejados
            if desejado != selecionar:
                continue
            botao = itens.nth(i).locator("button.sidra-toggle")
            estado = "true" if desejado else "false"
            if botao.get_attribute("aria-selected") != estado:
                botao.click()
            expect(botao).to_have_attribute("aria-selected", estado, timeout=10000)

    selecionados = itens.filter(
        has=itens.page.locator('button[aria-selected="true"]')
    ).locator("span.nome").all_text_contents()
    if {nome.strip() for nome in selecionados} != set(desejados):
        raise ValueError("A seleção final do filtro não corresponde ao solicitado.")


def configurar_grupo_idade(page):
    print("Configurando exclusivamente as faixas de 60 anos ou mais...")
    selecionar_exclusivamente(
        itens_do_filtro(page, "60 a 69 anos"),
        {"60 a 69 anos", "70 anos ou mais"},
    )


def encontrar_ano_mais_recente(page):
    nomes = page.locator("div.item-lista span.nome").filter(
        has_text=re.compile(r"^\d{4}$")
    )
    nomes.first.wait_for(state="attached", timeout=15000)
    anos = [int(nome.strip()) for nome in nomes.all_text_contents()]
    return str(max(anos))


def configurar_ano(page):
    ano = encontrar_ano_mais_recente(page)
    selecionar_exclusivamente(itens_do_filtro(page, ano), {ano})
    print(f"Ano selecionado: {ano}")
    return ano


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

    pasta_dados = PASTA_DADOS
    pasta_dados.mkdir(
        parents=True,
        exist_ok=True,
    )

    destino = (
        pasta_dados
        / "populacao_60mais_1209.csv"
    )

    print("Procurando link final de Download...")

    confirmar_download = page.locator("a:visible").filter(
        has_text=re.compile(r"^\s*Download\s*$", re.IGNORECASE)
    ).first
    confirmar_download.wait_for(state="visible", timeout=30000)

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

    print("Download concluído.")

    print(
        "Arquivo:",
        destino.resolve(),
    )

    print(
        "Tamanho:",
        tamanho,
        "bytes",
    )

def validar_csv(caminho=None, ano_esperado=None):
    print("\nValidando arquivo CSV...")

    caminho = Path(caminho) if caminho else PASTA_DADOS / "populacao_60mais_1209.csv"

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

    cabecalho = ["Unidade da Federação", "60 a 69 anos", "70 anos ou mais"]
    if cabecalho not in linhas:
        raise ValueError("CSV deve conter exclusivamente as duas faixas de 60 anos ou mais.")
    indice = linhas.index(cabecalho)
    periodo = linhas[indice - 1] if indice else []
    if len(periodo) != 2 or not re.fullmatch(r"\d{4}", periodo[1]):
        raise ValueError("CSV deve conter exatamente um ano válido.")
    if ano_esperado is not None and periodo[1] != str(ano_esperado):
        raise ValueError(f"Ano do CSV difere do selecionado: {ano_esperado}.")

    for linha in linhas[indice + 1:]:
        if not linha or not any(linha):
            continue
        nome = linha[0].strip()
        if nome.startswith("Fonte:"):
            break
        if nome not in ufs_esperadas:
            raise ValueError(f"Território inesperado no CSV: {nome}")
        if nome in ufs_encontradas:
            raise ValueError(f"UF duplicada no CSV: {nome}")
        if len(linha) != 3 or not all(re.fullmatch(r"\d+|-", v) for v in linha[1:]):
            raise ValueError(f"Valores de população inválidos para {nome}.")
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

def executar(headless=False):

    with sync_playwright() as p:

        browser = p.chromium.launch(
            headless=headless,
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

            ano = configurar_ano(page)

            configurar_unidade_federacao(page)

            print(
                "\nFiltros configurados com sucesso."
            )

            baixar_csv(page)
            validar_csv(ano_esperado=ano)

            print(
                "Automação concluída."
            )


        except Exception as erro:


            print(
                "Erro na automação:"
            )


            print(erro)

            raise

        finally:

            browser.close()


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Extrai a população 60+ pela interface do SIDRA.")
    parser.add_argument("--headless", action="store_true", help="Executa sem abrir uma janela.")
    executar(headless=parser.parse_args().headless)
