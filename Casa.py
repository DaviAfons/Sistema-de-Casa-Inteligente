"""
SISTEMA DE CASA INTELIGENTE
Sistema integrado para gerenciar moradores, tarefas, manutenção,
compras, contas e estoque com persistência em JSON.
"""

import json
import os
from datetime import datetime
from Morador import Morador
from Tarefas import Tarefas
from Manutencao import Manutencao
from Compras import Compras
from Conta import Conta
from ItemEstoque import ItemEstoque
from RelatoriosEstatisticas import RelatoriosEstatisticas


class Casa:
    """Gerenciador principal da casa inteligente"""
    
    ARQUIVO_DADOS = "dados_casa.json"
    
    def __init__(self):
        """Inicializa a casa e carrega dados persistidos"""
        self.dados = {
            'moradores': [],
            'tarefas': [],
            'manutencoes': [],
            'compras': [],
            'contas': [],
            'estoque': [],
            'ultima_atualizacao': None
        }
        self.carregar_dados()
    
    def salvar_dados(self):
        """Salva todos os dados em JSON"""
        try:
            dados_json = {
                'moradores': Morador.moradores,
                'tarefas': Tarefas.tarefas,
                'manutencoes': Manutencao.item_manutencao,
                'compras': [
                    {
                        'nome': c.nome,
                        'quantidade': c.quantidade,
                        'categoria': c.categoria,
                        'preco_estimado': c.preco_estimado,
                        'comprado': c.comprado,
                        'unidade': c.unidade
                    } for c in Compras.lista_compras
                ],
                'contas': [
                    {
                        'descricao': c.descricao,
                        'valor': c.valor,
                        'data_vencimento': c.data_vencimento,
                        'categoria': c.categoria,
                        'status': c.status,
                        'data_criacao': c.data_criacao
                    } for c in Conta.contas
                ],
                'estoque': ItemEstoque.itens,
                'ultima_atualizacao': datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            }
            
            with open(self.ARQUIVO_DADOS, 'w', encoding='utf-8') as arquivo:
                json.dump(dados_json, arquivo, indent=4, ensure_ascii=False)
            
            print(f"✓ Dados salvos com sucesso em '{self.ARQUIVO_DADOS}'")
            return True
        except Exception as e:
            print(f"✗ Erro ao salvar dados: {e}")
            return False
    
    def carregar_dados(self):
        """Carrega dados do JSON se existir"""
        if not os.path.exists(self.ARQUIVO_DADOS):
            print(f"ℹ Arquivo '{self.ARQUIVO_DADOS}' não encontrado. Iniciando com dados vazios.")
            return False
        
        try:
            with open(self.ARQUIVO_DADOS, 'r', encoding='utf-8') as arquivo:
                dados_json = json.load(arquivo)
            
            # Carregar moradores
            Morador.moradores = dados_json.get('moradores', [])
            
            # Carregar tarefas
            Tarefas.tarefas = dados_json.get('tarefas', [])
            
            # Carregar manutenções
            Manutencao.item_manutencao = dados_json.get('manutencoes', [])
            
            # Carregar compras
            Compras.lista_compras = []
            for c in dados_json.get('compras', []):
                compra = Compras(c['nome'], c['quantidade'], c['categoria'], 
                               c.get('preco_estimado', 0), c.get('comprado', False))
                compra.unidade = c.get('unidade', 'unidade')
                Compras.lista_compras.append(compra)
            
            # Carregar contas
            Conta.contas = []
            for c in dados_json.get('contas', []):
                conta = Conta(c['descricao'], c['valor'], c['data_vencimento'],
                            c['categoria'], c['status'])
                conta.data_criacao = c.get('data_criacao', datetime.now().strftime("%d/%m/%Y"))
                Conta.contas.append(conta)
            
            # Carregar estoque
            ItemEstoque.itens = dados_json.get('estoque', [])
            
            print(f"✓ Dados carregados com sucesso de '{self.ARQUIVO_DADOS}'")
            return True
        except Exception as e:
            print(f"✗ Erro ao carregar dados: {e}")
            return False
    
    @staticmethod
    def listar_status_sistema():
        """Exibe status geral do sistema"""
        print("\n" + "=" * 80)
        print("STATUS GERAL DO SISTEMA - CASA INTELIGENTE")
        print("=" * 80)
        
        print(f"\n📊 RESUMO:")
        print(f"   👥 Moradores: {len(Morador.moradores)}")
        print(f"   📋 Tarefas: {len(Tarefas.tarefas)} ({len([t for t in Tarefas.tarefas if t['status'] == 'pendente'])} pendentes)")
        print(f"   🔧 Manutenções: {len(Manutencao.item_manutencao)}")
        print(f"   🛒 Compras: {len(Compras.lista_compras)} ({len([c for c in Compras.lista_compras if c.comprado])} compradas)")
        print(f"   💳 Contas: {len(Conta.contas)} ({len([c for c in Conta.contas if c.status == 'pendente'])} pendentes)")
        print(f"   📦 Estoque: {len(ItemEstoque.itens)} itens")
        
        # Calcular total de contas pendentes
        total_contas = sum(c.valor for c in Conta.contas if c.status == 'pendente')
        if total_contas > 0:
            print(f"\n⚠️  Total de contas pendentes: R$ {total_contas:.2f}")


