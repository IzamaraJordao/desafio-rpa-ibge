import contextlib
import csv
import io
import tempfile
import unittest
from pathlib import Path

from desafio_ibge_1209 import PASTA_DADOS, validar_csv


class ValidacaoCsvTest(unittest.TestCase):
    def setUp(self):
        with (PASTA_DADOS / "populacao_60mais_1209.csv").open(encoding="utf-8-sig", newline="") as f:
            self.linhas = list(csv.reader(f, delimiter=";"))
        self.indice = next(i for i, linha in enumerate(self.linhas) if linha == [
            "Unidade da Federação", "60 a 69 anos", "70 anos ou mais"
        ])

    def validar(self, ano=None):
        with tempfile.TemporaryDirectory() as pasta:
            caminho = Path(pasta) / "dados.csv"
            with caminho.open("w", encoding="utf-8", newline="") as f:
                csv.writer(f, delimiter=";").writerows(self.linhas)
            with contextlib.redirect_stdout(io.StringIO()):
                validar_csv(caminho, ano)

    def test_csv_original(self):
        self.validar(self.linhas[self.indice - 1][1])

    def test_rejeita_uf_duplicada(self):
        self.linhas.insert(self.indice + 1, self.linhas[self.indice + 1][:])
        with self.assertRaisesRegex(ValueError, "duplicada"):
            self.validar()

    def test_rejeita_territorio_extra(self):
        self.linhas.insert(self.indice + 1, ["Brasil", "1", "2"])
        with self.assertRaisesRegex(ValueError, "Território"):
            self.validar()

    def test_rejeita_faixa_extra(self):
        self.linhas[self.indice].append("Total")
        with self.assertRaisesRegex(ValueError, "exclusivamente"):
            self.validar()

    def test_rejeita_ano_incorreto(self):
        with self.assertRaisesRegex(ValueError, "Ano do CSV"):
            self.validar("1900")

    def test_rejeita_valor_indisponivel(self):
        self.linhas[self.indice + 1][1] = "..."
        with self.assertRaisesRegex(ValueError, "inválidos"):
            self.validar()

    def test_rejeita_uf_ausente(self):
        del self.linhas[self.indice + 1]
        with self.assertRaisesRegex(Exception, "incompleto"):
            self.validar()

    def test_aceita_zero_absoluto(self):
        self.linhas[self.indice + 1][1] = "-"
        self.validar()
