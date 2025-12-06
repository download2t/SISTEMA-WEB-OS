from django.db import models

class ItemLavanderia(models.Model):
    nome = models.CharField(max_length=100)
    pesokg = models.DecimalField(max_digits=10, decimal_places=2)
    valormedio = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.nome

class RelatorioLav(models.Model):
    adata = models.DateTimeField()
    vrTotal = models.DecimalField(max_digits=10, decimal_places=2)
    pesoTotal = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Relatório {self.adata.strftime('%Y-%m-%d')}"

class ItemRelLavanderia(models.Model):
    relatorio = models.ForeignKey(RelatorioLav, on_delete=models.CASCADE)
    item_lavanderia = models.ForeignKey(ItemLavanderia, on_delete=models.CASCADE)
    qtd_itens = models.IntegerField()
    qtd_relavagens = models.IntegerField(default=0) 
    pesokg = models.DecimalField(max_digits=10, decimal_places=2,default=0)
    valormedio = models.DecimalField(max_digits=10, decimal_places=2,default=0)
    relavagemkg = models.DecimalField(max_digits=10, decimal_places=2,default=0)
    porcentagem_peso =models.DecimalField(max_digits=10, decimal_places=2,default=0)

    class Meta:
        unique_together = ('relatorio', 'item_lavanderia')

    def __str__(self):
        return f"{self.qtd_itens}x {self.item_lavanderia.nome} no relatório {self.relatorio.adata.strftime('%Y-%m-%d')}"


# ======= SISTEMA DE CONTROLE DE QUARTOS =======

class Funcionarios(models.Model):
    nome = models.CharField(max_length=100, verbose_name="Nome")
    cargo = models.CharField(max_length=100, verbose_name="Cargo")
    ativo = models.BooleanField(default=True, verbose_name="Ativo")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Funcionário"
        verbose_name_plural = "Funcionários"
        ordering = ['nome']

    def __str__(self):
        return f"{self.nome} - {self.cargo}"


class MotivoAusencia(models.Model):
    """Modelo para cadastro de motivos de ausência (férias, atestado, folga, etc.)"""
    nome = models.CharField(max_length=100, verbose_name="Nome do Motivo")
    descricao = models.TextField(blank=True, verbose_name="Descrição")
    cor = models.CharField(max_length=7, default="#dc3545", verbose_name="Cor (Hex)", 
                          help_text="Cor para identificação visual (ex: #FF0000)")
    ativo = models.BooleanField(default=True, verbose_name="Ativo")
    afeta_media = models.BooleanField(default=False, verbose_name="Afeta Média de Performance",
                                     help_text="Se marcado, este motivo será contado negativamente nas estatísticas")
    sistema = models.BooleanField(default=False, verbose_name="Motivo do Sistema",
                                 help_text="Motivos do sistema não podem ser editados ou excluídos")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Motivo de Ausência"
        verbose_name_plural = "Motivos de Ausência"
        ordering = ['nome']

    def __str__(self):
        return self.nome


