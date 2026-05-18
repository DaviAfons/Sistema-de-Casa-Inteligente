from collections import Counter


class Compras:
    """Gerenciador de lista de compras com categorias e status"""
    
    # Categorias válidas
    CATEGORIAS_VALIDAS = ['alimentos', 'higiene', 'limpeza', 'bebidas', 
                          'congelados', 'laticínios', 'frutas_vegetais', 'outro']
    
    # Itens sugeridos/essenciais que sempre devem estar em casa
    ITENS_ESSENCIAIS = {
        'alimentos': ['arroz', 'feijão', 'macarrão', 'pão', 'óleo', 'sal'],
        'higiene': ['papel higiênico', 'sabonete', 'escova de dentes', 'shampoo', 'desodorante'],
        'limpeza': ['detergente', 'desinfetante', 'esponja', 'pano', 'mop'],
        'bebidas': ['água', 'leite', 'suco'],
        'laticínios': ['leite', 'queijo', 'iogurte', 'manteiga']
    }
    
    # Lista global de compras
    lista_compras = []
    
    def __init__(self, nome, quantidade, categoria, preco_estimado=0.0, comprado=False):
        """
        Inicializa um item da lista de compras.
        
        Args:
            nome (str): Nome do item
            quantidade (float): Quantidade a comprar
            categoria (str): Categoria do item
            preco_estimado (float): Preço estimado do item
            comprado (bool): Status de compra
        """
        self.nome = nome
        self.quantidade = quantidade
        self.categoria = categoria.lower()
        self.preco_estimado = preco_estimado
        self.comprado = comprado
        self.unidade = 'unidade'  # padrão, pode ser alterado
    
    def adicionar_item(self):
        """Adiciona o item à lista de compras com validação"""
        if not self.validar_dados():
            print("✗ Erro: Dados inválidos!")
            return False
        
        Compras.lista_compras.append(self)
        print(f"✓ Item '{self.nome}' adicionado à lista de compras!")
        return True
    
    def validar_dados(self):
        """Valida os dados do item"""
        if not self.nome or not str(self.nome).strip():
            print("✗ Nome do item inválido!")
            return False
        
        if not self.quantidade or self.quantidade <= 0:
            print("✗ Quantidade deve ser maior que zero!")
            return False
        
        if self.categoria not in self.CATEGORIAS_VALIDAS:
            print(f"✗ Categoria inválida! Categorias válidas: {', '.join(self.CATEGORIAS_VALIDAS)}")
            return False
        
        if self.preco_estimado < 0:
            print("✗ Preço não pode ser negativo!")
            return False
        
        return True
    
    def marcar_como_comprado(self):
        """Marca o item como comprado"""
        self.comprado = True
        print(f"✓ Item '{self.nome}' marcado como comprado!")
        return True
    
    def marcar_como_nao_comprado(self):
        """Marca o item como não comprado"""
        self.comprado = False
        print(f"✓ Item '{self.nome}' marcado como não comprado!")
        return True
    
    @classmethod
    def item_comprado_por_nome(cls, nome):
        """Remove/marca um item como comprado pela busca de nome"""
        for item in cls.lista_compras:
            if item.nome.lower() == nome.lower():
                item.marcar_como_comprado()
                print(f"✓ Item '{nome}' marcado como comprado!")
                return True
        
        print(f"✗ Item '{nome}' não encontrado na lista de compras.")
        return False
    
    @classmethod
    def lista_compra_atual(cls):
        """Exibe a lista de compras atual"""
        if not cls.lista_compras:
            print("A lista de compras está vazia!")
            return
        
        print("\n" + "="*70)
        print("LISTA DE COMPRAS ATUAL")
        print("="*70)
        
        nao_comprados = [item for item in cls.lista_compras if not item.comprado]
        comprados = [item for item in cls.lista_compras if item.comprado]
        
        # Exibir itens não comprados
        if nao_comprados:
            print("\n📋 ITENS A COMPRAR:")
            print("-"*70)
            total_nao_comprado = 0
            for idx, item in enumerate(nao_comprados, 1):
                preco_total = item.preco_estimado * item.quantidade
                total_nao_comprado += preco_total
                
                print(f"{idx}. [{item.categoria.upper()}] {item.nome}")
                print(f"   Quantidade: {item.quantidade} {item.unidade}")
                if item.preco_estimado > 0:
                    print(f"   Preço Estimado: R$ {item.preco_estimado:.2f} (Total: R$ {preco_total:.2f})")
            
            print(f"\n   SUBTOTAL A COMPRAR: R$ {total_nao_comprado:.2f}")
        
        # Exibir itens comprados
        if comprados:
            print("\n✓ ITENS JÁ COMPRADOS:")
            print("-"*70)
            for idx, item in enumerate(comprados, 1):
                print(f"{idx}. [{item.categoria.upper()}] {item.nome} (COMPRADO)")
        
        print("="*70)
    
    @classmethod
    def buscar_por_categoria(cls, categoria):
        """Busca itens por categoria"""
        categoria = categoria.lower()
        
        if categoria not in cls.CATEGORIAS_VALIDAS:
            print(f"✗ Categoria inválida! Categorias válidas: {', '.join(cls.CATEGORIAS_VALIDAS)}")
            return
        
        itens_categoria = [item for item in cls.lista_compras if item.categoria == categoria]
        
        if not itens_categoria:
            print(f"Nenhum item na categoria '{categoria}'!")
            return
        
        print(f"\n{'='*70}")
        print(f"ITENS - CATEGORIA: {categoria.upper()}")
        print("="*70)
        
        total_categoria = 0
        nao_comprados = 0
        
        for idx, item in enumerate(itens_categoria, 1):
            status = "✓ COMPRADO" if item.comprado else "⏳ A COMPRAR"
            print(f"\n{idx}. {item.nome} [{status}]")
            print(f"   Quantidade: {item.quantidade} {item.unidade}")
            
            if item.preco_estimado > 0:
                preco_total = item.preco_estimado * item.quantidade
                print(f"   Preço Unitário: R$ {item.preco_estimado:.2f}")
                print(f"   Total: R$ {preco_total:.2f}")
                total_categoria += preco_total
            
            if not item.comprado:
                nao_comprados += 1
        
        print(f"\n{'='*70}")
        print(f"RESUMO DA CATEGORIA '{categoria.upper()}':")
        print(f"  Total de itens: {len(itens_categoria)}")
        print(f"  Itens a comprar: {nao_comprados}")
        print(f"  Itens comprados: {len(itens_categoria) - nao_comprados}")
        if total_categoria > 0:
            print(f"  Custo total estimado: R$ {total_categoria:.2f}")
        print("="*70)
    
    @classmethod
    def sugerir_itens_essenciais(cls):
        """Sugere itens essenciais que devem estar em casa"""
        print("\n" + "="*70)
        print("ITENS ESSENCIAIS SUGERIDOS")
        print("="*70)
        
        itens_nomes_atuais = [item.nome.lower() for item in cls.lista_compras]
        
        for categoria, itens in cls.ITENS_ESSENCIAIS.items():
            print(f"\n📌 {categoria.upper()}:")
            print("-"*70)
            
            for item in itens:
                if item.lower() in itens_nomes_atuais:
                    status = "✓ Já está na lista"
                else:
                    status = "⚠ Sugerido - não está na lista"
                
                print(f"  • {item.capitalize()}: {status}")
        
        print("\n" + "="*70)
    
    @classmethod
    def adicionar_item_essencial(cls, nome, quantidade=1):
        """Adiciona um item essencial à lista de compras"""
        nome = nome.lower()
        
        # Buscar a categoria do item essencial
        categoria_encontrada = None
        for categoria, itens in cls.ITENS_ESSENCIAIS.items():
            if nome in [item.lower() for item in itens]:
                categoria_encontrada = categoria
                break
        
        if categoria_encontrada:
            novo_item = cls(nome, quantidade, categoria_encontrada)
            if novo_item.adicionar_item():
                return True
        else:
            print(f"✗ Item '{nome}' não é um item essencial conhecido!")
            return False
    
    @classmethod
    def limpar_itens_comprados(cls):
        """Remove todos os itens marcados como comprados"""
        comprados = [item for item in cls.lista_compras if item.comprado]
        
        if not comprados:
            print("Nenhum item comprado para remover!")
            return False
        
        quantidade = len(comprados)
        cls.lista_compras = [item for item in cls.lista_compras if not item.comprado]
        
        print(f"✓ {quantidade} item(ns) comprado(s) removido(s) da lista!")
        return True
    
    @classmethod
    def listar_pendentes(cls):
        """Lista apenas itens que ainda não foram comprados"""
        pendentes = [item for item in cls.lista_compras if not item.comprado]
        
        if not pendentes:
            print("Nenhum item pendente de compra!")
            return
        
        print("\n" + "="*70)
        print("ITENS PENDENTES DE COMPRA")
        print("="*70)
        
        total_geral = 0
        for idx, item in enumerate(pendentes, 1):
            preco_total = item.preco_estimado * item.quantidade
            total_geral += preco_total
            
            print(f"\n{idx}. {item.nome}")
            print(f"   Categoria: {item.categoria.upper()}")
            print(f"   Quantidade: {item.quantidade} {item.unidade}")
            if item.preco_estimado > 0:
                print(f"   Preço: R$ {item.preco_estimado:.2f} (Total: R$ {preco_total:.2f})")
        
        print(f"\n{'='*70}")
        print(f"TOTAL A GASTAR: R$ {total_geral:.2f}")
        print("="*70)
    
    @classmethod
    def agrupar_por_categoria(cls):
        """Agrupa itens por categoria"""
        if not cls.lista_compras:
            print("A lista de compras está vazia!")
            return
        
        print("\n" + "="*70)
        print("LISTA DE COMPRAS AGRUPADA POR CATEGORIA")
        print("="*70)
        
        por_categoria = {}
        for item in cls.lista_compras:
            if item.categoria not in por_categoria:
                por_categoria[item.categoria] = []
            por_categoria[item.categoria].append(item)
        
        for categoria in sorted(por_categoria.keys()):
            itens = por_categoria[categoria]
            print(f"\n📌 {categoria.upper()}:")
            print("-"*70)
            
            for item in itens:
                status = "✓" if item.comprado else "⏳"
                print(f"  {status} {item.nome} - {item.quantidade} {item.unidade}")
                if item.preco_estimado > 0:
                    print(f"      R$ {item.preco_estimado:.2f} (Total: R$ {item.preco_estimado * item.quantidade:.2f})")
    
    @classmethod
    def deletar_item(cls, nome):
        """Deleta um item da lista de compras pelo nome"""
        for item in cls.lista_compras:
            if item.nome.lower() == nome.lower():
                cls.lista_compras.remove(item)
                print(f"✓ Item '{nome}' removido da lista!")
                return True
        
        print(f"✗ Item '{nome}' não encontrado!")
        return False
    
    @classmethod
    def limpar_lista(cls):
        """Limpa toda a lista de compras"""
        if cls.lista_compras:
            cls.lista_compras.clear()
            print("✓ Lista de compras limpa!")
            return True
        else:
            print("A lista já está vazia!")
            return False
    
    def to_dict(self):
        """Retorna os dados do item em formato de dicionário"""
        return {
            'nome': self.nome,
            'quantidade': self.quantidade,
            'categoria': self.categoria,
            'preco_estimado': self.preco_estimado,
            'comprado': self.comprado,
            'unidade': self.unidade
        }
    
    def __str__(self):
        """Representação em string do item"""
        status = "✓" if self.comprado else "⏳"
        return f"{status} {self.nome} ({self.quantidade} {self.unidade})"
    
    def __repr__(self):
        return self.__str__()