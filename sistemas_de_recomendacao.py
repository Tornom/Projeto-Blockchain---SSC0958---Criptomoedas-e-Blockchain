# -*- coding: utf-8 -*-

"""
# **Sistema de Recomendação**
* Vinícius de Moraes - 13749910 
* Bruno Ideriha Sugahara - 10310759
* Lucas Albano de Oliveira - 10377688
"""

#Bibliotecas Utilizadas
import numpy as np
import pandas as pd
import random
import matplotlib as plt


anime_data = pd.read_csv('anime.csv')
rating_data = pd.read_csv('rating.csv')
matriz_animes = pd.read_csv('/content/animesmimis.csv')

matriz_animes.drop('user_id', inplace=True, axis=1)

def adicionar_myanimelist(path):
  if '.xml' in path:
    myanimelist = pd.read_xml(path)
  else:
    myanimelist = pd.read_csv(path)
  myanimeswatched = myanimelist['series_title']
  myanimeswatched = myanimeswatched.str.lower()
  myanimeswatched = list(myanimeswatched)
  myanimelist = myanimelist[['my_id','series_animedb_id', 'my_score']]
  myanimelist = myanimelist.rename(columns = {'my_id':'user_id', 'series_animedb_id':'anime_id', 'my_score':'rating'})
  for i in range (len(myanimelist)):
    elem = myanimelist.iloc[i]
    if elem['rating'] == 0:
      myanimelist.at[i, 'rating'] = -1
  for i in range (len(myanimelist)):
    elem = myanimelist.iloc[i]
    myanimelist.at[i, 'user_id'] = -2

  df = myanimelist.merge(anime_data, left_on = 'anime_id', right_on = 'anime_id', suffixes= ['_user', ''])
  df = df[['user_id','name', 'rating_user']]

  matriz = df.pivot_table(index=['user_id'], columns=['name'], values='rating_user')
  matriz = matriz.replace(-1, np.NaN)

  return matriz, myanimeswatched

myanimelist_user, myanimeswatched_user = adicionar_myanimelist('/content/Boemio.csv') #AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA

column_headers = list(matriz_animes.columns.values)
for i in range(len(column_headers)):
  column_headers[i] = column_headers[i].lower()

matriz_animes.append(myanimelist_user)

matriz_animes = matriz_animes.reset_index()
matriz_animes.drop('index', inplace=True, axis=1)

matriz_R = matriz_animes.to_numpy()
matriz_R[matriz_R == -1] = None

def matrix_factorization(R, P, Q, K, iteracoes=100, alfa=0.0002, beta=0.02):

#    R: matriz de resultados
#    P: |U| * K (matriz de características do usuário)
#    Q: |D| * K (matriz de características do item)
#    K: características latentes
#    alfa: taxa de aprendizado
#    beta: parâmetro de regularização

  # Transpondo matriz
    Q = Q.T

    for step in range(iteracoes):
        for i in range(len(R)):
            for j in range(len(R[i])):
                if R[i][j] > 0:
                    # Cálculo do erro
                    eij = R[i][j] - np.dot(P[i,:],Q[:,j])

                    for k in range(K):
                        # Atualizando os valores de pik e qkj utilizando o gradiente
                        # Foi adicionada a variável beta para controlar a magnitude do item e evitar overfitting
                        P[i][k] = P[i][k] + alfa * (2 * eij * Q[k][j] - beta * P[i][k])
                        Q[k][j] = Q[k][j] + alfa * (2 * eij * P[i][k] - beta * Q[k][j])

        # Produto interno
        eR = np.dot(P,Q)

        # Calculando o erro geral da matriz
        e = 0
        for i in range(len(R)):
            for j in range(len(R[i])):
                if R[i][j] > 0:
                    e = e + pow(R[i][j] - np.dot(P[i,:],Q[:,j]), 2)
                    for k in range(K):
                        e = e + (beta/2) * (pow(P[i][k],2) + pow(Q[k][j],2))
        
        # 0.001: mínimo local 
        if e < 0.001:

            break

    return P, Q.T

# N: número de usuários
N = len(matriz_R)
# M: número de itens
M = len(matriz_R[0])
# K: número de características
K = 3
 
P = np.random.rand(N,K)
Q = np.random.rand(M,K)

nP, nQ = matrix_factorization(matriz_R, P, Q, K)

nR = np.dot(nP, nQ.T) #BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB

df_nR = pd.DataFrame(nR)


lista_recomendados_user = []
nota_prevista_user = []
for i in range(len(nR[0])):
  elem = nR[12][i] 
  if not (column_headers[i] in myanimeswatched_user):
    lista_recomendados_user.append(column_headers[i]) #IIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII
    nota_prevista_user.append(nR[0][i])

data = {'Nome do Anime': lista_recomendados_user, 'Score': nota_prevista_user}
df_recomendados_user = pd.DataFrame(data=data)
df_recomendados_user = df_recomendados_user.sort_values('Score', ascending = False)
df_recomendados_user = df_recomendados_user.reset_index()
df_recomendados_user.drop(columns = 'index', inplace=True)
df_recomendados_user.head(10)