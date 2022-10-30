

class ExtruturarMensagem:
    def __init__(self, cliente: str, menssagem: str = None, saudacao: str = None):
        self.cliente = cliente
        self.messagem = menssagem
        self.saudacao = saudacao


class Comandos:
    comecar = "começar"
    pedido = "Iniciar pedido"
    finalizar_pedido = "Finalizar pedido"
    cancelar_pedido = "Cancelar pedido"


class Menssagem:
    # Classe de dialogos com usúario
    def __init__(self):
        self.MENSSAGEM_FINALIZAR_PEDIDO: str = "Seu pedido foi realizado com sucesso."
        self.MESSAGEM_DE_ORIENTACAO: str = "Deseja continuar pedindo?"
        self.MENSSAGEM_CONTINUAR_DIGITANDO: str = "Ok, continue pedindo informando codído da opção e posterior a quantidade."
        self.MESSAGEM_DE_DECISAO_PEDIDO: str = "Deseja continuar pedindo?"
        self.MENSSAGEM_NAO_EXISTE_PEDIDO_PARA_FINALIZAR: str = "Não existe pedido a ser finalizado."
        self.MENSSAGEM_CANCELAR_PEDIDO: str = "Pedido cancelado com sucesso."
        self.MENSSAGEM_NAO_EXISTE_PEDIDO_PARA_CANCELAMENTO: str = "Não existe pedido a serem cancelados."
        self.MENSSAGEM_SUPERIOR_PEDIDO: str = "Infelizmente a quantidade informação não está disponivel."
        self.MENSSAGEM_INFORMAR_QUANTIADE: str = "informe a quantidade?"
        self.ATENTIMENTO_FINALIZADO: str = " Por falta de iteração na comunicação, estamos finalizando o seu atendimento."
        self.MENSSAGEM_INFORMAR_CODIGO_PRODUTO: str = "Por favor, informe o codígo da opção desejada."
        self.MENSSAGEM_CARDAPIO: str = "Selecione o opção cardápio."
        self.ID_NAO_LOCALIZADO: str = "Não conseguimos identificar o codígo do produto, tente novamente!"
        self.MENSSAGEM_NAO_COMPREENDIDA: str = f"Desculpe, não consigo compreender sua mensagem.\nDicas: comece a interação com o robô enviado uma menssagem por exemplo (oi, olá, boa noite , boa tarde, bom dia)."
        self.conversas_iniciais: list = ["olá", "ola", "boa noite", "bom dia", "boa tarde", "oi",
                                         "tudo bem?", "tudo bem", "oi", "como vai",  "robô", "robo",  "pedir",  "comprar",  "ajuda"]

    @property
    def sem_compreensao(self):
        return "{}".format(self.MENSSAGEM_NAO_COMPREENDIDA)

    @property
    def continuar_pedindo(self):
        return "{}".format(self.MESSAGEM_DE_DECISAO_PEDIDO)

    @property
    def mostrar_opcao_cardapio(self):
        return "{}".format(self.MENSSAGEM_CARDAPIO)

    @property
    def informe_numero_da_opcao(self):
        return "{}".format(self.MENSSAGEM_INFORMAR_CODIGO_PRODUTO)

    @property
    def codigo_nao_localizado(self):
        return "{}".format(self.ID_NAO_LOCALIZADO)

    @property
    def interromper_atendimento(self):
        return "{}".format(self.ATENTIMENTO_FINALIZADO)

    @property
    def quantidade_superior_ao_estoque(self):
        return "{}".format(self.MENSSAGEM_SUPERIOR_PEDIDO)

    @property
    def finalizacao_pedido(self):
        return "{}".format(self.MENSSAGEM_FINALIZAR_PEDIDO)

    @property
    def nao_existe_pedido_para_finalizar(self):
        return "{}".format(self.MENSSAGEM_NAO_EXISTE_PEDIDO_PARA_FINALIZAR)

    @property
    def cancelar_pedido(self):
        return "{}".format(self.MENSSAGEM_CANCELAR_PEDIDO)

    @property
    def nao_existe_pedido_para_cancelar(self):
        return "{}".format(self.MENSSAGEM_NAO_EXISTE_PEDIDO_PARA_CANCELAMENTO)

    @property
    def menssagem_de_orientacao(self):
        return "{}".format(self.MESSAGEM_DE_ORIENTACAO)

    @property
    def continuar_pedindo(self):
        return "{}".format(self.MENSSAGEM_CONTINUAR_DIGITANDO)

    def solitar_quantidade(self, codigo_informado):
        return "Ok número da opção {}, {} ".format(codigo_informado, self.MENSSAGEM_INFORMAR_QUANTIADE)
