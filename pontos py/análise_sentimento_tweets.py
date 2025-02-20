# -*- coding: utf-8 -*-
"""Análise Sentimento tweets.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1mJHPACX7H3EcsSfajDl58JNcEujKcQH7

Existe discurso de ódio nos tweets? Como podemos saber?

Se considerarmos que um discurso assim é racista ou sexista nossa tarefa fica mais clara: queremos saber entre todos os tweets quais deles são racistas ou sexistas.

Como podemos fazer isso? Vamos considerar que um tweet com discurso de ódio vale 1 e sem esse discurso 0.

Qual o primeiro passo para classificarmos tweets? Ter tweets, certo? Então:

# Obtenção dos dados
"""

import pandas as pd

tweets_treino = pd.read_csv('https://raw.githubusercontent.com/cassiasamp/secomp/master/dados/train_tweets.csv')
tweets_teste = pd.read_csv('https://raw.githubusercontent.com/cassiasamp/secomp/master/dados/test_tweets.csv')

"""# Exploraçao dos dados"""

tweets_treino.head(5)

"""Vemos que os dados de treino tem 3 colunas, id, um número para identificação, label, são as nossas identificações ou marcações e o texto do tweet, em tweet."""

tweets_teste.head(5)

"""Podemos dar uma olhada também em quais as quantidades de treino e teste."""

len(tweets_treino)

len(tweets_teste)

total_tweets = len(tweets_treino) + len(tweets_teste)

len(tweets_teste)/total_tweets*100

len(tweets_treino)/total_tweets*100

"""Repare que vamos treinar com aprox. 65% dos dados e testar com 35%.

Agora vamos focar nos tweets de treino, o que mais conseguimos entender deles?
"""

tweets_treino.head(5)

"""Sabemos quem foi que escreveu o tweet? Não, certo? Repare que eles anonimizam as pessoas com @user. Mas isso nos dá algum tipo deinfo para resolver o nosso problema? Não, então o que podemos fazer?

Vamos pensar. Se você tem um quarto ou sala que sempre está uma bagunça e um dia está com pressa para sair e quer encontrar o celular, eu te pergunto, é mais fácil achar esse celular se o quarto estiver arrumado ou bagunçado? Se ele estiver arrumado, certo? Com os nossos textos é a mesma coisa.

Se repararmos nesse @user aí ele não adiciona nada, então podemos arrumar esse quarto e nos livrarmos dele.

# Preprocessamento e limpeza dos tweets

Precisamos saber onde está o @ e tirá=lo de lá. Para isso vou chamar o @ do padrao que estamos procurando. E ai para dar match nesse padrão, vamos usar uma expressão regular.

## Removendo @user
"""

import re 

padrao = '@'
arrobas = re.findall(padrao, str(tweets_treino))

"""Além da expressão vamos também substituir, re.sub, o arroba nos tweets por nada '', uma string vazia."""

for arroba in arrobas:
  treino_arrumado = re.sub(arroba, ' ', str(tweets_treino))

treino_arrumado

"""Funcionou! Podemos aproveitar e fazer isso nos dois datasets juntos."""

dados = tweets_treino.append(tweets_teste, ignore_index=True) #ignore_index porque eu quero manter o índice que já tenho

import numpy as np

"""Exemplo com soma e subtração:"""

def subtrai_maior_soma_menor(entrada_1, entrada_2):
  
    if entrada_1 > entrada_2:
        return entrada_1 - entrada_2
    else:
        return entrada_1 + entrada_2

vetorizacao = np.vectorize(subtrai_maior_soma_menor)

entrada_1 = [1, 2, 3, 4]
entrada_2 = [2]
subtrai_maior_soma_menor(entrada_1, entrada_2)

"""Vamos voltar para os tweets. Queremos chamar a função que achar o regex e o substitui. Vamos montar essa função."""

def tchau_padrao(texto, padrao):
  
  padroes_encontrados = re.findall(padrao, texto)
  
  for um_padrao in padroes_encontrados:
    texto = re.sub(um_padrao, ' ', texto)
    
  return texto

