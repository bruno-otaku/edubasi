from importlib.resources import contents

import streamlit as st
import pandas as pd
import funcao_social as fs
from fontTools.cffLib import FDSelect
from streamlit import sidebar
import edubasi



def pagina_enem_social():
    edubasi.iniciar_sessao()
    
    st.title("Perspectiva Social")
    aux = []
    texto=''
    for ano in edubasi.obter_anos_selecionados():
        df = edubasi.obter_dados(ano = ano, id_municipio = edubasi.obter_municipio_selecionado())
        aux.append(df)
        texto += f"{ano}, "

    st.write(texto[:-2])
    df_original = pd.concat(aux, ignore_index=True, sort=False)

#====================== Cabeçalho ==============================================

    st.write("Município único selecionado:", edubasi.obter_municipio_selecionado())
    #st.write("Municípios múltiplos selecionados:", edubasi.obter_municipios_selecionados())



#==================================================================================================
# ==============================Cabeçalho do filtro================================================
    with sidebar:
        st.header("Filtros da pagina Social")
        with st.expander('Geral'):
# ==============================================Pensar em uma solução melhor\ tem que clicar duas vezes pra funcionar=======================================================
            lista_anos = edubasi.obter_anos()
            anos = st.multiselect(
                "Escolha os anos de análise:",
                lista_anos,
                default=edubasi.obter_anos_selecionados(),
                placeholder="Selecione ao menos um ano"
            )

            if not anos:
                st.warning("Escolha, pelo menos, um ano de análise.")
            else:
                #edubasi.selecionar_anos(anos)
                aux = []
                for ano in anos:
                    df = edubasi.obter_dados(ano=ano, id_municipio=edubasi.obter_municipio_selecionado())
                    aux.append(df)
                df_original = pd.concat(aux, ignore_index=True, sort=False)
                cont = len(df_original)
