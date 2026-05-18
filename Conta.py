from datetime import datetime

class Conta:
    # Lista de categorias válidas
    CATEGORIAS_VALIDAS = ['água', 'luz', 'internet', 'aluguel', 'gás', 'telefone', 
                          'condomínio', 'seguro', 'saúde', 'educação', 'outro']
    
    # Armazena todas as contas
    contas = []
    
    def __init__(self, descricao=None, valor=None, data_vencimento=None, 
                 categoria=None, status='pendente'):
        """
        Inicializa uma nova conta.
        
        Args:
            descricao (str): Descrição da conta
            valor (float): Valor da conta
            data_vencimento (str): Data de vencimento no formato dd/mm/yyyy
            categoria (str): Categoria da conta
            status (str): Status da conta (pendente/pago)
        """
        self.descricao = descricao
        self.valor = valor
        self.data_vencimento = data_vencimento
        self.categoria = categoria
        self.status = status.lower()
        self.data_criacao = datetime.now().strftime("%d/%m/%Y")
    
    def registrar_conta(self):
        """Registra uma nova conta na lista"""
        if not self.validar_dados():
            print("✗ Erro: Dados inválidos!")
            return False
        
        Conta.contas.append(self)
        print(f"✓ Conta '{self.descricao}' registrada com sucesso!")
        return True
    
    def validar_dados(self):
        """Valida os dados da conta"""
        if not self.descricao or not str(self.descricao).strip():
            print("✗ Descrição inválida!")
            return False
        
        if not self.valor or self.valor <= 0:
            print("✗ Valor deve ser maior que zero!")
            return False
        
        if not self._validar_data(self.data_vencimento):
            print("✗ Data inválida! Use formato dd/mm/yyyy")
            return False
        
        if self.categoria.lower() not in self.CATEGORIAS_VALIDAS:
            print(f"✗ Categoria inválida! Categorias válidas: {', '.join(self.CATEGORIAS_VALIDAS)}")
            return False
        
        if self.status not in ['pendente', 'pago']:
            print("✗ Status deve ser 'pendente' ou 'pago'!")
            return False
        
        return True
    
    @staticmethod
    def _validar_data(data_str):
        """Valida se a data está no formato correto"""
        try:
            datetime.strptime(data_str, "%d/%m/%Y")
            return True
        except ValueError:
            return False
    
    @staticmethod
    def _converter_para_datetime(data_str):
        """Converte string de data para objeto datetime"""
        return datetime.strptime(data_str, "%d/%m/%Y")
    
    def marcar_como_pago(self):
        """Marca a conta como paga"""
        self.status = 'pago'
        print(f"✓ Conta '{self.descricao}' marcada como paga!")
        return True
    
    def marcar_como_pendente(self):
        """Marca a conta como pendente"""
        self.status = 'pendente'
        print(f"✓ Conta '{self.descricao}' marcada como pendente!")
        return True
    
    @classmethod
    def listar_contas_pendentes(cls):
        """Lista todas as contas com status pendente"""
        pendentes = [c for c in cls.contas if c.status == 'pendente']
        
        if not pendentes:
            print("Nenhuma conta pendente!")
            return
        
        print("\n" + "="*70)
        print("CONTAS PENDENTES")
        print("="*70)
        
        for idx, conta in enumerate(pendentes, 1):
            print(f"\n{idx}. {conta.descricao}")
            print(f"   Valor: R$ {conta.valor:.2f}")
            print(f"   Data de Vencimento: {conta.data_vencimento}")
            print(f"   Categoria: {conta.categoria.capitalize()}")
            print(f"   Status: {conta.status.upper()}")
    
    @classmethod
    def listar_contas_vencidas(cls):
        """Lista todas as contas vencidas (pendentes e com data anterior a hoje)"""
        hoje = datetime.now()
        vencidas = []
        
        for conta in cls.contas:
            if conta.status == 'pendente':
                data_vencimento = cls._converter_para_datetime(conta.data_vencimento)
                if data_vencimento < hoje:
                    vencidas.append(conta)
        
        if not vencidas:
            print("Nenhuma conta vencida!")
            return
        
        print("\n" + "="*70)
        print("CONTAS VENCIDAS")
        print("="*70)
        
        total_vencido = 0
        for idx, conta in enumerate(vencidas, 1):
            data_vencimento = cls._converter_para_datetime(conta.data_vencimento)
            dias_vencimento = (hoje - data_vencimento).days
            
            print(f"\n{idx}. {conta.descricao}")
            print(f"   Valor: R$ {conta.valor:.2f}")
            print(f"   Data de Vencimento: {conta.data_vencimento} ({dias_vencimento} dias atrás)")
            print(f"   Categoria: {conta.categoria.capitalize()}")
            
            total_vencido += conta.valor
        
        print(f"\n{'='*70}")
        print(f"TOTAL EM ATRASO: R$ {total_vencido:.2f}")
        print("="*70)
    
    @classmethod
    def listar_todas_contas(cls):
        """Lista todas as contas registradas"""
        if not cls.contas:
            print("Nenhuma conta registrada!")
            return
        
        print("\n" + "="*70)
        print("TODAS AS CONTAS")
        print("="*70)
        
        total_pendente = 0
        total_pago = 0
        
        for idx, conta in enumerate(cls.contas, 1):
            status_icon = "⏳" if conta.status == 'pendente' else "✓"
            
            print(f"\n{idx}. [{status_icon}] {conta.descricao}")
            print(f"   Valor: R$ {conta.valor:.2f}")
            print(f"   Data de Vencimento: {conta.data_vencimento}")
            print(f"   Categoria: {conta.categoria.capitalize()}")
            print(f"   Status: {conta.status.upper()}")
            
            if conta.status == 'pendente':
                total_pendente += conta.valor
            else:
                total_pago += conta.valor
        
        print(f"\n{'='*70}")
        print(f"RESUMO FINANCEIRO:")
        print(f"  Total Pendente: R$ {total_pendente:.2f}")
        print(f"  Total Pago: R$ {total_pago:.2f}")
        print(f"  Total Geral: R$ {total_pendente + total_pago:.2f}")
        print("="*70)
    
    @classmethod
    def listar_por_categoria(cls, categoria):
        """Lista todas as contas de uma categoria específica"""
        categoria = categoria.lower()
        contas_categoria = [c for c in cls.contas if c.categoria.lower() == categoria]
        
        if not contas_categoria:
            print(f"Nenhuma conta na categoria '{categoria}'!")
            return
        
        print(f"\n{'='*70}")
        print(f"CONTAS - CATEGORIA: {categoria.upper()}")
        print("="*70)
        
        total_categoria = 0
        for idx, conta in enumerate(contas_categoria, 1):
            print(f"\n{idx}. {conta.descricao}")
            print(f"   Valor: R$ {conta.valor:.2f}")
            print(f"   Data de Vencimento: {conta.data_vencimento}")
            print(f"   Status: {conta.status.upper()}")
            total_categoria += conta.valor
        
        print(f"\n{'='*70}")
        print(f"TOTAL NESTA CATEGORIA: R$ {total_categoria:.2f}")
        print("="*70)
    
    @classmethod
    def deletar_conta(cls, indice):
        """Deleta uma conta pelo índice"""
        try:
            conta = cls.contas.pop(indice)
            print(f"✓ Conta '{conta.descricao}' deletada com sucesso!")
            return True
        except IndexError:
            print("✗ Índice inválido!")
            return False
    
    def to_dict(self):
        """Retorna os dados da conta em formato de dicionário"""
        return {
            'descricao': self.descricao,
            'valor': self.valor,
            'data_vencimento': self.data_vencimento,
            'categoria': self.categoria,
            'status': self.status,
            'data_criacao': self.data_criacao
        }
    
    def __str__(self):
        """Representação em string da conta"""
        return f"Conta({self.descricao}, R${self.valor:.2f}, {self.status})"
    
    def __repr__(self):
        return self.__str__()