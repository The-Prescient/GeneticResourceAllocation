#Importing necessary Libraries 

import pandas as pd
import random as rnd
import prettytable as prettytable
import collections as collect
import time
import numpy as np
import matplotlib.pyplot as plt

#Reading the data entities stored in working directory

Staff_Df = pd.read_excel('Staff.xlsx')
Unit_Activities_Df = pd.read_excel('Unit Activities.xlsx')
Unit_Offerrings_Df = pd.read_excel('Unit Offerrings.xlsx')


# Constructing base classes 

##############################################################################

class Staff:
    def __init__(self,domain,subDomain,id,name,campus,contractResearch,contractService,maxContractTeaching):
        self._domain = domain
        self._subDomain = subDomain
        self._id = id
        self._name = name
        self._campus = campus
        self._contractResearch = contractResearch
        self._contractService = contractService
        self._maxContractTeaching = maxContractTeaching
        self._ReducedTeachingHours = 0
        self._UsedHours = 0
    
    def get_staffName(self): return self._name
    def get_staffdomain(self): return self._domain
    def get_staffsubdomain(self): return self._subDomain
    def get_staffId(self): return self._id
    
    def get_staffCampus(self): return self._campus
    def get_Research(self): return self._contractResearch
    def get_Service(self): return self._contractService
    def get_Teaching(self): return self._maxContractTeaching
    def get_RemainningHours (self) : return self._ReducedTeachingHours
    def get_Used_Hours (self): return self._UsedHours
    
    
    def set_ReducedTeachingHrs (self,Hours) : self.ReducedTeachingHours = Hours
    def set_UsedHours(self,Hours): self._UsedHours = self._UsedHours + Hours
    
    def __str__(self): return self._id; self._name, self._maxContractTeaching

##############################################################################

class Activity:
    
    def __init__(self,activity, minHours, maxHours, priority):
        self._activity = activity
        self._minHours = minHours
        self._maxHours = maxHours
        self._priority = priority
        
    def get_activity(self): return self._activity
    def get_minHours(self): return self._minHours
    def get_maxHours(self): return self._maxHours
    def get_priority(self): return self._priority
    
##############################################################################

class Offerring:
    def __init__(self,domainO,subDomainO,unitCode,trimesterOfferring):
        self._domainO = domainO
        self._subDomainO =subDomainO
        self._unitCode = unitCode
        self._trimesterOfferring = trimesterOfferring
        
    def get_domainO(self): return self._domainO
    def get_subDomainO(self): return self._subDomainO
    def get_unitCode(self): return self._unitCode
    def get_trimester(self): return self._trimesterOfferring
    
    def __str__(self):return self._id, self._unitCode, self._trimesterOfferring

##############################################################################

class Unit:
    def __init__(self,offerring,activities):
        self._offerring = offerring
        self._activities = activities
        
    def get_offerring(self): return self._offerring
    def get_activities(self): return self._activities

##############################################################################

# Constructing Data class to initialize required data structures

