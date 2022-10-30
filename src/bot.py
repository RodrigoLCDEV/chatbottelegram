
import asyncio
import collections
import os
import time
from concurrent.futures import wait
from os import getenv
from typing import Union

from async_class import AsyncClass, AsyncObject, link, task
from asyncstdlib.builtins import map as ma
from asyncstdlib.builtins import tuple as tu
from dotenv import load_dotenv
from pyrogram import Client, enums, filters
from pyrogram.errors import FloodWait
from pyrogram.handlers import MessageHandler
from pyrogram.raw import functions, types
from pyrogram.types import (CallbackQuery, InlineKeyboardButton,
                            InlineKeyboardMarkup, InlineQueryResultArticle,
                            InputTextMessageContent, KeyboardButton, Message,
                            ReplyKeyboardMarkup)

from utils.botoes import Botao
from utils.dados import ListaProdutos
from utils.dialogo import Comandos, ExtruturarMensagem, Menssagem
from utils.jinja import JinjaTemplate
from utils.saudacao import Comprementar

# Carregar var de ambiente
load_dotenv()


Produtos = collections.namedtuple(
    "Produtos", ["id", "nome", "codigo_do_produto", "estoque", "foto", "descricao", "preco"])

Pedidos = collections.namedtuple(
    "Pedidos", ["id_cliente", "id", "nome", "codigo_do_produto", "estoque", "foto", "descricao", "preco", "quantidade_pedido"])


# Instânciar classe cliente
app = Client('cyberBurguerBot',
             api_id=getenv('APP_API_ID'),
             api_hash=getenv('APP_API_HASH'),
             bot_token=getenv('TOKEN_BOT_TELEGRAM'))


class CaminhoDaPasta:
    PASTA_PRINCIAL = "./src/"
    TEMPLATE_INICIAL = "{}{}".format(
        PASTA_PRINCIAL, "template/menssagem_inicial.html")
    TEMPLATE_CARDAPIO = "{}{}".format(PASTA_PRINCIAL, "template/cardapio.html")
    IMAGEM_LOGO = "{}{}".format(PASTA_PRINCIAL, "img/logo.jpg")
    TEMPLATE_PEDIDO = "{}{}".format(PASTA_PRINCIAL, "template/pedido.html")


class RegistrarPedido:
    def __init__(self):
        self.pedidos = []

    def adicionar_pedido(self, messagem):
        self._data.append(messagem)


class AnotacaoTemporariaPedido:
    def __init__(self):
        self.codigo: str = None
        self.quantidade: str = None

    def produto(self, codigo_produto):
        self.codigo = codigo_produto

    def quantidade_pedido(self, quatidade_produto):
        self.quantidade = quatidade_produto


class Situacao:
    def __init__(self):
        self.andamento_pedido: bool = False
        self.andamento_quantidade_pedido: bool = False
        self.andamento_cancelamento_pedido: bool = False
        self.andamento_finalizacao_pedido: bool = False

    def pedido(self, status: bool) -> None:
        self.andamento_pedido = status

    def quantidade(self, status: bool) -> None:
        self.andamento_quantidade_pedido = status

    def cancelamento(self, status: bool) -> None:
        self.andamento_cancelamento_pedido = status

    def finalizar(self, status: bool) -> None:
        self.andamento_finalizacao_pedido = status


situacao = Situacao()
registrar_pedido = RegistrarPedido()
messagem = Menssagem()
saudar = Comprementar()
anotacao_temporaria = AnotacaoTemporariaPedido()


async def answer(client, inline_query):
    # Assistente de ajuda
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


async def buscar_lista_produtos(produtos):
    return Produtos(
        produtos.get('id'),
        produtos.get('nome'),
        produtos.get('codigo_do_produto'),
        produtos.get('estoque'),
        produtos.get('foto'),
        produtos.get('descricao'),
        produtos.get('preco'),
    )


async def consultar_cadastros_produtos(produtos):
    # Função para consultar cadastro produto
    for produto in produtos:
        yield Produtos(
            produto.get('id'),
            produto.get('nome'),
            produto.get('codigo_do_produto'),
            produto.get('estoque'),
            produto.get('foto'),
            produto.get('descricao'),
            produto.get('preco'),
        )


@app.on_message(filters.command("start"))
async def conversa_inicial(client, message):
    # Função para inciar conversa
    # Messagem inicial de atendimento
    messagem = JinjaTemplate.template(
        CaminhoDaPasta.TEMPLATE_INICIAL, ExtruturarMensagem(cliente=message.chat.username, saudacao=saudar.pessoa()))
    await app.send_photo(message.chat.username, CaminhoDaPasta.IMAGEM_LOGO, caption="")
    await app.send_message(message.chat.username, str(messagem), parse_mode=enums.ParseMode.HTML, reply_markup=Botao.inicial)


async def messagem_nao_compreendida(client, message):
    # Função para sinalizar ha não compreensão da menssagem
    await app.send_message(message.chat.username, messagem.sem_compreensao)


async def oferecer_cardapio(client, message):
    # função para oferecer o cardápio ao cliente
    await message.reply(messagem.mostrar_opcao_cardapio, reply_markup=InlineKeyboardMarkup(Botao.cardapio))


