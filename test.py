import networkx as nx
import pandas as pd
import os
from termcolor import colored

print(colored('WELCOME TO ESSELWORLD....', 'green'))

G = nx.DiGraph()
reverse = {'north':'south', 'south':'north', 'east':'west', 'west':'east', 'northeast' : 'southwest', 'southeast': 'northwest', 'northwest' : 'southeast', 'southwest' : 'northeast'}
df = pd.read_csv('EsselWorld.csv')
f = pd.read_csv('Attractions.csv')
os.system("say 'Welcome To Esselworld'")



def find_shortest_path(self, start, des):

        """Given strings start and des, find the shortest path use networkx

            :param start: a string for the start point
            :param des: a string for destination
            :return: the shortest path in a list

            >>>
        """

        try:
            # print(list(self.node))
            shortest = nx.dijkstra_path(self, start, des)
            return shortest
        except nx.exception.NetworkXNoPath:
            os.system("say No path exists, Please refine your search")
            print('No path exists.Please refine your search')
            raise ValueError

        except nx.exception.NodeNotFound:
            os.system("say No path exists, Please refine your search")
            print('No path exists, Please refine your search')
            raise ValueError



def main():
    start = "7d"

    des = "aeroswinger"

    short = find_shortest_path(start, des)

    print(short)


main()
