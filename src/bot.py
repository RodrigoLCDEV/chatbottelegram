import asyncio
import math
from dataclasses import asdict, dataclass, field
from datetime import datetime, time
from os import getenv
from pathlib import Path

from pyrogram import Client, enums, filters
from pyrogram.types import (CallbackQuery, InlineKeyboardButton,
                            InlineKeyboardMarkup, InlineQueryResultArticle,
                            InputTextMessageContent, KeyboardButton, Message,
                            ReplyKeyboardMarkup)
from tinydb import Query, TinyDB
from utils.botoes import Botao
from utils.dialogo import Comandos, MensagemInicial, Menssagem
from utils.jinja import JinjaTemplate
from utils.saudacao import Comprementar

# Instânciar classe cliente
app = Client('cyberBurguerBot',
             api_id=getenv('APP_API_ID'),
             api_hash=getenv('APP_API_HASH'),
             bot_token=getenv('TOKEN_BOT_TELEGRAM'))

class Arquivos:
    # Classe SETAR arquivosas
    def __init__(self):
        self.TEMPLATE_INICIAL = Path(__file__).parent / 'template/menssagem_inicial.html'
        self.TEMPLATE_CARDAPIO = Path(__file__).parent /'template/cardapio.html'
        self.TEMPLATE_PEDIDO = Path(__file__).parent /'template/pedido.html'
        self.TEMPLATE_EXTRATO = Path(__file__).parent /'template/extrato.html'
        self.IMAGEM_LOGO =  Path(__file__).parent / 'img/logo.jpg'
        self.JSON_ATENDIMENTO = Path(__file__).parent / 'json/dados_atendimento.json'    
        self.JSON_PRODUTOS: str= Path(__file__).parent / 'json/produtos.json'

@dataclass
class Controle:    
    id_cliente: str
    hora: str      
    status_pedido: bool = False
    status_quantidade: bool = False
    status_cancelamento: bool = False
    status_finalizacao_pedido: bool  = False               

    def as_dicionario(self):
        # Método converter dataclass para dicionario
        return asdict(self) 

@dataclass
class Registro:    
    id_cliente: str
    registro: int 
    codigo_do_produto : int                 

    def as_dicionario(self):
        # Método converter dataclass para dicionario
        return asdict(self)

@dataclass
class DadosPessoais:  
    id_cliente : int 
    nome_complete: str = None
    telefone: int = None
    endereco : int  = None                

    def as_dicionario(self):
        # Método converter dataclass para dicionario
        return asdict(self)             

@dataclass
class Pedido: 
    id: int
    nome: str
    codigo_do_produto: int    
    descricao: str
    preco: str
    id_cliente : int 
    quantidade_pedido : int = 0
    valor_total :  int = 0                  

    def as_dicionario(self):
        # Método converter dataclass para dicionarios
        return asdict(self)  

@dataclass
class Produtos:    
    id: int
    nome: str
    codigo_do_produto: int
    estoque: int
    foto = None
    descricao: str
    preco: str                 

    def as_dicionario(self):
        # Método converter dataclass para dicionario
        return asdict(self)        

class ControleDataclass:

    @classmethod
    def controle(cls, *args):
        # Método criar atendimento inicial      
        return Controle(*args).as_dicionario() 

    @classmethod
    def pedido(cls, *args):
        # Método criar pedido     
        return Pedido(*args).as_dicionario()    

    @classmethod
    def registro(cls, *args):
        # Método criar pedido     
        return Registro(*args).as_dicionario()     

    @classmethod
    def dados(cls, *args):
        # Método criar pedido     
        return DadosPessoais(*args).as_dicionario()     

# Instânciar classes auxiliar
arquivos = Arquivos()
messagem = Menssagem()
saudar = Comprementar()
db_controle = TinyDB(arquivos.JSON_ATENDIMENTO, indent=4)
notar_pedido = db_controle.table("Pedido")
registro = db_controle.table("Registro")
dados_pessoais = db_controle.table("DadosPessoais")
db_produtos = TinyDB(arquivos.JSON_PRODUTOS, indent=4)
consulta = Query()

