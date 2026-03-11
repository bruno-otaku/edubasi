from email.utils import collapse_rfc2231_value

import streamlit as st
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
from unicodedata import category


def filtro_prova_treino(df, resp):
    if resp == True:
        return df
    elif resp == '1':
        df = df[df['IN_TREINEIRO'] == '1']
        return df
    else:
        df = df[df['IN_TREINEIRO'] == '0']
        return df

def filtro_alunos_sem_escola(df, resp):
    if resp == True:
        return df
    else:
        vet = ['1', '2', '3']
        df = df[df['TP_ENSINO'].isin(vet)]
        return df

def filtro_multiselect(df, sexo, map, coluna):
    aux = []
    if len(sexo) > 0:
        for i in sexo:
            aux.append(map[i])
        df = df[df[coluna].isin(aux)]
        return df
    else:
        return df

def multicolunas(df, resp):
    if resp == 'Possui Nenhum':
        vet = [['A'], ['A']]
    elif resp == 'Possui Carro':
        vet = [['B','C','D','E'], ['A']]
    elif resp == 'Possui Moto':
        vet = [['A'], ['B','C','D','E']]
    elif resp == 'Possui Ambos':
        vet = [['B','C','D','E'], ['B','C','D','E']]
    else:
        return df
    df_filtrado = df[(df['Q010'].isin(vet[0])) & (df['Q011'].isin(vet[1]))]
    return df_filtrado

def grafico_pizza (df, coluna, col1, col2, tile, map=False, legenda_baixa=False, categoria=False):


    if map:
        #modifica direto no dataframe para reuso depois, não meche se não tiver uma alternativa de troca de logica 😑
        df[coluna] = df[coluna].map(map)
        info = df[coluna].value_counts().reset_index()
        info.columns = [col1 , col2]
    else:
        info = df[coluna].value_counts().reset_index()
        info.columns = [col1, col2]

    info = info.sort_values(by=col1)


    #st.write(info)
    #cores_map = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd"]

    if categoria:
        pizza = px.pie(info,
                       names=col1,
                       values=col2,
                       color=col2,
                       category_orders={
                           col1: categoria
                       },
                       title=tile)
    else:
        pizza = px.pie(info,
                       names=col1,
                       values=col2,
                       color=col2,
                       category_orders={
                           col1: sorted(info[col1].unique(), key=lambda x: x.lower())
                       },
                       title=tile)

    if legenda_baixa:
        pizza.update_layout(legend=dict(orientation = 'h',yanchor="middle",y=-0.99, xanchor="auto", x=0.1))

    else:

        pizza.update_layout(legend_title_text= 'Legenda')



    return st.plotly_chart(pizza, use_container_width=True)

def colunas_cruzadas (df, col1, col2):
    df_novo = pd.DataFrame()
    df_novo['ANOS'] = df['NU_ANO']
    df_novo[col1] = df[col1]
    df_novo[col2] = df[col2]
    #st.write(df_novo)
    def classificar (linha):
        a = linha[col1]
        b = linha[col2]

        if a == 'Não.' and b == 'Nenhuma.':
            return 'A'
        elif a != 'Não.' and b == 'Nenhuma.':
            return 'B'
        elif a == 'Não.' and b != 'Nenhuma.':
            return 'C'
        else:
            return 'D'

    df_novo['Veiculos'] = df.apply(classificar, axis=1)
    return df_novo

def multi (df, col1, col2, col3=False):

    if col3 == False:
        df= df.groupby([col1,col2]).size().reset_index(name='quantidade')
    else:
        df = df.groupby([col1,col2,col3]).size().reset_index(name='quantidade')

    #st.write(df)

    return df