def menu_principal():
    """Menu principal do sistema"""
    casa = Casa()
    
    while True:
        print("\n" + "=" * 80)
        print("SISTEMA DE CASA INTELIGENTE")
        print("=" * 80)
        print("\n[1] Gerenciar Moradores")
        print("[2] Gerenciar Tarefas")
        print("[3] Gerenciar Manutenção")
        print("[4] Gerenciar Compras")
        print("[5] Gerenciar Contas")
        print("[6] Gerenciar Estoque")
        print("[7] Ver Relatórios e Estatísticas")
        print("[8] Status do Sistema")
        print("[9] Salvar Dados")
        print("[0] Sair")
        print("-" * 80)
        
        opcao = input("\nEscolha uma opção (0-9): ").strip()
        
        if opcao == "1":
            menu_moradores()
        elif opcao == "2":
            menu_tarefas()
        elif opcao == "3":
            menu_manutencao()
        elif opcao == "4":
            menu_compras()
        elif opcao == "5":
            menu_contas()
        elif opcao == "6":
            menu_estoque()
        elif opcao == "7":
            menu_relatorios()
        elif opcao == "8":
            Casa.listar_status_sistema()
        elif opcao == "9":
            casa.salvar_dados()
        elif opcao == "0":
            confirmacao = input("\nDeseja salvar dados antes de sair? (s/n): ").strip().lower()
            if confirmacao == 's':
                casa.salvar_dados()
            print("\n✓ Encerrando sistema...")
            break
        else:
            print("✗ Opção inválida! Tente novamente.")
        
        input("\nPressione ENTER para continuar...")


