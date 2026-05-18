from collections import Counter
from datetime import datetime

class RelatoriosEstatisticas:
    def __init__(self, contas=None, tarefas=None, estoque=None, manutencoes=None):
        """
        Inicializa o gerador de relatórios.
        
        Args:
            contas: Lista de contas (Conta)
            tarefas: Lista de tarefas (Tarefa)
            estoque: Lista de itens de estoque (ItemEstoque)
            manutencoes: Lista de manutenções (Manutencao)
        """
        self.contas = contas if contas else []
        self.tarefas = tarefas if tarefas else []
        self.estoque = estoque if estoque else []
        self.manutencoes = manutencoes if manutencoes else []

    def gastos_por_categoria_e_mes(self):
        """Relatório de gastos totais por categoria e por mês"""
        print("\n" + "="*60)
        print("GASTOS TOTAIS POR CATEGORIA E POR MÊS")
        print("="*60)
        
        if not self.contas:
            print("Nenhuma conta registrada.")
            return
        
        # Agrupar por categoria
        gastos_categoria = Counter()
        gastos_mes = Counter()
        
        for conta in self.contas:
            categoria = conta.get('categoria', 'Sem categoria') if isinstance(conta, dict) else getattr(conta, 'categoria', 'Sem categoria')
            valor = conta.get('valor', 0) if isinstance(conta, dict) else getattr(conta, 'valor', 0)
            data = conta.get('data_vencimento', 'Sem data') if isinstance(conta, dict) else getattr(conta, 'data_vencimento', 'Sem data')
            
            gastos_categoria[categoria] += valor
            
            # Extrair mês e ano da data (formato dd/mm/yyyy → MM/YYYY)
            if isinstance(data, str):
                try:
                    partes = data.split('/')
                    mes_ano = f"{partes[2]}-{partes[1]}" if len(partes) == 3 else data[:7]
                except:
                    mes_ano = "Desconhecido"
            else:
                mes_ano = data.strftime("%Y-%m") if hasattr(data, 'strftime') else "Desconhecido"
            
            gastos_mes[mes_ano] += valor
        
        # Exibir por categoria
        print("\nPor Categoria:")
        print("-" * 40)
        for categoria, total in gastos_categoria.most_common():
            print(f"  {categoria}: R$ {total:.2f}")
        
        # Exibir por mês
        print("\nPor Mês:")
        print("-" * 40)
        for mes, total in sorted(gastos_mes.items(), reverse=True):
            print(f"  {mes}: R$ {total:.2f}")
        
        total_geral = sum(gastos_categoria.values())
        print(f"\nTotal Geral: R$ {total_geral:.2f}")

    def moradores_com_mais_tarefas(self):
        """Relatório de moradores com mais tarefas pendentes"""
        print("\n" + "="*60)
        print("MORADORES COM MAIS TAREFAS PENDENTES")
        print("="*60)
        
        if not self.tarefas:
            print("Nenhuma tarefa registrada.")
            return
        
        # Contar tarefas por morador
        tarefas_por_morador = Counter()
        tarefas_pendentes_por_morador = Counter()
        
        for tarefa in self.tarefas:
            # CORREÇÃO Bug #1: tarefas são dicionários, não objetos.
            # getattr() nunca encontra chaves de dict — usar .get() no lugar.
            responsavel = tarefa.get('responsavel', 'Desconhecido') if isinstance(tarefa, dict) else getattr(tarefa, 'responsavel', 'Desconhecido')
            status = tarefa.get('status', 'pendente') if isinstance(tarefa, dict) else getattr(tarefa, 'status', 'pendente')
            
            tarefas_por_morador[responsavel] += 1
            
            if status.lower() in ['pendente', 'em progresso']:
                tarefas_pendentes_por_morador[responsavel] += 1
        
        # Exibir total de tarefas
        print("\nTotal de Tarefas por Morador:")
        print("-" * 40)
        for morador, total in tarefas_por_morador.most_common():
            pendentes = tarefas_pendentes_por_morador[morador]
            print(f"  {morador}: {total} tarefas ({pendentes} pendentes)")

    def itens_mais_comprados_e_estoque_critico(self, limite_critico=5):
        """Relatório de itens mais comprados e estoque crítico"""
        print("\n" + "="*60)
        print("ITENS MAIS COMPRADOS E ESTOQUE CRÍTICO")
        print("="*60)
        
        if not self.estoque:
            print("Nenhum item de estoque registrado.")
            return
        
        # Itens mais comprados
        print("\nItens Mais Comprados:")
        print("-" * 40)
        
        itens_comprados = Counter()
        for item in self.estoque:
            # CORREÇÃO Bug #2: itens do estoque são dicionários, não objetos.
            # getattr() nunca encontra chaves de dict — usar .get() no lugar.
            nome = item.get('nome', 'Desconhecido') if isinstance(item, dict) else getattr(item, 'nome', 'Desconhecido')
            quantidade_comprada = item.get('quantidade_comprada', 0) if isinstance(item, dict) else getattr(item, 'quantidade_comprada', 0)
            itens_comprados[nome] += quantidade_comprada
        
        for item, quantidade in itens_comprados.most_common(10):
            print(f"  {item}: {quantidade} unidades")
        
        # Estoque crítico
        print(f"\nItens em Estoque Crítico (< {limite_critico} unidades):")
        print("-" * 40)
        
        estoque_baixo = []
        for item in self.estoque:
            # CORREÇÃO Bug #2: usar .get() para acessar chaves de dicionário.
            # O campo de preço no ItemEstoque é 'preco', não 'preco_unitario'.
            nome = item.get('nome', 'Desconhecido') if isinstance(item, dict) else getattr(item, 'nome', 'Desconhecido')
            quantidade = item.get('quantidade', 0) if isinstance(item, dict) else getattr(item, 'quantidade', 0)
            preco = item.get('preco', 0) if isinstance(item, dict) else getattr(item, 'preco_unitario', 0)
            
            if quantidade <= limite_critico:
                estoque_baixo.append({
                    'nome': nome,
                    'quantidade': quantidade,
                    'preco': preco
                })
        
        if estoque_baixo:
            for item in sorted(estoque_baixo, key=lambda x: x['quantidade']):
                print(f"  {item['nome']}: {item['quantidade']} unidades (R$ {item['preco']:.2f} cada)")
        else:
            print("  Nenhum item em estoque crítico.")

    def resumo_geral_casa(self):
        """Resumo geral: contas pendentes + estoque baixo + manutenções urgentes"""
        print("\n" + "="*60)
        print("RESUMO GERAL DA CASA")
        print("="*60)
        
        # Contas pendentes
        print("\n1. CONTAS PENDENTES:")
        print("-" * 40)
        contas_pendentes = 0
        total_pendente = 0
        
        for conta in self.contas:
            # Conta pode ser objeto (tem .status) ou dict (usa .get)
            status = conta.get('status', 'pendente') if isinstance(conta, dict) else getattr(conta, 'status', 'pendente')
            if status.lower() == 'pendente':
                contas_pendentes += 1
                valor = conta.get('valor', 0) if isinstance(conta, dict) else getattr(conta, 'valor', 0)
                total_pendente += valor
        
        print(f"  Total de contas pendentes: {contas_pendentes}")
        print(f"  Valor total em aberto: R$ {total_pendente:.2f}")
        
        # Estoque baixo
        print("\n2. ESTOQUE EM NÍVEL CRÍTICO:")
        print("-" * 40)
        estoque_critico = sum(
            1 for item in self.estoque
            if (item.get('quantidade', 0) if isinstance(item, dict) else getattr(item, 'quantidade', 0)) <= 5
        )
        print(f"  Itens em estoque crítico: {estoque_critico}")
        
        # Manutenções urgentes
        print("\n3. MANUTENÇÕES URGENTES:")
        print("-" * 40)
        manutencoes_urgentes = 0
        
        for manutencao in self.manutencoes:
            status = manutencao.get('status', 'planejada') if isinstance(manutencao, dict) else getattr(manutencao, 'status', 'planejada')
            prioridade = manutencao.get('prioridade', 'normal') if isinstance(manutencao, dict) else getattr(manutencao, 'prioridade', 'normal')
            
            if status.lower() in ['pendente', 'em progresso'] and prioridade.lower() == 'urgente':
                manutencoes_urgentes += 1
        
        print(f"  Manutenções urgentes: {manutencoes_urgentes}")
        
        # Resumo final
        print("\n" + "="*60)
        print("ALERTAS:")
        print("-" * 40)
        if contas_pendentes > 0:
            print(f"⚠ {contas_pendentes} contas aguardando pagamento")
        if estoque_critico > 0:
            print(f"⚠ {estoque_critico} itens com estoque crítico")
        if manutencoes_urgentes > 0:
            print(f"⚠ {manutencoes_urgentes} manutenções urgentes pendentes")
        
        if contas_pendentes == 0 and estoque_critico == 0 and manutencoes_urgentes == 0:
            print("✓ Nenhum alerta no momento")

    def exportar_relatorio_completo(self, nome_arquivo="relatorio_casa.txt"):
        """Exporta relatório completo para arquivo"""
        print(f"\n📄 Exportando relatório completo para '{nome_arquivo}'...")
        
        try:
            with open(nome_arquivo, 'w', encoding='utf-8') as f:
                # Cabeçalho
                f.write("="*70 + "\n")
                f.write("RELATÓRIO COMPLETO DA CASA INTELIGENTE\n")
                f.write(f"Gerado em: {datetime.now().strftime('%d/%m/%Y às %H:%M:%S')}\n")
                f.write("="*70 + "\n\n")
                
                # Gastos por categoria e mês
                f.write("1. GASTOS TOTAIS POR CATEGORIA E MÊS\n")
                f.write("-"*70 + "\n")
                
                gastos_categoria = Counter()
                gastos_mes = Counter()
                
                for conta in self.contas:
                    categoria = conta.get('categoria', 'Sem categoria') if isinstance(conta, dict) else getattr(conta, 'categoria', 'Sem categoria')
                    valor = conta.get('valor', 0) if isinstance(conta, dict) else getattr(conta, 'valor', 0)
                    data = conta.get('data_vencimento', 'Sem data') if isinstance(conta, dict) else getattr(conta, 'data_vencimento', 'Sem data')
                    
                    gastos_categoria[categoria] += valor
                    
                    if isinstance(data, str):
                        try:
                            mes_ano = data[:7]
                        except:
                            mes_ano = "Desconhecido"
                    else:
                        mes_ano = data.strftime("%Y-%m") if hasattr(data, 'strftime') else "Desconhecido"
                    
                    gastos_mes[mes_ano] += valor
                
                f.write("Por Categoria:\n")
                for categoria, total in gastos_categoria.most_common():
                    f.write(f"  {categoria}: R$ {total:.2f}\n")
                
                f.write("\nPor Mês:\n")
                for mes, total in sorted(gastos_mes.items(), reverse=True):
                    f.write(f"  {mes}: R$ {total:.2f}\n")
                
                total_geral = sum(gastos_categoria.values())
                f.write(f"\nTotal Geral: R$ {total_geral:.2f}\n\n")
                
                # Moradores com mais tarefas
                f.write("2. MORADORES COM MAIS TAREFAS PENDENTES\n")
                f.write("-"*70 + "\n")
                
                tarefas_por_morador = Counter()
                tarefas_pendentes_por_morador = Counter()
                
                for tarefa in self.tarefas:
                    responsavel = tarefa.get('responsavel', 'Desconhecido') if isinstance(tarefa, dict) else getattr(tarefa, 'responsavel', 'Desconhecido')
                    status = tarefa.get('status', 'pendente') if isinstance(tarefa, dict) else getattr(tarefa, 'status', 'pendente')
                    
                    tarefas_por_morador[responsavel] += 1
                    
                    if status.lower() in ['pendente', 'em progresso']:
                        tarefas_pendentes_por_morador[responsavel] += 1
                
                for morador, total in tarefas_por_morador.most_common():
                    pendentes = tarefas_pendentes_por_morador[morador]
                    f.write(f"  {morador}: {total} tarefas ({pendentes} pendentes)\n")
                
                f.write("\n")
                
                # Itens mais comprados e estoque crítico
                f.write("3. ITENS MAIS COMPRADOS E ESTOQUE CRÍTICO\n")
                f.write("-"*70 + "\n")
                
                f.write("Itens Mais Comprados:\n")
                itens_comprados = Counter()
                for item in self.estoque:
                    nome = item.get('nome', 'Desconhecido') if isinstance(item, dict) else getattr(item, 'nome', 'Desconhecido')
                    quantidade_comprada = item.get('quantidade_comprada', 0) if isinstance(item, dict) else getattr(item, 'quantidade_comprada', 0)
                    itens_comprados[nome] += quantidade_comprada
                
                for item, quantidade in itens_comprados.most_common(10):
                    f.write(f"  {item}: {quantidade} unidades\n")
                
                f.write("\nItens em Estoque Crítico (< 5 unidades):\n")
                estoque_baixo = []
                for item in self.estoque:
                    nome = item.get('nome', 'Desconhecido') if isinstance(item, dict) else getattr(item, 'nome', 'Desconhecido')
                    quantidade = item.get('quantidade', 0) if isinstance(item, dict) else getattr(item, 'quantidade', 0)
                    preco = item.get('preco', 0) if isinstance(item, dict) else getattr(item, 'preco_unitario', 0)
                    
                    if quantidade <= 5:
                        estoque_baixo.append({
                            'nome': nome,
                            'quantidade': quantidade,
                            'preco': preco
                        })
                
                if estoque_baixo:
                    for item in sorted(estoque_baixo, key=lambda x: x['quantidade']):
                        f.write(f"  {item['nome']}: {item['quantidade']} unidades (R$ {item['preco']:.2f} cada)\n")
                else:
                    f.write("  Nenhum item em estoque crítico.\n")
                
                f.write("\n")
                
                # Resumo geral
                f.write("4. RESUMO GERAL DA CASA\n")
                f.write("-"*70 + "\n")
                
                contas_pendentes = 0
                total_pendente = 0
                
                for conta in self.contas:
                    status = conta.get('status', 'pendente') if isinstance(conta, dict) else getattr(conta, 'status', 'pendente')
                    if status.lower() == 'pendente':
                        contas_pendentes += 1
                        total_pendente += conta.get('valor', 0) if isinstance(conta, dict) else getattr(conta, 'valor', 0)
                
                f.write(f"Contas Pendentes: {contas_pendentes} (Total: R$ {total_pendente:.2f})\n")
                
                estoque_critico = sum(
                    1 for item in self.estoque
                    if (item.get('quantidade', 0) if isinstance(item, dict) else getattr(item, 'quantidade', 0)) <= 5
                )
                f.write(f"Itens em Estoque Crítico: {estoque_critico}\n")
                
                manutencoes_urgentes = 0
                for manutencao in self.manutencoes:
                    status = manutencao.get('status', 'planejada') if isinstance(manutencao, dict) else getattr(manutencao, 'status', 'planejada')
                    prioridade = manutencao.get('prioridade', 'normal') if isinstance(manutencao, dict) else getattr(manutencao, 'prioridade', 'normal')
                    
                    if status.lower() in ['pendente', 'em progresso'] and prioridade.lower() == 'urgente':
                        manutencoes_urgentes += 1
                
                f.write(f"Manutenções Urgentes: {manutencoes_urgentes}\n")
                
                f.write("\n" + "="*70 + "\n")
                f.write("FIM DO RELATÓRIO\n")
                f.write("="*70 + "\n")
            
            print(f"✓ Relatório exportado com sucesso para '{nome_arquivo}'")
            return True
        
        except Exception as e:
            print(f"✗ Erro ao exportar relatório: {str(e)}")
            return False

    def menu_relatorios(self):
        """Menu interativo de relatórios"""
        while True:
            print("\n" + "="*60)
            print("SUBMENU - RELATÓRIOS E ESTATÍSTICAS")
            print("="*60)
            print("1. Gastos totais por categoria e mês")
            print("2. Moradores com mais tarefas pendentes")
            print("3. Itens mais comprados e estoque crítico")
            print("4. Resumo geral da casa")
            print("5. Exportar relatório completo")
            print("0. Voltar ao menu principal")
            print("="*60)
            
            opcao = input("Escolha uma opção: ").strip()
            
            if opcao == "1":
                self.gastos_por_categoria_e_mes()
            elif opcao == "2":
                self.moradores_com_mais_tarefas()
            elif opcao == "3":
                self.itens_mais_comprados_e_estoque_critico()
            elif opcao == "4":
                self.resumo_geral_casa()
            elif opcao == "5":
                nome = input("Nome do arquivo (padrão: relatorio_casa.txt): ").strip()
                if not nome:
                    nome = "relatorio_casa.txt"
                self.exportar_relatorio_completo(nome)
            elif opcao == "0":
                break
            else:
                print("Opção inválida!")
            
            input("\nPressione ENTER para continuar...")