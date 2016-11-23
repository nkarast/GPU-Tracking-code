import sys
import math
import pickle
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl

from modules.tracker import *
from modules.naff import *
from modules.grid import *
from modules.tune_resonances import *
from modules.FMA import *

############################ LATTICE ##################################
lattice = Lattice()
lattice.read_twiss_table("small_ring/lattice_octupole.twi")
lattice.optimise()
lattice.compile()
lattice.n_turns =10000
lattice.collect_tbt_data = 1 # every 1 turn
lattice.norm_emit_x=1e-4
lattice.norm_emit_y=1e-4
#lattice.bunch_energy_spread=1e-4
#lattice.bunch_length=1e-4

############################ BUNCH  ##################################
#n_particles=100
#b=lattice.make_matched_bunch(n_particles)

b,grid = cmp_grid(lattice.sigma_x(),lattice.sigma_x()*15,lattice.sigma_y(),lattice.sigma_y()*15,0.5)
n_particles=b.size()

lattice.track(b)

filename = 'tbt.dat'
tbt = [ (b.x[0], b.xp[0], b.y[0], b.yp[0], b.z[0] , b.d[0]) for b in lattice.turns ]
with open(filename,'w') as outfile:
  for t in tbt:
    outfile.write("{} {} {} {} {} {}\n".format(t[0], t[1], t[2], t[3], t[4], t[5]))

############################ NAFF  ##################################

tunes_x = naff(lattice.turns[0:lattice.n_turns], vec_HostBunch.x, vec_HostBunch.xp, second_half=True)
tunes_y = naff(lattice.turns[0:lattice.n_turns], vec_HostBunch.y, vec_HostBunch.yp)
fig,ax=create_plot(tunes_x,tunes_y, grid,resonance_diagram=False)
plt.show()

############################ FMA  ##################################

tunes_x1, tunes_y1, tunes_x2, tunes_y2, tune_diffusion = FMA(lattice.turns[0:3000], lattice.turns[7000:10000], second_half_x = True)
fig,ax=create_plot(tunes_x2,tunes_y2, diff_tunes=tune_diffusion, colorbar=True, resonance_diagram=True, order=10)
plt.show()