def menu_moradores():
    """Submenu de moradores"""
    while True:
        print("\n" + "=" * 80)
        print("GERENCIAR MORADORES")
        print("=" * 80)
        print("\n[1] Cadastrar novo morador")
        print("[2] Listar todos os moradores")
        print("[3] Buscar morador por nome")
        print("[4] Editar morador")
        print("[5] Remover morador")
        print("[6] Ver estatísticas de moradores")
        print("[0] Voltar")
        print("-" * 80)
        
        opcao = input("\nEscolha uma opção: ").strip()
        
        if opcao == "1":
            print("\n" + "-" * 80)
            try:
                nome = input("Nome completo: ").strip()
                if not nome:
                    print("✗ Nome não pode estar vazio!")
                    continue
                
                if Morador.obter_morador_por_nome(nome):
                    print(f"✗ Morador '{nome}' já está cadastrado!")
                    continue
                
                idade = int(input("Idade: "))
                if idade < 0 or idade > 150:
                    print("✗ Idade inválida!")
                    continue
                
                quarto = input("Quarto: ").strip()
                if not quarto:
                    print("✗ Quarto não pode estar vazio!")
                    continue
                
                telefone = input("Telefone: ").strip()
                if not telefone:
                    print("✗ Telefone não pode estar vazio!")
                    continue
                
                novo_morador = Morador(nome, idade, quarto, telefone)
                novo_morador.cadastrar()
            except ValueError:
                print("✗ Entrada inválida!")
        
        elif opcao == "2":
            Morador.listar_todos()
        elif opcao == "3":
            nome = input("\nDigite o nome para buscar: ").strip()
            Morador.listar_busca_nome(nome)
        elif opcao == "4":
            nome = input("\nNome do morador a editar: ").strip()
            if Morador.obter_morador_por_nome(nome):
                print("(Deixe em branco para manter o valor atual)")
                novo_nome = input("Novo nome [Enter para manter]: ").strip() or None
                try:
                    nova_idade_str = input("Nova idade [Enter para manter]: ").strip()
                    nova_idade = int(nova_idade_str) if nova_idade_str else None
                except ValueError:
                    print("✗ Idade inválida!")
                    continue
                novo_quarto = input("Novo quarto [Enter para manter]: ").strip() or None
                novo_telefone = input("Novo telefone [Enter para manter]: ").strip() or None
                Morador.editar_morador(nome, novo_nome, nova_idade, novo_quarto, novo_telefone)
            else:
                print(f"✗ Morador '{nome}' não encontrado!")
        elif opcao == "5":
            nome = input("\nNome do morador a remover: ").strip()
            confirmacao = input(f"Tem certeza que deseja remover '{nome}'? (s/n): ").strip().lower()
            if confirmacao == 's':
                Morador.deletar_morador(nome)
        elif opcao == "6":
            Morador.obter_estatisticas()
        elif opcao == "0":
            break
        else:
            print("✗ Opção inválida!")
        
        input("\nPressione ENTER para continuar...")


def menu_tarefas():
    """Submenu de tarefas"""
    while True:
        print("\n" + "=" * 80)
        print("GERENCIAR TAREFAS")
        print("=" * 80)
        print("\n[1] Criar nova tarefa")
        print("[2] Listar todas as tarefas")
        print("[3] Listar tarefas pendentes")
        print("[4] Listar tarefas por morador")
        print("[5] Listar tarefas pendentes por morador")
        print("[6] Marcar tarefa como feita")
        print("[7] Ver estatísticas")
        print("[0] Voltar")
        print("-" * 80)
        
        opcao = input("\nEscolha uma opção: ").strip()
        
        if opcao == "1":
            print("\n" + "-" * 80)
            try:
                nome = input("Nome da tarefa: ").strip()
                descricao = input("Descrição: ").strip()
                responsavel = input("Responsável (morador): ").strip()
                recorrencia = int(input("Recorrência em dias (1=diária, 7=semanal, etc): "))
                
                tarefa = Tarefas(nome, descricao, responsavel, recorrencia)
                tarefa.adicionar_tarefa()
            except ValueError:
                print("✗ Entrada inválida!")
        
        elif opcao == "2":
            Tarefas.listar_todas_tarefas()
        elif opcao == "3":
            Tarefas.listar_tarefas_pendentes()
        elif opcao == "4":
            responsavel = input("\nNome do morador: ").strip()
            Tarefas.listar_tarefas_por_morador(responsavel)
        elif opcao == "5":
            Tarefas.listar_tarefas_pendentes_por_morador()
        elif opcao == "6":
            nome_tarefa = input("\nNome da tarefa a marcar como feita: ").strip()
            Tarefas.marcar_como_feita(nome_tarefa)
        elif opcao == "7":
            Tarefas.obter_estatisticas()
        elif opcao == "0":
            break
        else:
            print("✗ Opção inválida!")
        
        input("\nPressione ENTER para continuar...")