"""Como vamos fazer uma transformação num grande volume de dados, vamos usar np.vectorize para aplicar essa função nos nossos dados como de uma vez só ao invés de ela rodar 49.000 vezes."""

# \w busca global pelo caractere 
# * = com uma ou mais ocorrências

expressao_regular = "@[\w]*"

# vou aproveitar e criar uma coluna de tweet arrumado, em en, tidy tweet
dados['tidy_tweet'] = np.vectorize(tchau_padrao)(dados['tweet'], expressao_regular)

"""Vamos dar uma olhada nos nosso dados para ver se funcionou."""

dados.head(7)

"""Beleza, funcionou. Agora já não temos mais @user nos nossos tweets.

## Removendo caracteres especiais

Repare também que se olharmos para esses dois pontos aqui, um ponto, virgula, caracter especial ou número sabemos algo sobre a classificação que queremos fazer? Não, né. Repare que pontos, virgulas, números e caracteres especiais não são expressivos sobre o sentimento do nosso texto, então são considerados ruídos e precisamos limpar o nosso texto também desses ruídos.
"""

# todos os pontos, virgulas e caracteres especiais
expressao_regular_2 = "[^a-zA-Z#]"

dados['tidy_tweet'] = dados['tidy_tweet'].str.replace(expressao_regular_2, ' ')

dados.head(15)

#caso eu tenha problemas dislexicos
#dados.drop(columns=['tidy tweets', 'tidy tweet'])

"""Será que já acabamos? Repare também que podemos ter interjeições como ahm, hum, hmm e essas palavras ajudam a gente a saber o sentimento? Também só acrescentam ruído. Logo, vamos filtrá-las.

## Removendo palavras curtas

Palavras assim são chamadas de stop words (palavras de parada).

Para filtrá-las vamos usar algo que se chama lambda. E funciona mais ou menos assim:
"""

lambda x : x

(lambda x : x)(1)

(lambda x : x*5)(1)

"""Vamos combinar a nossa lambda com a divisao split dos dados em palavras, sua posterior junção com join e a verificação de se a palavra é curta, até 3 caracteres."""

dados['tidy_tweet'] = dados['tidy_tweet'].apply(lambda x: ' '.join([palavra for palavra in x.split() if len(palavra)>3]))

(lambda x: ' '.join([word for word in x.split() if len(word)>3]))('exemplo basta eu escrever algo até três caracteres e a lambda vai ter excluido')

"""### Cuidado ao usar lambdas

Uma nota sobre lambdas que são conhecidas também como funções anônimas, se puder evitá-las, evite, pois melhor a leitura do código. É que nesse caso limpeza de dados é a parte mais dolorosa do processo O.O', estamos quase acabando.

jà olhamos para coisas do conjunto dos tweets como pontos e virgulas, caracteres especiais e começamos a olhar para as palavras com o tamanho delas. Podemos nos atentar bem mais para as palavras agora. Se você vai entender um texto, é mais fácil se alguémfalareletodomuitorápidopravocê? Ou se você  for  ouvindo  palavra  por  palavra  de va ga ri nho? O segundo né? O que podemos fazer que é parecido com isso e nos permite mexer mais no texto e dividir os tweets em suas menores unidades, palavras ou tokens..

Isso também é chamado de tokenização.
"""

tweet_tokenizado = dados['tidy_tweet'].apply(lambda x: x.split())
tweet_tokenizado.head(25)

"""Ao fazermos isso, podemos agora olhar mais para as palavras individuais.

Olhando para os nossos tweets, podemos simplificar ainda mais.Veja que palavras como thanks, thank, thankful tem todas uma origem parecida, podemos ao invés de tentar entendê-las assim, deixá-las nessa origem, tirando os seus sufixos. Esse processo se chama estematização ou stemming.

## Normalizando as palavras

Para isso, vamos usar uma lib especializada em manipulação de linguagem que é o nltk e o seu originador ou stemmer.
"""

from nltk.stem.porter import *

