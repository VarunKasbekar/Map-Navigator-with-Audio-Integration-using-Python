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

class MyGraph(nx.DiGraph):
    __edges={}
    __nodes={}
    def __init__(self):
        """
            >>> G= MyGraph()
            Are you disabled?
            Please enter YES or NO
        """

        nx.DiGraph.__init__(self)
        #add edges
        #consider the disable people
        os.system("say 'Are you disabled? Please enter YES or NO'")
        criteria = input("Are you disabled?\nPlease enter YES or NO\n")

        if criteria == 'YES' or criteria == 'yes' or criteria == 'Yes':
            for i in range(len(df['from_node'])):
                if df['accessible'][i] != 0:
                    if df['bidirectional'][i] == 1:
                        self.add_edge(df['from_node'][i], df['to_node'][i], weight=df['weight'][i])
                        self.add_edge(df['to_node'][i], df['from_node'][i], weight=df['weight'][i])
                        self.__edges[df['from_node'][i], df['to_node'][i]] = (
                        df['edge'][i], df['weight'][i], df['direction'][i])
                        self.__edges[df['to_node'][i], df['from_node'][i]] = (
                        df['edge'][i], df['weight'][i], reverse[df['direction'][i]])
                    else:
                        self.add_edge(df['from_node'][i], df['to_node'][i], weight=df['weight'][i])
                        self.__edges[df['from_node'][i], df['to_node'][i]] = (
                        df['edge'][i], df['weight'][i], df['direction'][i])

        elif criteria == 'NO' or criteria == 'No' or criteria == 'no':
            for i in range(len(df['from_node'])):
                if df['bidirectional'][i] == 1:
                    self.add_edge(df['from_node'][i], df['to_node'][i], weight=df['weight'][i])
                    self.add_edge(df['to_node'][i], df['from_node'][i], weight=df['weight'][i])
                    self.__edges[df['from_node'][i], df['to_node'][i]] = (df['edge'][i], df['weight'][i], df['direction'][i])
                    self.__edges[df['to_node'][i], df['from_node'][i]] = (df['edge'][i], df['weight'][i], reverse[df['direction'][i]])
                else:
                    self.add_edge(df['from_node'][i], df['to_node'][i], weight=df['weight'][i])
                    self.__edges[df['from_node'][i], df['to_node'][i]] = (df['edge'][i], df['weight'][i], df['direction'][i])
        else:
            os.system("say Incorrect input")
            raise ValueError('Incorrect Input')

        #add node
        for k in range(len(f['name'])):
           self.__nodes[f['name'][k]]= (f['type'][k],f['min_height'][k],f['avg_wait_time'][k])

    # find the shortest path between start and destination
    def find_shortest_path(self, start, des):

        """Given strings start and des, find the shortest path use networkx. Storage name of all attractions on the path.

            :param start: a string for the start point
            :param des: a string for destination
            :return: the name of attractions on the path in a list

            >>> find_shortest_path("7d", "exit")
            ['7d', 'southerntreat', 'thunder', 'arcticcircle', 'junction15', 'junction16', 'junction17', 'rockingalley', 'junction19', 'exit']

        """


        try:
            #print(list(self.node))
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





    # the routes of the shortest path
    def shortest_route(self,shortest):

        """Given a list shortest, use for loop to get records for the route

            :param shortest: a list include name of attractions on the path
            :return: a list of records

            >>> shortest_route(['7d', 'southerntreat', 'thunder', 'arcticcircle', 'junction15', 'junction16', 'junction17', 'rockingalley', 'junction19', 'exit'])

            [' Please continue on 7d_streat road northwest for 0.34 miles', ' Please continue on streat_thunder road east for 0.4 miles',
            ' Please continue on thunder_arc road east for 0.25 miles', ' Please continue on arc_junc15 road east for 0.31 miles',
            ' Please continue on junc15_junc16 road northeast for 0.11 miles', ' Please continue on junc16_junc17 road northeast for 0.19 miles',
            ' Please continue on junc17_ralley road east for 0.32 miles', ' Please continue on ralley_junc19 road north for 0.34 miles',
            ' Please continue on junc19_exit road northwest for 0.28 miles']

        """


        route = []
        record=''
        for k in range(len(shortest) - 1):
            stri = shortest[k]
            des = shortest[k + 1]
            paths = self.__edges[(stri, des)]
            os.system("say Continue on" + paths[0] + "road")
            os.system("say for" + str(paths[1])+"miles")
            os.system("say with direction" + paths[2])
            record = ' Please continue on %s road %s for %s miles' % (paths[0], paths[2], paths[1])
            route.append(record)


        return route

    #find the name and weight of each route
    def shortest_routes(self,shortest):


        """Given a list shortest, use for loop to get the mileage for each segment

            :param shortest: a list include name of attractions on the path
            :return: a list of mileage for each segment

            >>> shortest_routes(['7d', 'southerntreat', 'thunder', 'arcticcircle', 'junction15', 'junction16', 'junction17', 'rockingalley', 'junction19', 'exit'])

            [0.34, 0.4, 0.25, 0.31, 0.11, 0.19, 0.32, 0.34, 0.28]

        """

        routes=[]
        for x in range(len(shortest) - 1):
            stri = shortest[x]
            des = shortest[x + 1]
            paths = self.__edges[(stri, des)]
            routes.append(float(paths[1]))

        return routes


    #print each route
    def print_output(self, route):

        """Given a list route, use for loop to print each record

            :param route: a list for segments
            :return: print

            >>> print_output([' Please continue on 7d_streat road northwest for 0.34 miles', ' Please continue on streat_thunder road east for 0.4 miles',
            ' Please continue on thunder_arc road east for 0.25 miles', ' Please continue on arc_junc15 road east for 0.31 miles',
            ' Please continue on junc15_junc16 road northeast for 0.11 miles', ' Please continue on junc16_junc17 road northeast for 0.19 miles',
            ' Please continue on junc17_ralley road east for 0.32 miles', ' Please continue on ralley_junc19 road north for 0.34 miles',
            ' Please continue on junc19_exit road northwest for 0.28 miles'])


             Please continue on 7d_streat road northwest for 0.34 miles
             Please continue on streat_thunder road east for 0.4 miles
             Please continue on thunder_arc road east for 0.25 miles
             Please continue on arc_junc15 road east for 0.31 miles
             Please continue on junc15_junc16 road northeast for 0.11 miles
             Please continue on junc16_junc17 road northeast for 0.19 miles
             Please continue on junc17_ralley road east for 0.32 miles
             Please continue on ralley_junc19 road north for 0.34 miles
             Please continue on junc19_exit road northwest for 0.28 miles


        """


        for record in route:
            print(record)




    #print the min height and average waiting time of the destination
    def print_info(self, node):

        """Given a string node which is name of the destination, print information for the node.

            :param node: a list include type, minimun height and wait time of the attraction
            :return: print

            >>> print_info(exit)
            The type of the destination is : Way To Exit
            The minimun height for this attraction is : 1 cm
            The average waiting time is : 1 minutes

        """

        type=self.__nodes[(node)][0]
        height=self.__nodes[(node)][1]
        time=self.__nodes[(node)][2]
        os.system("say The type of the destination is"+type+ ", The minimun height required for this attraction is"+str(height)+"cm, The average waiting time is"+str(time)+"minutes")
        info='The type of the destination is : %s \nThe minimun height for this attraction is : %s cm \nThe average waiting time is : %s minutes ' % (type,height, time)
        print(info)