#=====================================================================================================

            resp = st.checkbox('Incluir estudantes sem informação de escola', value=True)
            df = fs.filtro_alunos_sem_escola(df_original, resp)

            resp1 = st.checkbox('Incluir alunos Treneiros', value=True)
            df = fs.filtro_prova_treino(df, resp1)

            Sexualidade = st.multiselect(
                "Selecione a sexualidade:",
                ['Masculino', "Feminino"],
                placeholder="Selecione uma sexualidade"
            )
            map_sexo = {
                "Masculino": 'M',
                "Feminino": 'F'
            }
            df = fs.filtro_multiselect(df, Sexualidade, map_sexo, 'TP_SEXO')

            est_civil = st.multiselect(
                "Selecione o estado civil:",
                ['Não informado','Solteiro(a)','Casado(a)/Mora com companheiro(a)','Divorciado(a)/Desquitado(a)/Separado(a)','Viúvo(a)'],
                placeholder="Selecione uma estado civil"
            )
            map_est_civil = {
                'Não informado':'0',
                'Solteiro(a)':'1',
                'Casado(a)/Mora com companheiro(a)':'2',
                'Divorciado(a)/Desquitado(a)/Separado(a)':'3',
                'Viúvo(a)':'4'}

            df = fs.filtro_multiselect(df, est_civil, map_est_civil, 'TP_ESTADO_CIVIL')

            raça = st.multiselect(
                "Selecione a raça:",
                ['Não declarado', 'Branca', 'Preta', 'Parda', 'Amarela', 'Indígena'],
                placeholder='Selecione a raça'
            )
            map_raça = {'Não declarado': '0',
                        'Branca': '1',
                        'Preta': '2',
                        'Parda': '3',
                        'Amarela': '4',
                        'Indígena': '5'}
            df = fs.filtro_multiselect(df, raça, map_raça, 'TP_COR_RACA')


            idade = st.multiselect(
                "Selecione a idade:",
                ["Menor de 17 anos",
                 "17 anos",
                 "18 anos",
                 "19 anos",
                 "20 anos",
                 "21 anos",
                 "22 anos",
                 "23 anos",
                 "24 anos",
                 "25 anos",
                 "Entre 26 e 30 anos",
                 "Entre 31 e 35 anos",
                 "Entre 36 e 40 anos",
                 "Entre 41 e 45 anos",
                 "Entre 46 e 50 anos",
                 "Entre 51 e 55 anos",
                 "Entre 56 e 60 anos",
                 "Entre 61 e 65 anos",
                 "Entre 66 e 70 anos",
                 "Maior de 70 anos"],
                placeholder="Selecione uma idade"
            )
            map_idade = {
                "Menor de 17 anos": '1',
                "17 anos": '2',
                "18 anos": '3',
                "19 anos": '4',
                "20 anos": '5',
                "21 anos": '6',
                "22 anos": '7',
                "23 anos": '8',
                "24 anos": '9',
                "25 anos": '10',
                "Entre 26 e 30 anos": '11',
                "Entre 31 e 35 anos": '12',
                "Entre 36 e 40 anos": '13',
                "Entre 41 e 45 anos": '14',
                "Entre 46 e 50 anos": '15',
                "Entre 51 e 55 anos": '16',
                "Entre 56 e 60 anos": '17',
                "Entre 61 e 65 anos": '18',
                "Entre 66 e 70 anos": '19',
                "Maior de 70 anos": '20'
            }
            df = fs.filtro_multiselect(df, idade, map_idade, 'TP_FAIXA_ETARIA')

            renda_familiar = st.multiselect(
                "Selecione a renda familiar:",
                [
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
                ],
                placeholder="Selecione uma renda familiar"
            )

            map_renda_familiar = {
                "Nenhuma renda.": "A",
                "Até 1 salário minímo.": "B",
                "De 1  até 1 salário minímo e meio.": "C",
                "De 1,5 até 2 salários minímo.": "D",
                "De 2 até 2 salários minímo e meio": "E",
                "De 2,5 até  3 salários minímo.": "F",
                "De 3 até 4 salários minímo.": "G",
                "De 4 até 5 salários minímo.": "H",
                "De 5 até 6 salários minímo.": "I",
                "De 6 até 7 salários minímo.": "J",
                "De 7 até 8 salários minímo.": "K",
                "De 8 até 9 salários minímo.": "L",
                "De 9 até 10 salários minímo.": "M",
                "De 10 até 12 salários minímo.": "N",
                "De 12 até 15 salários minímo.": "O",
                "De 15 até 20 salários minímo.": "P",
                "Mais de 20 salários minímo.": "Q"
            }
            df = fs.filtro_multiselect(df, renda_familiar, map_renda_familiar, 'Q006')

        with st.expander('Escola'):
            map_adimin = {
                'Não informado': None,
                "Federal":'1',
                "Estadual":'2',
                "Municipal":'3',
                "Privada":'4'
            }

            admin = st.multiselect(
                "Tipo de depedência administrativa",
                [
                    'Não informado',
                    "Federal",
                "Estadual",
                "Municipal",
                "Privada"
                 ],
                placeholder="Selecione o tipo de depedência"
            )
            df = fs.filtro_multiselect(df, admin, map_adimin, 'TP_DEPENDENCIA_ADM_ESC')

            map_ensino = {
                'Não informado':None,
                'Ensino Regular':'1',
                'Educação Especial - Modalidade Substitutiva':'2',
                'Educação de Jovens e Adultos':'3'
            }
            tp_ensino = st.multiselect(
                'Tipo de ensino',
                [
                    'Não informado',
                    'Ensino Regular',
                    'Educação Especial - Modalidade Substitutiva',
                    'Educação de Jovens e Adultos'

                ],
                placeholder="Selecione o tipo de ensino"
            )
            df = fs.filtro_multiselect(df, tp_ensino, map_ensino, 'TP_ENSINO')

            map_localidadde = {
                'Não informado': None,
                'Urbana':'1',
                'Rural':'2'
            }
            localidade = st.multiselect(
                'Tipo de localidade',
                [
                    'Não informado',
                    'Urbana',
                    'Rural'
                ],
                placeholder="Selecione o tipo de localidade"
            )
            df = fs.filtro_multiselect(df, localidade, map_localidadde, 'TP_LOCALIZACAO_ESC')

        with st.expander('Moradia, bens e serviço'):
            map = {
                    "Não": "A",
                    "Sim, um": "B",
                    "Sim, dois": "C",
                    "Sim, três": "D",
                    "Sim, quatro ou mais": "E"
                }
            compu = st.multiselect(
                'Computador',
                [
                    "Não",
                    "Sim, um",
                    "Sim, dois",
                    "Sim, três",
                    "Sim, quatro ou mais"
                ],
                placeholder="Selecione o computador"
            )
            df = fs.filtro_multiselect(df, compu, map, 'Q024')

            celular = st.multiselect(
                'Celular',
                [
                    "Não",
                    "Sim, um",
                    "Sim, dois",
                    "Sim, três",
                    "Sim, quatro ou mais"
                ],
                placeholder="Selecione o computador"
            )
            df = fs.filtro_multiselect(df, celular, map, 'Q022')

            internet = st.multiselect(
                'Internet',
                [
                    "Não",
                    "Sim, um",
                    "Sim, dois",
                    "Sim, três",
                    "Sim, quatro ou mais"
                ],
                placeholder="Selecione o computador"
            )
            df = fs.filtro_multiselect(df, internet, map, 'Q025')

            tv = st.multiselect(
                'Televisão de cor',
                [
                    "Não",
                    "Sim, um",
                    "Sim, dois",
                    "Sim, três",
                    "Sim, quatro ou mais"
                ],
                placeholder="Selecione uma opção"
            )
            df = fs.filtro_multiselect(df, tv, map, 'Q019')


            map_empregada = {
                'Não possui':'A',
                'Sim, um ou dois dias por semana':'B',
                'Sim, três ou quatro dias por semana':'C',
                'Sim, pelo menos cinco dias por semana':'D'
            }
            empregada = st.multiselect(
                'Empregada',
                [
                'Não possui',
                'Sim, um ou dois dias por semana',
                'Sim, três ou quatro dias por semana',
                'Sim, pelo menos cinco dias por semana'
                ],
                placeholder="Selecione uma opção"
            )
            df = fs.filtro_multiselect(df, empregada, map_empregada, 'Q007')

            banheiro = st.multiselect(
                'Banheiro',
                [
                    "Não",
                    "Sim, um",
                    "Sim, dois",
                    "Sim, três",
                    "Sim, quatro ou mais"
                ],
                placeholder="Selecione uma opção"
            )
            df = fs.filtro_multiselect(df, banheiro, map, 'Q008')

            quarto = st.multiselect(
                'Quarto',
                [
                    "Não",
                    "Sim, um",
                    "Sim, dois",
                    "Sim, três",
                    "Sim, quatro ou mais"
                 ],
                placeholder='Selecione uma opção'
            )
            df = fs.filtro_multiselect(df, quarto, map, 'Q009')

            maq_lavar = st.multiselect(
                'Máquina de lavar roupa',
                [
                    "Não",
                    "Sim, um",
                    "Sim, dois",
                    "Sim, três",
                    "Sim, quatro ou mais"
                ],
                placeholder='Selecione uma opção'
            )
            df = fs.filtro_multiselect(df, maq_lavar, map, 'Q014')

            micro_ondas = st.multiselect(
                'Micro-ondas',
                [
                    "Não",
                    "Sim, um",
                    "Sim, dois",
                    "Sim, três",
                    "Sim, quatro ou mais"
                ],
                placeholder='Selecione uma opção'
            )
            df = fs.filtro_multiselect(df, micro_ondas, map, 'Q016')

            geladeira = st.multiselect(
                'Geladeira',
                [
                    "Não",
                    "Sim, um",
                    "Sim, dois",
                    "Sim, três",
                    "Sim, quatro ou mais"
                ],
                placeholder='Selecione uma opção'
            )
            df = fs.filtro_multiselect(df, geladeira, map, 'Q012')


            automovel = st.radio(
                'Automovel',
                ['Possui Nenhum', 'Possui Carro', 'Possui Moto', 'Possui Ambos'], index=None
            )

            df = fs.multicolunas(df, automovel)

        with st.expander('Prova'):
            map_lingua = {
                "Inglês":'0',
                "Espanhol":'1'
            }
            lingua = st.multiselect(
                'Tipo de lingua estrangeira',
                [
                    'Inglês',
                    'Espanhol',
                ],
                placeholder="Selecione o tipo de lingua"
            )
            df = fs.filtro_multiselect(df, lingua, map_lingua, 'TP_LINGUA')

            map_redacao = {
                'Ausente':None,
                "Sem problemas": "1",
                "Anulada": "2",
                "Cópia Texto Motivador": "3",
                "Em Branco": "4",
                "Fuga ao tema": "6",
                "Não atendimento ao tipo textual": "7",
                "Texto insuficiente": "8",
                "Parte desconectada": "9"
            }
            redacao = st.multiselect(
                'Situação da redação',
                [
                    'Ausente',
                    "Sem problemas",
                    "Anulada",
                    "Cópia Texto Motivador",
                    "Em Branco",
                    "Fuga ao tema",
                    "Não atendimento ao tipo textual",
                    "Texto insuficiente",
                    "Parte desconectada"
                ],
                placeholder="Selecione o tipo de situação"
            )
            df = fs.filtro_multiselect(df, redacao, map_redacao, 'TP_STATUS_REDACAO')
