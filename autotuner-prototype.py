#!/usr/bin/python3
# Auto-tuner prototype
# Built for INE5540 robot overlords

import subprocess # to run stuff
import sys # for args, in case you want them
import time  # for time
import math  # for inf
import itertools

def tuner(argv):
    exec_file = 'matmult'
    compilation_line = ['gcc','-o',exec_file,'mm.c']
    steps = ['-DSTEP=']
    possible_steps = range(1, 4)
    possible_flags = ['-O2', '-O3', '-Ofast', '-funroll-all-loops', '-funroll-loops', '-fno-defer-pop',
                      '-fforce-addr', '-fomit-frame-pointer', '-finline-functions',
                      '-ffast-math', '-fstrength-reduce', '-fthread-jumps']
    current_flags = []
    historico_tempo = {}

    combination_depth = int(argv[0])  # A quantidade máxima de flags por combinação
    isDebug = ('-d' in argv)

    print("Iniciando autotuning")

    for i in range(1, combination_depth + 1):

        flags_combinadas = itertools.combinations(possible_flags, i)

        for flag in flags_combinadas:
            current_flags = list(flag)

            tempo_best_step = math.inf
            for step in possible_steps:
                step_power = pow(2, step)
                current_step = [steps[0] + str(step_power)]

                if isDebug:
                	print(compilation_line + current_step + current_flags)

                # Compile code
                compilation_try = subprocess.run(compilation_line + current_step + current_flags)
                if (compilation_try.returncode != 0):
                    print("Sad compilation")
                else:
                    if isDebug:
                        print("Happy compilation")

                # Run code
                input_size = str(4)
                if isDebug:
                    print("Start execution\n")
                t_begin = time.time() # timed run
                run_trial = subprocess.run(['./'+exec_file, input_size])
                t_end = time.time()
                tempo_decorrido = t_end-t_begin
                if (run_trial.returncode != 0):
                    print("\nSad execution")
                else:
                    if isDebug:
                        print("\nHappy execution in "+str(tempo_decorrido))
                    
                if tempo_decorrido < tempo_best_step:
                    tempo_best_step = tempo_decorrido
            historico_tempo[tuple(current_step + current_flags)] = tempo_best_step

    melhor_par = ('', math.inf)
    for key in historico_tempo.keys():
        if historico_tempo[key] < melhor_par[1]:
            melhor_par = (key, historico_tempo[key])
    
    print("\nMelhor comando de compilação:")
    best_flags = " ".join(compilation_line) + " " + " ".join(melhor_par[0]) + "\nEm: " + str(melhor_par[1]) + " segundos."
    print(best_flags)
        



if __name__ == "__main__":
    tuner(sys.argv[1:]) # go auto-tuner
