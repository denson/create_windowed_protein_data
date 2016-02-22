# create_windowed_protein_data
Takes protein sequence data as input and generates windowed data as output

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
