import sys
class Person:
    def __init__(self, name, mother_name=None, spouce=None):
        self.name = name
        self.mother = mother_name
        self.spouce = spouce
    

class Female(Person):
        
    def __init__(self, name, mom, spouce):
        self.children = []
        self.sex = "Female"
        super().__init__(name, mom, spouce)

    def get_married(self, own_name, spouce_name):
        if self.spouce == None and self.name == own_name:
            self.spouce =  spouce_name
        else:
            for i in range(len(self.children)):
                self.children[i].get_married(own_name, spouce_name)

    def add_child(self, mother_name, child_name, sex):
        result=-1
        if mother_name == self.name and self.spouce!=None:
            if sex == "Male":
                child = Male(child_name, self.name, None)
            else:
                child = Female(child_name, self.name, None)
            self.children.append(child)
            result=1
        else:
            for i in range(len(self.children)):
                result=self.children[i].add_child(mother_name, child_name, sex)
                if result == 1 or result==0:
                    break
        return result

    def get_children(self, sex = None, excluded_child = None):
        kids=[]
        for child in self.children:
            if ((child.sex == sex or sex==None) and    # if Child's sex is specified or default
                 child.name != excluded_child):
                kids.append(child.name)
        if len(self.children)==0:
            kids.append("NONE")
        if len(self.children)==1 and self.children[0].name==excluded_child:
            kids.append("NONE")
        if len(kids)==0:
            kids=None
        return kids
    
    def get_father(self,name):
        father=None
        for child in self.children:
            if child.name==name:
                father=self.spouce
                break
            else:
                father=child.get_father(name)
                if father!=None:
                    break
        return father

    def get_mother(self,name):
        mother=None
        for child in self.children:
            if child.name==name:
                mother=self.name
                break
            else:
                mother=child.get_mother(name)
                if mother!=None:
                    break
        return mother
    
    def get_siblings(self,name,sex= None):
        siblings=None
        for child in self.children:
            if child.name==name:
                siblings=self.get_children(sex,name)
                break
            else:
                siblings=child.get_siblings(name,sex)
                if siblings!=None:
                    break
                
        return siblings
    
    def get_spouce(self,name):
        spouce=None
        if self.spouce != None:
            if self.name==name:
                spouce = self.spouce
            elif self.spouce==name:
                spouce = self.name
            else:
                for child in self.children:
                    spouce = child.get_spouce(name)
                    if spouce!=None:
                        break
        return spouce
    
class Male(Person):
    
    def __init__(self, name, mom, spouce):
        self.sex = "Male"
        super().__init__(name, mom, spouce)    

    def get_married(self, own_name,spouce_name):
        if self.spouce == None and self.name == own_name:
            self.spouce = Female(spouce_name, None, self.name)
        else:
            if self.spouce!=None:
                self.spouce.get_married(own_name,spouce_name)  #Men are stupid in this world. Telling their wives to get married

    def add_child(self, mother_name, child_name, sex):
        if self.name == mother_name:
            return 0
        if self.spouce!=None:
            return self.spouce.add_child(mother_name, child_name, sex)
            
        
    def get_children(self, sex = None, excluded_child = None):
        if self.spouce!=None:
            return self.spouce.get_children(sex)

    def get_father(self,name):
        if self.spouce!=None:
            return self.spouce.get_father(name)

    def get_mother(self,name):
        if self.spouce!=None:
            return self.spouce.get_mother(name)   
    
    def get_siblings(self,name,sex= None):
        if self.spouce!=None:
            return self.spouce.get_siblings(name,sex) 

    def get_spouce(self,name):
        if self.spouce!=None:
            if self.name==name:
                return self.spouce.name
            else:
                return self.spouce.get_spouce(name)
    
            

# All Class definition above this comment

def create_initial_tree():
    queen = Female("Anga", None, None)
    
    queen.get_married("Anga","Shan")

    f = open('tree.txt','r')
    lines = f.readlines()
    for line in lines:
        segments=line.split()
        if segments[0] == "ADD_CHILD":
            result=queen.add_child(segments[1], segments[2], segments[3])
        else:
            queen.get_married(segments[1],segments[2])
    return queen

def printout(items):
    if isinstance(items,(list)):
        print(*items)
    else:
        print(items)

def get_relationship(queen, name, relationship):
    answer=[]
    if relationship=="Son" or relationship=="Daughter":
        if relationship=="Son":
            gender="Male"
        else:
            gender="Female"
        if queen.name==name:
            answer=queen.get_children(gender)
        else:
            if isinstance(queen, Male):
                if queen.spouce!=None:
                    queen=queen.spouce
                    for child in queen.children:
                        answer=get_relationship(child, name, relationship)
                        if answer!=None:
                            break
    
    elif relationship=="Siblings":
        answer=queen.get_siblings(name)
    
    elif (relationship == "Paternal-Uncle" or 
          relationship == "Paternal-Aunt"):
        father = queen.get_father(name)
        if relationship == "Paternal-Uncle":
            answer = queen.get_siblings(father,"Male")
        else:
            answer = answer+queen.get_siblings(father,"Female")
            

    elif (relationship == "Maternal-Uncle" or 
          relationship == "Maternal-Aunt"):
        mother = queen.get_mother(name)
        if relationship == "Maternal-Uncle":
            answer = queen.get_siblings(mother,"Male")
        else:
            answer = queen.get_siblings(mother,"Female")
    
    elif (relationship == "Sister-In-Law" or
          relationship == "Brother-In-Law"):
          spouce = queen.get_spouce(name)
          brothers = queen.get_siblings(name,"Male")
          sisters = queen.get_siblings(name,"Female")

          if relationship == "Sister-In-Law":
              sisters_of_spouce = queen.get_siblings(spouce,"Female")
              if brothers!=None:
                for brother in brothers:
                    wives_of_brothers =  queen.get_spouce(brother)
                    if wives_of_brothers!=None:
                        answer.append(wives_of_brothers)
              if sisters_of_spouce!=None:
                  answer = sisters_of_spouce + answer

          else:
              brothers_of_spouce = queen.get_siblings(spouce,"Male")
              if sisters!=None:
                for sister in sisters:
                    husbands_of_sisters =  queen.get_spouce(sister)
                    if husbands_of_sisters!=None:
                        answer.append(husbands_of_sisters)
              if brothers_of_spouce!=None:
                  answer = brothers_of_spouce + answer
    if len(answer)==0:
        answer=["PERSON_NOT_FOUND"]
    return answer


def main():
    input_file = sys.argv[1]
    f=open(input_file,'r')
    lines=f.readlines() #List of all lines in the input file
    queen = create_initial_tree()
    
    for line in lines:
        segments=line.split()
        if segments[0] == "ADD_CHILD":
            result = queen.add_child(segments[1], segments[2], segments[3])
            if result==1:
                print("CHILD_ADDITION_SUCCEEDED")
            elif result==0:
                print("CHILD_ADDITION_FAILED")
            else:
                print("PERSON_NOT_FOUND ")
        else:
            display=get_relationship(queen,segments[1],segments[2])
            printout(display)
    
if __name__ == "__main__":
    main()
