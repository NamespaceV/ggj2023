class Person():
    def __init__(self, id, displayName, parents):
        self.id = id
        self.displayName = displayName
        self.parents = parents
        self.genes = genes = [1,1,1]
    
    def updateGene(self, geneId):
        if len(self.parents) > 1:
            print(f'blocked mod on {self.id} due to parents {self.parents} ')
            return False
        old = self.genes[geneId]
        self.genes[geneId] = (self.genes[geneId]) % 3 + 1
        print("gene modified ",self.id," gene ",geneId,"[",old," => ", self.genes[geneId],"]")
        self.updateChildren()
        return True
        
    def parentUpdated(self):
        print("parent updated for ",self.id);
        for i in range(len(self.genes)):
            gene = 3
            for pId in self.parents:
                gene = min(people[pId].genes[i], gene)
            self.genes[i] = gene
        
    def updateChildren(self):
        s = getSpouses(self.id)
        for sId in range(len(s)):
            children = getChildren(self.id, s[sId])
            for c in children:
                people[c].parentUpdated()
                people[c].updateChildren()
    
class Level():
    def __init__(self):
        self.people = []
        self.startId = ""
        self.help=""

class DorothyVampireLevel(Level):
    def __init__(self):
        self.people = [
            Person(id="frank",   displayName="Frank",   parents=[]),
            Person(id="lisa",    displayName="Lisa",    parents=[]),
            Person(id="dorothy", displayName="Dorothy", parents=["lisa", "frank"]),
        ]
        self.startId="dorothy"
        self.help="dorothy_help"
        self.win="dorothy_win"

    def checkWinCon(self, charactersOnScreen):
#         print (people["dorothy"].genes)
#         print (charactersOnScreen)
        return people["dorothy"].genes == [3,3,2] \
               and "dorothy" in charactersOnScreen
    

class BibleLevel(Level):
    def __init__(self):
        self.people = [
            Person(id="god",   displayName="God",   parents=["god"]),
            Person(id="adam",  displayName="Adam",  parents=["god"]),
            Person(id="eve",   displayName="Eve",   parents=["god"]),
            Person(id="kain",  displayName="Kain",  parents=["adam", "eve"]),
            Person(id="abel",  displayName="Abel",  parents=["adam", "eve"]),
            Person(id="seth",  displayName="Seth",  parents=["adam", "eve"]),
            Person(id="awan",  displayName="Awan",  parents=["adam", "eve"]),
            Person(id="enoch", displayName="Enoch", parents=["kain", "awan"]),
        ]
        self.startId="adam"
        self.help="bible_help"

    def checkWinCon(self, charactersOnScreen):
        return False

people = {}

def loadLevel(level):
    global people
    for p in level.people:
        people[p.id] = p

def getSpouses(name):
    spouses = set()
    for pId in people:
        p = people[pId]
        if name in p.parents:
            spouses.update(p.parents)
#     print(name," -> ", spouses)
    spouses.discard(name)
    spouses.discard(None)
    return list(spouses)

def getSpouse(name, spouseIdx = 0):
    spouses = getSpouses(name)
#     print(name," -2> ", spouses)
    return spouses[spouseIdx] if spouseIdx < len(spouses) else None

def getChildren(left, right):
    c = []
    for pId in people:
        p = people[pId]
        if left in p.parents and (right in p.parents or right == None)\
           and pId != left:
            c.append(pId)
    return c

def loadFamily(name, spouseIdx = 0):
    r = lambda:None
    r.left = name
    r.right = getSpouse(name, spouseIdx)
    lp = people[r.left].parents if (r.left in people) else []
    rp = people[r.right].parents if (r.right in people) else []
    r.grand = [
        lp[0] if len(lp) >= 1 else None,
        lp[1] if len(lp) >= 2 else None,
        rp[0] if len(rp) >= 1 else None,
        rp[1] if len(rp) >= 2 else None]
    r.children = getChildren(r.left, r.right)
    return r
