#coding: utf-8
#import des modules
#lecture des json
import json 
#affichage des dictionnaires avec idententation
import pprint
pp = pprint.PrettyPrinter(indent=4, )
#librairie des graphes
import networkx as nx
#affichage des graphs
import matplotlib
import matplotlib.pyplot as plt
#calcul
import numpy as np
from itertools import combinations
#%matplotlib inline

    
def load_versions(art_file="article9.json"):
    '''charger l'ensemble des versions de l'article'''
    versions_d = {}
    with open(art_file, "r") as f:
        article9 = json.load(f)
    
    #Pour rappel
    #print article9.keys()
    versions_d[article9["article_link"].split("/")[-1]] = {
                "id": 0,
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
                "total_votes": article9["votes_total"],
                #les décomptes de votes sur les arguments ne sont pas disponible dans l'article9
                  # seulement le nombre d'arguments
                "total_arguments_votes": article9["arguments_count"]
               }
    
    versions = article9["versions"]
    
    #on construit une liste de versions
    for i,v in enumerate(versions):
        #pour rappel
        #print v.keys()
        versions_d[v["slug"]] = {"date":v["created_at"],
                "id": i+1,
                "link":v["link"],
                #"slug":v["slug"],
                "title":v["title"],
                "text": v['comment'],
                "author": v["author"],
                "votes":[], 
                "arguments":[], 
                "votes_arguments": [],
                "sources":[],
                "votes_sources": [],
                "total_votes":v["votes_total"],
              #ici il s'agit bien du nombre de votes sur un argument
                "total_arguments_votes": v["arguments_count"]
             }
    print(len(versions_d)), "versions"
    return versions_d
    
def load_participants():
    #charger les votes des participants
    with open("participants.json", "r") as f:
        data = json.load(f)
        participants = data["participants"]
    
    participants_d = {}
    for part in participants:
        for k,v in part.items():
            
            participants_d[k] = v["votes"]
        
    print (len(participants_d), "participants sur l'ensemble des articles")
    return participants_d

def update_versions(participants, versions_d, art="article-9-acces-aux-travaux-de-la-recherche-financee-par-des-fonds-publics"):
    for user, votes in participants.items():
        for vote in votes:            
            link = vote["link"]
            
            if art in link:
                date =  vote["date"]
                opinion = vote["opinion"]
                slug = link.split("/")[-1]
                try:
                    slug, tid = slug.split("#") 
                    
                    
                    if "arg-" in tid:
                        versions_d[slug]["votes_arguments"].append({"electeur":user,"vote": opinion, "date":date, "id":tid})
                    elif "source-" in tid:
                        versions_d[slug]["votes_sources"].append({"electeur":user,"vote": opinion, "date":date, "id":tid})
                    else:
                        print slug
                except:
                    versions_d[slug]["votes"].append({"electeur":user,"vote": opinion, "date":date})
    return versions_d
    
def load_votes(participants,art ="article-9-acces-aux-travaux-de-la-recherche-financee-par-des-fonds-publics"):
    #charger les votes des electeurs de l'article 9
    votes_v = []
    votes_args = []
    votes_src = []
    for user, votes in participants.items():
        for vote in votes:
            link = vote["link"]
            if art in link:
                date =  vote["date"]
                opinion = vote["opinion"]
                slug = link.split("/")[-1]
                try:
                    slug, tid = slug.split("#") 
                    if "arg-" in tid:
                        votes_args.append({"electeur":user,"vote": opinion, "slug":slug, "date":date, "id":tid})
                    elif "source-" in tid:
                        votes_src.append({"electeur":user,"vote": opinion, "slug":slug, "date":date, "id":tid})
                    else:
                        print slug
                except:
                    votes_v.append({"electeur":user,"vote": opinion, "slug":slug, "date":date})
            
    print len(votes_v),"votes", len(votes_args),"votes sur les arg", len(votes_src), "votes sur les sources"
    return votes_v, votes_args, votes_src
        
        
        

    
