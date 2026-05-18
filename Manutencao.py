import dateutil.parser
import dateutil.relativedelta
from datetime import datetime

class Manutencao:
    item_manutencao = []
    
    def __init__(self, item_nome, data_ultima_revisao, periodicidade_meses, descricao="", responsavel=""):
        """
        Inicializa um item de manutenção
        
        Args:
            item_nome: Nome do item (ex: 'Filtro de água')
            data_ultima_revisao: Data da última revisão (formato DD/MM/YYYY)
            periodicidade_meses: Periodicidade em meses (ex: 3, 6, 12)
            descricao: Descrição da manutenção
            responsavel: Pessoa responsável pela manutenção
        """
        self.item_nome = item_nome
        self.data_ultima_revisao = data_ultima_revisao
        self.periodicidade_meses = periodicidade_meses
        self.descricao = descricao
        self.responsavel = responsavel
        
    def registrar_manutencao(self):
        """Registra o item de manutenção na lista"""
        item = {
            'item_nome': self.item_nome,
            'data_ultima_revisao': self.data_ultima_revisao,
            'periodicidade_meses': self.periodicidade_meses,
            'descricao': self.descricao,
            'responsavel': self.responsavel
        }
        Manutencao.item_manutencao.append(item)
        print(f"✓ Manutenção de '{self.item_nome}' registrada com sucesso!")
        
    @staticmethod
    def calcular_proxima_revisao(data_ultima_revisao, periodicidade_meses):
        """
        Calcula a data da próxima revisão
        
        Args:
            data_ultima_revisao: Data da última revisão (formato DD/MM/YYYY)
            periodicidade_meses: Número de meses até a próxima revisão
            
        Returns:
            datetime object da próxima revisão
        """
        data = dateutil.parser.parse(data_ultima_revisao, dayfirst=True)
        proxima_data = data + dateutil.relativedelta.relativedelta(months=periodicidade_meses)
        return proxima_data
    
    @staticmethod
    def dias_para_revisao(proxima_data_revisao):
        """Calcula quantos dias faltam para a próxima revisão"""
        hoje = datetime.now()
        diferenca = proxima_data_revisao - hoje
        return diferenca.days
    
    @staticmethod
    def listar_manutencoes_pendentes():
        """Lista todas as manutenções vencidas ou vencendo"""
        print("\n" + "=" * 70)
        print("MANUTENÇÕES PENDENTES")
        print("=" * 70)
        
        manutencos_pendentes = []
        
        for item in Manutencao.item_manutencao:
            proxima_revisao = Manutencao.calcular_proxima_revisao(
                item['data_ultima_revisao'],
                item['periodicidade_meses']
            )
            dias_restantes = Manutencao.dias_para_revisao(proxima_revisao)
            
            if dias_restantes <= 0:
                manutencos_pendentes.append((item, proxima_revisao, dias_restantes))
        
        if not manutencos_pendentes:
            print("✓ Nenhuma manutenção pendente no momento!")
        else:
            for item, proxima_revisao, dias_restantes in sorted(manutencos_pendentes, key=lambda x: x[2]):
                print(f"\n⚠ Item: {item['item_nome']}")
                print(f"   Descrição: {item['descricao']}")
                print(f"   Última revisão: {item['data_ultima_revisao']}")
                print(f"   Periodicidade: {item['periodicidade_meses']} meses")
                print(f"   Próxima revisão: {proxima_revisao.strftime('%d/%m/%Y')}")
                print(f"   Status: VENCIDA ({abs(dias_restantes)} dias atrás)")
                print(f"   Responsável: {item['responsavel']}")
                print("-" * 70)
    
    @staticmethod
    def listar_manutencoes_este_mes():
        """Lista manutenções que precisam ser revisadas este mês"""
        print("\n" + "=" * 70)
        print("MANUTENÇÕES PROGRAMADAS PARA ESTE MÊS")
        print("=" * 70)
        
        hoje = datetime.now()
        primeiro_dia = datetime(hoje.year, hoje.month, 1)
        
        # Calcula o primeiro dia do próximo mês
        if hoje.month == 12:
            ultimo_dia = datetime(hoje.year + 1, 1, 1)
        else:
            ultimo_dia = datetime(hoje.year, hoje.month + 1, 1)
        
        manutencoes_mes = []
        
        for item in Manutencao.item_manutencao:
            proxima_revisao = Manutencao.calcular_proxima_revisao(
                item['data_ultima_revisao'],
                item['periodicidade_meses']
            )
            
            # Verifica se a próxima revisão cai neste mês
            if primeiro_dia <= proxima_revisao < ultimo_dia:
                dias_restantes = Manutencao.dias_para_revisao(proxima_revisao)
                manutencoes_mes.append((item, proxima_revisao, dias_restantes))
        
        if not manutencoes_mes:
            print("✓ Nenhuma manutenção programada para este mês!")
        else:
            for item, proxima_revisao, dias_restantes in sorted(manutencoes_mes, key=lambda x: x[2]):
                status = "URGENTE" if dias_restantes <= 7 else "PROGRAMADA"
                print(f"\n📅 Item: {item['item_nome']}")
                print(f"   Descrição: {item['descricao']}")
                print(f"   Última revisão: {item['data_ultima_revisao']}")
                print(f"   Periodicidade: {item['periodicidade_meses']} meses")
                print(f"   Próxima revisão: {proxima_revisao.strftime('%d/%m/%Y')}")
                print(f"   Dias restantes: {dias_restantes}")
                print(f"   Status: {status}")
                print(f"   Responsável: {item['responsavel']}")
                print("-" * 70)
    
    @staticmethod
    def listar_todas_manutencoes():
        """Lista todos os itens de manutenção com seus status"""
        print("\n" + "=" * 70)
        print("LISTA COMPLETA DE ITENS DE MANUTENÇÃO")
        print("=" * 70)
        
        if not Manutencao.item_manutencao:
            print("Nenhum item de manutenção registrado.")
            return
        
        for item in sorted(Manutencao.item_manutencao, key=lambda x: x['item_nome']):
            proxima_revisao = Manutencao.calcular_proxima_revisao(
                item['data_ultima_revisao'],
                item['periodicidade_meses']
            )
            dias_restantes = Manutencao.dias_para_revisao(proxima_revisao)
            
            # Determina status
            if dias_restantes < 0:
                status = f"VENCIDA ({abs(dias_restantes)} dias)"
                emoji = "🔴"
            elif dias_restantes <= 7:
                status = f"URGENTE ({dias_restantes} dias)"
                emoji = "🟡"
            else:
                status = f"OK ({dias_restantes} dias)"
                emoji = "🟢"
            
            print(f"\n{emoji} Item: {item['item_nome']}")
            print(f"   Descrição: {item['descricao']}")
            print(f"   Última revisão: {item['data_ultima_revisao']}")
            print(f"   Periodicidade: {item['periodicidade_meses']} meses")
            print(f"   Próxima revisão: {proxima_revisao.strftime('%d/%m/%Y')}")
            print(f"   Status: {status}")
            print(f"   Responsável: {item['responsavel']}")
            print("-" * 70)
    
    @staticmethod
    def registrar_revisao_realizada(item_nome):
        """Registra que uma revisão foi realizada e atualiza a data"""
        for item in Manutencao.item_manutencao:
            if item['item_nome'].lower() == item_nome.lower():
                data_atual = datetime.now().strftime("%d/%m/%Y")
                item['data_ultima_revisao'] = data_atual
                print(f"\n✓ Revisão do item '{item_nome}' registrada!")
                print(f"  Nova data de última revisão: {data_atual}")
                proxima = Manutencao.calcular_proxima_revisao(
                    item['data_ultima_revisao'],
                    item['periodicidade_meses']
                )
                print(f"  Próxima revisão programada para: {proxima.strftime('%d/%m/%Y')}")
                return
        print(f"✗ Item '{item_nome}' não encontrado para registrar revisão.")