stemmer = PorterStemmer()

tweet_tokenizado = tweet_tokenizado.apply(lambda x: [stemmer.stem(palavra) for palavra in x]) # stematização
tweet_tokenizado.head(25)

"""Repare que agora as palavras estão no 'singular' e sem declinações.

Agora, vamos reunir esses tokens para formarmos frases novamente e voltá-los para os nossos dados.
"""

for token in range(len(tweet_tokenizado)):
    tweet_tokenizado[token] = ' '.join(tweet_tokenizado[token])

dados['tidy_tweet'] = tweet_tokenizado

dados.head(5)

"""# Perguntas e visualizações

Agora que estamos mais íntimos dos nossos dados, podemos começar a tentar responder algumas perguntas.

* Quais são as palavras mais comuns no dataset?
* Quais são as palavras que mais ocorrem em tweets negativos e em tweets positivos?
* Quantas hashtags tem em um tweet?
* Que tendências eu tenho no meu dataset?
* Será que tem alguma tendência associada com os sentimentos? Será que a tendência e os sentimento são compatíveis?

## Entendendo quais são as palavras mais usadas com word cloud

Primeiro vamos juntar nossas palavras de novo.
"""

todas_as_palavras = ' '.join([texto for texto in dados['tidy_tweet']])

todas_as_palavras

"""Agora podemos criar o word cloud."""

from wordcloud import WordCloud

wordcloud = WordCloud(width=800, height=500, random_state=42, max_font_size=110,).generate(todas_as_palavras) #background_color="white").generate(todas_as_palavras)

wordcloud

"""Vamos plota-lo/ ebibi-lo com matplotlib."""

import matplotlib.pyplot as plt

plt.figure(figsize=(10, 7))
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis('off')
plt.show()

"""Como nossos dados possuel labels (que foram feitas manualmente) podemos fazer uma wordcloud só para sentimentos positvos ou 0 e outra para coisas complicadas ou 1.

## Wordcloud positiva
"""

palavras_normais =' '.join([texto for texto in dados['tidy_tweet'][dados['label'] == 0]])

wordcloud = WordCloud(width=800, height=500, random_state=42, max_font_size=110, background_color="white", colormap='spring').generate(palavras_normais)

plt.figure(figsize=(10, 7))
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis('off')
plt.show()

"""## Wordcloud complicada"""

palavras_complicadas =' '.join([texto for texto in dados['tidy_tweet'][dados['label'] == 1]])

wordcloud = WordCloud(width=800, height=500, random_state=42, max_font_size=110, colormap='twilight').generate(palavras_complicadas)

plt.figure(figsize=(10, 7))
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis('off')
plt.show()

"""Podemos perceber com essas visualizações que as duas wordclous fazem sentido, então temos bons dados para trabalharmos.

## Analisando hastags

O que mais é impactante no twitter? Geralmente temos trending topics e eles acontecem devido as hashtags. Como será que as hashtags estão distribuidas no nosso caso?
 
 Para analisarmos as hashtags precisamos te-las, Como fazemos isso? Com regex
"""

# identificando as palavras com hashtags com regex
# #(\w+) padrão: catacter que queremos encontrar(palavra que queremos fazer match)

exemplo_hash = '#model, love, #hello'
exemplo_hash2 = ['#model, love, take, with, #time', '#oi']

re.findall(r"#(\w+)", exemplo_hash)

"""Agora que já testamos e sabemos que funciona, vamos fazer uma função para extrair as hashtags"""

for tweet in exemplo_hash2:
  print(tweet)
  hts = re.findall(r"#(\w+)", tweet)
hts

"""Repare que estamos pegando só o último, para termos todas as palavras, vamos guardá-las em uma lista com append"""

def pegar_hashtags(tweet):
    hashtags = []
    for palavra in tweet:
        hts = re.findall(r"#(\w+)", palavra)
        hashtags.append(hts)

    return hashtags