def menu_manutencao():
    """Submenu de manutenção"""
    while True:
        print("\n" + "=" * 80)
        print("GERENCIAR MANUTENÇÃO")
        print("=" * 80)
        print("\n[1] Registrar novo item de manutenção")
        print("[2] Listar todos os itens")
        print("[3] Listar manutenções pendentes (vencidas)")
        print("[4] Listar manutenções este mês")
        print("[5] Registrar revisão realizada")
        print("[0] Voltar")
        print("-" * 80)
        
        opcao = input("\nEscolha uma opção: ").strip()
        
        if opcao == "1":
            print("\n" + "-" * 80)
            try:
                nome = input("Nome do item: ").strip()
                data = input("Data da última revisão (DD/MM/YYYY): ").strip()
                periodicidade = int(input("Periodicidade em meses: "))
                descricao = input("Descrição: ").strip()
                responsavel = input("Responsável: ").strip()
                
                item = Manutencao(nome, data, periodicidade, descricao, responsavel)
                item.registrar_manutencao()
            except ValueError:
                print("✗ Entrada inválida!")
        
        elif opcao == "2":
            Manutencao.listar_todas_manutencoes()
        elif opcao == "3":
            Manutencao.listar_manutencoes_pendentes()
        elif opcao == "4":
            Manutencao.listar_manutencoes_este_mes()
        elif opcao == "5":
            nome_item = input("\nNome do item: ").strip()
            Manutencao.registrar_revisao_realizada(nome_item)
        elif opcao == "0":
            break
        else:
            print("✗ Opção inválida!")
        
        input("\nPressione ENTER para continuar...")


def menu_compras():
    """Submenu de compras"""
    while True:
        print("\n" + "=" * 80)
        print("GERENCIAR COMPRAS")
        print("=" * 80)
        print("\n[1] Adicionar item à lista")
        print("[2] Listar compras não realizadas")
        print("[3] Listar todas as compras")
        print("[4] Marcar como comprado")
        print("[5] Ver categorias disponíveis")
        print("[0] Voltar")
        print("-" * 80)
        
        opcao = input("\nEscolha uma opção: ").strip()
        
        if opcao == "1":
            print("\n" + "-" * 80)
            print(f"Categorias disponíveis: {', '.join(Compras.CATEGORIAS_VALIDAS)}")
            try:
                nome = input("Nome do item: ").strip()
                quantidade = float(input("Quantidade: "))
                categoria = input("Categoria: ").strip().lower()
                preco = float(input("Preço estimado: R$ "))
                
                item = Compras(nome, quantidade, categoria, preco)
                item.adicionar_item()
            except ValueError:
                print("✗ Entrada inválida!")
        
        elif opcao == "2":
            print("\n🛒 Itens não comprados:")
            nao_comprados = [c for c in Compras.lista_compras if not c.comprado]
            if nao_comprados:
                for i, item in enumerate(nao_comprados, 1):
                    print(f"{i}. {item.nome} ({item.quantidade} {item.unidade}) - {item.categoria}")
            else:
                print("✓ Todos os itens foram comprados!")
        
        elif opcao == "3":
            print("\n📋 Lista completa de compras:")
            if Compras.lista_compras:
                for i, item in enumerate(Compras.lista_compras, 1):
                    status = "✓" if item.comprado else "✗"
                    print(f"{i}. {status} {item.nome} ({item.quantidade} {item.unidade}) - {item.categoria} - R$ {item.preco_estimado:.2f}")
            else:
                print("Lista vazia!")
        
        elif opcao == "4":
            nome_item = input("\nNome do item a marcar como comprado: ").strip()
            Compras.item_comprado_por_nome(nome_item)
        
        elif opcao == "5":
            print("\n📂 Categorias disponíveis:")
            for cat in Compras.CATEGORIAS_VALIDAS:
                print(f"   • {cat}")
        
        elif opcao == "0":
            break
        else:
            print("✗ Opção inválida!")
        
        input("\nPressione ENTER para continuar...")


