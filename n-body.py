import pygame, sys, math, copy
from pygame.locals import *
import numpy as np
import numpy.random as rand

pygame.init()

FPS = 100
fpsClock = pygame.time.Clock()

dim = (1080,720)
DISPLAYSURF = pygame.display.set_mode(dim,0,32)
pygame.display.set_caption('n-body Dynamics')

BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
RED 	= (255,   0,   0)
GREEN = (  0, 255,   0)
BLUE 	= (  0,   0, 255)
COLOUR = [RED,GREEN,BLUE]
x,y = 0,1


class particle:
	def __init__(self, name, mass, orbital_radius, G):
		if name == "Sun":
			self.radius = 5
			self.mass = mass
			self.orbital_radius = orbital_radius
			self.force = False
			self.name = name
			self.orbital_velocity = 0
			self.location = np.array([[dim[x]/2],[dim[y]/2]])
			self.velocity = np.array([[0],[0]])
		else:
			self.radius = 2*int(mass**(1/3))
			self.mass = mass
			self.orbital_radius = orbital_radius
			self.force = False
			self.name = name
			self.orbital_velocity = -1*math.sqrt(G*1e6/orbital_radius)
			self.location = np.array([[dim[x]/2],[dim[y]/2 - orbital_radius]])
			self.velocity = np.array([[self.orbital_velocity],[0]])
		
def particle_gen(G):
	universe = []
	universe.append(particle("Sun",1000000,0,G))
	universe.append(particle("Mercury",0.330,5.79,G))
	universe.append(particle("Venus",4.87,10.82,G))
	universe.append(particle("Earth",5.97,14.96,G))
	universe.append(particle("Mars",0.642,22.79,G))
	universe.append(particle("Jupiter",1898,77.86,G))
	universe.append(particle("Saturn",568,143.35,G))
	universe.append(particle("Unranus",86.8,287.25,G))
	universe.append(particle("Neptune",102,449.51,G))
	universe.append(particle("Pluto",0.0146,443.68,G))
	return universe	
		
def force_calc(particle_index,universe,G):
	u_c = copy.deepcopy(universe)
	u_c.pop(particle_index) #remove particle from universe
	r,f = [],[]
	#calculate individual forces
	for i in range(len(u_c)):
		r.append(universe[particle_index].location - u_c[i].location)
		f.append(-1*(G*universe[particle_index].mass*u_c[i].mass*r[i])/pow(np.linalg.norm(r[i]),3))
	f_total = sum(f) #vector sum of individual forces
	return f_total

def position_calc(particle_index,universe):
	pygame.draw.circle(DISPLAYSURF,COLOUR[particle_index%3],tuple(int(x) for x in universe[particle_index].location),universe[particle_index].radius,0) #draw ball at current position
	universe[particle_index].velocity = universe[particle_index].velocity + universe[particle_index].force/universe[particle_index].mass #calculate new velocity
	universe[particle_index].location = universe[particle_index].location + universe[particle_index].velocity
	return universe[particle_index]
	
	
G = 0.000130087
universe = particle_gen(G)
DISPLAYSURF.fill(WHITE)
while True:
#	DISPLAYSURF.fill(WHITE)
	for i in range(len(universe)):
		universe[i].force = force_calc(i,universe,G)
	for i in range(len(universe)):
		universe[i] = position_calc(i,universe)

	for event in pygame.event.get():
		if event.type == QUIT:
			pygame.quit()
			sys.exit()
	pygame.display.update()
	fpsClock.tick(FPS)
