from email.utils import collapse_rfc2231_value

import streamlit as st
import plotly.express as px
import pandas as pd

def filtro_prova_treino(df, resp):
    if resp == True:
        return df
    elif resp == '1':
        df = df[df['IN_TREINEIRO'] == '1']
        return df
    else:
        df = df[df['IN_TREINEIRO'] == '0']
        return df
#=======================================================================================
def filtro_alunos_sem_escola(df, resp):
    if resp == True:
        return df
    else:
        vet = ['1', '2', '3']
        df = df[df['TP_ENSINO'].isin(vet)]
        return df
# ========================filtro Sexualidade=============================================
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
#-======================================graficos===========================================================
#==========================================================================================================
def grafico_pizza (df, coluna, col1, col2, tile, map):
    info = df[coluna].map(map).value_counts().reset_index()
    info.columns = [col1 , col2]
    #st.write(info)
    cores_map = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd"]

    pizza = px.pie(info, names=col1, values=col2, color_discrete_sequence=cores_map, title=tile)
    pizza.update_traces(textfont_size=18)

    return st.plotly_chart(pizza, use_container_width=True)

def colunas_cruzadas (df, col1, col2):
    df_novo = pd.DataFrame()
    df_novo['ANOS'] = df['NU_ANO']
    df_novo[col1] = df[col1]
    df_novo[col2] = df[col2]
    def classificar (linha):
        a = linha[col1]
        b = linha[col2]

        if a == 'A' and b == 'A':
            return 'A'
        elif a != 'A' and b == 'A':
            return 'B'
        elif a == 'A' and b != 'A':
            return 'C'
        else:
            return 'D'

    df_novo['Veiculos'] = df.apply(classificar, axis=1)
    return df_novo

def multi (df, col1, col2):

    df= df.groupby([col1,col2]).size().reset_index(name='quantidade')

    #st.write(df)

    return df

def grafico_renda(df, col1, col2, col3, horientacao=False):
    df['percentual'] = (df['quantidade'] / df.groupby(col1)['quantidade'].transform('sum')) * 100
    df['label'] = df['percentual'].map('{:.1f}%'.format)

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
    else:
        barra = px.bar(
            df,
            x=col1,
            y=col2,
            color=col3,
            text=df["label"],
            orientation='v',
            barmode='group'
        )

    return st.plotly_chart(barra, use_container_width=True)

def grafico_teste(df):

    df = df.copy()

    # 🔥 garante que ano seja categórico
    df['NU_ANO'] = df['NU_ANO'].astype(str)

    # 🔥 calcula percentual dentro de cada ano
    df['percentual'] = (
        df['quantidade'] /
        df.groupby('NU_ANO')['quantidade'].transform('sum')
    ) * 100

    st.write(df)


    fig = px.bar(
        df,
        x='NU_ANO',
        y='percentual',
        color= 'quantidade' ,
        barmode='stack'
    )

    fig.update_traces(textposition='inside')

    fig.update_layout(
        title='Percentuais por ano e faixa de renda',
        yaxis=dict(
            title='Percentual',
            range=[0,100]   # 🔥 força 0 a 100%
        ),
        xaxis=dict(title='Anos'),
        legend_title='Faixa de renda',
        paper_bgcolor='white',
        plot_bgcolor='#EAEAEA'
    )

    return st.plotly_chart(fig, use_container_width=True)



def grafico_barra(df, coluna, col1, col2, titulo, orientacao, mapa=False, cat=None):
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

    # =============================================
    # Paleta de cores
    # =============================================
    paleta = ["#1f77b4", "#ff7f0e", "#2ca02c", "#d62728", "#9467bd"]
    cores = {cat: paleta[i % len(paleta)] for i, cat in enumerate(info[col1].unique())}
    info["cor"] = info[col1].map(cores)
    st.write(info)

    # =============================================
    # Criação do gráfico
    # =============================================
    if orientacao == 'h':
        info = info.sort_values(by=col2, ascending=True).reset_index(drop=True)
        barra = px.bar(
            info,
            x=col2,
            y=col1,
            text=info["Porcentagem"],
            orientation='h'
        )
    else:
        barra = px.bar(
            info,
            x=col1,
            y=col2,
            text=info["Porcentagem"],
            orientation='v',
            height=600
        )
    # =============================================
    # Ajustes visuais
    # =============================================
    barra.update_traces(
        marker_color=info["cor"],
        width=0.7,
        textfont=dict(family="Arial", size=20, color="black"),
        hoverinfo='x',
        marker=dict(line=dict(width=2, color='black'))
    )

    # Remove títulos de eixo (caso seja categórico)
    if cat:
        barra.update_xaxes(title_text='',
                           type='category',
                           tickfont=dict(
                               family="Arial",  # tipo de fonte
                               size=16,  # tamanho da fonte
                               color="black"  # cor da fonte
                                )
                           )
    barra.update_xaxes(title_text='',
                       tickfont=dict(
                           family="Arial",  # tipo de fonte
                           size=16,  # tamanho da fonte
                           color="black"  # cor da fonte
                            )
                       )
    barra.update_yaxes(title_text='',
                       tickfont=dict(
                            family="Arial",   # tipo de fonte
                            size=16,          # tamanho da fonte
                            color="black"     # cor da fonte
                            )
                       )

    # =============================================
    # Layout e borda
    # =============================================
    barra.update_layout(
        autosize=True,
        bargap=0.05,
        bargroupgap=0.0,
        showlegend=False,
        margin=dict(l=200, r=200, t=50, b=150),
        paper_bgcolor="white",
        plot_bgcolor="#E3E3E3",

        # Título estilizado
        title={
            'text': titulo,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'
        },
        title_font=dict(
            family="Arial Black",
            size=24,
            color="black"
        ),

        # Contorno externo (moldura)
        shapes=[dict(
            type="rect",
            xref="paper", yref="paper",
            x0=0, y0=0, x1=1, y1=1,
            line=dict(color="black", width=3)
        )]
    )

    return st.plotly_chart(barra, theme=None, use_container_width=True)
#========================================================================================================