class Data:
    RESOURCES = Staff_Df.iloc[:,:].values
    UNITOFFERRINGS = Unit_Offerrings_Df.iloc[:,:].values
    UNITACTIVITIES = Unit_Activities_Df.iloc[:,:].values
    
    def __init__(self):
        self._activities = []; self._offerrings = []; self._resources = []
        for i in range(0,len(self.RESOURCES)):
            self._resources.append(Staff(self.RESOURCES[i][0],self.RESOURCES[i][1],self.RESOURCES[i][2],self.RESOURCES[i][3],self.RESOURCES[i][4],self.RESOURCES[i][5],self.RESOURCES[i][6],self.RESOURCES[i][7]))
        for i in range(0,len(self.UNITOFFERRINGS)):
            self._offerrings.append(Offerring(self.UNITOFFERRINGS[i][0],self.UNITOFFERRINGS[i][1],self.UNITOFFERRINGS[i][2],self.UNITOFFERRINGS[i][3]))
        for i in range(0,len(self.UNITACTIVITIES)):
            self._activities.append(Activity(self.UNITACTIVITIES[i][0],self.UNITACTIVITIES[i][1],self.UNITACTIVITIES[i][2],self.UNITACTIVITIES[i][3]))
        
        # Unit + Activities
        self._units =[]
        for i in range(0,len(self._offerrings)):
            self._units.append(Unit(self._offerrings[i],[self._activities[0],self._activities[1],self._activities[2],self._activities[3],self._activities[4],self._activities[5],self._activities[6],self._activities[7],self._activities[8]]))
            
        # Resource Capability mapping
        self._capabilities = []
        self._HrUnits = []
        self._MgtUnits = []
        self._ArtUnits = []
        self._HrFaculty = []
        self._MgtFaculty = []
        self._ArtFaculty = []
        
        #Capability mapping through sub-Domain [The model can be scaled to multidomain problem]
        for i in range(0,len(self._units)):
            if (self._units[i].get_offerring().get_subDomainO() =="HR"):
                self._HrUnits.append(self._units[i])
            else:
                if (self._units[i].get_offerring().get_subDomainO()=="ART"):
                    self._ArtUnits.append(self._units[i])
                else: 
                    self._MgtUnits.append(self._units[i])
        
        for i in range(0,len(self._resources)):
            if (self._resources[i].get_staffsubdomain() =="HR"):
                self._HrFaculty.append(self._resources[i])
            else:
                if (self._resources[i].get_staffsubdomain() =="ART"):
                    self._ArtFaculty.append(self._resources[i])
                else: 
                    self._MgtFaculty.append(self._resources[i])
        
        Subdomain1 = Capability("HR",self._HrFaculty,self._HrUnits)
        Subdomain2 = Capability("ART",self._ArtFaculty,self._ArtUnits)
        Subdomain3 = Capability("MGT",self._MgtFaculty,self._MgtUnits)
        
        self._subdomains = [Subdomain1,Subdomain2,Subdomain3]
        
            
    def get_activities(self): return self._activities
    def get_offerrings(self): return self._offerrings
    def get_resources(self): return self._resources
    def get_units(self): return self._units
    def get_capabilitymap(self): return self._subdomains
    def get_HR_Units(self): return self._HrUnits
    def get_ART_Units(self): return self._ArtUnits
    def get_MGT_Units(self): return self._MgtUnits
    
##############################################################################
# Allocation Process happens here