#==================================================================================================
    #cont = len(df)
    #st.metric('Quantidade de registros', value=str(cont), border=False)
    #st.write(df)

    tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9 = st.tabs(
        [
        'GERAL',
        'ESTUDANTE',
        'DADOS ESCOLARES',
        'RENDA',
        'DADOS DA PROVA ',
        'DADOS SOBRE ELETRO-DOMESTICO',
        'MORADIA E BENS',
        'TECNOLOGIA',
        'QUESTIONÁRIO'
    ]
    )
#==================================================================================================
    with tab1:

        col2, col3 = st.columns(2)
        cont1 = len(fs.filtro_prova_treino(df,False))
        cont2 = len(fs.filtro_prova_treino(df, '1'))
        col2.metric('Regulares',value = str(cont1),border=True)
        col3.metric('Treneiros',value=str(cont2), border=True)
        #st.write(df)

        barra = fs.grafico_barra(
            df,
            "NU_ANO",
            "NU_ANOS",
            "Quantidade",
            "Anos",
            False,
        )

    with tab2:

        with st.expander('Informações sobre sexo'):
            col1, col2 = st.columns(2)
            with col1:
                map_sexo = {
                    'M':"Masculino",
                    'F':"Feminino"
                }

                pizza0 = fs.grafico_pizza(
                    df,
                    'TP_SEXO',
                    'Sexualidade',
                    'Quantidade',
                    'Percentual de inscritos por sexo em todos os anos',
                    map_sexo
                )
                #===================================================================
            with col2:
                pass
                df_filtrado = fs.multi(df,'NU_ANO','TP_SEXO')
                multi_tab_sexo = fs.grafico_renda(df_filtrado,'NU_ANO', 'quantidade', 'TP_SEXO' )

        with st.expander('Informações sobre estado civil'):
            col1, col2 = st.columns(2)
            with col1:
                map_estado_civil= {
                    '0':'Não informado',
                    '1':'Solteiro(a)',
                    '2':'Casado(a) / Mora com companheiro(a)',
                    '3':'Divorciado(a) / Desquitado(a) / Separado(a)',
                    '4':'Viúvo(a)'
                }
                pizza = fs.grafico_pizza(
                    df,
                    'TP_ESTADO_CIVIL',
                    'Estado Civil ',
                    'Quantidade',
                    'Estado Civil em todos os anos',
                    map_estado_civil
                )
            with col2:
                df_filtrado = fs.multi(df,'NU_ANO','TP_ESTADO_CIVIL')
                multi_tab_estado = fs.grafico_renda(df_filtrado,'NU_ANO', 'quantidade', 'TP_ESTADO_CIVIL' )
    #===================================================================
        with st.expander('Informações sobre cor/raça'):
            col1, col2 = st.columns(2)
            with col1:
                map_cores = {
                    '0': "Não declarado",
                    '1': "Branca",
                    '2': "Preta",
                    '3': "Parda",
                    '4': "Amarela",
                    '5': "Indígena"
                }

                pizza10 = fs.grafico_pizza(
                    df,
                    'TP_COR_RACA',
                    'Cor/Raça',
                    'quantidade',
                    'Cor/Raça em todos os anos',
                    map_cores
                )
            with col2:
                df_filtrado = fs.multi(df,'NU_ANO','TP_COR_RACA')
                multi_tab_cores = fs.grafico_renda(df_filtrado,'NU_ANO', 'quantidade', 'TP_COR_RACA' )

        with st.expander('informações sobre faixa etária'):
            col1, col2 = st.columns(2)
            with col1:
                map_faixa = {
                    '1': "Menor de 17 anos",
                    '2': "17 anos",
                    '3': "18 anos",
                    '4': "19 anos",
                    '5': "20 anos",
                    '6': "21 anos",
                    '7': "22 anos",
                    '8': "23 anos",
                    '9': "24 anos",
                    '10': "25 anos",
                    '11': "Entre 26 e 30 anos",
                    '12': "Entre 31 e 35 anos",
                    '13': "Entre 36 e 40 anos",
                    '14': "Entre 41 e 45 anos",
                    '15': "Entre 46 e 50 anos",
                    '16': "Entre 51 e 55 anos",
                    '17': "Entre 56 e 60 anos",
                    '18': "Entre 61 e 65 anos",
                    '19': "Entre 66 e 70 anos",
                    '20': "Maior de 70 anos"
                }

                catego = [
                    "Menor de 17 anos",
                    "17 anos",
                    "18 anos",
                    "19 anos",
                    "20 anos",
                    "21 anos",
                    "22 anos",
                    "23 anos",
                    "24 anos",
                    "25 anos",
                    "Entre 26 e 30 anos",
                    "Entre 31 e 35 anos",
                    "Entre 36 e 40 anos",
                    "Entre 41 e 45 anos",
                    "Entre 46 e 50 anos",
                    "Entre 51 e 55 anos",
                    "Entre 56 e 60 anos",
                    "Entre 61 e 65 anos",
                    "Entre 66 e 70 anos",
                    "Maior de 70 anos"
                ]

                pizza11 = fs.grafico_pizza(
                    df,
                    'TP_FAIXA_ETARIA',
                    'Faixa etária',
                    'quantidade',
                    'Faixa etária em todos os anos',
                    map_faixa,
                    None,
                    catego

                )
            with col2:
                df_filtrado = fs.multi(df, 'NU_ANO', 'TP_FAIXA_ETARIA')
                multi_tab_faixa = fs.grafico_renda(df_filtrado, 'NU_ANO', 'quantidade', 'TP_FAIXA_ETARIA',catego,None, True, )

    with tab3:
        # ============ tipo de depedencia ===========================

        with st.expander("Distribuição por administração"):
            col1, col2 = st.columns(2)
            with col1:
                map = {
                    None: 'Não informado',
                    '1': "Federal",
                    '2': "Estadual",
                    '3': "Municipal",
                    '4': "Privada"
                }
                pizza1 = fs.grafico_pizza(df,
                                          "TP_DEPENDENCIA_ADM_ESC",
                                          "Tipo de dependência",
                                          "Quantidade",
                                          'Tipo de dependência em todos os anos',
                                          map)
            with col2:
                df_filtrado = fs.multi(df, 'NU_ANO', 'TP_DEPENDENCIA_ADM_ESC')
                multi_tab_faixa = fs.grafico_renda(df_filtrado, 'NU_ANO', 'quantidade', 'TP_DEPENDENCIA_ADM_ESC')
        # =========== zona territorial ==============================
        with st.expander('Distribuição por localidade'):
            col1, col2 = st.columns(2)
            with col1:
                map = {
                    None: 'Não informada',
                    '1': 'Urbana',
                    '2': 'Rural'
                }
                pizza2 = fs.grafico_pizza(
                    df,
                    'TP_LOCALIZACAO_ESC',
                    'Tipo de zona',
                    'Quantidade',
                    'Tipos de Zonas em todos os anos',
                    map,
                )
            with col2:
                df_filtrado = fs.multi(df, 'NU_ANO', 'TP_LOCALIZACAO_ESC')
                multi_tab_faixa = fs.grafico_renda(df_filtrado, 'NU_ANO', 'quantidade', 'TP_LOCALIZACAO_ESC')
        # ============ Tipo de ensino ================================
        with st.expander('Distribuição por tipo de ensino'):
            col1, col2 = st.columns(2)
            with col1:
                map = {
                    None : 'Não informado',
                    '1': "Ensino Regular",
                    '2': "Educação Especial - Modalidade Substitutiva",
                    '3': "Educação de Jovens e Adultos"
                }
                PIZZA = fs.grafico_pizza(
                    df,
                    'TP_ENSINO',
                    'tipo de ensino',
                    'Quantidade',
                    'Tipo de ensino em todos os anos',
                    map
                )
            with col2:
                df_filtrado = fs.multi(df, 'NU_ANO', 'TP_ENSINO')
                multi_tab_ensino = fs.grafico_renda(df_filtrado, 'NU_ANO', 'quantidade', 'TP_ENSINO' )

    with tab4:

        # mapeamento de faixas de renda
        map_FR = {
            "A": "Nenhuma renda.",
            "B": "Até 1 salário minímo.",
            "C": "De 1  até 1 salário minímo e meio.",
            "D": "De 1,5 até 2 salários minímo.",
            "E": "De 2 até 2 salários minímo e meio",
            "F": "De 2,5 até  3 salários minímo.",
            "G": "De 3 até 4 salários minímo.",
            "H": "De 4 até 5 salários minímo.",
            "I": "De 5 até 6 salários minímo.",
            "J": "De 6 até 7 salários minímo.",
            "K": "De 7 até 8 salários minímo.",
            "L": "De 8 até 9 salários minímo.",
            "M": "De 9 até 10 salários minímo.",
            "N": "De 10 até 12 salários minímo.",
            "O": "De 12 até 15 salários minímo.",
            "P": "De 15 até 20 salários minímo.",
            "Q": "Mais de 20 salários minímo."
        }

        df['Q006'] = df['Q006'].map(map_FR)
        #st.write(df['Q006'])
        with st.expander('Distribuição por renda'):


            teste = fs.multi(df,'NU_ANO','Q006')
            tab16 = fs.grafico_teste(teste)

        with st.expander('Distribuição por classe social'):
            col1, col2 = st.columns(2)
            with col1:

                df_teste = df.copy()
                df_tratado = fs.classes(df_teste)
                teste = fs.multi(df_tratado, 'NU_ANO', 'Q006')

                #st.write(teste)

                pizza10 = fs.grafico_pizza(
                    df_tratado,
                    'Q006',
                    'Q006',
                    'quantidade',
                    'Percentuais gerais em todos os anos',
                )

            with col2:
                tab20 = fs.grafico_renda(teste,'NU_ANO','quantidade','Q006', None, True)

        with st.expander('Distribuição de renda por cor/raça'):

            df_tratado2 = fs.multi(df,'TP_COR_RACA','Q006')
            #st.write(df_tratado2)
            tab20 = fs.grafico_relative(df_tratado2, 'TP_COR_RACA', 'percentual', 'Q006', 'Percentuais por cor/raça em todos os anos')

        with st.expander('Distribuição de renda por estado civil'):

            df_tratado = fs.multi(df,'TP_ESTADO_CIVIL', 'Q006')
            tab21 = fs.grafico_relative(df_tratado, 'TP_ESTADO_CIVIL', 'percentual', 'Q006', 'Percentuais por estado civil em todos os anos')

        with st.expander('Distribuição de renda por idade'):

            df_tratado = fs.multi(df,'TP_FAIXA_ETARIA', 'Q006')
            tab22 = fs.grafico_relative(df_tratado,'TP_FAIXA_ETARIA', 'percentual', 'Q006', 'Percentuais por idade em todos os anos')

        with st.expander('Distribuição de renda por administração da escola'):

            df_tratado = fs.multi(df,'TP_DEPENDENCIA_ADM_ESC', 'Q006')
            tab22 = fs.grafico_relative(df_tratado, 'TP_DEPENDENCIA_ADM_ESC', 'percentual', 'Q006', 'Percentuais por administração escolar em todos os anos')

        with st.expander('Distribuição de renda por localidade'):

            df_tratado = fs.multi(df,'TP_LOCALIZACAO_ESC', 'Q006')
            tab22 = fs.grafico_relative(df_tratado, 'TP_LOCALIZACAO_ESC', 'percentual', 'Q006','Percentuais por localidade em todos os anos')

        with st.expander('Distribuição de renda por tipo de ensino'):

            df_tratado = fs.multi(df, 'TP_ENSINO', 'Q006')
            tab22 = fs.grafico_relative(df_tratado, 'TP_ENSINO', 'percentual', 'Q006','Percentuais por tipo de ensino em todos os anos')

    with tab5:
        pass
    with tab6:
        with st.expander('Micro-ondas'):
            col1, col2 = st.columns(2)
            with col1:
                # ======== micro-ondas ======================================
                map = {
                    "A": "Nenhum.",
                    "B": "Um.",
                    "C": "Dois.",
                    "D": "Três.",
                    "E": "Quatro ou mais."
                }
                pizza5 = fs.grafico_pizza(
                    df,
                    "Q016",
                    'Quantos micro-ondas possui?',
                    'Quantidade de respostas',
                    'Possuem Micro-ondas em todos os anos',
                    map)
            with col2:
                df_filtrado = fs.multi(df, 'NU_ANO','Q016')
                multi_tab_generico = fs.grafico_renda(df_filtrado, 'NU_ANO', 'quantidade', 'Q016')
        with st.expander('Maquina de lavar roupa'):
            col1, col2 = st.columns(2)
            with col1:
                # ======== maquina de lavar ================================
                map = {
                    "A": "Nenhuma.",
                    "B": "Uma.",
                    "C": "Duas.",
                    "D": "Três.",
                    "E": "Quatro ou mais."
                }
                barra8 = fs.grafico_pizza(
                    df,
                    'Q014',
                    'possui quantas maquinas de lavar?',
                    'Quantidade de respostas',
                    'Possuem maquinas de lavar roupa em todos os anos',
                    map
                )
            with col2:
                catego = [
                    'Duas.',
                    'Nenhuma.',
                    'Quatro ou mais.',
                    'Três.',
                    'Uma.',
                ]
                df_filtrado = fs.multi(df, 'NU_ANO', 'Q014')
                multi_tab_generico = fs.grafico_renda(df_filtrado, 'NU_ANO', 'quantidade', 'Q014', catego)
        with st.expander('Televisão'):
            col1, col2 = st.columns(2)
            with col1:
                # ========= televisão =======================================
                map = {
                    "A": "Nenhuma.",
                    "B": "Uma.",
                    "C": "Duas.",
                    "D": "Três.",
                    "E": "Quatro ou mais."
                }
                pizza6 = fs.grafico_pizza(
                    df,
                    'Q019',
                    'Possui quntas televisão de cor?',
                    'Quantidade de respostas',
                    'Possuem televisão de cor em todos os anos',
                    map)
            with col2:
                df_filtrado = fs.multi(df, 'NU_ANO', 'Q019')
                multi_tab_generico = fs.grafico_renda(df_filtrado,'NU_ANO', 'quantidade', 'Q019')

    with tab7:

        with st.expander('Empregado(a) doméstico(a)'):
            col1, col2 = st.columns(2)
            with col1:
                # =========== empregada domestica ===========================
                map = {
                    "A": "Não.",
                    "B": "Sim, um ou dois dias por semana.",
                    "C": "Sim, três ou quatro dias por semana.",
                    "D": "Sim, pelo menos cinco dias por semana."
                }
                barra3 = fs.grafico_pizza(
                    df,
                    'Q007',
                    'Possui empregada domestica?',
                    'Quantidade de respostas',
                    'Possue Empregada em todos os anos',
                    map,
                )
            with col2:
                df_filtrado = fs.multi(df, 'NU_ANO', 'Q007')
                multi_tab_faixa = fs.grafico_renda(df_filtrado, 'NU_ANO', 'quantidade', 'Q007')
        with st.expander('Banheiro'):
            col1, col2 = st.columns(2)
            with col1:
                # ========== possui banheiro ===============================
                map = {
                    "A": "Nenhuma.",
                    "B": "Uma.",
                    "C": "Duas.",
                    "D": "Três.",
                    "E": "Quatro ou mais."
                }
                barra4 = fs.grafico_pizza(
                    df,
                    'Q008',
                    'Possui quantos banheiro?',
                    'Quantidade de respostas',
                    'Possuem Banheiro em todos os anos',
                    map)
            with col2:
                df_filtrado = fs.multi(df, 'NU_ANO', 'Q008')
                multi_tab_faixa = fs.grafico_renda(df_filtrado, 'NU_ANO', 'quantidade', 'Q008')
        with st.expander('Quartos'):
            col1, col2 = st.columns(2)
            with col1:
                # ========== quartos ======================================
                map = {
                    "A": "Nenhuma.",
                    "B": "Uma.",
                    "C": "Duas.",
                    "D": "Três.",
                    "E": "Quatro ou mais."
                }
                barra5 = fs.grafico_pizza(
                    df,
                    'Q009',
                    'Possui quantos quartos?',
                    'Quantidade de respostas',
                    'Possui quantos quartos na casa em todos os anos',
                    map)
            with col2:
                df_filtrado = fs.multi(df, 'NU_ANO', 'Q009')
                multi_tab_faixa = fs.grafico_renda(df_filtrado, 'NU_ANO', 'quantidade', 'Q009')
        with st.expander('Motos'):
            col1, col2 = st.columns(2)
            with col1:
                # ======== automovel moto =================================
                map = {
                    "A": "Nenhuma.",
                    "B": "Uma.",
                    "C": "Duas.",
                    "D": "Três.",
                    "E": "Quatro ou mais."
                }
                barra7 = fs.grafico_pizza(
                    df,
                    'Q011',
                    'Possui quantas motos?',
                    'Quantidade de respostas',
                    'Possuem Moto em todos os anos',
                    map,
                )
            with col2:
                df_filtrado = fs.multi(df, 'NU_ANO', 'Q011')
                multi_tab_generico = fs.grafico_renda(df_filtrado, 'NU_ANO', 'quantidade', 'Q011')
        with st.expander('Carros'):
            col1, col2 = st.columns(2)
            with col1:
                # ========== automovel carro ==============================
                map = {
                    "A": "Não.",
                    "B": "Sim, um.",
                    "C": "Sim, dois.",
                    "D": "Sim, três.",
                    "E": "Sim, quatro ou mais."
                }
                barra6 = fs.grafico_pizza(
                    df,
                    'Q010',
                    'Possui quantos carros?',
                    'Quantidade de respostas',
                    'Possuem Carro em todos os anos',
                    map)
            with col2:
                df_filtrado = fs.multi(df, 'NU_ANO', 'Q010')
                multi_tab_generico = fs.grafico_renda(df_filtrado, 'NU_ANO', 'quantidade', 'Q010')
        with st.expander('Carro e moto'):
            col1, col2 = st.columns(2)
            with col1:
                # ================== ambos os automoveis =====================
                tab = fs.colunas_cruzadas(df, 'Q010', 'Q011')
                #st.write(tab)
                map = {
                    "A": "Não possui nenhum",
                    "B": "Possui Carro",
                    "C": "Possui moto",
                    "D": 'Possui Ambos'
                }

                barra9 = fs.grafico_pizza(
                    tab,
                    'Veiculos',
                    'Possui ambos ou somente um veiculo',
                    'Quantidade de respostas',
                    'Possui ambos ou somente um veiculo de trasnporte(Carro e moto) em todos os anos',
                    map,
                )
            with col2:
                df_filtrado = fs.multi(tab, 'ANOS', 'Veiculos')
                multi_tab_generico = fs.grafico_renda(df_filtrado, 'ANOS', 'quantidade', 'Veiculos')

    with tab8:
        # ============ internet ====================================
        with st.expander("Acessor à internet"):
            col1, col2 = st.columns(2)
            with col1:
                map = {
                    'A': 'Não.',
                    'B': 'Sim.'
                }
                pizza4 = fs.grafico_pizza(
                    df,
                    'Q025',
                    'Possui internet?',
                    'Quantidades de respostas',
                    'Possuem Internet em todos os anos',
                    map)
            with col2:
                df_filtrado = fs.multi(df, 'NU_ANO', 'Q025')
                multi_tab_faixa = fs.grafico_renda(df_filtrado, 'NU_ANO', 'quantidade', 'Q025')
        with st.expander("Computador em casa"):
            col1, col2 = st.columns(2)
            with col1:
                # ========= computador ======================================
                map = {
                    "A": "Nenhuma.",
                    "B": "Uma.",
                    "C": "Duas.",
                    "D": "Três.",
                    "E": "Quatro ou mais."
                }
                pizza7 = fs.grafico_pizza(
                    df,
                    'Q024',
                    'Possui quantos computadores',
                    'Quantidade de respostas',
                    'Possuem Computador em todos os anos',
                    map)
            with col2:
                df_filtrado = fs.multi(df, 'NU_ANO', 'Q024')
                multi_tab_faixa = fs.grafico_renda(df_filtrado, 'NU_ANO', 'quantidade', 'Q024')
        with st.expander("Celular em casa"):
            col1, col2 = st.columns(2)
            with col1:
                # =========  celular ========================================
                map = {
                    "A": "Nenhuma.",
                    "B": "Uma.",
                    "C": "Duas.",
                    "D": "Três.",
                    "E": "Quatro ou mais."
                }
                barra9 = fs.grafico_pizza(
                    df,
                    'Q022',
                    'Possui qunatos celulares?',
                    'Quantidades de respostas',
                    'Possuem Celular em todos os anos',
                    map)
            with col2:
                df_filtrado = fs.multi(df, 'NU_ANO', 'Q022')
                multi_tab_faixa = fs.grafico_renda(df_filtrado, 'NU_ANO', 'quantidade', 'Q022')

    with tab9:
        #st.write(df)
        select = st.selectbox(
            "Escolha uma pergunta do questionário do ENEM",
            (
            'Até que série seu pai, ou o homem responsável por você, estudou?',
            'Até que série sua mãe, ou a mulher responsável por você, estudou?',
            'A partir da apresentação de algumas ocupações divididas em grupos ordenados, indique o grupo que contempla a ocupação mais próxima da ocupação do seu pai ou do homem responsável por você. (Se ele não estiver trabalhando, escolha uma ocupação pensando no último trabalho dele).',
            'A partir da apresentação de algumas ocupações divididas em grupos ordenados, indique o grupo que contempla a ocupação mais próxima da ocupação da sua mãe ou da mulher responsável por você. (Se ela não estiver trabalhando, escolha uma ocupação pensando no último trabalho dela).',
            'Incluindo você, quantas pessoas moram atualmente em sua residência?',
            'Na sua residência tem geladeira?',
            'Na sua residência tem freezer (independente ou segunda porta da geladeira)?',
            'Na sua residência tem máquina de secar roupa (independente ou em conjunto com a máquina de lavar roupa)?',
            'Na sua residência tem máquina de lavar louça?',
            'Na sua residência tem aspirador de pó?',
            'Na sua residência tem aparelho de DVD?',
            'Na sua residência tem TV por assinatura?',
            'Na sua residência tem telefone fixo?',
            'Você já concluiu ou está concluindo o Ensino Médio?',
            'Em que tipo de escola você frequentou o Ensino Médio?',

                        ),
            index=None,
            placeholder="Selecione uma opção..",
        )
        if select:
            st.write("Você selecionou:", select)

            col1, col2 = st.columns(2)
            with col1:
                # =========  celular ========================================
                controle = fs.mapeamento(select)

                barra9 = fs.grafico_pizza(
                    df,
                    controle[0],
                    controle[1],
                    controle[2],
                    controle[3],
                    controle[4],
                    controle[6]
                )
            with col2:
                df_filtrado = fs.multi(df, 'NU_ANO', controle[0])
                multi_tab_faixa = fs.grafico_renda(df_filtrado, 'NU_ANO', 'quantidade', controle[0], controle[5], controle[6])


        else:
            st.write("Nada selecionado")