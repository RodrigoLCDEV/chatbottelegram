from dataclasses import dataclass


@dataclass
class MensagemInicial:
    cliente : str
    saudacao : str    

@dataclass
class Comandos:
    comecar : str = "começar"
    pedido : str = "Iniciar pedido"
    finalizar_pedido : str = "Finalizar pedido"
    cancelar_pedido : str = "Cancelar pedido"

        


class Menssagem:
    # Classe de dialogos com usúario
    def __init__(self):
        self.MENSSAGEM_DADOS_PESSOAL: str = "verificamos em nosso sistema, e não encontramos o seu cadastro, digite as seguintes informações (Nome, Telefone, Endereço)"
        self.MENSSAGEM_INICIAL: str = "Seja bem-vindo (a) ao Cyber Burguer, para iniciar atendimento selecione o teclado digital na opção 'COMEÇAR'!"
        self.MENSSAGEM_FINALIZAR_PEDIDO: str = "Seu pedido foi realizado com sucesso."
        self.MESSAGEM_DE_ORIENTACAO: str = "Deseja continuar pedindo?"
        self.MENSSAGEM_CONTINUAR_DIGITANDO: str = "Ok, continue pedindo informando codído da opção e posterior a quantidade."
        self.MESSAGEM_DE_DECISAO_PEDIDO: str = "Deseja continuar pedindo?"
        self.MENSSAGEM_NAO_EXISTE_PEDIDO_PARA_FINALIZAR: str = "Não existe pedido a ser finalizado."
        self.MENSSAGEM_STATUS_PEDIDO: str = "O seu pedido está em andamento."
        self.MENSSAGEM_CANCELAR_PEDIDO: str = "Pedido cancelado com sucesso."
        self.MENSSAGEM_NAO_EXISTE_PEDIDO_PARA_CANCELAMENTO: str = "Não existe pedido a serem cancelados."
        self.MENSSAGEM_SUPERIOR_PEDIDO: str = "Infelizmente a quantidade informação não está disponivel, favor insira um novo código da opção do cardápio."
        self.MENSSAGEM_INFORMAR_QUANTIADE: str = "informe a quantidade?"
        self.ATENTIMENTO_FINALIZADO: str = " Por falta de iteração na comunicação, estamos finalizando o seu atendimento."
        self.MENSSAGEM_INFORMAR_CODIGO_PRODUTO: str = "Por favor, informe o codígo da opção desejada."
        self.MENSSAGEM_CARDAPIO: str = "Selecione o opção cardápio."
        self.ID_NAO_LOCALIZADO: str = "Não conseguimos identificar o codígo do produto, verifique o cardápio e insira o código da opção novamente!"
        self.MENSSAGEM_NAO_COMPREENDIDA: str = 'Desculpe, não consigo compreender sua mensagem. você pode digitar "ajudar" para adiquirir mais informações '
        self.conversas_iniciais: list = ["olá", "ola", "boa noite", "bom dia", "boa tarde", "oi",
                                         "tudo bem?", "tudo bem", "oi", "como vai",  "robô", "robo",  "pedir",  "comprar",  "ajuda"]
    

    
    def formatada(self, texto:str)->str:
        return "{}".format(texto)

    def solitar_quantidade(self, codigo_informado):
        return "Ok número da opção {}, {} ".format(codigo_informado, self.MENSSAGEM_INFORMAR_QUANTIADE)
  