class ControleQuartos(models.Model):
    """Modelo para controle diário de quartos com funcionários"""
    
    # Campos básicos
    data = models.DateField(verbose_name="Data")
    funcionario = models.ForeignKey(Funcionarios, on_delete=models.CASCADE, verbose_name="Funcionário")
    
    # Campo para motivo de ausência (opcional)
    motivo_ausencia = models.ForeignKey(
        MotivoAusencia, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        verbose_name="Motivo de Ausência",
        help_text="Se preenchido, este dia não contará para as metas"
    )
    
    # Metas (zeradas quando há motivo de ausência)
    permanece_entrada = models.IntegerField(default=0, verbose_name="Meta de Quartos que Permanecem")
    saida_entrada = models.IntegerField(default=0, verbose_name="Meta de Quartos de Saída")
    quantidade_quartos = models.IntegerField(default=16, verbose_name="Quantidade Total de Quartos")
    
    # Realizações (zeradas quando há motivo de ausência)
    reservas_realizadas = models.IntegerField(default=0, verbose_name="Reservas Realizadas", help_text="Quartos de saída do tipo reserva (já incluído no total de saídas)")
    permanece_realizadas = models.IntegerField(default=0, verbose_name="Entradas Realizadas")
    saidas_realizadas = models.IntegerField(default=0, verbose_name="Saídas Realizadas")
    
    # Cálculos automáticos
    realizados = models.IntegerField(default=0, verbose_name="Total Realizados")
    porcentagem = models.FloatField(default=0.0, verbose_name="Porcentagem (%)")
    
    # Metadados
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Controle de Quartos"
        verbose_name_plural = "Controles de Quartos"
        unique_together = ['data', 'funcionario']
        ordering = ['-data', 'funcionario__nome']

    def save(self, *args, **kwargs):
        """Calcula automaticamente os valores antes de salvar"""
        # Se há motivo de ausência
        if self.motivo_ausencia:
            # Para motivos que afetam média (como falta não justificada),
            # manter quantidade_quartos mas zerar realizações
            if self.motivo_ausencia.afeta_media:
                # Manter quantidade_quartos (ou definir padrão se não informado)
                if self.quantidade_quartos == 0:
                    self.quantidade_quartos = 16
                # Zerar apenas realizações
                self.permanece_entrada = 0
                self.saida_entrada = 0
                self.reservas_realizadas = 0
                self.permanece_realizadas = 0
                self.saidas_realizadas = 0
                self.realizados = 0
                self.porcentagem = 0.0  # 0% porque não realizou nada
            else:
                # Para motivos que não afetam média (folga, férias, etc.),
                # zerar tudo
                self.permanece_entrada = 0
                self.saida_entrada = 0
                self.quantidade_quartos = 0
                self.reservas_realizadas = 0
                self.permanece_realizadas = 0
                self.saidas_realizadas = 0
                self.realizados = 0
                self.porcentagem = 0.0
        else:
            # Calcular normalmente
            self.realizados = self.permanece_realizadas + self.saidas_realizadas
            realizados_base = self.permanece_realizadas + self.saidas_realizadas
            
            if self.quantidade_quartos > 0:
                self.porcentagem = (realizados_base / self.quantidade_quartos) * 100
            else:
                self.porcentagem = 0.0
        
        super().save(*args, **kwargs)

    def __str__(self):
        if self.motivo_ausencia:
            return f"{self.funcionario.nome} - {self.data.strftime('%d/%m/%Y')} - {self.motivo_ausencia.nome}"
        return f"{self.funcionario.nome} - {self.data.strftime('%d/%m/%Y')} - {self.porcentagem:.1f}%"

    @property
    def status_desempenho(self):
        """Retorna o status baseado na porcentagem"""
        if self.motivo_ausencia:
            return self.motivo_ausencia.nome
        
        if self.porcentagem >= 100:
            return "Excelente"
        elif self.porcentagem >= 80:
            return "Bom"
        elif self.porcentagem >= 60:
            return "Regular"
        else:
            return "Abaixo do Esperado"

    @property
    def meta_total(self):
        """Retorna a meta total (quantidade de quartos do dia)"""
        return self.quantidade_quartos

    @property
    def realizados_base(self):
        """Retorna apenas os realizados que contam para a porcentagem (sem reservas)"""
        return self.permanece_realizadas + self.saidas_realizadas

    def afeta_estatisticas(self):
        """Retorna se este controle deve afetar as estatísticas de média"""
        if not self.motivo_ausencia:
            return True  # Trabalho normal sempre conta
        return self.motivo_ausencia.afeta_media  # Só afeta se o motivo permite

    @classmethod
    def calcular_estatisticas_funcionario(cls, funcionario, data_inicio=None, data_fim=None):
        """Calcula estatísticas de um funcionário considerando apenas dias que afetam médias"""
        controles = cls.objects.filter(funcionario=funcionario)
        
        if data_inicio:
            controles = controles.filter(data__gte=data_inicio)
        if data_fim:
            controles = controles.filter(data__lte=data_fim)
        
        # Separar controles por tipo
        trabalho_normal = []
        ausencias_justificadas = []
        faltas_nao_justificadas = []
        
        for controle in controles:
            if not controle.motivo_ausencia:
                trabalho_normal.append(controle)
            elif controle.motivo_ausencia.afeta_media:
                faltas_nao_justificadas.append(controle)
            else:
                ausencias_justificadas.append(controle)
        
        # Calcular médias apenas com trabalho normal + faltas não justificadas
        controles_para_media = trabalho_normal + faltas_nao_justificadas
        
        if not controles_para_media:
            return {
                'total_dias': len(controles),
                'dias_trabalho': len(trabalho_normal),
                'dias_ausencia_justificada': len(ausencias_justificadas),
                'dias_falta_nao_justificada': len(faltas_nao_justificadas),
                'media_performance': 0,
                'total_quartos': 0,
                'total_realizados': 0,
            }
        
        total_quartos = sum(c.quantidade_quartos for c in controles_para_media)
        total_realizados = sum(c.realizados_base for c in controles_para_media)
        media_performance = (total_realizados / total_quartos * 100) if total_quartos > 0 else 0
        
        return {
            'total_dias': len(controles),
            'dias_trabalho': len(trabalho_normal),
            'dias_ausencia_justificada': len(ausencias_justificadas),
            'dias_falta_nao_justificada': len(faltas_nao_justificadas),
            'media_performance': media_performance,
            'total_quartos': total_quartos,
            'total_realizados': total_realizados,
        }

    @classmethod
    def calcular_estatisticas_gerais(cls, data_inicio=None, data_fim=None):
        """Calcula estatísticas gerais do sistema"""
        controles = cls.objects.all()
        
        if data_inicio:
            controles = controles.filter(data__gte=data_inicio)
        if data_fim:
            controles = controles.filter(data__lte=data_fim)
        
        # Filtrar apenas controles que afetam estatísticas
        controles_para_stats = [c for c in controles if c.afeta_estatisticas()]
        
        if not controles_para_stats:
            return {
                'total_registros': controles.count(),
                'media_porcentagem': 0,
                'total_quartos': 0,
                'total_realizados': 0,
            }
        
        total_quartos = sum(c.quantidade_quartos for c in controles_para_stats)
        total_realizados = sum(c.realizados_base for c in controles_para_stats)
        media_porcentagem = (total_realizados / total_quartos * 100) if total_quartos > 0 else 0
        
        return {
            'total_registros': controles.count(),
            'registros_para_media': len(controles_para_stats),
            'media_porcentagem': media_porcentagem,
            'total_quartos': total_quartos,
            'total_realizados': total_realizados,
        }
    def tipo_registro(self):
        """Retorna se é um registro normal ou de ausência"""
        return "ausencia" if self.motivo_ausencia else "normal"