def menu_contas():
    """Submenu de contas"""
    while True:
        print("\n" + "=" * 80)
        print("GERENCIAR CONTAS")
        print("=" * 80)
        print("\n[1] Registrar nova conta")
        print("[2] Listar contas pendentes")
        print("[3] Listar todas as contas")
        print("[4] Marcar conta como paga")
        print("[5] Ver categorias disponíveis")
        print("[0] Voltar")
        print("-" * 80)
        
        opcao = input("\nEscolha uma opção: ").strip()
        
        if opcao == "1":
            print("\n" + "-" * 80)
            print(f"Categorias: {', '.join(Conta.CATEGORIAS_VALIDAS)}")
            try:
                descricao = input("Descrição: ").strip()
                valor = float(input("Valor: R$ "))
                data = input("Data de vencimento (DD/MM/YYYY): ").strip()
                categoria = input("Categoria: ").strip()
                
                conta = Conta(descricao, valor, data, categoria)
                conta.registrar_conta()
            except ValueError:
                print("✗ Entrada inválida!")
        
        elif opcao == "2":
            Conta.listar_contas_pendentes()
        elif opcao == "3":
            Conta.listar_todas_contas()
        elif opcao == "4":
            descricao = input("\nDescrição da conta: ").strip()
            for conta in Conta.contas:
                if conta.descricao.lower() == descricao.lower():
                    conta.marcar_como_pago()
                    break
            else:
                print(f"✗ Conta '{descricao}' não encontrada!")
        elif opcao == "5":
            print("\n📂 Categorias disponíveis:")
            for cat in Conta.CATEGORIAS_VALIDAS:
                print(f"   • {cat}")
        elif opcao == "0":
            break
        else:
            print("✗ Opção inválida!")
        
        input("\nPressione ENTER para continuar...")


def menu_estoque():
    """Submenu de estoque"""
    estoque = ItemEstoque()
    
    while True:
        print("\n" + "=" * 80)
        print("GERENCIAR ESTOQUE")
        print("=" * 80)
        print("\n[1] Adicionar item ao estoque")
        print("[2] Ver estoque atual")
        print("[3] Atualizar quantidade de item")
        print("[4] Remover item")
        print("[0] Voltar")
        print("-" * 80)
        
        opcao = input("\nEscolha uma opção: ").strip()
        
        if opcao == "1":
            print("\n" + "-" * 80)
            try:
                nome = input("Nome do item: ").strip()
                quantidade = int(input("Quantidade: "))
                preco = float(input("Preço: R$ "))
                data = input("Data de validade (DD/MM/YYYY) [Enter para sem validade]: ").strip() or None
                
                estoque.adicionarItem(nome, quantidade, preco, data)
            except ValueError:
                print("✗ Entrada inválida!")
        
        elif opcao == "2":
            estoque.estoqueAtual()
        elif opcao == "3":
            nome = input("\nNome do item: ").strip()
            try:
                quantidade = int(input("Nova quantidade: "))
                estoque.atualizarItem(nome, quantidade=quantidade)
            except ValueError:
                print("✗ Entrada inválida!")
        elif opcao == "4":
            nome = input("\nNome do item a remover: ").strip()
            estoque.removerItem(nome)
        elif opcao == "0":
            break
        else:
            print("✗ Opção inválida!")
        
        input("\nPressione ENTER para continuar...")


def menu_relatorios():
    """Submenu de relatórios"""
    relatorios = RelatoriosEstatisticas(
        contas=Conta.contas,
        tarefas=Tarefas.tarefas,
        estoque=ItemEstoque.itens,
        manutencoes=Manutencao.item_manutencao
    )
    
    while True:
        print("\n" + "=" * 80)
        print("RELATÓRIOS E ESTATÍSTICAS")
        print("=" * 80)
        print("\n[1] Gastos por categoria e mês")
        print("[2] Moradores com mais tarefas")
        print("[3] Itens com estoque crítico")
        print("[0] Voltar")
        print("-" * 80)
        
        opcao = input("\nEscolha uma opção: ").strip()
        
        if opcao == "1":
            relatorios.gastos_por_categoria_e_mes()
        elif opcao == "2":
            relatorios.moradores_com_mais_tarefas()
        elif opcao == "3":
            relatorios.itens_mais_comprados_e_estoque_critico()
        elif opcao == "0":
            break
        else:
            print("✗ Opção inválida!")
        
        input("\nPressione ENTER para continuar...")


if __name__ == "__main__":
    menu_principal()
