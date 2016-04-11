#coding: utf-8
#import des modules

import json 
import pprint
pp = pprint.PrettyPrinter(indent=4, )

import matplotlib.pyplot as plt
import numpy as np
import networkx as nx
#chargement de l'article 9
with open("article9.json", "r") as f:
    article9 = json.load(f)

version_originale = {
                "date": article9["created_at"],
                "link": article9["article_link"],
                "slug": article9["article_link"].split("/")[-1],
                "title": article9["article_link"].split("/")[-1].replace("-", " "),
                "text": article9['body'],
                "author": article9["author"],
                "votes":[], 
                "arguments":article9["arguments"], 
                "votes_arguments": [],
                "sources":article9["sources"],
                "votes_sources": [],
               }

versions = article9["versions"]
versions_c = []
for v in versions:
    vn = {"date":v["created_at"],
            "link":v["link"],
            "slug":v["slug"],
            "title":v["title"],
            "text": v['comment'],
            "author": v["author"],
                      "votes":[], 
            "arguments":[], 
            "votes_arguments": [],
            "sources":[],
            "votes_sources": []}
    versions_c.append(vn)

versions_c.append(version_originale)
versions_d = {}

for v in versions_c:
    versions_d[v["slug"]] = v

print len(versions_d)

#Ici on ne s'intéresse qu'aux votes
#qui sont détaillés par participants
with open("participants.json", "r") as f:
    data = json.load(f)
    participants = data["participants"]
#Verifions le nombre de participants

print len(participants), "participants sur l'ensemble des articles"
#les noms des participants
electeurs = list(set([n.keys()[0] for n in participants]))
art = "article-9-acces-aux-travaux-de-la-recherche-financee-par-des-fonds-publics"
votes = []

for user in participants:
    #accesible via son nom
    name =  user.keys()[0]
    electeurs_d[name] = []
    #récupérer les votes de l'utilisateur dans "votes"
    #filtrer ceux qui ont des votes qui correspondent à l'article
    for vote in user[name]["votes"]:
        if art in vote["link"]:
            vote["electeur"] = name
            electeurs_d[name].append(vote)
            if vote not in votes:
                votes.append(vote)
print len(votes), "votes sur des articles, arguments ou sources"
print len(electeurs_d), "electeurs"

for vote in votes:
    url = vote["link"]
    slug = url.split("/")[-1]
    #vote sur un argument        
    if "#arg" in slug:
        vote["slug"], vote["id"] = slug.split("#")
        versions_d[vote["slug"]]["votes_arguments"].append(vote)
        
        #vote sur une source
    elif "#source" in slug:
        vote["slug"], vote["id"] = slug.split("#")
        versions_d[vote["slug"]]["votes_sources"].append(vote)
        
    #vote sur un article
    else:
        vote["slug"] = slug
        versions_d[vote["slug"]]["votes"].append(vote)
print len(versions_d[art]["votes"])
auteur_electeur = []
electeurs_d = {}
auteurs_d = 

for version, data in versions_d.items():
    for vote in data["votes"]:
        
        auteur_electeur.append([version, data["author"], vote["electeur"], vote["opinion"]])
#~ with open("votes_auteur_electeur.csv", "w") as f:
    #~ f.write("version\tauteur\telecteur\tvote\n")
    #~ for line in auteur_electeur:
        #~ f.write(("\t").join(line)+"\n")
#~ 
#~ from collections import Counter
#~ import operator
#~ votes_electeurs = Counter([n[2] for n in auteur_electeur])
#~ nb_electeurs = len(votes_electeurs)
#~ nb_votes = sum(votes_electeurs.values())
#~ print nb_votes,"votes", nb_electeurs, "electeurs"
#top_votants = votes_electeurs.most_common(563)

#print top_votants

#plt.bar(range(len(top_votants)), top_votants.values(), align='center')
#plt.xticks(range(len(top_votants)), range(len(top_votants)))
#plt.show()

one_vote = {k:v for k,v in votes_electeurs.items() if v ==1}
nb_one_vote = len(one_vote)
print nb_one_vote, "electeurs uniques qui ont voté une seule fois"
multiple_vote = {k:v for k,v in votes_electeurs.items() if v > 1}
print len(multiple_vote), "electeurs uniques qui ont voté plusieurs fois"
print "pour un total de", sum(multiple_vote.values()), "votes"
g = nx.Graph()

for name, data in electeurs_d.items():
    if data == []:
        del electeurs_d[name]
    else:
        g.add_node(name, font_size = 16, weight=len(data))
        
        for n in data:
            #g.add_edge(n
            print name, n["electeur"]
            #g.add_edge(name, n["author"], font_size = 16, weight=len(electeurs_d[name]))
        break
'''
>>> solitary=[ n for n,d in G.degree_iter(with_labels=True) if d==0 ]
>>> G.delete_nodes_from(solitary)


For more general node removal, I would suggest the subgraph() method.
If you can get a list of the nodes you want to keep, use that as an
argument
to the subgraph routine. Something like:

>>> keepers=node_connected_component(original_graph, 1000)
>>> new_graph=original_graph.subgraph(keepers)
'''
#seuil de participations = 5
#votes_seuil = {k:v for k,v in votes_electeurs.items() if v >= 5}
#print len(votes_seuil), sum(votes_seuil.values())
'''
from itertools import combinations
from math import factorial as fact
combo = list(set(combinations(votes_seuil.keys(), 2)))
similarity_score = {}
g = nx.Graph()
for c in combinations(votes_seuil.keys(), 2):
    #print c
    userA, userB = c
    g.add_node(userA, font_size = 16, weight=len(electeurs_d[userA]))
    g.add_node(userB, font_size = 16, weight=len(electeurs_d[userB]))
    #add_node(G, c, label=contributions[c]["name"], total_votes=contributions[c]["votes_total"], type=contributions[c]["type"], author=contributions[c]["author"], url=contributions[c]['url'], section=contributions[c]['section'], votes_pro=contributions[c]['votes_pro'], votes_against=contributions[c]['votes_against'], votes_unsure=contributions[c]['votes_unsure'], type_source=aut_type)
    #print userA, userB
    similarity_score[c] = 0
    userweight = 0
    for v, k in versions_d.items():
        electeur_d = {e["electeur"]:e["opinion"] for e in k["votes"]}
        #print electeur_d.keys()
        if userA in electeur_d.keys() and userB in electeur_d.keys():
            if electeur_d[userA] == electeur_d[userB]:
                similarity_score[c] += 1

#pos = nx.balanced_tree(3,5)
#g.add_nodes_from(votes_seuil.keys(), font_size = 16)
#nx.draw_networkx_labels(g,pos,votes_seuil,font_size=16)

#plt.show()
edges = [(user_co[0], user_co[1]) for user_co, score in similarity_score.items() if score > 5]
#, {"color":"green", "weight":score})
g.add_edges_from(edges)
nx.write_gexf(g, "electeurs5.gexf")
'''
