#coding: utf-8

#import des modules
import json 
import pprint
pp = pprint.PrettyPrinter(indent=4)
import matplotlib.pyplot as plt
import numpy as np
import networkx as nx
from collections import defaultdict, Counter
# Les versions de l'article 9

## La version originale
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
## Les versions alternatives

versions = article9["versions"]
versions_c = []
#
auteurs_d = defaultdict.fromkeys([v["author"] for v in versions], [])

versions_d = defaultdict.fromkeys([v["slug"] for v in versions], {})
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
    auteurs_d[v["author"]].append(vn)
    versions_c.append(vn)
    versions_d[v["slug"]] = vn
versions_c.append(version_originale)
versions_d[version_originale["slug"]] = version_originale
#versions_d = {versions_d[v["slug"]]: v for v in versions_c}
auteurs_d["gouvernement"] = [version_originale]




# Les votes
## Les votes sur l'ensemble des articles

#Les votes sont détaillés par participants
with open("participants.json", "r") as f:
    data = json.load(f)
    participants = data["participants"]
#Verifions le nombre de participants
print len(participants), "participants sur l'ensemble des articles"

#la liste des noms des participants
electeurs = list(set([n.keys()[0] for n in participants]))
## Les votes sur l'article 9
art = "article-9-acces-aux-travaux-de-la-recherche-financee-par-des-fonds-publics"
votes = []
electeurs_d = dict.fromkeys(electeurs, [])
for user in participants:
    #accesible via son nom
    name =  user.keys()[0]
    #récupérer les votes de l'utilisateur dans "votes"
    #filtrer ceux qui ont des votes qui correspondent à l'article
    for vote in user[name]["votes"]:
        if art in vote["link"]:
            vote["electeur"] = name
            electeurs_d[name].append(vote)
            if vote not in votes:
                votes.append(vote)
                electeurs_d[name].append(vote)
electeurs_d = {k:v for k,v in electeurs_d.items() if k!= []}
print len(votes), "votes sur des articles, arguments ou sources"
print len(electeurs_d), "electeurs sur l'article 9"
print len(set(auteurs_d.keys())), "auteurs de versions d'article"
#Rappatrier les votes de versions
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
#Construire le graphe electeur -> auteur
g = nx.Graph()
#ajouter les electeurs
for n in list(set(electeurs_d.keys()) & set(auteurs_d.keys())):
    try:
        g.add_nodes_from(n, color='red', weight=len(auteurs_d[n]))
    except:
        g.add_nodes_from(n, color='blue', weight=len(electeurs_d[n]))
        

#g.add_nodes_from(auteurs_d, color='red', weight=[len(v) for v in auteurs_d.values()])
#votes_vs_auteur = defaultdict.fromkeys(electeurs_d, [])
#~ from itertools import combination
#~ combo = combination(electeurs_d, 2)
#~ for n in combo:
    #~ if n[1] not in auteurs_d.keys():
        #~ combo.pop(n)
#~ print len(combo)

#cooc = defaultdict.from_keys(electeurs_d, 
edges = []
auteurs_v = []
electeurs_v = []
for version, data in versions_d.items():
    
    v_pour = [(vote["electeur"],data["author"]) for vote in data["votes"] if vote["opinion"] == "1"]
    #edges_count.append(data["electeur")
    edges.extend(v_pour)
    
for k,v in Counter(edges).items():
    print k[0], k[1]
    g.add_edge(k[0], k[1], weight=v)
#print len(edges)

print len(nx.isolates(g)), "noeuds isolés"
for ni in nx.isolates(g):
    #~ print ni
    g.remove_node(ni)
    
nx.write_gexf(g, "electeurs_pour.gexf")


        
