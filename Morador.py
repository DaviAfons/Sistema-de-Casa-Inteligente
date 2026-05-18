import os
from datetime import datetime

class Morador:
    """Gerenciador de moradores da casa inteligente"""
    
    moradores = []
    
    def __init__(self, nome, idade, quarto, telefone):
        """
        Inicializa um morador
        
        Args:
            nome: Nome completo
            idade: Idade em anos
            quarto: Número ou identificação do quarto
            telefone: Número de telefone
        """
        self.nome = nome
        self.idade = idade
        self.quarto = quarto
        self.telefone = telefone
        self.data_cadastro = datetime.now().strftime("%d/%m/%Y")
    
    def cadastrar(self):
        """Registra o morador na lista de moradores"""
        morador_dict = {
            'nome': self.nome,
            'idade': self.idade,
            'quarto': self.quarto,
            'telefone': self.telefone,
            'data_cadastro': self.data_cadastro
        }
        Morador.moradores.append(morador_dict)
        print(f"✓ Morador '{self.nome}' cadastrado com sucesso!")
        return morador_dict
    
    @staticmethod
    def listar_todos():
        """Lista todos os moradores cadastrados"""
        print("\n" + "=" * 80)
        print("LISTA COMPLETA DE MORADORES")
        print("=" * 80)
        
        if not Morador.moradores:
            print("Nenhum morador cadastrado.")
            return
        
        for idx, morador in enumerate(sorted(Morador.moradores, key=lambda x: x['nome']), 1):
            print(f"\n{idx}. 👤 {morador['nome'].upper()}")
            print(f"   Idade: {morador['idade']} anos")
            print(f"   Quarto: {morador['quarto']}")
            print(f"   Telefone: {morador['telefone']}")
            print(f"   Cadastrado em: {morador['data_cadastro']}")
            print("-" * 80)
    
    @staticmethod
    def buscar_por_nome(nome):
        """
        Busca um morador pelo nome
        
        Args:
            nome: Nome ou parte do nome para buscar
            
        Returns:
            Dicionário do morador ou None se não encontrado
        """
        nome_lower = nome.lower()
        for morador in Morador.moradores:
            if nome_lower in morador['nome'].lower():
                return morador
        return None
    
    @staticmethod
    def listar_busca_nome(nome):
        """Lista resultados da busca por nome"""
        print("\n" + "=" * 80)
        print(f"RESULTADO DA BUSCA: '{nome}'")
        print("=" * 80)
        
        nome_lower = nome.lower()
        resultados = [m for m in Morador.moradores if nome_lower in m['nome'].lower()]
        
        if not resultados:
            print(f"✗ Nenhum morador encontrado com o nome '{nome}'")
            return False
        
        for morador in resultados:
            print(f"\n✓ 👤 {morador['nome']}")
            print(f"   Idade: {morador['idade']} anos")
            print(f"   Quarto: {morador['quarto']}")
            print(f"   Telefone: {morador['telefone']}")
            print(f"   Cadastrado em: {morador['data_cadastro']}")
            print("-" * 80)
        
        return True
    
    @staticmethod
    def obter_morador_por_nome(nome):
        """Obtém um morador específico pelo nome exato"""
        for morador in Morador.moradores:
            if morador['nome'].lower() == nome.lower():
                return morador
        return None
    
    @staticmethod
    def editar_morador(nome_antigo, nome_novo=None, idade=None, quarto=None, telefone=None):
        """Edita informações de um morador"""
        morador = Morador.obter_morador_por_nome(nome_antigo)
        
        if not morador:
            print(f"✗ Morador '{nome_antigo}' não encontrado.")
            return False
        
        if nome_novo:
            morador['nome'] = nome_novo
        if idade is not None:
            morador['idade'] = idade
        if quarto:
            morador['quarto'] = quarto
        if telefone:
            morador['telefone'] = telefone
        
        print(f"✓ Dados do morador atualizados com sucesso!")
        return True
    
    @staticmethod
    def deletar_morador(nome):
        """Remove um morador do cadastro"""
        morador = Morador.obter_morador_por_nome(nome)
        
        if not morador:
            print(f"✗ Morador '{nome}' não encontrado.")
            return False
        
        Morador.moradores.remove(morador)
        print(f"✓ Morador '{nome}' removido do sistema.")
        return True
    
    @staticmethod
    def obter_estatisticas():
        """Exibe estatísticas dos moradores"""
        print("\n" + "=" * 80)
        print("ESTATÍSTICAS DE MORADORES")
        print("=" * 80)
        
        if not Morador.moradores:
            print("Nenhum morador cadastrado.")
            return
        
        total = len(Morador.moradores)
        idade_media = sum(m['idade'] for m in Morador.moradores) / total
        idade_min = min(m['idade'] for m in Morador.moradores)
        idade_max = max(m['idade'] for m in Morador.moradores)
        quartos_unicos = len(set(m['quarto'] for m in Morador.moradores))
        
        print(f"\n📊 Resumo:")
        print(f"   Total de moradores: {total}")
        print(f"   Idade média: {idade_media:.1f} anos")
        print(f"   Idade mínima: {idade_min} anos")
        print(f"   Idade máxima: {idade_max} anos")
        print(f"   Quartos ocupados: {quartos_unicos}")
        
        print(f"\n👥 Moradores por quarto:")
        quartos = {}
        for m in Morador.moradores:
            if m['quarto'] not in quartos:
                quartos[m['quarto']] = []
            quartos[m['quarto']].append(m['nome'])
        
        for quarto in sorted(quartos.keys()):
            print(f"   Quarto {quarto}: {', '.join(quartos[quarto])}")


