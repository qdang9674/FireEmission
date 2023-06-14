months       = '01','02','03','04','05','06','07','08','09','10','11','12'
#sources      = ['SAVA','BORF','TEMF','DEFO','PEAT','AGRI']
sources      = ['BORF']

# in this example we will calculate annual CO emissions for the 14 GFED 
# basisregions over 1997-2014. Please adjust the code to calculate emissions
# for your own specie, region, and time period of interest. Please
# first download the GFED4.1s files and the GFED4_Emission_Factors.txt
# to your computer and adjust the directory where you placed them below

directory    = 'C:/Users/DinhMenh/Desktop/aaaaaa/'


"""
Read in emission factors
"""
species = [] # names of the different gas and aerosol species
EFs     = np.zeros((41, 6)) # 41 species, 6 sources

k = 0
f = open(directory+'/GFED4_Emission_Factors.txt')
while 1:
    line = f.readline()
    if line == "":
        break
        
    if line[0] != '#':
        contents = line.split()
        species.append(contents[0])
        EFs[k,:] = contents[1:]
        k += 1
                
f.close()

# we are interested in CO for this example (4th row):
#EF_CO2 = EFs[2,:]
EF_CO2 = [EFs[2,2]]
start_year = 1997
end_year   = 2022
data_all = []


"""
make table with summed DM emissions for each region, year, and source
"""
CO2_table = np.zeros((15, end_year - start_year + 1)) # region, year

for year in range(start_year, end_year+1):
    string = directory+'/GFED4.1s_'+str(year)+'.hdf5'
    f = h5py.File(string, 'r')
    
    
    if year == start_year: # these are time invariable    
        basis_regions = f['/ancill/basis_regions'][:]
        grid_area     = f['/ancill/grid_cell_area'][:]
    
    
    #CO2_emissions = np.zeros((720, 1440))
    for month in range(12):
        CO2_emissions = np.zeros((720, 1440))
        # read in DM emissions
        string = '/emissions/'+months[month]+'/DM'
        DM_emissions = f[string][:]
        for source in range(len(sources)):
            # read in the fractional contribution of each source
            string = '/emissions/'+months[month]+'/partitioning/DM_'+sources[source]
            contribution = f[string][:]
            # calculate CO emissions as the product of DM emissions (kg DM per 
            # m2 per month), the fraction the specific source contributes to 
            # this (unitless), and the emission factor (g CO per kg DM burned)
            CO2_emissions += DM_emissions * contribution * EF_CO2[source]
        
        data_all.append(grid_area* CO2_emissions / 1E12)
    
#     # fill table with total values for the globe (row 15) or basisregion (1-14)
#     for region in range(15):
#         if region == 14:
#             mask = np.ones((720, 1440))
#         else:
#             mask = basis_regions == (region + 1)            
#         CO2_table[region, year-start_year] = np.sum(grid_area * mask * CO2_emissions)
        
    print(year)
data_all = np.array(data_all)

# # convert to Tg CO 
# CO2_table = CO2_table / 1E12
# print(CO2_table.shape)
# print(CO2_table)

# please compare this to http://www.falw.vu/~gwerf/GFED/GFED4/tables/GFED4.1s_CO.txt