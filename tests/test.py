from vdf_wrapper import *
from statistics import mean, stdev
from time import perf_counter
import csv

X_VALUE = b"\x08" + (b"\x00" * 99)
EXPS = 10

def testVDF(lbda, T):
    pp = setup(lbda,T)

    t0 = perf_counter()
    y, proof = eval(pp, X_VALUE)
    t1 = perf_counter()
    is_valid = verify(pp, X_VALUE, y, proof)
    t2 = perf_counter()

    return (t1 - t0), (t2 - t1)

if __name__ == '__main__':

    csvfile = open('../results/exec_time.csv', 'w', newline='')
    writer = csv.writer(csvfile, delimiter='\t', quotechar='|', quoting=csv.QUOTE_MINIMAL)
    
    for lbda in [256, 512, 1024]:

        writer.writerow([f'Lambda = {lbda}'])
        writer.writerow([
            'T',
            'Eval Mean',
            'Eval Stdev',
            'Verify Mean', 
            'Verify Stdev'
        ])

        for T in range(1,11):
            T *= 500000
            tps = []
            tvs = []

            print(f'λ = {lbda} T = {T}')

            for i in range(EXPS):
                print(f'Experiment {i+1}/{EXPS}', end='\t')
                t_prove, t_verify = testVDF(lbda, T)
                print(f'TP = {t_prove} \t TV = {t_verify}')
                tps.append(t_prove)
                tvs.append(t_verify)

            eval_mean, eval_stdev = mean(tps), stdev(tps)
            verf_mean, verf_stdev = mean(tvs), stdev(tvs)

            writer.writerow([T, eval_mean, eval_stdev, verf_mean, verf_stdev])