class Process:
    def __init__(self):
        self._data = data
        self._Allocations = []
        self._NumberOfConflicts = 0
        self._fitness =-1
        self._AllocationNumber = 0
        self._isFitnessChanged =True
        
    def get_Allocations(self):
        self._isFitnessChanged =True
        return self._Allocations
    
    def get_numberOfCoflicts(self):
        return self._NumberOfConflicts
    
    def get_HowFit(self):
        if(self._isFitnessChanged== True):
            self._fitness = self.Measure_Fitness()
            self._isFitnessChanged =False
        return self._fitness
    
    def initialize(self):
        cap = self._data.get_capabilitymap()
        
        for i in range (0,len(cap)):
            units = cap[i].get_UnitsC()
            for j in range(0,len(units)):
                acts = units[j].get_activities()
                newAllocation = Allocation(self._AllocationNumber,units[j])
                self._AllocationNumber +=1
                newAllocation.set_Staff(cap[i].get_ResourcesC()[rnd.randrange(0,len(cap[i].get_ResourcesC()))])
                
                for k in range(0, len(acts)):
                    newAllocation.set_Activity(acts[k].get_activity())
                    if(acts[k].get_minHours() == acts[k].get_maxHours()):
                        if(newAllocation.get_Staff().get_RemainningHours()!=0):Available_Teaching_Hours = newAllocation.get_Staff().get_RemainningHours()
                        else: Available_Teaching_Hours = newAllocation.get_Staff().get_Teaching()
                        Hours_for_Task = acts[k].get_maxHours()
                        newAllocation.get_Staff().set_UsedHours(Hours_for_Task)
                        Remaining_Hours = Available_Teaching_Hours-Hours_for_Task
                        newAllocation.set_Hours(Hours_for_Task)
                        newAllocation.get_Staff().set_ReducedTeachingHrs(Remaining_Hours)
                        
                    else:
                        if(newAllocation.get_Staff().get_RemainningHours()!=0):Available_Teaching_Hours = newAllocation.get_Staff().get_RemainningHours()
                        else: Available_Teaching_Hours = newAllocation.get_Staff().get_Teaching()
                        Hours_for_Task= rnd.randrange(acts[k].get_minHours(),acts[k].get_maxHours())
                        newAllocation.get_Staff().set_UsedHours(Hours_for_Task)
                        Remaining_Hours = Available_Teaching_Hours-Hours_for_Task
                        newAllocation.set_Hours(Hours_for_Task)
                        newAllocation.get_Staff().set_ReducedTeachingHrs(Remaining_Hours)
                    
                        
                self._Allocations.append(newAllocation)
        return self
    
    def Measure_Fitness(self):
        self._StaffT1 = []
        self._StaffT2 = []
        self._StaffT3 = []
        
        self._NumberOfConflicts = 0
        
        allocations = self.get_Allocations()
         # Conflict Type 1: In A trimester if a staff is allocated to more than 2 units 
         
         
        for i in range(0,len(allocations)):
            if(allocations[i].get_Unit().get_offerring().get_trimester() == "T1"):
                self._StaffT1.append(allocations[i].get_Staff().get_staffName())
            else:
                if(allocations[i].get_Unit().get_offerring().get_trimester() == "T2"):
                    self._StaffT2.append(allocations[i].get_Staff().get_staffName())
                else:
                    self._StaffT3.append(allocations[i].get_Staff().get_staffName())
        
        a = collect.Counter(self._StaffT1)
        b = collect.Counter(self._StaffT2)
        c = collect.Counter(self._StaffT3)        
        
        A_conflicts = [element for element in a if a[element] >2 ]
        self._NumberOfConflicts = self._NumberOfConflicts + len(A_conflicts )
        B_conflicts = [element for element in b if b[element]>2 ]
        self._NumberOfConflicts = self._NumberOfConflicts + len(B_conflicts)
        C_conflicts = [element for element in c if c[element]>2 ]
        self._NumberOfConflicts = self._NumberOfConflicts + len(C_conflicts)
   
        
        # Conflict Type 2: Capability Mismatch with respect to the domain
        for i in range(0,len(allocations)):
            if(allocations[i].get_Unit().get_offerring().get_subDomainO() != allocations[i].get_Staff().get_staffsubdomain()):
                self._NumberOfConflicts += 1
                
        # Conflict Type 3: Total Allocated hours exceed contract teaching hours
        self._Staff = []
        
        for i in range(0,len(allocations)):
            s = allocations[i].get_Staff().get_staffId()
            h = sum(allocations[i].get_Hours())
            for j in range (0,len(self._Staff)):
                if(s == self._Staff[j]):
                    self._Staff[j][1] = self._Staff[j][1]+ h
                else:
                    self._Staff.append(s,h)
                
        r = data.get_resources()
        for i in range(0,len(self._Staff)):
            id = self._Staff[i][0]
            hour = self._Staff[i][1]
            for j in range(0,len(r)):
               if(r[i].get_staffId()== id and hour > r[i].get_Teaching()):
                   self._NumberOfConflicts += 1
                   
        return 1/((1.0*self._NumberOfConflicts+1))
        return a
    
    def __str__(self):
        returnValue =""
        for i in range (0,len(self._allocations)-1):
            returnValue += str(self.allocations[i]) + "," 
        returnValue += str(self.allocations[len(self.allocations)-1])
        return returnValue
      
##############################################################################

class Population:
    def __init__(self,size):
        self._size = size
        self._data = data
        self._allocationpaths = []
        for i in range(0,size): self._allocationpaths.append(Process().initialize())
    
    def get_AllocationPaths(self):
        return self._allocationpaths
    
##############################################################################

# Genetic Algorithm that evolves the allocations.

