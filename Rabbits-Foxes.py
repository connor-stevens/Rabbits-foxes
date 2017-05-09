#Skeleton Program code for the AQA A Level Paper 1 2017 examination
#this code should be used in conjunction with the Preliminary Material
#written by the AQA Programmer Team
#developed in the Python 3.4.1 programming environment

import enum
import random
import math

class Location:
  def __init__(self):
    self.Fox = None
    self.Warren = None

class Simulation:
  def __init__(self, LandscapeSize, InitialWarrenCount, InitialFoxCount, Variability, FixedInitialLocations):
    self.ViewRabbits = ""
    self.TimePeriod = 0
    self.WarrenCount = 0
    self.FoxCount = 0
    self.ShowDetail = False
    self.LandscapeSize = LandscapeSize
    self.Variability = Variability
    self.FixedInitialLocations = FixedInitialLocations
    self.Landscape = []
    for Count1 in range (self.LandscapeSize):
      LandscapeRow = []
      for Count2 in range (self.LandscapeSize):
        LandscapeLocation = None
        LandscapeRow.append(LandscapeLocation)
      self.Landscape.append(LandscapeRow)
    self.CreateLandscapeAndAnimals(InitialWarrenCount, InitialFoxCount, self.FixedInitialLocations)
    self.DrawLandscape()
    MenuOption = 0
    while (self.WarrenCount > 0 or self.FoxCount > 0) and MenuOption != 5:
      print()
      print("1. Advance to next time period showing detail")
      print("2. Advance to next time period hiding detail")
      print("3. Inspect fox")
      print("4. Inspect warren")
      print("5. Exit")
      print()
      MenuOption = int(input("Select option: "))
      if MenuOption == 1:
        self.TimePeriod += 1
        self.ShowDetail = True
        self.AdvanceTimePeriod()
      if MenuOption == 2:
        self.TimePeriod += 1
        self.ShowDetail = False
        self.AdvanceTimePeriod()
      if MenuOption == 3:
        x = self.InputCoordinate("x")
        y = self.InputCoordinate("y")
        if not self.Landscape[x][y].Fox is None:
          self.Landscape[x][y].Fox.Inspect()
      if MenuOption == 4:
        x = self.InputCoordinate("x")
        y = self.InputCoordinate("y")
        if not self.Landscape[x][y].Warren is None:
          self.Landscape[x][y].Warren.Inspect()
          self.ViewRabbits = input("View individual rabbits (y/n)? ")
          if self.ViewRabbits == "y":
            self.Landscape[x][y].Warren.ListRabbits()
    input()
    
  def InputCoordinate(self, CoordinateName):
    Coordinate = int(input("  Input " + CoordinateName + " coordinate:"))
    return Coordinate
  
  def AdvanceTimePeriod(self):
    NewFoxCount = 0
    if self.ShowDetail:
      print()
    for x in range (0, self.LandscapeSize):
      for y in range (0, self.LandscapeSize):
        if not self.Landscape[x][y].Warren is None:
          if self.ShowDetail:
            print("Warren at (", x, ",", y, "):", sep = "")
            print("  Period Start: ", end = "")
            self.Landscape[x][y].Warren.Inspect()
          if self.FoxCount > 0:
            self.FoxesEatRabbitsInWarren(x, y)
          if self.Landscape[x][y].Warren.NeedToCreateNewWarren():
            self.CreateNewWarren()
          self.Landscape[x][y].Warren.AdvanceGeneration(self.ShowDetail)
          if self.ShowDetail:
            print("  Period End: ", end = "")
            self.Landscape[x][y].Warren.Inspect()
            input()
          if self.Landscape[x][y].Warren.WarrenHasDiedOut():
            self.Landscape[x][y].Warren = None
            self.WarrenCount -= 1
    for x in range (0, self.LandscapeSize):
      for y in range (0, self.LandscapeSize):
        if not self.Landscape[x][y].Fox is None:
          if self.ShowDetail:
            print("Fox at (", x, ",", y, "): ", sep = "")
          self.Landscape[x][y].Fox.AdvanceGeneration(self.ShowDetail)
          if self.Landscape[x][y].Fox.CheckIfDead():
            self.Landscape[x][y].Fox = None
            self.FoxCount -= 1
          else:
            if self.Landscape[x][y].Fox.ReproduceThisPeriod():
              if self.ShowDetail:
                print("  Fox has reproduced. ")
              NewFoxCount += 1
            if self.ShowDetail:
              self.Landscape[x][y].Fox.Inspect()
            self.Landscape[x][y].Fox.ResetFoodConsumed()
    if NewFoxCount > 0:
      if self.ShowDetail:
        print("New foxes born: ")
      for f in range (0, NewFoxCount):
        self.CreateNewFox()
    if self.ShowDetail:
      input()
    self.DrawLandscape()
    print()

  def CreateLandscapeAndAnimals(self, InitialWarrenCount, InitialFoxCount, FixedInitialLocations):
    for x in range (0, self.LandscapeSize):
      for y in range (0, self.LandscapeSize):
        self.Landscape[x][y] = Location()
    if FixedInitialLocations:
      self.Landscape[1][1].Warren = Warren(self.Variability, 38)
      self.Landscape[2][8].Warren = Warren(self.Variability, 80) 
      self.Landscape[9][7].Warren = Warren(self.Variability, 20)
      self.Landscape[10][3].Warren = Warren(self.Variability, 52)
      self.Landscape[13][4].Warren = Warren(self.Variability, 67)
      self.WarrenCount = 5
      self.Landscape[2][10].Fox = Fox(self.Variability)
      self.Landscape[6][1].Fox = Fox(self.Variability)
      self.Landscape[8][6].Fox = Fox(self.Variability)
      self.Landscape[11][13].Fox = Fox(self.Variability)
      self.Landscape[12][4].Fox = Fox(self.Variability)
      self.FoxCount = 5
    else:
      for w in range (0, InitialWarrenCount):
        self.CreateNewWarren()
      for f in range (0, InitialFoxCount):
        self.CreateNewFox()

  def CreateNewWarren(self):
    x = random.randint(0, self.LandscapeSize - 1)
    y = random.randint(0, self.LandscapeSize - 1)
    while not self.Landscape[x][y].Warren is None:
      x = random.randint(0, self.LandscapeSize - 1)
      y = random.randint(0, self.LandscapeSize - 1)
    if self.ShowDetail:
      print("New Warren at (", x, ",", y, ")", sep = "")
    self.Landscape[x][y].Warren = Warren(self.Variability)
    self.WarrenCount += 1
  
  def CreateNewFox(self):
    x = random.randint(0, self.LandscapeSize - 1)
    y = random.randint(0, self.LandscapeSize - 1)
    while not self.Landscape[x][y].Fox is None:
      x = random.randint(0, self.LandscapeSize - 1)
      y = random.randint(0, self.LandscapeSize - 1)
    if self.ShowDetail:
      print("  New Fox at (", x, ",", y, ")", sep = "")
    self.Landscape[x][y].Fox = Fox(self.Variability)
    self.FoxCount += 1

  def FoxesEatRabbitsInWarren(self, WarrenX, WarrenY):
    RabbitCountAtStartOfPeriod  = self.Landscape[WarrenX][WarrenY].Warren.GetRabbitCount()
    for FoxX in range(0, self.LandscapeSize):
      for FoxY in range (0, self.LandscapeSize):
        if not self.Landscape[FoxX][FoxY].Fox is None:
          Dist = self.DistanceBetween(FoxX, FoxY, WarrenX, WarrenY)
          if Dist <= 3.5:
            PercentToEat = 20
          elif Dist <= 7:
            PercentToEat = 10
          else:
            PercentToEat = 0
          RabbitsToEat = int(round(float(PercentToEat * RabbitCountAtStartOfPeriod / 100)))
          FoodConsumed = self.Landscape[WarrenX][WarrenY].Warren.EatRabbits(RabbitsToEat)
          self.Landscape[FoxX][FoxY].Fox.GiveFood(FoodConsumed)
          if self.ShowDetail:
            print("  ", FoodConsumed, " rabbits eaten by fox at (", FoxX, ",", FoxY, ").", sep = "")

  def DistanceBetween(self, x1, y1, x2, y2):
    return math.sqrt((pow(x1 - x2, 2) + pow(y1 - y2, 2)))

  def DrawLandscape(self):
    print()
    print("TIME PERIOD:", self.TimePeriod)
    print()
    print("   ", end = "")
    for x in range (0, self.LandscapeSize):
      if x < 10:
        print(" ", end = "")
      print(x, "|", end = "")
    print()
    for x in range (0, self.LandscapeSize * 4 + 3):
      print("-", end = "")
    print()
    for y in range (0, self.LandscapeSize):
      if y < 10:
        print(" ", end = "")
      print("", y, "|", sep = "", end = "")
      for x in range (0, self.LandscapeSize):
        if not self.Landscape[x][y].Warren is None:
          if self.Landscape[x][y].Warren.GetRabbitCount() < 10:
            print(" ", end = "")
          print(self.Landscape[x][y].Warren.GetRabbitCount(), end = "")
        else:
          print("  ", end = "")
        if not self.Landscape[x][y].Fox is None:
          print("F", end = "")
        else:
          print(" ", end = "")
        print("|", end = "")
      print()

