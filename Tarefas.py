from datetime import datetime, timedelta

class Tarefas:
    """Gerenciador de tarefas recorrentes da casa inteligente"""
    
    tarefas = []
    
    def __init__(self, nome, descricao, responsavel, recorrencia_dias, data_criacao=None):
        """
        Inicializa uma tarefa recorrente
        
        Args:
            nome: Nome da tarefa (ex: 'Limpar casa')
            descricao: Descrição detalhada da tarefa
            responsavel: Nome do morador responsável
            recorrencia_dias: Frequência em dias (1=diariamente, 7=semanalmente, etc.)
            data_criacao: Data de criação (padrão: hoje)
        """
        self.nome = nome
        self.descricao = descricao
        self.responsavel = responsavel
        self.recorrencia_dias = recorrencia_dias
        self.data_criacao = data_criacao or datetime.now().strftime("%d/%m/%Y")
        self.data_ultima_conclusao = None
        self.status = "pendente"
        self.id = len(Tarefas.tarefas) + 1
    
    def adicionar_tarefa(self):
        """Adiciona a tarefa à lista de tarefas"""
        tarefa_dict = {
            'id': self.id,
            'nome': self.nome,
            'descricao': self.descricao,
            'responsavel': self.responsavel,
            'recorrencia_dias': self.recorrencia_dias,
            'data_criacao': self.data_criacao,
            'data_ultima_conclusao': self.data_ultima_conclusao,
            'status': self.status
        }
        Tarefas.tarefas.append(tarefa_dict)
        print(f"✓ Tarefa '{self.nome}' adicionada com sucesso!")
        return tarefa_dict
    
    @staticmethod
    def marcar_como_feita(nome_tarefa, responsavel=None):
        """
        Marca uma tarefa como concluída registrando a data
        
        Args:
            nome_tarefa: Nome da tarefa a marcar
            responsavel: Nome do morador (opcional, para validação)
        """
        for tarefa in Tarefas.tarefas:
            if tarefa['nome'].lower() == nome_tarefa.lower():
                if responsavel and tarefa['responsavel'].lower() != responsavel.lower():
                    print(f"✗ Esta tarefa não é responsabilidade de {responsavel}")
                    return False
                
                tarefa['data_ultima_conclusao'] = datetime.now().strftime("%d/%m/%Y %H:%M")
                tarefa['status'] = "concluída"
                print(f"\n✓ Tarefa '{nome_tarefa}' marcada como concluída!")
                print(f"  Data/hora: {tarefa['data_ultima_conclusao']}")
                print(f"  Próxima revisão esperada: em {tarefa['recorrencia_dias']} dia(s)")
                return True
        
        print(f"✗ Tarefa '{nome_tarefa}' não encontrada.")
        return False
    
    @staticmethod
    def listar_tarefas_pendentes():
        """Lista todas as tarefas pendentes"""
        print("\n" + "=" * 75)
        print("TAREFAS PENDENTES")
        print("=" * 75)
        
        pendentes = [t for t in Tarefas.tarefas if t['status'] == "pendente"]
        
        if not pendentes:
            print("✓ Nenhuma tarefa pendente!")
        else:
            for tarefa in sorted(pendentes, key=lambda x: x['responsavel']):
                print(f"\n📋 Tarefa: {tarefa['nome']}")
                print(f"   Descrição: {tarefa['descricao']}")
                print(f"   Responsável: {tarefa['responsavel']}")
                print(f"   Recorrência: A cada {tarefa['recorrencia_dias']} dia(s)")
                print(f"   Data de criação: {tarefa['data_criacao']}")
                if tarefa['data_ultima_conclusao']:
                    print(f"   Última conclusão: {tarefa['data_ultima_conclusao']}")
                print("-" * 75)
    
    @staticmethod
    def listar_tarefas_por_morador(responsavel):
        """Lista todas as tarefas atribuídas a um morador específico"""
        print("\n" + "=" * 75)
        print(f"TAREFAS DE {responsavel.upper()}")
        print("=" * 75)
        
        tarefas_morador = [t for t in Tarefas.tarefas if t['responsavel'].lower() == responsavel.lower()]
        
        if not tarefas_morador:
            print(f"Nenhuma tarefa atribuída a {responsavel}.")
            return
        
        # Separar por status
        pendentes = [t for t in tarefas_morador if t['status'] == "pendente"]
        concluidas = [t for t in tarefas_morador if t['status'] == "concluída"]
        
        print(f"\n🔴 TAREFAS PENDENTES ({len(pendentes)}):")
        print("-" * 75)
        if pendentes:
            for tarefa in pendentes:
                print(f"\n  • {tarefa['nome']}")
                print(f"    Descrição: {tarefa['descricao']}")
                print(f"    Recorrência: A cada {tarefa['recorrencia_dias']} dia(s)")
                if tarefa['data_ultima_conclusao']:
                    print(f"    Última conclusão: {tarefa['data_ultima_conclusao']}")
                print(f"    Status: ⏳ PENDENTE")
        else:
            print("  ✓ Nenhuma tarefa pendente!")
        
        print(f"\n🟢 TAREFAS CONCLUÍDAS ({len(concluidas)}):")
        print("-" * 75)
        if concluidas:
            for tarefa in concluidas:
                print(f"\n  • {tarefa['nome']}")
                print(f"    Descrição: {tarefa['descricao']}")
                print(f"    Última conclusão: {tarefa['data_ultima_conclusao']}")
                print(f"    Status: ✓ CONCLUÍDA")
        else:
            print("  Nenhuma tarefa concluída ainda.")
    
    @staticmethod
    def listar_tarefas_pendentes_por_morador():
        """Lista tarefas pendentes agrupadas por morador"""
        print("\n" + "=" * 75)
        print("TAREFAS PENDENTES POR MORADOR")
        print("=" * 75)
        
        # Agrupar tarefas por morador
        moradores_tarefas = {}
        for tarefa in Tarefas.tarefas:
            if tarefa['status'] == "pendente":
                morador = tarefa['responsavel']
                if morador not in moradores_tarefas:
                    moradores_tarefas[morador] = []
                moradores_tarefas[morador].append(tarefa)
        
        if not moradores_tarefas:
            print("✓ Nenhuma tarefa pendente!")
            return
        
        for morador in sorted(moradores_tarefas.keys()):
            tarefas = moradores_tarefas[morador]
            print(f"\n👤 {morador.upper()} - {len(tarefas)} tarefa(s)")
            print("-" * 75)
            for tarefa in tarefas:
                print(f"\n  📌 {tarefa['nome']}")
                print(f"     Descrição: {tarefa['descricao']}")
                print(f"     Recorrência: {tarefa['recorrencia_dias']} dia(s)")
                if tarefa['data_ultima_conclusao']:
                    dias_decorridos = (datetime.now() - datetime.strptime(tarefa['data_ultima_conclusao'], "%d/%m/%Y %H:%M")).days
                    print(f"     Última conclusão: {tarefa['data_ultima_conclusao']} ({dias_decorridos} dias atrás)")
                else:
                    print(f"     Criada em: {tarefa['data_criacao']}")
    
    @staticmethod
    def listar_todas_tarefas():
        """Lista todas as tarefas cadastradas"""
        print("\n" + "=" * 75)
        print("LISTA COMPLETA DE TAREFAS")
        print("=" * 75)
        
        if not Tarefas.tarefas:
            print("Nenhuma tarefa cadastrada.")
            return
        
        for tarefa in sorted(Tarefas.tarefas, key=lambda x: (x['responsavel'], x['nome'])):
            status_emoji = "🟢" if tarefa['status'] == "concluída" else "🔴"
            status_texto = "Concluída" if tarefa['status'] == "concluída" else "Pendente"
            
            print(f"\n{status_emoji} {tarefa['nome']}")
            print(f"   Descrição: {tarefa['descricao']}")
            print(f"   Responsável: {tarefa['responsavel']}")
            print(f"   Recorrência: {tarefa['recorrencia_dias']} dia(s)")
            print(f"   Status: {status_texto}")
            print(f"   Criada em: {tarefa['data_criacao']}")
            if tarefa['data_ultima_conclusao']:
                print(f"   Última conclusão: {tarefa['data_ultima_conclusao']}")
            print("-" * 75)
    
    @staticmethod
    def obter_estatisticas():
        """Exibe estatísticas sobre as tarefas"""
        print("\n" + "=" * 75)
        print("ESTATÍSTICAS DE TAREFAS")
        print("=" * 75)
        
        total = len(Tarefas.tarefas)
        pendentes = len([t for t in Tarefas.tarefas if t['status'] == "pendente"])
        concluidas = len([t for t in Tarefas.tarefas if t['status'] == "concluída"])
        
        print(f"\n📊 Resumo Geral:")
        print(f"   Total de tarefas: {total}")
        print(f"   🔴 Pendentes: {pendentes}")
        print(f"   🟢 Concluídas: {concluidas}")
        
        # Por morador
        moradores = set(t['responsavel'] for t in Tarefas.tarefas)
        print(f"\n👥 Distribuição por Morador:")
        for morador in sorted(moradores):
            tarefas_morador = [t for t in Tarefas.tarefas if t['responsavel'] == morador]
            pend = len([t for t in tarefas_morador if t['status'] == "pendente"])
            conc = len([t for t in tarefas_morador if t['status'] == "concluída"])
            print(f"   • {morador}: {len(tarefas_morador)} tarefas ({pend} pendentes, {conc} concluídas)")