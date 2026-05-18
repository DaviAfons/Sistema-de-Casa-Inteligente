import datetime

class ItemEstoque:
    itens = []
    
    def adicionarItem(self, nome, quantidade, preco, data_validade=None):
        """Adiciona um novo item ao estoque."""
        # Verifica se o item já existe
        for item in ItemEstoque.itens:
            if item['nome'].lower() == nome.lower():
                print(f"Item '{nome}' já existe no estoque. Use a função atualizar para modificá-lo.")
                return False
        
        # Valida a data de validade se fornecida
        if data_validade:
            try:
                datetime.datetime.strptime(data_validade, "%d/%m/%Y")
            except ValueError:
                print("Data de validade inválida. Use o formato dd/mm/aaaa")
                return False
        
        novo_item = {
            'nome': nome,
            'quantidade': quantidade,
            'preco': preco,
            'data_validade': data_validade
        }
        ItemEstoque.itens.append(novo_item)
        print(f"Item '{nome}' adicionado com sucesso!")
        return True
    
    def adicionarItemManual(self):
        """Adiciona um item através de entrada do usuário."""
        nome = input("Digite o nome do item (ex: arroz, leite, shampoo): ").strip()
        if not nome:
            print("Nome do item não pode estar vazio.")
            return
        
        try:
            quantidade = int(input("Digite a quantidade do item: "))
            preco = float(input("Digite o preço do item: "))
        except ValueError:
            print("Quantidade e preço devem ser números válidos.")
            return
        
        data_validade = input("Digite a data de validade (dd/mm/aaaa) ou deixe em branco se não houver: ").strip()
        if not data_validade:
            data_validade = None
        
        self.adicionarItem(nome, quantidade, preco, data_validade)
    
    def atualizarItem(self, nome, quantidade=None, preco=None, data_validade=None):
        """Atualiza um item existente no estoque."""
        for item in ItemEstoque.itens:
            if item['nome'].lower() == nome.lower():
                if quantidade is not None:
                    item['quantidade'] = quantidade
                if preco is not None:
                    item['preco'] = preco
                if data_validade is not None:
                    try:
                        datetime.datetime.strptime(data_validade, "%d/%m/%Y")
                        item['data_validade'] = data_validade
                    except ValueError:
                        print("Data de validade inválida. Use o formato dd/mm/aaaa")
                        return False
                print(f"Item '{nome}' atualizado com sucesso!")
                return True
        print(f"Item '{nome}' não encontrado no estoque.")
        return False
    
    def removerItem(self, nome):
        """Remove um item do estoque."""
        for item in ItemEstoque.itens:
            if item['nome'].lower() == nome.lower():
                ItemEstoque.itens.remove(item)
                print(f"Item '{nome}' removido do estoque.")
                return True
        print(f"Item '{nome}' não encontrado no estoque.")
        return False
    
    def estoqueAtual(self):
        """Exibe todos os itens do estoque atual."""
        if not ItemEstoque.itens:
            print("Estoque vazio!")
            return
        
        print("\n" + "=" * 60)
        print("ESTOQUE ATUAL")
        print("=" * 60)
        for i, item in enumerate(ItemEstoque.itens, 1):
            print(f"\n{i}. Nome: {item['nome']}")
            print(f"   Quantidade: {item['quantidade']} unidades")
            print(f"   Preço: R$ {item['preco']:.2f}")
            if item['data_validade']:
                print(f"   Data de Validade: {item['data_validade']}")
            else:
                print(f"   Data de Validade: Sem validade definida")
        print("\n" + "=" * 60)
    
    def alertasEstoqueBaixo(self):
        """Exibe itens com estoque baixo (< 3 unidades)."""
        itens_baixos = [item for item in ItemEstoque.itens if item['quantidade'] < 3]
        
        if not itens_baixos:
            print("Nenhum item com estoque baixo.")
            return
        
        print("\n" + "=" * 60)
        print("⚠️  ALERTA: ITENS COM ESTOQUE BAIXO (< 3 unidades)")
        print("=" * 60)
        for i, item in enumerate(itens_baixos, 1):
            print(f"\n{i}. Nome: {item['nome']}")
            print(f"   Quantidade: {item['quantidade']} unidades")
            print(f"   Preço: R$ {item['preco']:.2f}")
        print("\n" + "=" * 60)
    
    def alertasValidade(self):
        """Exibe itens próximos do vencimento ou vencidos."""
        hoje = datetime.datetime.now().date()
        itens_vencimento = []
        
        for item in ItemEstoque.itens:
            if item['data_validade']:
                try:
                    data_validade = datetime.datetime.strptime(item['data_validade'], "%d/%m/%Y").date()
                    # Alerta para itens que vão vencer em até 7 dias ou já venceram
                    if data_validade <= hoje + datetime.timedelta(days=7):
                        itens_vencimento.append({
                            'item': item,
                            'data': data_validade,
                            'dias': (data_validade - hoje).days
                        })
                except ValueError:
                    pass
        
        if not itens_vencimento:
            print("Nenhum item próximo do vencimento.")
            return
        
        print("\n" + "=" * 60)
        print("⚠️  ALERTA: ITENS PRÓXIMOS DO VENCIMENTO")
        print("=" * 60)
        for i, entrada in enumerate(itens_vencimento, 1):
            item = entrada['item']
            dias = entrada['dias']
            if dias < 0:
                status = f"VENCIDO há {abs(dias)} dias"
            elif dias == 0:
                status = "VENCE HOJE!"
            else:
                status = f"Vence em {dias} dias"
            
            print(f"\n{i}. Nome: {item['nome']}")
            print(f"   Quantidade: {item['quantidade']} unidades")
            print(f"   Preço: R$ {item['preco']:.2f}")
            print(f"   Data de Validade: {item['data_validade']}")
            print(f"   Status: {status}")
        print("\n" + "=" * 60)
    
    def alertasCompletos(self):
        """Exibe todos os alertas (estoque baixo e validade)."""
        print("\n" + "🔔 RELATÓRIO COMPLETO DE ALERTAS 🔔".center(60))
        self.alertasEstoqueBaixo()
        self.alertasValidade()
        