class Warren:
  def __init__(self, Variability, RabbitCount = 0):
    self.MAX_RABBITS_IN_WARREN = 99
    self.RabbitCount = RabbitCount
    self.PeriodsRun = 0
    self.AlreadySpread = False
    self.Variability = Variability
    self.Rabbits = []
    for Count in range(0, self.MAX_RABBITS_IN_WARREN):
      self.Rabbits.append(None)
    if self.RabbitCount == 0:
      self.RabbitCount = int(self.CalculateRandomValue(int(self.MAX_RABBITS_IN_WARREN / 4), self.Variability))
    for r in range (0, self.RabbitCount):
      self.Rabbits[r] = Rabbit(self.Variability)

  def CalculateRandomValue(self, BaseValue, Variability):
    return BaseValue - (BaseValue * Variability / 100) + (BaseValue * random.randint(0, Variability * 2) / 100)

  def GetRabbitCount(self): 
    return self.RabbitCount
  
  def NeedToCreateNewWarren(self): 
    if self.RabbitCount == self.MAX_RABBITS_IN_WARREN and not self.AlreadySpread:
      self.AlreadySpread = True
      return True
    else:
      return False
    
  def WarrenHasDiedOut(self):
    if self.RabbitCount == 0:
      return True
    else:
      return False

  def AdvanceGeneration(self, ShowDetail):
    self.PeriodsRun += 1
    if self.RabbitCount > 0:
      self.KillByOtherFactors(ShowDetail)
    if self.RabbitCount > 0:
      self.AgeRabbits(ShowDetail)
    if self.RabbitCount > 0 and self.RabbitCount <= self.MAX_RABBITS_IN_WARREN:
      if self.ContainsMales():
        self.MateRabbits(ShowDetail)
    if self.RabbitCount == 0 and ShowDetail:
      print("  All rabbits in warren are dead")
    
  def EatRabbits(self, RabbitsToEat):
    DeathCount = 0
    if RabbitsToEat > self.RabbitCount:
      RabbitsToEat = self.RabbitCount
    while DeathCount < RabbitsToEat:
      RabbitNumber = random.randint(0, self.RabbitCount - 1)
      if not self.Rabbits[RabbitNumber] is None:
        self.Rabbits[RabbitNumber] = None
        DeathCount += 1
    self.CompressRabbitList(DeathCount)
    return RabbitsToEat

  def KillByOtherFactors(self, ShowDetail):
    DeathCount = 0
    for r in range (0, self.RabbitCount):
      if self.Rabbits[r].CheckIfKilledByOtherFactor():
        self.Rabbits[r] = None
        DeathCount += 1
    self.CompressRabbitList(DeathCount)
    if ShowDetail:
      print(" ", DeathCount, "rabbits killed by other factors.")

  def AgeRabbits(self, ShowDetail):
    DeathCount = 0
    for r in range (0, self.RabbitCount):
      self.Rabbits[r].CalculateNewAge()
      if self.Rabbits[r].CheckIfDead():
        self.Rabbits[r] = None
        DeathCount += 1
    self.CompressRabbitList(DeathCount)
    if ShowDetail:
      print(" ", DeathCount, "rabbits die of old age.")

  def MateRabbits(self, ShowDetail):
    Mate = 0
    Babies = 0 
    for r in range (0, self.RabbitCount):
      if self.Rabbits[r].IsFemale() and self.RabbitCount + Babies < self.MAX_RABBITS_IN_WARREN:
        Mate = random.randint(0, self.RabbitCount - 1)
        while Mate == r or self.Rabbits[Mate].IsFemale():
          Mate = random.randint(0, self.RabbitCount - 1)
        CombinedReproductionRate = (self.Rabbits[r].GetReproductionRate() + self.Rabbits[Mate].GetReproductionRate()) / 2
        if CombinedReproductionRate >= 1:
          self.Rabbits[self.RabbitCount + Babies] = Rabbit(self.Variability, CombinedReproductionRate)
          Babies += 1
    self.RabbitCount = self.RabbitCount + Babies
    if ShowDetail:
      print(" ", Babies, "baby rabbits born.")

  def CompressRabbitList(self, DeathCount):
    if DeathCount > 0:
      ShiftTo = 0
      ShiftFrom  = 0
      while ShiftTo < self.RabbitCount - DeathCount:
        while self.Rabbits[ShiftFrom] is None:
          ShiftFrom += 1
        if ShiftTo != ShiftFrom:
          self.Rabbits[ShiftTo] = self.Rabbits[ShiftFrom]
        ShiftTo += 1
        ShiftFrom += 1
      self.RabbitCount = self.RabbitCount - DeathCount

  def ContainsMales(self):
    Males = False
    for r in range (0, self.RabbitCount):
      if not self.Rabbits[r].IsFemale():
        Males = True
    return Males

  def Inspect(self):
    print("Periods Run", self.PeriodsRun, "Size", self.RabbitCount)

  def ListRabbits(self):
    if self.RabbitCount > 0:
      for r in range (0, self.RabbitCount):
        self.Rabbits[r].Inspect()

