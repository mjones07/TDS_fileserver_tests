#!/usr/bin/env python2.7

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd




def import_results(testname):
    # return pandas array for whole results
    data = pd.read_csv('./results')

    return data

#def parse_results(req_param, par):
#    # get the req param out of pandas

def count_repeats(data):
    rank = data['rank']
    count = 0
    for i in rank:
        if i == 0:
            count+=1

    if count == 0:
        count = 1

    return count

def agg_rate(rates,par):
    #print rates, par
    repeats = int(np.ceil((len(rates)/float(par))))
    try:
        len_rate = float(len(rates))
        #print repeats, len(rates), float(par)
        #print int(np.ceil(len_rate/repeats))
        reshaped =  rates.reshape(repeats,int(np.ceil(len_rate/repeats)))
        rate = np.array(reshaped)
        return np.sum(rate,axis=1)
    except ValueError:
        agg = np.zeros(repeats)
        
        for i in range(repeats-1):
            for j in range(par):
                agg[i] += rates[j+i*par]
        if agg[-1] == 0:
            agg[-1] = np.mean(rates[j+i*par+1:])*par
        
        return agg
   
def agg_rate_from_median(rates,par):
    #print rates, par
    repeats = int(np.ceil((len(rates)/float(par))))
    agg = np.zeros(repeats)

    grouped = [[] for x in range(repeats)]
    #print(grouped)
    i = 0
    j = 0
    for rate in rates:
        #print(i,j)
        grouped[i].append(rate)
        j += 1
        if j==par:
            i += 1
            j = 0

    for i,group in enumerate(grouped):
        agg[i] = np.min(group)*par            

    return agg
   
def testplot(data,test,subplot_list):


    # sub select data for plot
    selection = data[data.file.str.contains(test)]

    pars = data.mpisize.unique()

    results = []
    for par in pars:
        rates = selection[selection.mpisize==par]['rate(MB/s)'].values
        # now aggregate
        results.append(agg_rate_from_median(rates,par))#list(np.array(rates)*par))#agg_rate(rates,par)) 
        
    
    plt.subplot(subplot_list[0],subplot_list[1],subplot_list[2])
    

    plt.boxplot(results)

    print test
    print 'Reapeats for test:'
    for a,v in zip(pars,results):
        print 'par: %s, count: %s' %(a,len(v))
    
    plt.xticks(np.arange(len(pars))+1,pars)
    plt.ylabel('Aggregate rate (MB/s)')
    plt.xlabel('Concurrent requests')
    


def main():
    # import results
    data = pd.read_csv('./results_atsrrepro.csv')
    # two tests defined by file loc

    plt.figure()
    testplot(data,'host298',(2,1,1))
    plt.title('high performance server')
    testplot(data,'dap4gws',(2,1,2))
    plt.title('OpenDAP4GWS server')
    plt.tight_layout()
    plt.show()
    

if __name__ == '__main__':
    main()