def menu_principal():
    """Menu interativo principal do sistema de moradores"""
    
    while True:
        print("\n" + "=" * 80)
        print("SISTEMA DE GERENCIAMENTO DE MORADORES - CASA INTELIGENTE")
        print("=" * 80)
        print("\n[1] Cadastrar novo morador")
        print("[2] Listar todos os moradores")
        print("[3] Buscar morador por nome")
        print("[4] Editar informações de um morador")
        print("[5] Remover morador")
        print("[6] Ver estatísticas")
        print("[0] Sair")
        print("-" * 80)
        
        opcao = input("\nEscolha uma opção (0-6): ").strip()
        
        if opcao == "1":
            menu_cadastrar()
        elif opcao == "2":
            Morador.listar_todos()
        elif opcao == "3":
            menu_buscar()
        elif opcao == "4":
            menu_editar()
        elif opcao == "5":
            menu_deletar()
        elif opcao == "6":
            Morador.obter_estatisticas()
        elif opcao == "0":
            print("\n✓ Encerrando sistema...")
            break
        else:
            print("✗ Opção inválida! Tente novamente.")
        
        input("\nPressione ENTER para continuar...")


def menu_cadastrar():
    """Menu para cadastrar novo morador"""
    print("\n" + "=" * 80)
    print("CADASTRAR NOVO MORADOR")
    print("=" * 80)
    
    try:
        nome = input("\nNome completo: ").strip()
        if not nome:
            print("✗ Nome não pode estar vazio!")
            return
        
        # Verificar se morador já existe
        if Morador.obter_morador_por_nome(nome):
            print(f"✗ Morador '{nome}' já está cadastrado!")
            return
        
        idade = int(input("Idade: "))
        if idade < 0 or idade > 150:
            print("✗ Idade inválida!")
            return
        
        quarto = input("Quarto (ex: 101, Suíte, Sala): ").strip()
        if not quarto:
            print("✗ Quarto não pode estar vazio!")
            return
        
        telefone = input("Telefone (ex: (11) 99999-9999): ").strip()
        if not telefone:
            print("✗ Telefone não pode estar vazio!")
            return
        
        # Criar e cadastrar morador
        novo_morador = Morador(nome, idade, quarto, telefone)
        novo_morador.cadastrar()
        
    except ValueError:
        print("✗ Entrada inválida! Verifique os dados.")


def menu_buscar():
    """Menu para buscar morador"""
    print("\n" + "=" * 80)
    print("BUSCAR MORADOR")
    print("=" * 80)
    
    nome = input("\nDigite o nome (ou parte do nome) para buscar: ").strip()
    if not nome:
        print("✗ Por favor, digite um nome!")
        return
    
    Morador.listar_busca_nome(nome)


def menu_editar():
    """Menu para editar informações de morador"""
    print("\n" + "=" * 80)
    print("EDITAR INFORMAÇÕES DE MORADOR")
    print("=" * 80)
    
    nome = input("\nNome do morador a editar: ").strip()
    morador = Morador.obter_morador_por_nome(nome)
    
    if not morador:
        print(f"✗ Morador '{nome}' não encontrado!")
        return
    
    print(f"\nEditando morador: {morador['nome']}")
    print("(Deixe em branco para manter o valor atual)")
    print("-" * 80)
    
    novo_nome = input("Novo nome [Enter para manter]: ").strip() or None
    
    try:
        nova_idade_str = input("Nova idade [Enter para manter]: ").strip()
        nova_idade = int(nova_idade_str) if nova_idade_str else None
    except ValueError:
        print("✗ Idade inválida!")
        return
    
    novo_quarto = input("Novo quarto [Enter para manter]: ").strip() or None
    novo_telefone = input("Novo telefone [Enter para manter]: ").strip() or None
    
    Morador.editar_morador(nome, novo_nome, nova_idade, novo_quarto, novo_telefone)


def menu_deletar():
    """Menu para deletar morador"""
    print("\n" + "=" * 80)
    print("REMOVER MORADOR")
    print("=" * 80)
    
    nome = input("\nNome do morador a remover: ").strip()
    
    confirmacao = input(f"Tem certeza que deseja remover '{nome}'? (s/n): ").strip().lower()
    if confirmacao == 's':
        Morador.deletar_morador(nome)
    else:
        print("Operação cancelada.")


# Ponto de entrada se executado diretamente
if __name__ == "__main__":
    menu_principal()
    
    @classmethod
    def from_dict(cls, dados):
        """Cria um objeto Morador a partir de um dicionário"""
        morador = cls()
        morador.cadastrar_morador(
            dados['nome'],
            dados['idade'],
            dados['quarto'],
            dados['telefone'],
            dados['email']
        )
        return morador