async def answer(client, inline_query):
    # Função Assistente de ajuda ####Ajustar######
    await inline_query.answer(
        results=[
            InlineQueryResultArticle(
                title="Site Cyberburguer",
                input_message_content=InputTextMessageContent(
                    "Site *Cyberburguer**"
                ),
                url="https://docs.pyrogram.org/intro/install",
                description="Cardápio de opções",
                reply_markup=InlineKeyboardMarkup(
                    [
                        [InlineKeyboardButton(
                            "Abrir site",
                            url="https://docs.pyrogram.org/intro/install"
                        )]
                    ]
                )
            )
        ],
        cache_time=1
    )

@app.on_message(filters.private & filters.command("start"))
async def conversa_inicial(client, message):
    # Função para inciar conversa
    if not db_controle.search(consulta.id_cliente == message.chat.id): 
        # Lançar dados no arquivo json para o atendimento inicial
        db_controle.insert(ControleDataclass.controle(message.chat.id, message.date.strftime("%m/%d/%Y, %H:%M:%S")))   
    # Consulta será via request API - está forma é provisoria para fins de testes
    if not dados_pessoais.search(consulta.id_cliente == message.chat.id):          
        # Criar resgistro
        dados_pessoais.insert(ControleDataclass.dados(message.chat.id))
        await message.reply(f"{saudar.pessoa} {message.chat.username}, {messagem.formatada(messagem.__dict__['MENSSAGEM_DADOS_PESSOAL'])}")  
        return
    await app.send_message(message.chat.username, 
                           f"{saudar.pessoa} {message.chat.username}, {messagem.formatada(messagem.__dict__['MENSSAGEM_INICIAL'])}", 
                           reply_markup=Botao.inicial)    

async def messagem_nao_compreendida(client, message):
    # Função para sinalizar caso não haja compreensão da menssagem
    await app.send_message(message.chat.username, messagem.formatada(messagem.__dict__['MENSSAGEM_NAO_COMPREENDIDA']))

async def oferecer_cardapio(client, message):
    # função para oferecer o cardápio ao cliente   
    await message.reply(messagem.formatada(messagem.__dict__['MENSSAGEM_STATUS_PEDIDO']), reply_markup=InlineKeyboardMarkup(Botao.cardapio))

@app.on_message(filters.command('StatusPedido'))
async def status_pedido(client, message):
    await message.reply(messagem.formatada(messagem.__dict__['MENSSAGEM_STATUS_PEDIDO']))

@app.on_callback_query()
async def callback_query(client, callback_query):
    # Callback dos botões Iniline
    if callback_query.data == "comando_card":
        # Lista dos produtos        
        await app.send_message(callback_query.message.chat.username,JinjaTemplate.template(arquivos.TEMPLATE_CARDAPIO, db_produtos.all()), parse_mode=enums.ParseMode.HTML)
        await app.send_message(callback_query.message.chat.username, JinjaTemplate.template(arquivos.TEMPLATE_PEDIDO), parse_mode=enums.ParseMode.HTML, reply_markup=Botao.pedido)
    
    if callback_query.data == "/sim":
        # Desativar quantidade   
        db_controle.update({'status_quantidade': False}, consulta.id_cliente== callback_query.from_user.id)        
        await app.send_message(callback_query.message.chat.username, messagem.formatada(messagem.__dict__['MENSSAGEM_CONTINUAR_DIGITANDO']))
        
    if callback_query.data == "/nao":
        # Ponto de decisão do cliente    
        db_controle.update({'status_pedido': False}, consulta.id_cliente == callback_query.from_user.id)    
        await app.send_message(callback_query.message.chat.username, messagem.formatada(messagem.__dict__['MESSAGEM_DE_ORIENTACAO']), parse_mode=enums.ParseMode.HTML, reply_markup=Botao.concluir_atendimento_pedido)

async def controle_atendimentos():
    for dado in db_controle:
        yield Controle(**dado)