def grafico_renda(df, col1, col2, col3, catego = False, horientacao=False, legenda_top=False):
    df = df.copy()
    df['percentual'] = (df['quantidade'] / df.groupby(col1)['quantidade'].transform('sum')) * 100
    df['label'] = df['percentual'].map('{:.1f}%'.format)


    if catego:
        st.write('passei aqui')
        if horientacao == 'h':
            barra=px.bar(
                df,
                x=col1,
                y=col2,
                color = col3,
                category_orders={col3: catego},
                text=df["label"],
                orientation='h',
                barmode = 'group'
            )
            barra.update_layout(
                xaxis=dict(title='Anos'),
                legend_title='Legenda',
                paper_bgcolor='white',
                plot_bgcolor='#EAEAEA'
            )
        else:
            barra = px.bar(
                df,
                x=col1,
                y=col2,
                color=col3,
                category_orders={col3: catego},
                text=df["label"],
                orientation='v',
                barmode='group')
    else:
        if horientacao == 'h':
            barra=px.bar(
                df,
                x=col1,
                y=col2,
                color = col3,
                text=df["label"],
                orientation='h',
                barmode = 'group'
            )
            barra.update_layout(
                xaxis=dict(title='Anos'),
                legend_title='Legenda',
                paper_bgcolor='white',
                plot_bgcolor='#EAEAEA'
            )
        else:
            barra = px.bar(
                df,
                x=col1,
                y=col2,
                color=col3,
                text=df["label"],
                orientation='v',
                barmode='group')

    if legenda_top:
        barra.update_layout(
            xaxis=dict(title='Anos'),
            legend_title='Legenda',
            paper_bgcolor='white',
            plot_bgcolor='#EAEAEA',
            legend=dict(
                orientation="h",
                yanchor="top",
                y=-0.25,  # controla o quão para baixo ela fica
                xanchor="center",
                x=0.5
            ),
            margin=dict(b=120)
        )
    else:
        barra.update_layout(
            xaxis=dict(title='Anos'),
            legend_title='Legenda',
            paper_bgcolor='white',
            plot_bgcolor='#EAEAEA'
        )




    return st.plotly_chart(barra, use_container_width=True)

def grafico_teste(df):

    df = df.copy()

    df_final = pd.concat([
        df,
        df.groupby('Q006', as_index=False)['quantidade']
        .sum()
        .assign(NU_ANO="todos")
    ], ignore_index=True)

    df_final['percentual'] = (df_final['quantidade'] /df_final.groupby('NU_ANO')['quantidade'].transform('sum')) * 100
    df_final["Porcentagem"] = df_final["percentual"].map("{:.2f}%".format)

    df_final['NU_ANO'] = df_final['NU_ANO'].astype(str)
    df_final['percentual_acumulado'] = (df_final.groupby(['NU_ANO'])['percentual'].cumsum())
    st.write(df_final)

    ordem = [
        "Nenhuma renda.",
        "Até 1 salário minímo.",
        "De 1  até 1 salário minímo e meio.",
        "De 1,5 até 2 salários minímo.",
        "De 2 até 2 salários minímo e meio",
        "De 2,5 até  3 salários minímo.",
        "De 3 até 4 salários minímo.",
        "De 4 até 5 salários minímo.",
        "De 5 até 6 salários minímo.",
        "De 6 até 7 salários minímo.",
        "De 7 até 8 salários minímo.",
        "De 8 até 9 salários minímo.",
        "De 9 até 10 salários minímo.",
        "De 10 até 12 salários minímo.",
        "De 12 até 15 salários minímo.",
        "De 15 até 20 salários minímo.",
        "Mais de 20 salários minímo."
    ]

    fig = px.bar(
        df_final,
        x='NU_ANO',
        y='percentual',
        color='Q006',
        category_orders={'Q006': ordem},
        barmode='stack'
    )

    fig.update_traces(textposition='inside')

    fig.update_layout(
        title='Percentuais por ano e faixa de renda',
        yaxis=dict(
            title='Percentual',
            range=[0,100]
        ),
        xaxis=dict(title='Anos'),
        legend_title='Faixa de renda',
        paper_bgcolor='white',
        plot_bgcolor='#EAEAEA'
    )

    return st.plotly_chart(fig, use_container_width=True)