class Animal:
  _ID = 1

  def __init__(self, AvgLifespan, AvgProbabilityOfDeathOtherCauses, Variability):
    self._NaturalLifespan = int(AvgLifespan * self._CalculateRandomValue(100, Variability) / 100)
    self._ProbabilityOfDeathOtherCauses = AvgProbabilityOfDeathOtherCauses * self._CalculateRandomValue(100, Variability) / 100
    self._IsAlive = True
    self._ID = Animal._ID
    self._Age = 0
    Animal._ID += 1

  def CalculateNewAge(self):
    self._Age += 1
    if self._Age >= self._NaturalLifespan:
      self._IsAlive = False

  def CheckIfDead(self): 
    return not self._IsAlive

  def Inspect(self):
    print("  ID", self._ID, "", end = "")
    print("Age", self._Age, "", end = "")
    print("LS", self._NaturalLifespan, "", end = "")
    print("Pr dth", round(self._ProbabilityOfDeathOtherCauses, 2), "", end = "")

  def CheckIfKilledByOtherFactor(self):
    if random.randint(0, 100) < self._ProbabilityOfDeathOtherCauses * 100:
      self._IsAlive = False
      return True
    else:
      return False

  def _CalculateRandomValue(self, BaseValue, Variability):
    return BaseValue - (BaseValue * Variability / 100) + (BaseValue * random.randint(0, Variability * 2) / 100)