async def cancelar_atedimento():
    # Função encerra o atendimento após 5 minutos   
    async for atendimento in controle_atendimentos(): 
        # Delta
        agora = datetime.now()
        hora_atendimento =  datetime.strptime(atendimento.hora,"%m/%d/%Y, %H:%M:%S")        
        delta = agora - hora_atendimento
        if delta.seconds >= 350:
            # Exluir registros   
            enviar_mensagem =  db_controle.search((consulta.id_cliente== atendimento.id_cliente) & (consulta.status_finalizacao_pedido == True))      
            db_controle.remove(consulta.id_cliente== atendimento.id_cliente)
            registro.remove(consulta.id_cliente == atendimento.id_cliente)
            notar_pedido.remove(consulta.id_cliente == atendimento.id_cliente)
            dados_pessoais.remove(consulta.id_cliente == atendimento.id_cliente)
            if not enviar_mensagem:
                await app.send_message(atendimento.id_cliente, messagem.formatada(messagem.__dict__['ATENTIMENTO_FINALIZADO']))  

@app.on_message(filters.regex(Comandos.pedido))
async def iniciar_pedido(client, message):
    # Função ativar atendimento do pedido
    if db_controle.search((consulta.id_cliente == message.chat.id) & (consulta.status_pedido == False)):
        # Atualizar o status do atendimento do pedido 
        db_controle.update({'status_pedido': True}, consulta.id_cliente == message.chat.id)  
        db_controle.update({'status_cancelamento': True}, consulta.id_cliente == message.chat.id)
        await message.reply(messagem.formatada(messagem.__dict__['MENSSAGEM_INFORMAR_CODIGO_PRODUTO']))        
        await asyncio.sleep(500)        
        await cancelar_atedimento() 

@app.on_message(filters.regex(Comandos.cancelar_pedido))
async def cancelamento_do_pedido(client, message):
    # Função para Finalização do pedido
    if db_controle.search((consulta.id_cliente == message.chat.id) & (consulta.status_cancelamento == False)):
        db_controle.update({'status_cancelamento': True}, consulta.id_cliente == message.chat.id)
        notar_pedido.remove(consulta.id_cliente == message.chat.id)
        registro.remove(consulta.id_cliente == message.chat.id)
        dados_pessoais.remove(consulta.id_cliente == message.chat.id)
        await message.reply(messagem.__dict__['MENSSAGEM_CANCELAR_PEDIDO'])      

async def gerar_extrato(client, message) -> None:
    # Função para gerar extrato
    extratos = notar_pedido.search(consulta.id_cliente == message.chat.id)
    total  = [float(extrado.get('valor_total').replace(',','.')) for extrado in extratos]  
    template_menssagem = JinjaTemplate.template(arquivos.TEMPLATE_EXTRATO, extratos, f"{math.fsum(total):.2f}")
    await app.send_message(message.chat.username, str(template_menssagem), parse_mode=enums.ParseMode.HTML)
  
@app.on_message(filters.regex(Comandos.finalizar_pedido))
async def finalizar_pedido(client, message) -> None:
    # Função para finalizar o pedido
    db_controle.update({'status_finalizacao_pedido': True}, consulta.id_cliente == message.chat.id)    
    await message.reply(messagem.formatada(messagem.__dict__['MENSSAGEM_FINALIZAR_PEDIDO']))
    await gerar_extrato(client, message)

