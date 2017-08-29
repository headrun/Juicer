import sys
import csv

def main(in_final_alexarank):
    f = open(in_final_alexarank,'r')
    output_file = 'in_alexasort'
    for i in f:
        i = i.split('\t')
        if i[-1].strip() != '' :
            s = i[-1].strip()
            if int(s.replace(',','')) <= 100:
                out_file = file(output_file,'ab+')
                out_file.write('%s\t%s\n'%(i[0],i[-1].strip()))
                out_file.close()

main('in_final_alexarank')