def grafico_relative(df,col1,col2,col3,title):
    ordem = [
        "Nenhuma renda.",
        "Até 1 salário minímo.",
        "De 1  até 1 salário minímo e meio.",
        "De 1,5 até 2 salários minímo.",
        "De 2 até 2 salários minímo e meio",
        "De 2,5 até  3 salários minímo.",
        "De 3 até 4 salários minímo.",
        "De 4 até 5 salários minímo.",
        "De 5 até 6 salários minímo.",
        "De 6 até 7 salários minímo.",
        "De 7 até 8 salários minímo.",
        "De 8 até 9 salários minímo.",
        "De 9 até 10 salários minímo.",
        "De 10 até 12 salários minímo.",
        "De 12 até 15 salários minímo.",
        "De 15 até 20 salários minímo.",
        "Mais de 20 salários minímo."
    ]
    df[col3] = pd.Categorical(
        df[col3],
        categories=ordem,
        ordered=True
    )
    df = df.sort_values(col3)

    df['percentual'] = (
                   df['quantidade'] /
                   df.groupby(col1)['quantidade'].transform('sum')
           ) * 100
    df["Porcentagem"] = df["percentual"].map("{:.2f}%".format)


    df['percentual_acumulado'] = (df.groupby([col1])['percentual'].cumsum())
    df["Porcentagem_acumulada"] = df["percentual_acumulado"].map("{:.2f}%".format)

    #st.write(df)

    fig = px.bar(
        df,
        x=col1,
        y=col2,
        color=col3,
        hover_data={
            'Q006': True,
            'Porcentagem': True,
            'Porcentagem_acumulada': True,
            col1: False,
            'quantidade': False,
            'percentual': False,
            'percentual_acumulado': False
        },
        labels={
            'Q006': 'Faixa de salário',
            'Porcentagem': 'Percentual (%)',
            'Porcentagem_acumulada': 'Porcentagem acumulada (%)',
        },
        barmode='stack',
        orientation='v'
    )

    fig.update_traces(textposition='inside')

    fig.update_layout(
        title=title,
        yaxis=dict(
            title='Percentual',
            range=[0, 100]
        ),
        xaxis=dict(title=''),
        legend_title='Faixa de renda',
        paper_bgcolor='white',
        plot_bgcolor='#EAEAEA'
    )

    return st.plotly_chart(fig, use_container_width=True)

def grafico_barra(df, coluna, col1, col2, titulo, mapa=False):
    # =============================================
    # Pré-processamento
    # =============================================
    if mapa:
        info = df[coluna].map(mapa).value_counts().reset_index()
        info.columns = [col1, col2]
    else:
        info = df[coluna].value_counts().reset_index()
        info.columns = [col1, col2]

    # Calcula porcentagens
    total = info[col2].sum()
    info["percentual"] = info[col2] / total * 100
    info["Porcentagem"] = info["percentual"].map("{:.2f}%".format)

    info = info.sort_values(by=col1)

    barra = px.bar(
        info,
        x=col1,
        y=col2,
        text=info["Quantidade"],
        orientation='v',
        barmode='stack',


    )



    barra.update_layout(
        xaxis=dict(title='Anos'),
        legend_title='Legenda',
        paper_bgcolor='white',
        plot_bgcolor='#EAEAEA'
    )
    barra.update_xaxes(type="category")

    return st.plotly_chart(barra, use_container_width=True)

def classes(df):

    df_tratado = df
    clas_F = ['Nenhuma renda.']
    clas_A = ['Mais de 20 salários minímo.']
    clas_B = ['De 10 até 12 salários minímo.', 'De 12 até 15 salários minímo.', 'De 15 até 20 salários minímo.']
    clas_C = ['De 4 até 5 salários minímo.',
              'De 5 até 6 salários minímo.',
              'De 6 até 7 salários minímo.',
              'De 7 até 8 salários minímo.',
              'De 8 até 9 salários minímo.',
              'De 9 até 10 salários minímo.']
    clas_D = ['De 2 até 2 salários minímo e meio',
              'De 2,5 até  3 salários minímo.',
              'De 3 até 4 salários minímo.']
    clas_E = ['Até 1 salário minímo.',
              'De 1  até 1 salário minímo e meio.',
              'De 1,5 até 2 salários minímo.']


    vet = [clas_F,clas_A, clas_B, clas_C, clas_D, clas_E]

    # transformação de registros para um compreensivel
    df_tratado['Q006'] = df_tratado['Q006'].replace(vet[0], 'Sem Rendimento')
    df_tratado['Q006'] = df_tratado['Q006'].replace(vet[1], 'Classe A')
    df_tratado['Q006'] = df_tratado['Q006'].replace(vet[2], 'Classe B')
    df_tratado['Q006'] = df_tratado['Q006'].replace(vet[3], 'Classe C')
    df_tratado['Q006'] = df_tratado['Q006'].replace(vet[4], 'Classe D')
    df_tratado['Q006'] = df_tratado['Q006'].replace(vet[5], 'Classe E')


    return df_tratado