class GeneticEvolution:
    def evolve(self,population): return self._mutate_population(self._crossover_population(population))
    
    def _crossover_population (self,pop):
        crossover_pop = Population(0)
        for i in range(ELITE_ALLOCATIONS):
            crossover_pop.get_AllocationPaths().append(pop.get_AllocationPaths()[i])
        i= ELITE_ALLOCATIONS
        while i< ALLOCATIONS_POPULATION_SIZE:
            Allocation1 = self._select_tournament_population(pop).get_AllocationPaths()[0]
            Allocation2 = self._select_tournament_population(pop).get_AllocationPaths()[0]
            crossover_pop.get_AllocationPaths().append(self._crossover_Allocation(Allocation1, Allocation2))
            i +=1
        return crossover_pop
    
    def _mutate_population(self,population):
        for i in range(ELITE_ALLOCATIONS,ALLOCATIONS_POPULATION_SIZE):
            self._mutate_Allocation(population.get_AllocationPaths()[i])   
        return population
        
    def _crossover_Allocation(self, Allocation1, Allocation2):
        crossoverAllocation = Process().initialize()
        for i in range(0,len(crossoverAllocation.get_Allocations())):
            if(rnd.random()>0.5): crossoverAllocation.get_Allocations()[i] = Allocation1.get_Allocations()[i]
            else : crossoverAllocation.get_Allocations()[i] = Allocation2.get_Allocations()[i]
        return crossoverAllocation
    
    def _mutate_Allocation (self,mutateAllocation):
        Allocation = Process().initialize()
        for i in range(0, len(mutateAllocation.get_Allocations())):
            if(MUTATION_RATE> rnd.random()): mutateAllocation.get_Allocations()[i] = Allocation.get_Allocations()[i]
        return mutateAllocation
    
    def _select_tournament_population(self,pop):
        tournament_pop = Population(0)
        i = 0
        while i < TOURNAMENT_SELECTION_SIZE:
            tournament_pop.get_AllocationPaths().append(pop.get_AllocationPaths()[rnd.randrange(0, ALLOCATIONS_POPULATION_SIZE)])
            i +=1
        tournament_pop.get_AllocationPaths().sort(key= lambda x : x.get_HowFit(), reverse=True)
        return tournament_pop
    
##############################################################################

class Visualize:
    
    def DisplayAllocationTable(self,Allocation):
        print('The Allocation Table: \n')
        Path = Allocation.get_Allocations()
        AllocationPathTable = prettytable.PrettyTable(['ID','Unit Code','Dept','Teaching Term','Staff ID','Staff Name','Unit Chair', 'Unit Review','Class', 'Seminar','Cloud Seinar', 'Unit Dev', 'Online Resource MGT','Consultation','Marking','Total Hours Allocated'])
        for i in range(0,len(Path)):        
            AllocationPathTable.add_row([str(Path[i].get_id()), Path[i].get_Unit().get_offerring().get_unitCode(),Path[i].get_Unit().get_offerring().get_subDomainO(),Path[i].get_Unit().get_offerring().get_trimester(),Path[i].get_Staff().get_staffId(),Path[i].get_Staff().get_staffName(),
                                         Path[i].get_Hours()[0],Path[i].get_Hours()[1],Path[i].get_Hours()[2],Path[i].get_Hours()[3],Path[i].get_Hours()[4],Path[i].get_Hours()[5],Path[i].get_Hours()[6],Path[i].get_Hours()[7],Path[i].get_Hours()[8],sum(Path[i].get_Hours())])
        print(AllocationPathTable)
        
    def DisplayTheGeneration(self,population):
        Generation = prettytable.PrettyTable(['Allocation#','fitness of Allocation ','# of conflicts'])
        Paths = population.get_AllocationPaths()
        for i in range(0,len(Paths)):
            Generation.add_row([str(i),round(Paths[i].get_HowFit(),3),str(Paths[i].get_numberOfCoflicts())])
        print(Generation)
        
    def DisplayGap(self,Allocation):
        StaffHours = prettytable.PrettyTable(['StaffID','Staff Name','Hours Remaining After Allocation'])
        Path = Allocation.get_Allocations()
        for i in range(0,len(Path)):
            StaffHours.add_row([Path[i].get_Staff().get_staffId(), Path[i].get_Staff().get_staffName(),Path[i].get_Staff().get_Used_Hours()])
        print(StaffHours)
        
    def DisplayUnitCount(self,Allocation):
        Path = Allocation.get_Allocations()
        stafflist = []
        for i in range(0,len(Path)):
            stafflist.append(Path[i].get_Staff().get_staffName())
            
        n = collect.Counter(stafflist)
        print(n)
       
