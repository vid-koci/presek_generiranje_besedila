import re
import random
from random import choices
from os import listdir
from os.path import isfile, join
random.seed(0)
red_markovske_verige = 2
mapa = "preseren"

besedila=[]
#zbremo besedila in jih očistimo
for esej in [f for f in listdir(mapa) if isfile(join(mapa, f))]:
    besedila.append(re.sub('[^0-9a-zčžš !\.\?]','',open(join(mapa,esej),'r').read().strip().lower().replace('\n',' ').replace("."," .").replace("?"," ?").replace("!"," !")).split())
markov = {}
#štejemo ponovitve
for besedilo in besedila:
    besedilo.append("<konec>")
    n_gram = tuple("<start>" for _ in range(red_markovske_verige))
    for beseda in besedilo:
        if not n_gram in markov:
            markov[n_gram]={}
        if not beseda in markov[n_gram]:
            markov[n_gram][beseda]=0
        markov[n_gram][beseda]+=1
        n_gram = tuple(list(n_gram[1:])+[beseda])
#normaliziramo vsako tabelo, da iz št. ponovitev dobimo verjetnostno porazdelitev
for n_gram, tabela in markov.items():
    vsota = sum(p for b,p in tabela.items())
    for b,p in tabela.items():
        markov[n_gram][b]=p/float(vsota)

#generiramo nov esej!
n_gram = tuple("<start>" for _ in range(red_markovske_verige))
esej=[]
while True:#ignoriramo profesorja programiranja, ki pravi, da neskončne zanke niso lepa praksa
    kandidati = [b for b,_ in markov[n_gram].items()]
    verjetnosti = [p for _,p in markov[n_gram].items()]
    nova_beseda = choices(kandidati,verjetnosti)[0]
    if nova_beseda=="<konec>":
        break
    esej.append(nova_beseda)
    n_gram = tuple(list(n_gram[1:])+[nova_beseda])
print(" ".join(esej).replace(" .",".").replace(" !","!").replace(" ?","?"))