"""Vamos extrair nossas hashtags cujo sentiment é ok primeiro. Como sabemos que o sentimento é ok? Quando a label é 0, podemos fazer esse teste dentro do próprio dataframe. Vou pegar os 5 primeiros tweets cuja label é 0."""

dados[:5]['label'] == 0
# ou dados[:5].label == 0 para quem preferir

dados[:5]['tidy_tweet'][dados['label'] == 0]

"""Vamos assigna-los para hts_regulares para analisarmos depois"""

hts_regulares = pegar_hashtags(dados['tidy_tweet'][dados['label'] == 0])
hts_regulares[:5]

"""Agora o mesmo para os complicados..."""

hts_complicados = pegar_hashtags(dados['tidy_tweet'][dados['label'] == 1])

"""Repare que as nossas listas se tornaram listas de listas, como queremos só as palavras, temos um truque para voltarmos para uma lista só que é somando duas listas. Vamos somar a nossa com uma lista vazia para fazer esse des ecadeamento."""

# desencadeando lista
hts_regulares = sum(hts_regulares,[])
hts_complicados = sum(hts_complicados,[])

"""## Contando a frequencia das hashs com NLTK

Temos todas as nossas hashtags, agora podemos analisa-las, então vamos fazer um gráfico para saber quais são as mais usadas regularmente. Mas como, será que podemos contar as palavras? Sim, se fizermos isso vamos saber qual a frequencia delas e usar no nosso grafico. Felizmente a lib nltk do python já faz isso pra gente com a classe FreqDist.
"""

import nltk

frequencia_hts_regulares = nltk.FreqDist(hts_regulares)
frequencia_hts_regulares

frequencia_hts_complicados = nltk.FreqDist(hts_complicados)

"""Legal agora temos um dicionário de distribuição de frequências das palavras, como em todo dict, podemos usar .keys para as palavras e .values para os numeros. Para fazer o plot vamos organizar esse dicionario primeiro com o nome das colunas e os valores."""

frequencia_hts_regulares.keys()

frequencia_hts_regulares.values()

"""Não queremos criar um dict de dicts, então vou converter nossas chaves e valores para listas."""

dict_frequencias_reg = {'Hashtag': list(frequencia_hts_regulares.keys()),
                  'Contagem': list(frequencia_hts_regulares.values())}

"""E então transformá-lo em dataframe."""

df_frequencia_hts_regulares = pd.DataFrame(dict_frequencias_reg)

df_frequencia_hts_regulares.head(5)

"""Vamos fazer o mesmo para os tweets complicados."""

dict_freq_compl = {'Hashtag': list(frequencia_hts_complicados.keys()),
                  'Contagem': list(frequencia_hts_complicados.values())}
df_frequencia_hts_complicados = pd.DataFrame(dict_freq_compl)
df_frequencia_hts_complicados.head(5)

"""## Plotando hashtags top 10 com seaborn

Vamos usar a lib seaborn para fazer esse gráfico. Para que ele não fique gigante, vamos olhar as 10 primeiras palavras com maior frequencia.
"""

import seaborn as sns

# selecionando as 10 hts com maior freq  

top_10_regulares = df_frequencia_hts_regulares.nlargest(columns="Contagem", n=10)
top_10_complicados = df_frequencia_hts_complicados.nlargest(columns='Contagem', n=10)

plt.figure(figsize=(16,5))
plt.title('10 Hashtags com maior frequência nos tweets positivos')
ax = sns.barplot(data=top_10_regulares, x="Hashtag", y ="Contagem", palette='RdPu')
ax.set(ylabel='Contagem')
plt.show()

plt.figure(figsize=(16,5))
plt.title('10 Hashtags com maior frequência nos tweets negativos')
ax = sns.barplot(data=top_10_complicados, x="Hashtag", y ="Contagem", palette="Blues_d")
ax.set(ylabel='Contagem')
plt.show()

