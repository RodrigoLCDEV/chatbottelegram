from pyrogram.types import (InlineKeyboardButton, InlineKeyboardMarkup,
                            InlineQueryResultArticle, InputTextMessageContent,
                            ReplyKeyboardMarkup)


class Botao:

    # Cardápio
    cardapio = [[InlineKeyboardButton(
        'Cardápio', callback_data="comando_card")]]

    decisao = [[
        InlineKeyboardButton('SIM', callback_data="/sim"),
        InlineKeyboardButton('NÂO', callback_data="/nao"),
    ]]

    # Botão COMEÇAR
    inicial = ReplyKeyboardMarkup(
        [[("COMEÇAR")]], one_time_keyboard=True, resize_keyboard=True)

    # Botão PEDIDO
    pedido = ReplyKeyboardMarkup(
        [[("Iniciar pedido")]], one_time_keyboard=True, resize_keyboard=True)

    # Botão PEDIDO
    concluir_atendimento_pedido = ReplyKeyboardMarkup(
        [[("Cancelar pedido"), ("Finalizar pedido")]], one_time_keyboard=True, resize_keyboard=True)