@ app.on_message(filters.private)
async def monitoramento_dos_dialogos(client, message) -> None:  
        
    
    if message.text.lower().isnumeric():        

        if db_controle.search((consulta.id_cliente == message.chat.id) & (consulta.status_quantidade == False)):
  
            if db_controle.search((consulta.id_cliente == message.chat.id) & (consulta.status_pedido == True)):              

                # Consulta será via request API - está forma é provisoria para fins de testes
                produtos = db_produtos.get(consulta.codigo_do_produto == int(message.text))

                if produtos:
                    if not notar_pedido.search((consulta.id_cliente == message.chat.id) & (consulta.codigo_do_produto == int(message.text))):
                        # Criar estrutura da anotação de pedido
                        numero_registro =    notar_pedido.insert(ControleDataclass.pedido(produtos.get('id'),
                                                                                                produtos.get('nome'),
                                                                                                produtos.get('codigo_do_produto'),
                                                                                                produtos.get('descricao'), 
                                                                                                produtos.get('preco'),
                                                                                                message.chat.id))  
                        
                        registro.remove((consulta.id_cliente == message.chat.id))                      
                        registro.insert(ControleDataclass.registro(message.chat.id, numero_registro, int(message.text)))
                    # Ativar status anotar quantidade do pedido 
                    db_controle.update({'status_quantidade': True}, consulta.id_cliente == message.chat.id)
                    # solicitar quantidade do produto.
                    await message.reply(messagem.solitar_quantidade(message.text))                                            
                else:                    
                    await message.reply(messagem.formatada(messagem.__dict__['ID_NAO_LOCALIZADO']))               
            return
        
        else:        
            # Consulta será via request API - está forma é provisoria para fins de testes
            consultar_produto = db_produtos.get(consulta.codigo_do_produto == registro.get(consulta.id_cliente == message.chat.id).get("codigo_do_produto"))

            if  consultar_produto.get("estoque") >= int(message.text):
                quantidade_pedido = notar_pedido.get(doc_id=registro.get(consulta.id_cliente == message.chat.id).doc_id).get("quantidade_pedido") + int(message.text)
                valor_total_pedido = quantidade_pedido * float(notar_pedido.get(doc_id=registro.get(consulta.id_cliente == message.chat.id).doc_id).get('preco'))
                notar_pedido.update({"quantidade_pedido": quantidade_pedido, "valor_total":  f"{valor_total_pedido:.2f}".replace('.',',')}, doc_ids=[registro.get(consulta.id_cliente == message.chat.id).doc_id])                       
            else:
                # Messagem: quantidade do produto indisponivel.
                await message.reply(messagem.formatada(messagem.__dict__['MENSSAGEM_SUPERIOR_PEDIDO']))                 
                notar_pedido.remove(doc_ids=[registro.get(consulta.id_cliente == message.chat.id).doc_id])                

            # Decisão: continuar pedido, sim / não?
            await message.reply(messagem.formatada(messagem.__dict__['MESSAGEM_DE_ORIENTACAO']), reply_markup=InlineKeyboardMarkup(Botao.decisao))
            return    

    if dados_pessoais.search((consulta.id_cliente == message.chat.id) & (consulta.endereco == None)):

        if dados_pessoais.search((consulta.id_cliente == message.chat.id) & (consulta.nome_complete == None)):
            dados_pessoais.update({'nome_complete': message.text}, consulta.id_cliente == message.chat.id)
            await message.reply("Seu nome foi cadastrado.")

        elif dados_pessoais.search((consulta.id_cliente == message.chat.id) & (consulta.telefone == None)):
            dados_pessoais.update({'telefone': message.text}, consulta.id_cliente == message.chat.id)
            await message.reply("Seu telefone foi cadastrado.")

        elif dados_pessoais.search((consulta.id_cliente == message.chat.id) & (consulta.endereco == None)):
            dados_pessoais.update({'endereco': message.text}, consulta.id_cliente == message.chat.id)
            await message.reply("Seu endereço foi cadastrado.") 
            await app.send_message(message.chat.username, "Para iniciar atendimento selecione o teclado digital na opção 'COMEÇAR'!", parse_mode=enums.ParseMode.HTML, reply_markup=Botao.inicial)     
        return      

    # Oferecer cardápio
    if message.text.lower() == Comandos.comecar:        
        await oferecer_cardapio(client, message)
        return

    # menssagem de primeiro atendimento
    if message.text.lower() in messagem.conversas_iniciais: 
        await conversa_inicial(client, message) 
        return       

    # menssagem não compreendida
    if not message.text.lower() in [Comandos.comecar, Comandos.pedido, Comandos.finalizar_pedido, Comandos.cancelar_pedido]:
        await messagem_nao_compreendida(client, message)
        return


if __name__ == "__main__":
    app.run()