@app.on_callback_query()
async def callback_query(client, callback_query):
    # Callback dos botões Iniline
    if callback_query.data == "comando_card":
        # Lista dos produtos
        produtos = await tu(ma(buscar_lista_produtos, ListaProdutos.produtos))
        # Criar renderização template: messagem cardápio
        messagem1 = JinjaTemplate.template(
            CaminhoDaPasta.TEMPLATE_CARDAPIO, produtos)
        # Enviar mensagem cardápio
        await callback_query.edit_message_text(messagem1, parse_mode=enums.ParseMode.HTML)
        # Criar renderização template: messagem pedido
        messagem2 = JinjaTemplate.template(
            CaminhoDaPasta.TEMPLATE_PEDIDO)
        await app.send_message(callback_query.message.chat.username, str(messagem2), parse_mode=enums.ParseMode.HTML, reply_markup=Botao.pedido)

    elif callback_query.data == "/sim":
        if situacao.andamento_pedido:
            await callback_query.edit_message_text(messagem.continuar_pedindo)

    elif callback_query.data == "/nao":
        if situacao.andamento_pedido:
            situacao.pedido(False)
            await app.send_message(callback_query.message.chat.username, messagem.menssagem_de_orientacao, parse_mode=enums.ParseMode.HTML, reply_markup=Botao.concluir_atendimento_pedido)


async def cancelar_atedimento(client, message):
    # Função encerra o atendimento após 5 minutos
    if situacao.andamento_pedido:
        situacao.pedido(False)
        await message.reply(messagem.interromper_atendimento)


async def verificar_atendimento_se_esta_ativo(client, message):
    # Função verificando a se o atendimento está ativo
    await asyncio.sleep(350)
    verificar_atendimento = asyncio.create_task(
        cancelar_atedimento(client, message))
    await verificar_atendimento


@app.on_message(filters.regex(Comandos.pedido))
async def iniciar_pedido(client, message):
    # Função ativar atendimento do pedido
    if not situacao.andamento_pedido:
        situacao.pedido(True)
        await message.reply(messagem.informe_numero_da_opcao)
        verificar_atendimento = asyncio.create_task(
            verificar_atendimento_se_esta_ativo(client, message))
        await verificar_atendimento


@app.on_message(filters.regex(Comandos.cancelar_pedido))
async def cancelamento_do_pedido(client, message):
    # Função para Finalização do pedido
    if registrar_pedido.pedidos:
        situacao.cancelamento(True)
        situacao.pedido(False)
        await message.reply(messagem.cancelar_pedido)
    else:
        await message.reply(messagem.informe_numero_da_opcao)


@app.on_message(filters.regex(Comandos.finalizar_pedido))
async def finalizar_pedido(client, message):
    # Função para finalizar o pedido
    if registrar_pedido.pedidos:
        # situacao.pedido(False)
        situacao.finalizar(True)
        await message.reply(messagem.finalizacao_pedido)
    else:
        await message.reply(messagem.nao_existe_pedido_para_cancelar)


async def consultar_numero_pedido(client, message) -> Union[object, None]:
    # Função para realizar consulta do pedido
    async for pedido in consultar_cadastros_produtos(ListaProdutos.produtos):
        if int(message.text) == pedido.id:
            return pedido
    return None


async def anotar_pedido(client, message) -> bool:
    # Função para realizar consulta do pedido
    async for pedido in consultar_cadastros_produtos(ListaProdutos.produtos):
        if int(anotacao_temporaria.codigo) == pedido.id:
            if int(anotacao_temporaria.quantidade) <= pedido.estoque:
                registrar_pedido.pedidos.append(
                    Pedidos(
                        id_cliente=0,
                        id=pedido.id,
                        nome=pedido.nome,
                        codigo_do_produto=pedido.codigo_do_produto,
                        estoque=pedido.estoque,
                        foto=pedido.foto,
                        descricao=pedido.descricao,
                        preco=pedido.preco,
                        quantidade_pedido=anotacao_temporaria.quantidade
                    )
                )
                break
            else:
                await message.reply(messagem.quantidade_superior_ao_estoque)
                return False
    return True


@app.on_message(filters.private)
async def monitoramento_dos_dialogos(client, message):

    if message.text.lower().isnumeric():

        if situacao.andamento_pedido and situacao.andamento_quantidade_pedido is False:

            # Consultar id produto
            consultar_codigo_pedido = await consultar_numero_pedido(client, message)

            if consultar_codigo_pedido:
                # Anotar codigo produto
                anotacao_temporaria.produto(message.text)
                # Ativar anotação da quantidade do produto
                situacao.quantidade(True)
                # Menssagem para informar quantidade do produto
                await message.reply(messagem.solitar_quantidade(message.text))
                return
            else:
                # Pedido não localizado
                await message.reply(messagem.codigo_nao_localizado)
                return

        if situacao.andamento_quantidade_pedido:
            # Anotar quantidade
            anotacao_temporaria.quantidade_pedido(message.text)

            # Anotar o pedido
            informar_nova_quantidade = await anotar_pedido(client, message)

            # Verificar se será necessário informar uma nova quantidade
            if informar_nova_quantidade:
                await message.reply(messagem.menssagem_de_orientacao, reply_markup=InlineKeyboardMarkup(Botao.decisao))
                situacao.quantidade(False)
                return
        return

     # Oferecer cardápio
    if message.text.lower() == Comandos.comecar:
        cardapio = asyncio.create_task(oferecer_cardapio(client, message))
        await cardapio
        return

    # menssagem de atendimento inicial
    if message.text.lower() in messagem.conversas_iniciais:
        conversa = asyncio.create_task(conversa_inicial(client, message))
        await conversa
        return

    # menssagem não compreendidas
    if not message.text.lower() in [Comandos.comecar, Comandos.pedido, Comandos.finalizar_pedido, Comandos.cancelar_pedido]:
        conversa = asyncio.create_task(
            messagem_nao_compreendida(client, message))
        await conversa
        return

if __name__ == '__main__':
    app.run()
