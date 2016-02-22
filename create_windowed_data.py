# -*- coding: utf-8 -*-
"""
Created on Fri Feb 12 09:19:39 2016

@author: denson
"""


import os

import pandas as pd

import numpy as np

import string

def check_directory(dirname):
    if not os.path.exists(dirname):
        os.makedirs(dirname)

def convert_line_endings(temp):

        # remove windows line endings
        temp = string.replace(temp, '\r\n', '')
        temp = string.replace(temp, '\r', '')


        return temp
        




def generate_window(win_1_array,window_size,number_of_features,terminal_ID_col):
    
    '''
    win_1_array = input array
    window_size = the size window array we are creating
    number_of_features = number of features in each row of win_1_array, not counting class ID and row #
    terminal_ID_col = column where the terminal ID is, this tells us where sequences start and end.
    
    This function reads in a csv file with each row containing a class ID in
    column #0 and number_of_features additional features in each row. 
    It creates an array with a class ID in column #0 and "windowed" rows.
    
    The value 9999.9999 represents NaN (not a number) in this case.
    
    For example with number_of_features = 3 and window_size = 3 and 12 rows of data:
    
     1,1,2,3
     1,2,3,4
    -1,3,4,5
     1,4,5,6
    -1,5,6,7
    -1,6,7,8
     1,7,8,9
     1,8,9,10
     1,9,10,11
    -1,10,11,12
     1,11,12,13
    -1,12,13,14

    
     windowed data:
    
    
     1,9999.9999,9999.9999,9999.9999,1,2,3,2,3,4
     1,1,2,3,2,3,4,3,4,5
    -1,2,3,4,3,4,5,4,5,6
     1,3,4,5,4,5,6,5,6,7
    -1,4,5,6,5,6,7,6,7,8
    -1,5,6,7,6,7,8,7,8,9
     1,6,7,8,7,8,9,8,9,10
     1,7,8,9,8,9,10,9,10,11
     1,8,9,10,9,10,11,10,11,12
    -1,9,10,11,10,11,12,11,12,13
     1,10,11,12,11,12,13,12,13,14
    -1,11,12,13,12,13,14,9999.9999,9999.9999,9999.9999
    
    
    '''
 
 

    
    before_and_after_size = (window_size - 1)/2
    m,n = np.shape(win_1_array)
    
    # make a new array that is window_size x number of features wide + 1 more 
    # column for the class information and + 1 more column for the row numbers
    
    window_array = np.ones((m,(number_of_features*window_size)+1))
    
    # 9999.9999 is our representation of nan
    window_array = window_array * 9999.9999
    

    
    row_number = 0
    sequence_count = 0
    
    
    # copy the class values to the window array
    window_array[:,0] = win_1_array[:,0]
    
    sequence_start_row = 0
    sequence_end_row   = 1
    for line in range(m):
        
    
    
            
        if win_1_array[row_number,terminal_ID_col] == 1:
            sequence_count = sequence_count + 1
            sequence_end_row = row_number + 1
            
            thisSequence = win_1_array[sequence_start_row:sequence_end_row,1:]
            
            
            
            # set up to do the middle
            startRow = sequence_start_row 
            endRow   = sequence_end_row 

            startCol = ((before_and_after_size)*number_of_features) + 1
            endCol   = ((before_and_after_size)*number_of_features) + number_of_features + 1
            window_array[startRow:endRow, startCol:endCol] = thisSequence[:,:]
            
            for idx in range(before_and_after_size,0,-1):

                # set up to do the left side
                startRow = sequence_start_row + idx 
                endRow   = sequence_end_row 
                startCol = ((before_and_after_size-idx)*number_of_features) + 1
                endCol   = ((before_and_after_size-idx)*number_of_features) + number_of_features + 1
     
                window_array[startRow:endRow, startCol:endCol] = thisSequence[:-idx,:]

                

                # set up to do the right side
                startRow = sequence_start_row  
                endRow   = sequence_end_row - idx
                startCol = ((before_and_after_size+idx)*number_of_features) + 1
                endCol   = ((before_and_after_size+idx)*number_of_features) + number_of_features + 1

                window_array[startRow:endRow, startCol:endCol] = thisSequence[idx:,:]
                                   
            
            # the next row after the end row is the new start row
            # in python ranges do not include the last index
            # so win_1_array[0:10,:] is the first 10 rows and
            # win_1_array[10:20,:] is the next 10 rows
            sequence_start_row = sequence_end_row
            
    
        row_number = row_number + 1   
        

        
    return window_array
    
    


        

        
        

# set the proper path separator for this operating system
path_sep = os.sep

full_path = os.path.realpath(__file__)
script_path, file_name = os.path.split(full_path)

# the path to the input data files
input_path = script_path + path_sep 

output_path = script_path + path_sep 

check_directory(output_path)

input_file_name = input_path + 'sample_data' + path_sep + 'sample_input.csv'
out_file_name = output_path + 'sample_data' + path_sep + 'sample_output_window_size_15.csv'

# input_file_name = input_path + 'train_Denson_WINDOW_SIZE_1_61_features_MCC+AUC_elite_9.csv'
# out_file_name = output_path + 'train_Denson_WINDOW_SIZE_1_61_features_MCC+AUC_elite_9_window_size_15.csv'

win_1_array = np.genfromtxt(input_file_name,skip_header=1,delimiter = ",")

rows,cols = np.shape(win_1_array )

window_size = 15
number_of_features = cols - 1
terminal_id_col = cols - 1

# read in the non-windowed data
windowed_data = generate_window(win_1_array,window_size,number_of_features,terminal_id_col)

# we have an integer class followed by window_size * number_of_features floats
data_fmt = '%.6f'


    
# remove class = 0 (unknown), keep class = 1 (disordered) and class = -1
# ordered before saving
    
the_args = np.where(windowed_data[:,0] != 0.0)
the_args = the_args[0]

windowed_data = windowed_data[the_args,:]

rows,cols = np.shape(windowed_data)



np.savetxt(out_file_name, windowed_data , fmt=data_fmt, delimiter = ',')

windowed_data = np.genfromtxt(out_file_name,skip_header=0,delimiter = ",")

# TODO: vectorize this 
for row in range(rows):
    for col in range(cols):
        if np.isnan(windowed_data[row,col]):
            print('NaN at %i, %i' %(row,col))

