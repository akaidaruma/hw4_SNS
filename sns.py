# link.txtの読み込みからlink_listまでのリスト化を行う
def read_linkfile(linkfile_name):
    links_file = open(linkfile_name, "r")
    links = links_file.readlines()
    links_file.close()
    return links

def txt2linklist(line):
    num = ""
    target = {}
    for i in range(len(line)):
        if line[i] != ",":
            num += line[i]
        else:
            target["from"] = int(num)
            num = ""  
        if i==len(line)-1:
            target["to"] = int(num)
            num = ""
    return target

def make_linklist(links):
    for line in links:
        l = list(line.replace("\t", ",").replace("\n",""))
        link_list.append(txt2linklist(l))
    return link_list

# nickname.txtの読み込みからnickname_listまでのリスト化を行う
def read_nicknamefile(nicknamefile_name):
    nicknames_file = open(nicknamefile_name, "r")
    nicknames = nicknames_file.readlines()
    nicknames_file.close()
    return nicknames

def txt2nicknamelist(line):
    num = ""
    name = ""
    target = {}
    for i in range(len(line)):
        if line[i].isdigit():
            num += line[i]
        else:
            name += line[i]
        if line[i]==",":
            target["number"] = int(num)
        elif i==len(line)-1:
            target["name"] = name.replace(",", "")
    return target

def make_nicknamelist(nicknames):
    for line in nicknames:
        n = list(line.replace("\t", ",").replace("\n",""))
        nickname_list.append(txt2nicknamelist(n))
    return nickname_list

# linkとlinkを構成するノードのidからグラフを作成
def make_graph(link_list, nodenum_list):
    relation = []
    for num in nodenum_list:
        relation.append([link.get("to") for link in link_list if link["from"]==num])
    return relation

# 訪問したかどうかをvisit_statesで管理するために初期化
def set_unvisited(graph):
    visit_states = []
    for _ in range(len(graph)):
        visit_states.append(None)
    return visit_states

# 最短ルートの長さを出力
def bfs(graph, start, goal):
    queue = []
    visit_states[start] = True
    queue.append(start)
    route = {}
    route[start] = [start]
    while queue:
        #print(queue)
        pos = queue.pop(0)
        if pos == goal:
            #print(route)
            return len(route[pos])-1
        for index in graph[pos]:
            if visit_states[index] == None:
                queue.append(index)
                visit_states[index] = True
                route[index] = route[pos] + [index]

if __name__ == '__main__':

    links = read_linkfile("links.txt")
    nicknames = read_nicknamefile("nicknames.txt")

    link_list = []
    link_list = make_linklist(links)

    nickname_list = []
    nickname_list = make_nicknamelist(nicknames)

    nodenum_list = [line["number"] for line in nickname_list]

    relation = make_graph(link_list, nodenum_list)

    visit_states = set_unvisited(relation)

    print("your account_id:")
    # start_name = input()
    start_num = int(input())
    print("target account_id:")
    # goal_num = input()
    goal_num = int(input())
    step = bfs(relation, start_num, goal_num)

    print("shortest path: %d" % step)