class Fox(Animal):
  def __init__(self, Variability):
    self.DEFAULT_LIFE_SPAN = 7
    self.DEFAULT_PROBABILITY_DEATH_OTHER_CAUSES = 0.1
    super(Fox, self).__init__(self.DEFAULT_LIFE_SPAN, self.DEFAULT_PROBABILITY_DEATH_OTHER_CAUSES, Variability)
    self.FoodUnitsNeeded = int(10 * self._CalculateRandomValue(100, Variability) / 100)
    self.FoodUnitsConsumedThisPeriod  = 0

  def AdvanceGeneration(self, ShowDetail):
    if self.FoodUnitsConsumedThisPeriod == 0:
      self._IsAlive = False
      if ShowDetail:
        print("  Fox dies as has eaten no food this period.")
    else:
      if self.CheckIfKilledByOtherFactor():
        self._IsAlive = False
        if ShowDetail:
          print("  Fox killed by other factor.")
      else:
        if self.FoodUnitsConsumedThisPeriod < self.FoodUnitsNeeded:
          self.CalculateNewAge()
          if ShowDetail:
            print("  Fox ages further due to lack of food.")
        self.CalculateNewAge()
        if not self._IsAlive:
          if ShowDetail:
            print("  Fox has died of old age.")

  def ResetFoodConsumed(self):
    self.FoodUnitsConsumedThisPeriod = 0

  def ReproduceThisPeriod(self): 
    REPRODUCTION_PROBABILITY  = 0.25
    if random.randint(0, 100) < REPRODUCTION_PROBABILITY * 100:
      return True
    else:
      return False

  def GiveFood(self, FoodUnits):
    self.FoodUnitsConsumedThisPeriod = self.FoodUnitsConsumedThisPeriod + FoodUnits
  
  def Inspect(self):
    super(Fox, self).Inspect()
    print("Food needed", self.FoodUnitsNeeded, "", end = "")
    print("Food eaten", self.FoodUnitsConsumedThisPeriod, "", end = "")
    print()