##############################################################################

class Allocation:
    def __init__(self, id, Unit):
        self._id = id
        self._Unit = Unit # has Unit Class instances with the unit Id and the offerring and the activities
        self._Activities = []
        self._Staff = None
        self._Hours = []

        
    def get_id(self): return self._id
    def get_Unit(self): return self._Unit
    def get_Staff(self): return self._Staff
    def get_Activities(self): return self._Activities
    def get_Hours(self): return self._Hours
    
    
    def set_Staff(self,Staff): self._Staff = Staff
    def set_Activity(self,Activity): self._Activities.append(Activity)
    def set_Hours(self,Hours): self._Hours.append(Hours)
    
    def __str__(self):
        return str(self._id) +"," + str(self._Unit.get_offerring().get_unitCode())  +"," + str(self._Unit.get_offerring().get_UnitName()) +"," + str(self._Staff.get_StaffName())
        
##############################################################################

class Capability:
    def __init__(self,SubDomainName, Resources, Units):
        self._SubDomainName = SubDomainName
        self._Resources = Resources
        self._Units = Units
        
    def get_SubdomainNameC(self): return self._SubDomainName
    def get_ResourcesC(self): return self._Resources
    def get_UnitsC(self): return self._Units
    
##############################################################################

# Evaluation class to assess the performance of the algorithm

class PlotEvaluate:
    
    def TimeOfConvergence(self,n):
        a= [] 
        self._n = n
        for i in range(self._n):
            start = time.time()
            generationNumber = 0
            print("\n> Generation # " + str(generationNumber))
            population = Population(ALLOCATIONS_POPULATION_SIZE)
            population.get_AllocationPaths().sort(key=lambda x : x.get_HowFit(), reverse=True)
            geneticAllocation = GeneticEvolution()
            try:
                while(population.get_AllocationPaths()[0].get_HowFit()!= 1.0):
                    generationNumber +=1
                    print ("\n > Generation # " + str(generationNumber))
                    population = geneticAllocation.evolve(population)
                    population.get_AllocationPaths().sort(key= lambda x : x.get_HowFit(), reverse=True)
            except KeyboardInterrupt:
                print("Press Ctrl-C to terminate while statement")
                pass
            end = time.time()
            a.append(end-start) 
             
        x = np.arange(1,(self._n+1),1)
        y = a
        y_mean = [np.mean(a)]*len(a)
        plt.plot(x,y)   
        plt.plot(x,y_mean,linestyle = '--',label ="Avg Ref.")
        plt.xlabel("Algorithm Iterations")
        plt.ylabel("Time(seconds)")
        plt.title("Time to Convergence")
        plt.legend(loc='upper right')
        plt.show()
        
    def LOpt(self,n,k):
        self._a= [] 
        self._n = n
        self._k = k
        
        for i in range(self._n):
            
            generationNumber = 0
            print("\n> Generation # " + str(generationNumber))
            population = Population(ALLOCATIONS_POPULATION_SIZE)
            population.get_AllocationPaths().sort(key=lambda x : x.get_HowFit(), reverse=True)
            geneticAllocation = GeneticEvolution()
            try:
                while(population.get_AllocationPaths()[0].get_HowFit()!= 1.0 and generationNumber<k):
                    generationNumber +=1
                    print ("\n > Generation # " + str(generationNumber))
                    population = geneticAllocation.evolve(population)
                    population.get_AllocationPaths().sort(key= lambda x : x.get_HowFit(), reverse=True)
            except KeyboardInterrupt:
                print("Press Ctrl-C to terminate while statement")
                pass
            if (generationNumber < k):
                self._a.append(generationNumber)
                
        Loptv = (len(self._a)/(self._n))* 100
        
        return Loptv
            
    def AvgFit(self,n,k):
        self._a= [] 
        self._n = n
        self._k = k
        
        for i in range(self._n):
            fit = 0
            generationNumber = 0
            print("\n> Generation # " + str(generationNumber))
            population = Population(ALLOCATIONS_POPULATION_SIZE)
            population.get_AllocationPaths().sort(key=lambda x : x.get_HowFit(), reverse=True)
            geneticAllocation = GeneticEvolution()
            try:
                while(generationNumber<k):
                    generationNumber +=1
                    print ("\n > Generation # " + str(generationNumber))
                    population = geneticAllocation.evolve(population)
                    population.get_AllocationPaths().sort(key= lambda x : x.get_HowFit(), reverse=True)
            except KeyboardInterrupt:
                print("Press Ctrl-C to terminate while statement")
                pass
            
            for j in range(0,len(population.get_AllocationPaths())):
                m = population.get_AllocationPaths()[j].get_HowFit()
                fit += m
                
            self._a.append(fit)
            
        x = np.arange(1,(self._n+1),1)
        y = self._a
        plt.plot(x,y)   
        plt.xlabel("Algoruthm Iteration")
        plt.ylabel("Average Fitness")
        plt.title("Average Fitness at Kth Gen")
        plt.show()
            
        
        