def mapeamento(select):
    # ====================================================================================================================
    if select == 'Na sua residência tem telefone fixo?':

        map = {
            'A' : 'Nâo',
            'B' : 'Sim'
        }
        vet = [
            'Q023',
            'Possui telefone fixo?',
            'Quantidades de respostas',
            'Possuem telefone fixo?',
            map,
            None,
            None
        ]
        return vet
    # ====================================================================================================================
    elif select == 'Até que série seu pai, ou o homem responsável por você, estudou?':

        mapa_escolaridade = {
            'A': "Nunca estudou.",
            'B': "Não completou a 4ª série/5º ano do Ensino Fundamental.",
            'C': "Completou a 4ª série/5º ano, mas não completou a 8ª série/9º ano do Ensino Fundamental.",
            'D': "Completou a 8ª série/9º ano do Ensino Fundamental, mas não completou o Ensino Médio.",
            'E': "Completou o Ensino Médio, mas não completou a Faculdade.",
            'F': "Completou a Faculdade, mas não completou a Pós-graduação.",
            'G': "Completou a Pós-graduação.",
            'H': "Não sei."
        }

        vet = [
            'Q001',
            'Até que série o pai ou homem responsável fez:',
            'Quantidade de respostas',
            'Até que série seu pai, ou o homem responsável por você, estudou?',
            mapa_escolaridade,
            None,
            True
        ]
        return vet
    # ====================================================================================================================
    elif select == 'Até que série sua mãe, ou a mulher responsável por você, estudou?':

        map = {
            'A': "Nunca estudou.",
            'B': "Não completou a 4ª série/5º ano do Ensino Fundamental.",
            'C': "Completou a 4ª série/5º ano, mas não completou a 8ª série/9º ano do Ensino Fundamental.",
            'D': "Completou a 8ª série/9º ano do Ensino Fundamental, mas não completou o Ensino Médio.",
            'E': "Completou o Ensino Médio, mas não completou a Faculdade.",
            'F': "Completou a Faculdade, mas não completou a Pós-graduação.",
            'G': "Completou a Pós-graduação.",
            'H': "Não sei."
        }
        vet = [
            'Q002',
            'Até que série a mãe ou mulher responsável fez:',
            'Quantidade de respostas',
            'Até que série a mãe, ou mullher responsável por você, estudou?',
            map,
            None,
            True
        ]
        return vet
    # ====================================================================================================================
    elif select == 'A partir da apresentação de algumas ocupações divididas em grupos ordenados, indique o grupo que contempla a ocupação mais próxima da ocupação do seu pai ou do homem responsável por você. (Se ele não estiver trabalhando, escolha uma ocupação pensando no último trabalho dele).':

        map = {
            "A": "Grupo 1: Lavrador, agricultor sem empregados, bóia fria, criador de animais (gado, porcos, galinhas, ovelhas, cavalos etc.), apicultor, pescador, lenhador, seringueiro, extrativista.",

            "B": "Grupo 2: Diarista, empregado doméstico, cuidador de idosos, babá, cozinheiro (em casas particulares), motorista particular, jardineiro, faxineiro de empresas e prédios, vigilante, porteiro, carteiro, office-boy, vendedor, caixa, atendente de loja, auxiliar administrativo, recepcionista, servente de pedreiro, repositor de mercadoria.",

            "C": "Grupo 3: Padeiro, cozinheiro industrial ou em restaurantes, sapateiro, costureiro, joalheiro, torneiro mecânico, operador de máquinas, soldador, operário de fábrica, trabalhador da mineração, pedreiro, pintor, eletricista, encanador, motorista, caminhoneiro, taxista.",

            "D": "Grupo 4: Professor (de ensino fundamental ou médio, idioma, música, artes etc.), técnico (de enfermagem, contabilidade, eletrônica etc.), policial, militar de baixa patente (soldado, cabo, sargento), corretor de imóveis, supervisor, gerente, mestre de obras, pastor, microempresário (proprietário de empresa com menos de 10 empregados), pequeno comerciante, pequeno proprietário de terras, trabalhador autônomo ou por conta própria.",

            "E": "Grupo 5: Médico, engenheiro, dentista, psicólogo, economista, advogado, juiz, promotor, defensor, delegado, tenente, capitão, coronel, professor universitário, diretor em empresas públicas ou privadas, político, proprietário de empresas com mais de 10 empregados.",

            "F": "Não sei."
        }
        vet = [
            'Q003',
            'Grupo que contempla a ocupação mais próxima da ocupação do pai ou do homem responsável',
            'Quantidade de respostas',
            'Grupo que contempla a ocupação mais próxima da ocupação do pai ou do homem responsável',
            map,
            None,
            True
        ]
        return vet
    # ====================================================================================================================
    elif select == 'A partir da apresentação de algumas ocupações divididas em grupos ordenados, indique o grupo que contempla a ocupação mais próxima da ocupação da sua mãe ou da mulher responsável por você. (Se ela não estiver trabalhando, escolha uma ocupação pensando no último trabalho dela).':

        map = {
            "A": "Grupo 1: Lavradora, agricultora sem empregados, bóia fria, criadora de animais (gado, porcos, galinhas, ovelhas, cavalos etc.), apicultora, pescadora, lenhadora, seringueira, extrativista.",

            "B": "Grupo 2: Diarista, empregada doméstica, cuidadora de idosos, babá, cozinheira (em casas particulares), motorista particular, jardineira, faxineira de empresas e prédios, vigilante, porteira, carteira, office-boy, vendedora, caixa, atendente de loja, auxiliar administrativa, recepcionista, servente de pedreiro, repositora de mercadoria.",

            "C": "Grupo 3: Padeira, cozinheira industrial ou em restaurantes, sapateira, costureira, joalheira, torneira mecânica, operadora de máquinas, soldadora, operária de fábrica, trabalhadora da mineração, pedreira, pintora, eletricista, encanadora, motorista, caminhoneira, taxista.",

            "D": "Grupo 4: Professora (de ensino fundamental ou médio, idioma, música, artes etc.), técnica (de enfermagem, contabilidade, eletrônica etc.), policial, militar de baixa patente (soldado, cabo, sargento), corretora de imóveis, supervisora, gerente, mestre de obras, pastora, microempresária (proprietária de empresa com menos de 10 empregados), pequena comerciante, pequena proprietária de terras, trabalhadora autônoma ou por conta própria.",

            "E": "Grupo 5: Médica, engenheira, dentista, psicóloga, economista, advogada, juíza, promotora, defensora, delegada, tenente, capitã, coronel, professora universitária, diretora em empresas públicas ou privadas, política, proprietária de empresas com mais de 10 empregados.",

            "F": "Não sei."
        }
        vet = [
            'Q004',
            'Grupo que contempla a ocupação mais próxima da ocupação da mãe ou da mulher responsável',
            'Quantidade de respostas',
            'Grupo que contempla a ocupação mais próxima da ocupação da mãe ou da mulher responsável',
            map,
            None,
            True
        ]
        return vet
    # ====================================================================================================================
    elif select == 'Incluindo você, quantas pessoas moram atualmente em sua residência?':

        map = {
            "1": "1, pois moro sozinho(a).",
            "2": "2",
            "3": "3",
            "4": "4",
            "5": "5",
            "6": "6",
            "7": "7",
            "8": "8",
            "9": "9",
            "10": "10",
            "11": "11",
            "12": "12",
            "13": "13",
            "14": "14",
            "15": "15",
            "16": "16",
            "17": "17",
            "18": "18",
            "19": "19",
            "20": "20"
        }
        vet = [
            'Q005',
            'Quantidade de pessoas que moram na residência',
            'Quantidade de respostas',
            'Quantidade de pessoas que moram na residência',
            map,
            None,
            None
        ]
        return vet
    #====================================================================================================================
    elif select == 'Na sua residência tem geladeira?':

        map = {
            "A": "Não.",
            "B": "Sim, uma.",
            "C": "Sim, duas.",
            "D": "Sim, três.",
            "E": "Sim, quatro ou mais."
        }
        vet = [
            'Q012',
            'Possue geladeira?',
            'Quantidade de respostas',
            'Possue geladeira?',
            map,
            None,
            None
        ]
        return vet
    # ====================================================================================================================
    elif select == 'Na sua residência tem freezer (independente ou segunda porta da geladeira)?':

        map = {
            "A": "Não.",
            "B": "Sim, um.",
            "C": "Sim, dois.",
            "D": "Sim, três.",
            "E": "Sim, quatro ou mais."
        }
        vet = [
            'Q013',
            'Possue freezer?',
            'Quantidade de respostas',
            'Possue freezer?',
            map,
            None,
            None
        ]
        return vet
    # ====================================================================================================================
    elif select == 'Na sua residência tem máquina de secar roupa (independente ou em conjunto com a máquina de lavar roupa)?':

        map = {
            "A": "Não.",
            "B": "Sim, um.",
            "C": "Sim, dois.",
            "D": "Sim, três.",
            "E": "Sim, quatro ou mais."
        }
        vet = [
            'Q015',
            'Possue maquina de secar roupa?',
            'Quantidade de respostas',
            'Possue maquina de secar roupa?',
            map,
            None,
            None
        ]
        return vet
    # ====================================================================================================================
    elif select == 'Na sua residência tem máquina de lavar louça?':

        map = {
            "A": "Não.",
            "B": "Sim, um.",
            "C": "Sim, dois.",
            "D": "Sim, três.",
            "E": "Sim, quatro ou mais."
        }
        vet = [
            'Q017',
            'Possue máquina de lavar louça?',
            'Quantidade de respostas',
            'Possue máquina de lavar louça?',
            map,
            None,
            None
        ]
        return vet
    # ====================================================================================================================
    elif select == 'Na sua residência tem aspirador de pó?':

        map = {
            'A': 'Nâo',
            'B': 'Sim'
        }
        vet = [
            'Q018',
            'Possue aspirador de pó?',
            'Quantidade de respostas',
            'Possue aspirador de pó?',
            map,
            None,
            None
        ]
        return vet
    # ====================================================================================================================
    elif select == 'Na sua residência tem aparelho de DVD?':

        map = {
            'A': 'Nâo',
            'B': 'Sim'
        }
        vet = [
            'Q020',
            'Possue aparelho de DVD?',
            'Quantidade de respostas',
            'Possue aparelho de DVD?',
            map,
            None,
            None
        ]
        return vet
    # ====================================================================================================================
    elif select == 'Na sua residência tem TV por assinatura?':

        map = {
            'A': 'Nâo',
            'B': 'Sim'
        }
        vet = [
            'Q021',
            'Possue TV por assinatura?',
            'Quantidade de respostas',
            'Possue TV por assinatura?',
            map,
            None,
            None
        ]
        return vet
    # ====================================================================================================================
    else:
        st.write("não caiu em nenhuma opção")
    '''''
    elif select == 'Você já concluiu ou está concluindo o Ensino Médio?':

        map = {
            "A": "Já concluí o Ensino Médio.",
            "B": "Estou cursando e concluirei o Ensino Médio em 2018.",
            "C": "Estou cursando e concluirei o Ensino Médio após 2018.",
            "D": "Não concluí e não estou cursando o Ensino Médio."
        }
        vet = [
            'Q026',
            'Concluiu ou está concluindo o Ensino Médio?',
            'Quantidade de respostas',
            'Concluiu ou está concluindo o Ensino Médio?',
            map
        ]
        return vet
    # ====================================================================================================================
    elif select == 'Em que tipo de escola você frequentou o Ensino Médio?':

        map = {
            "A": "Somente em escola pública.",
            "B": "Parte em escola pública e parte em escola privada SEM bolsa de estudo integral.",
            "C": "Parte em escola pública e parte em escola privada COM bolsa de estudo integral.",
            "D": "Somente em escola privada SEM bolsa de estudo integral.",
            "E": "Somente em escola privada COM bolsa de estudo integral.",
            "F": "Não frequentei a escola."
        }
        vet = [
            'Q027',
            'Tipo de escola frequentada no Ensino Médio?',
            'Quantidade de respostas',
            'Tipo de escola frequentada no Ensino Médio?',
            map
        ]
        return vet
    # ====================================================================================================================
    '''''