def filter_top_electeurs(votes, SEUIL):
    from collections import Counter, defaultdict
    electeurs_d = defaultdict.fromkeys([v["electeur"] for v in votes], [])
    for vote in votes:
        electeurs_d[vote["electeur"]].append(v)
    
    top_users = []
    f = Counter([data["electeur"] for data in votes])
    
    for n,cpt in f.items():
        if cpt < SEUIL:
            del electeurs_d[n]
    #for k, v in electeurs_d.items():
    #    top_users.append(v)
    print len(electeurs_d), "electeurs uniques ayant voté au moins %i fois" %SEUIL
    return electeurs_d
    
def calc_similarity(electeurs, versions_d, SEUIL=0):
    
    from itertools import combinations
    votes_by_version = {}
    for v, k in versions_d.items():
        votes_by_version[v] = {e["electeur"]:e["vote"] for e in k["votes"]}
        
    similarity_score = {}
    for couple in combinations(electeurs.keys(), 2):
        userA, userB = couple
        similarity_score[couple] = 0
        for k,v in votes_by_version.items():
            if userA in v.keys() and userB in v.keys():
                if v[userA] == v[userB]:
                    similarity_score[couple] += 1
    return {k:v for k,v in similarity_score.items() if v > SEUIL}
        
def build_graph(simil, top_users):
    g = nx.Graph()
    pos = nx.spring_layout(g)
    
    
    for k in simil.keys():
        g.add_nodes_from(k[0], weight=len(top_users[k[0]]))
        g.add_nodes_from(k[1], weight=len(top_users[k[1]]))
    #nodesize=[len(top_users[v])*1000 for v in g.nodes()]
    #nx.draw_networkx_nodes(g, pos, nodelist=g.nodes(), node_size=, alpha=1, label=True)
    for couple, score in simil.items():
        userA, userB = couple
        g.add_edge(userA, userB, weight=score)
        
    for node in nx.isolates(g):
        g.remove_node(node)
    nx.write_gexf(g, "electeurs_VF_SEUIL_5_5.gexf")
    nx.draw(g)
    plt.show()
    return
    
def build_histogram(versions_nb):
    import pylab
    N = len(versions_d)
    votes_infos = [v["total_votes"]  for v in versions_nb.values()]
    
    args_infos = [v["total_arguments_votes"]  for v in versions_nb.values()]
    plt.title("Historique des votes et votes d'arguments par version")
    plt.ylabel('Nb votes')
    #pylab.xlim([0,108])
    plt.plot(votes_infos,color='r')
    plt.plot(args_infos,color='b')

    plt.show()
    plt.title("historique des votes des arguments par version")
    plt.ylabel('Nb votes sur les arguments')
    pylab.xlim([0,len(versions_nb)])
    plt.plot(args_infos,color='b')
    plt.show()
    return
    
def build_distrib(freq):
    '''build repartition votes'''
    N = len(freq)
    plt.title("Nombre de votes par auteurs")
    plt.plot(sorted(freq.values()),color='r')
    plt.show()
    plt.title("historique des votes des arguments par version")
    plt.ylabel('Nb votes sur les arguments')
    pylab.xlim([0,N])
    pylab.ylim([1,50])
    plt.show()
    return 

if __name__ == "__main__":
    #versions_d = build_versions()
    #votes, electeurs_d = load_electeurs()
    vs = load_versions()
    part = load_participants()
    vs = update_versions(part, vs)
    votes,vvargs, vsources= load_votes(part)
    SEUIL = (4, 2)
    top_electeurs = filter_top_electeurs(votes, SEUIL[0])
    similar_couple = calc_similarity(top_electeurs, vs, SEUIL[1])
    #~ with open("./similarity_score.json", "w") as f:
        #~ f.write(json.dumps(similar_couple, indent=4))
    graph = build_graph(similar_couple, top_electeurs)
