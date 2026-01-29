from importlib.resources import contents

import streamlit as st
import pandas as pd
import funcao_social as fs
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
                    "Até R$ 954,00.",
                    "De R$ 954,01 até R$ 1.431,00.",
                    "De R$ 1.431,01 até R$ 1.908,00.",
                    "De R$ 1.908,01 até R$ 2.385,00.",
                    "De R$ 2.385,01 até R$ 2.862,00.",
                    "De R$ 2.862,01 até R$ 3.816,00.",
                    "De R$ 3.816,01 até R$ 4.770,00.",
                    "De R$ 4.770,01 até R$ 5.724,00.",
                    "De R$ 5.724,01 até R$ 6.678,00.",
                    "De R$ 6.678,01 até R$ 7.632,00.",
                    "De R$ 7.632,01 até R$ 8.586,00.",
                    "De R$ 8.586,01 até R$ 9.540,00.",
                    "De R$ 9.540,01 até R$ 11.448,00.",
                    "De R$ 11.448,01 até R$ 14.310,00.",
                    "De R$ 14.310,01 até R$ 19.080,00.",
                    "Mais de R$ 19.080,00."
                ],
                placeholder="Selecione uma renda familiar"
            )
            map_renda_familiar = {
                "Nenhuma renda.": "A",
                "Até R$ 954,00.": "B",
                "De R$ 954,01 até R$ 1.431,00.": "C",
                "De R$ 1.431,01 até R$ 1.908,00.": "D",
                "De R$ 1.908,01 até R$ 2.385,00.": "E",
                "De R$ 2.385,01 até R$ 2.862,00.": "F",
                "De R$ 2.862,01 até R$ 3.816,00.": "G",
                "De R$ 3.816,01 até R$ 4.770,00.": "H",
                "De R$ 4.770,01 até R$ 5.724,00.": "I",
                "De R$ 5.724,01 até R$ 6.678,00.": "J",
                "De R$ 6.678,01 até R$ 7.632,00.": "K",
                "De R$ 7.632,01 até R$ 8.586,00.": "L",
                "De R$ 8.586,01 até R$ 9.540,00.": "M",
                "De R$ 9.540,01 até R$ 11.448,00.": "N",
                "De R$ 11.448,01 até R$ 14.310,00.": "O",
                "De R$ 14.310,01 até R$ 19.080,00.": "P",
                "Mais de R$ 19.080,00.": "Q"
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
    cont = len(df)
    st.metric('Quantidade de registros', value=str(cont), border=False)
    #st.write(df)

    tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9 = st.tabs(
        [
        'GERAL',
        'ESTUDANTE',
        'DADOS ESCOLARES',
        'RENDA',
        'DADOS DA PROVA ',
        'DADOS SOBRE ELETRO-DOMESTICO',
        'DADOS SOBRE VEICULOS',
        'DADOS SOBRE A MORADIA',
        'DADOS SOBRE APARELHOS DIGITAIS E INTERNET'
    ]
    )

    with tab1:

        col2, col3 = st.columns(2)
        cont1 = len(fs.filtro_prova_treino(df_original,False))
        cont2 = len(fs.filtro_prova_treino(df_original, '1'))
        col2.metric('Regulares',value = str(cont1),border=True)
        col3.metric('Treneiros',value=str(cont2), border=True)
        #st.write(df)

        barra = fs.grafico_barra(
            df,
            "NU_ANO",
            "Ano",
            "Quantidade",
            "Anos",
            "v",
            False,
            True
        )

    with tab2:

        with st.expander('Informações sobre sexo'):
                map_sexo = {
                    'M':"Masculino",
                    'F':"Feminino"
                }

                pizza0 = fs.grafico_pizza(
                    df,
                    'TP_SEXO',
                    'Sexualidade',
                    'Quantidade',
                    'Sexualidade',
                    map_sexo
                )
                #===================================================================
        with st.expander('Informações sobre estado civil'):
            map_estado_civil= {
                '0':'Solteiro(a)',
                '1':'Casado(a) / Mora com companheiro(a)',
                '2':'Divorciado(a) / Desquitado(a) / Separado(a)',
                '3':'Viúvo(a)'
            }
            pizza = fs.grafico_pizza(
                df,
                'TP_ESTADO_CIVIL',
                'Estado Civil',
                'Quantidade',
                'Estado Civil',
                map_estado_civil
            )
    #===================================================================
        with st.expander('Informações sobre cor/raça'):
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
                'Cor/Raça',
                map_cores
            )
        with st.expander('informações sobre faixa etária'):
            pass

    with tab3:
        # ============ tipo de depedencia ===========================

        with st.expander("Distribuição por administração"):
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
                                      'Tipo de dependência',
                                      map)
        # =========== zona territorial ==============================
        with st.expander('Distribuição por localidade'):
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
                'Tipos de Zonas',
                map,
            )

        # ============ Tipo de ensino ================================
        with st.expander('Distribuição por tipo de ensino'):
            map = {
                None : 'Não informado',
                '1': "Ensino Regular",
                '2': "Educação Especial - Modalidade Substitutiva",
                '3': "Educação de Jovens e Adultos"
            }
            barra1 = fs.grafico_barra(
                df,
                'TP_ENSINO',
                'tipo de ensino',
                'Quantidade',
                'Tipo de ensino',
                'v',
                map,
                True,
                True
            )

    with tab4:
        st.write('em desenvolvimento')

        clas_A = ['Q']
        clas_B = ['N','O','P']
        clas_C = ['H','I','J','K','L','M']
        clas_D = ['E','F','G']
        clas_E = ['B','C','D']
        clas_F = ['A']

        vet = [clas_A, clas_B, clas_C, clas_D, clas_E, clas_F]

        teste = fs.multi(df, vet)

        tab16 = fs.grafico_renda(teste,'quantidade','Q006')

    with tab5:
        # =========== lingua estrangeira ============================
        with st.expander(''):
            map = {
                '0': "Inglês",
                '1': "Espanhol"
            }
            barra2 = fs.grafico_barra(
                df,
                'TP_LINGUA',
                'tipo de lingua',
                'Quantidade',
                'Tipo de linguagem estrangeira escolhida',
                'v',
                map,
                True
            )

        # =========== prova treino ou não =========================
        map = {
            '1': 'Realizando prova para treino',
            '0': 'Prova valendo pontuação'
        }
        pizza3 = fs.grafico_pizza(
            df,
            'IN_TREINEIRO',
            'Qual modalidade',
            'Quantidade',
            'Tipo de Modalidade de Prova',
            map)

    with tab6:
        # ======== maquina de lavar ================================
        map = {
            "A": "Nenhuma.",
            "B": "Uma.",
            "C": "Duas.",
            "D": "Três.",
            "E": "Quatro ou mais."
        }
        barra8 = fs.grafico_barra(
            df,
            'Q014',
            'possui quantas maquinas de lavar?',
            'Quantidade de respostas',
            'Possuem maquinas de lavar roupa',
            'h',
            map,
        )

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
            'Possuem Micro-ondas',
            map)

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
            'Possuem televisão de cor',
            map)

    with tab7:
        # ======== automovel moto =================================
        map = {
            "A": "Nenhuma.",
            "B": "Uma.",
            "C": "Duas.",
            "D": "Três.",
            "E": "Quatro ou mais."
        }
        barra7 = fs.grafico_barra(
            df,
            'Q011',
            'Possui quantas motos?',
            'Quantidade de respostas',
            'Possuem Moto',
            'h',
            map,
        )

        # ========== automovel carro ==============================
        map = {
            "A": "Não.",
            "B": "Sim, um.",
            "C": "Sim, dois.",
            "D": "Sim, três.",
            "E": "Sim, quatro ou mais."
        }
        barra6 = fs.grafico_barra(
            df,
            'Q010',
            'Possui quantos carros?',
            'Quantidade de respostas',
            'Possuem Carro',
            'h',
            map)

        #================== ambos os automoveis =====================
        tab = fs.colunas_cruzadas(df,'Q010','Q011')
        map = {
            "A": "Não possui nenhum",
            "B": "Possui Carro",
            "C": "Possui moto",
            "D": 'Possui Ambos'
        }

        barra9 = fs.grafico_barra(
            tab,
            'Veiculos',
            'Possui ambos ou somente um veiculo',
            'Quantidade de respostas',
            'Possui ambos ou somente um veiculo de trasnporte(Carro e moto) ?',
            'h',
            map,
        )

    with tab8:
        # =========== empregada domestica ===========================
        map = {
            "A": "Não.",
            "B": "Sim, um ou dois dias por semana.",
            "C": "Sim, três ou quatro dias por semana.",
            "D": "Sim, pelo menos cinco dias por semana."
        }
        barra3 = fs.grafico_barra(
            df,
            'Q007',
            'Possui empregada domestica?',
            'Quantidade de respostas',
            'Possue Empregada',
            'v',
            map,
            True,
            True
        )

        # ========== possui banheiro ===============================
        map = {
            "A": "Nenhuma.",
            "B": "Uma.",
            "C": "Duas.",
            "D": "Três.",
            "E": "Quatro ou mais."
        }
        barra4 = fs.grafico_barra(
            df,
            'Q008',
            'Possui quantos banheiro?',
            'Quantidade de respostas',
            'Possuem Banheiro',
            'h',
            map)

        # ========== quartos ======================================
        map = {
            "A": "Nenhuma.",
            "B": "Uma.",
            "C": "Duas.",
            "D": "Três.",
            "E": "Quatro ou mais."
        }
        barra5 = fs.grafico_barra(
            df,
            'Q009',
            'Possui quantos quartos?',
            'Quantidade de respostas',
            'Possui quantos quartos na casa ',
            'h',
            map)

    with tab9:
        # ============ internet ====================================
        map = {
            'A': 'Não.',
            'B': 'Sim.'
        }
        pizza4 = fs.grafico_pizza(
            df,
            'Q025',
            'Possui internet?',
            'Quantidades de respostas',
            'Possuem Internet',
            map)
        # =========  celular ========================================
        map = {
            "A": "Nenhuma.",
            "B": "Uma.",
            "C": "Duas.",
            "D": "Três.",
            "E": "Quatro ou mais."
        }
        barra9 = fs.grafico_barra(
            df,
            'Q022',
            'Possui qunatos celulares?',
            'Quantidades de respostas',
            'Possuem Celular',
            'h',
            map)
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
            'Possuem Computador',
            map)