"""Repare que já podemos entender vieses, o que é neutro e o que é positivo para nós com esses gráficos.

# Fazendo previsões com tweets

Agora podemos usar esses tweets para fazer um modelo que vai saber dizer o que é positivo ou negativo em outros tweets.

Para isso como vamos fazer que a máquina que entende números entenda as nossas palavras? Convertendo-as em sequencias lineares de numeros ou vetorizando. Um jeito de fazer isso é fazendo um 'saco de palavras' ou bag of words, BOW.

## Convertendo texto em vetor usando BOW
"""

from sklearn.feature_extraction.text import CountVectorizer
# max_df significa que se a palavra estiver em 90% dos documentos, vamos ignora-la.  
# min_df significa que se estiver em apenas 2 documentos, também.
vetorizador_bow = CountVectorizer(max_df=0.90, min_df=2, stop_words='english')

bow = vetorizador_bow.fit_transform(dados['tidy_tweet'])

bow

"""Show, agora temos vetores de frequencias de palavras. 

Vamos criar o nosso classificador. Vamos fazer uma regressão logística para prever o sentimento de novos tweets.

## Criando e treinando o clf

Dividindo entre treino e validacao.
"""

# Dividindo os dados em treino e teste novamente
from sklearn.model_selection import train_test_split

treino_bow = bow[:31962,:]
teste_bow = bow[31962:,:]

x_treino_bow, x_validacao_bow, y_treino, y_validacao = train_test_split(treino_bow, tweets_treino['label'], random_state=42, test_size=0.3)

"""Criando o classificador."""

from sklearn.linear_model import LogisticRegression

clf_regressao_logistica = LogisticRegression()

"""Treinando o modelo."""

clf_regressao_logistica.fit(x_treino_bow, y_treino)

"""Fazendo as predições para o conjunto de validação.

## Prevendo para validação
"""

predicoes_bow = clf_regressao_logistica.predict(x_validacao_bow)

predicoes_bow[:3]

y_validacao[:3]

"""Além de usar o predict, podemos também saber qual foi a estimativa da regressão para cada uma das classificacoes, 0 ou 1. Fazemos isso chamando o predict_proba."""

predicoes_bow_proba = clf_regressao_logistica.predict_proba(x_validacao_bow)
predicoes_bow_proba

#mantendo apenas a segunda coluna
predicoes_bow_proba[:,1]

from sklearn.metrics import f1_score

f1_score(y_validacao, predicoes_bow)

# é pra dar erro mesmo aqui
f1_score(y_validacao, predicoes_bow_proba)

"""Vamos arrumar nossas predições para calcular o f1. Se a probabilidade for igual a 0.3 ou maior, vai ser negativo, senão, vai ser positivo."""

# com [:,1] pegamos apenas a coluna com os valores das predições
predicoes_transformadas = predicoes_bow_proba[:,1] >= 0.3

predicoes_transformadas

"""Repare que ao colocarmos uma condição, nossos valores contínuos viraram booleanos, agora basta converte-los para inteiros."""

predicoes_int = predicoes_transformadas.astype(np.int)
# algumas pessoas chamam teste de validação, outras dividem em treino, teste e validação
f1_score(y_validacao, predicoes_int)

from sklearn.metrics import classification_report

print(classification_report(y_validacao, predicoes_int))

"""Fazendo predições para teste."""

predicoes_teste = clf_regressao_logistica.predict_proba(teste_bow)

predicoes_teste_int = predicoes_teste[:,1] >= 0.3
predicoes_teste_int = predicoes_teste_int.astype(np.int)

tweets_teste['label'] = predicoes_teste_int

resultados = tweets_teste[['id','label']]

resultados.head(5)

"""Vamos salvar os resultados em um csv"""

resultados.to_csv('resultados_reg_log_bow.csv', index=False)

tweets_teste.head(35)

"""## Salvando o modelo"""

import pickle

nome_arquivo = 'modelo_reg_log_tweets.pkl'
pickle.dump(clf_regressao_logistica, open(nome_arquivo, 'wb'))

"""Vendo se ele funciona."""

modelo_carregado = pickle.load(open(nome_arquivo, 'rb'))
acuracia = modelo_carregado.score(x_validacao_bow, y_validacao)

acuracia