def main():
    while True:
        try:
            G = MyGraph()
            #showing the type, height, average waiting type of the destination
            name = f['name'].values.tolist()
            names=sorted(name)
            os.system("say this is the list of all attractions")
            print('This is the list of all the ATTRACTIONS:\n')
            for x in names:
                print((names.index(x)+1), x)
            try:
                #os.system("say Enter your current location number according to the list")
                startnumber=int(input('\nEnter your current location number according to the list:\n'))
                start=names[startnumber-1]
                os.system("say Enter your destination number according to the list")
                destinationnumber=int(input('\nEnter your destination number according to the list:\n'))
                destination=names[destinationnumber-1]
                os.system("say The way from " + start + " to " + destination + " is as follows")
                shortest = G.find_shortest_path(start, destination)
                route = G.shortest_route(shortest)
                routes=G.shortest_routes(shortest)
                print("\nThe way from " + start + " to " + destination + " is as follows:")
                G.print_output(route)
                #finding sum of the total distance
                ans=sum(routes)
                #Rounding the total distance upto 3 decimal places
                totdist=round(ans,2)
                os.system("say The total distance to your destination is"+str(totdist)+"miles")
                print("\nThe total distance to your destination is", totdist, "miles")
                G.print_info(destination)
                option="no"
                os.system("say Do you wish to travel to another destination or Quit?, Enter YES or QUIT")
                option = input('\nDo you wish to travel to another destination or Quit?\nEnter YES or QUIT')
                quitcond=["QUIT", "quit", "Quit"]
                yescond=["YES", "yes", "Yes"]
                while option in yescond:
                    print('This is the list of all the ATTRACTIONS:\n')
                    for x in names:
                        print((names.index(x) + 1), x)
                    os.system("say Enter your destination number according to the list")
                    destination_next_number = int(input('\nEnter your destination number according to the list:\n'))
                    destination_next=names[destination_next_number-1]
                    shortest = G.find_shortest_path(destination, destination_next)
                    route = G.shortest_route(shortest)
                    routes = G.shortest_routes(shortest)
                    os.system("say The way from " + destination  + " to " + destination_next+ " is as follows")
                    print("\nThe way from " + destination + " to " + destination_next + " is as follows:")
                    G.print_output(route)
                    ans2=sum(routes)
                    totdist2=round(ans2,2)
                    os.system("say The total distance to your destination is" + str(totdist2) + "miles")
                    print("\nThe total distance to your destination is", totdist2, "miles")
                    G.print_info(destination_next)
                    os.system("say Do you wish to travel to another destination or Quit, Enter YES or QUIT")
                    option = input('\nDo you wish to travel to another destination or Quit?\nEnter YES or QUIT\n')
                    destination = destination_next
                if option in quitcond:
                    os.system("say Thank you")
                    print("THANK YOU")
                    break
                else:
                    print('Incorrect Input')
                    raise ValueError
            except ValueError:
                pass
        except ValueError as e:
            print(e)





if __name__ == "__main__":
    main()