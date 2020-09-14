import numpy as np

import matplotlib as mpl

import matplotlib.pyplot as plt

import os, sys
import time

def read_parameter_file(filename):


    params = None

    return params



def calculate_accelerations(pos, masses, soft_length):
	# positions r = [x,y,z] for all particles
    x = pos[:,0:1]
    y = pos[:,1:2]
    z = pos[:,2:3]

    # matrix that stores all pairwise particle separations: r_j - r_i
    dx = x.T - x
    dy = y.T - y
    dz = z.T - z

    G = 5
    # matrix that stores 1/r^3 for all particle pairwise particle separations
    inv_r3 = (dx**2 + dy**2 + dz**2 + soft_length**2)
    inv_r3[inv_r3>0] = inv_r3[inv_r3>0]**(-1.5)

    ax = G * (dx * inv_r3) @ masses
    ay = G * (dy * inv_r3) @ masses
    az = G * (dz * inv_r3) @ masses

    a = np.hstack((ax, ay, az))
    print(a)
    return a

def convert_to_com_frame():
    pass

def main(ax):

    # Simulation parameters
    #N         = 10    # Number of particles

    #np.random.seed(17)            # set the random number generator seed

    #mass = 20.0*np.ones((N,1))/N  # total mass of particles is 20
    #pos  = np.random.randn(N,3)   # randomly selected positions and velocities
    #vel  = np.random.randn(N,3)



    pos = np.random.randn(150, 3)
    vel = np.random.randn(150, 3)
    mass = 20 * np.ones((150, 1)) / 20

    acc = calculate_accelerations(pos, mass, 0.1)
    t = 0
    dt = 0.01
    boxwidth=50.0

    vel -= np.sum(mass * vel) / np.sum(mass)
    pos -= np.sum(mass * pos) / np.sum(mass)
    for i in range(500):
        vel += acc * dt/2.0

        # drift
        pos += vel * dt

        # update accelerations
        acc = calculate_accelerations(pos, mass, 0.1)

        # (1/2) kick
        vel += acc * dt/2.0


        # update time
        t += dt

        pos[pos[:, :] > boxwidth/2] -= boxwidth
        pos[pos[:, :] < -boxwidth/2] += boxwidth


        posx = pos[:, 0:1]
        posy = pos[:, 1:2]

        plt.cla()

        ax.scatter(posx, posy, c="b", s=1)
        ax.set_xlim(-boxwidth/4, boxwidth/4)
        ax.set_ylim(-boxwidth/4, boxwidth/4)
        plt.pause(0.001)









if __name__ == "__main__":

    param_filename = "parameters.yml"
    params = read_parameter_file(param_filename)


    plt.ion()
    fig, ax = plt.subplots()

    main(ax)


    plt.ioff()
    plt.show()