class Genders(enum.Enum):
  Male = 1
  Female = 2
    
class Rabbit(Animal):
  def __init__(self, Variability, ParentsReproductionRate = 1.2):
    self.DEFAULT_LIFE_SPAN = 4
    self.DEFAULT_PROBABILITY_DEATH_OTHER_CAUSES  = 0.05
    super(Rabbit, self).__init__(self.DEFAULT_LIFE_SPAN, self.DEFAULT_PROBABILITY_DEATH_OTHER_CAUSES, Variability)
    self.ReproductionRate = ParentsReproductionRate * self._CalculateRandomValue(100, Variability) / 100
    if random.randint(0, 100) < 50:
      self.Gender = Genders.Male
    else:
      self.Gender = Genders.Female

  def Inspect(self):
    super(Rabbit, self).Inspect()
    print("Rep rate", round(self.ReproductionRate, 1), "", end = "")
    if self.Gender == Genders.Female:
      print("Gender Female")
    else:
      print("Gender Male")
    
  def IsFemale(self):
    if self.Gender == Genders.Female:
      return True
    else:
      return False
    
  def GetReproductionRate(self): 
    return self.ReproductionRate

def __Main__():
  MenuOption = 0
  while MenuOption != 3:
    print("Predator Prey Simulation Main Menu")
    print()
    print("1. Run simulation with default settings")
    print("2. Run simulation with custom settings")
    print("3. Exit")
    print()
    MenuOption = int(input("Select option: "))
    if MenuOption == 1 or MenuOption == 2:
      if MenuOption == 1:
        LandscapeSize = 15
        InitialWarrenCount = 5
        InitialFoxCount = 5
        Variability = 0
        FixedInitialLocations = True
      else:
        LandscapeSize = int(input("Landscape Size: "))
        InitialWarrenCount = int(input("Initial number of warrens: "))
        InitialFoxCount = int(input("Initial number of foxes: "))
        Variability = int(input("Randomness variability (percent): "))
        FixedInitialLocations = False
      Sim = Simulation(LandscapeSize, InitialWarrenCount, InitialFoxCount, Variability, FixedInitialLocations)
  input()

if __name__ == "__main__":
  __Main__()
