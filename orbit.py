from math import *
import time
import pygame
G = 6.67408*10**(-11)
starttime = time.time()
pygame.init()

class OrbitingObject:
    def __init__(self, init_speed_x, init_speed_y, x, y, masse, size, color):
        self.velocity_x = 0
        self.velocity_y = 0
        self.speed_x = init_speed_x
        self.speed_y = init_speed_y
        self.x = x
        self.y = y
        self.masse = masse
        self.size = size
        self.color = color
        
    def update(self, dt):
        self.speed_x = self.velocity_x * dt + self.speed_x
        self.speed_y = self.velocity_y * dt + self.speed_y
        self.x = self.speed_x * dt + self.x
        self.y = self.speed_y * dt + self.y
    
    def setvelocity(self, F):
        self.velocity_x = projection_u_sur_v(F, (1, 0))
        #print(projection_u_sur_v(F, (1, 0)))
        self.velocity_y = projection_u_sur_v(F, (0, 1))
        #print(projection_u_sur_v(F, (0, 1)))
    
    def getposition(self) -> tuple:
        return(self.x, self.y)
    
    def getspeed(self) -> tuple:
        return (self.speed_x,self.speed_y)

    def draw(self, fenetre):
        pygame.draw.circle(fenetre, self.color, (self.x/1000000, self.y/1000000), self.size)
    
    def calculforceavec(self, object):
        dAB = distance(object.getposition(), self.getposition()) #calcul la distance entre la terre et la lune
        fAB = Fg(self.masse, object.masse, dAB) #calcul la force exercé par la terre sur la lune
        uAB = normalisation(creervecteur(self.getposition(),object.getposition() )) #créer une vecteur normalisé qui part de la lune vers la terre
        uAB = scalaire_foix_vecteur(uAB, fAB) #met à l'échelle de la force le vecteur uAB le - c'est pour dire que c'est une attraction
        self.setvelocity(uAB) #Application des forces à la lune

def scalaire(u : tuple, v : tuple) -> float:
    return sum([u[i]*v[i] for i in range(0,len(u))])

def projection_u_sur_v(u : tuple, v : tuple) -> float:
    return (scalaire(u,v))/(scalaire(v,v))

def Fg(mA : int, mB: int, dAB: float) -> float:
    return G*((mA*mB)/dAB**2)

def distance(A: tuple, B: tuple) -> float:
    return sqrt(sum([(B[i] - A[i])**2 for i in range(0, len(A))]))

def creervecteur(point1: tuple, point2: tuple) -> tuple:
    return tuple(point2[i]-point1[i] for i in range(0,len(point1)))

def norme_vecteur(u:tuple) -> float:
    return sqrt(sum([u[i]**2 for i in range(0, len(u))]))

def normalisation(u:tuple) -> tuple:
    norme = norme_vecteur(u)
    return tuple(u[i]/norme for i in range(0, len(u)))

def scalaire_foix_vecteur(u : tuple, k: int) -> tuple:
    return tuple(u[i] * k for i in range(0, len(u)))


if __name__ == "__main__":
    #Pygame
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    
    pygame.display.set_caption("Ma fenêtre Pygame")


    terre = OrbitingObject(init_speed_x = 0, init_speed_y = 0, x = 0, y = 0, masse = 5.9737*10**24, size = 5, color = (0,0,250))
    lune = OrbitingObject(init_speed_x = 2000000000000000, init_speed_y = 2000000000000000, x = 384400*10**3, y = 10**8, masse = 5.9737*10**24, size = 5, color = (250,0,0))
    lune.draw(screen)
    terre.draw(screen)
    pygame.display.flip()

    
    #Boucle de simulation
    dx = 0.0000000001
    actual_time = time.time()
    last_time = time.time()
    end = False
    while end == False:
        #Gerer le temps pour la simulation ---------------------------------------------------------------
        last_time = time.time()
        if last_time-actual_time > dx: #Permet de faire bouger les choses toutes les dx = 0.5 secondes
            actual_time = time.time()

            #Gerer les evenement --------------------------------------------------------------------------
            for event in pygame.event.get(): 
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        end = True
                        break # break out of the for loop
                    elif event.type == pygame.QUIT:
                        end = True
                        break # break out of the for loop
                if end:
                    break # to break out of the while loop

            
            #Calculs ----------------------------------------------------------------------------------------

            #calcul pour force appliqué à la lune
            lune.calculforceavec(terre)
            lune.update(dx)
        
            lune.draw(screen)

            #calcul pour force appliqué à la terre
            
            terre.calculforceavec(lune)
            terre.update(dx)
            

            terre.draw(screen)
            
            pygame.display.flip()
            screen.fill((0,0,0))
    pygame.quit()

            
            



 