##############################################################################       

#Implementation and Evaluation of The Algorithm 

# Setting the Parameters

ALLOCATIONS_POPULATION_SIZE = 10
ELITE_ALLOCATIONS = 1
TOURNAMENT_SELECTION_SIZE = 3
MUTATION_RATE = 0.1

# Initializing the data class.

data = Data()

# Standard iplementation of the algorithm.


show = Visualize()
generationNumber = 0
print("\n> Generation # " + str(generationNumber))
population = Population(ALLOCATIONS_POPULATION_SIZE)
population.get_AllocationPaths().sort(key=lambda x : x.get_HowFit(), reverse=True)
gen0 =  population
gen01 = population.get_AllocationPaths()[0]
geneticAllocation = GeneticEvolution()

try:
    while(population.get_AllocationPaths()[0].get_HowFit()!= 1.0):
        generationNumber +=1
        print ("\n > Generation # " + str(generationNumber))
        population = geneticAllocation.evolve(population)
        population.get_AllocationPaths().sort(key= lambda x : x.get_HowFit(), reverse=True)
        show.DisplayTheGeneration(population)
        show.DisplayAllocationTable(population.get_AllocationPaths()[0])
        show.DisplayUnitCount(population.get_AllocationPaths()[0])
    print("\n\n")
except KeyboardInterrupt:
    print("Press Ctrl-C to terminate while statement")
    pass

show.DisplayTheGeneration(gen0)
show.DisplayAllocationTable(gen01)


# Evaluation of the algorithm 

Evaluation = PlotEvaluate()

#1 Speed of the algorithm to reach convergence

# n - number of evolution runs

n= 30
Evaluation.TimeOfConvergence(n)

# ##############################################################################  

#2 Likelihood of Optimality (LOpt)

# # n - number of evolution runs
# # k - cap on the number of generations for every n runs

n = 10
k = 500 
lopt= []
while k < 1500 :
    result = Evaluation.LOpt(n,k) 
    lopt.append(result)
    k+=100
    
x = np.arange(500,k,100)
y = lopt
plt.plot(x,y)   
plt.xlabel("Number of Generation Cap")
plt.ylabel("LOpt (%)")
plt.title("The Likelihood of Optimal Performance")
plt.show()   

##############################################################################  

#3 Average Conflicts in generation.

# n - number of evolution runs
# k - cap on the number of generations for every n runs

n= 50
k= 500
Evaluation.AvgFit(n, k)