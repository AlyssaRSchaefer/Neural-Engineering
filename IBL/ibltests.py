from one.api import ONE
ONE.setup(silent=True) #connect to public IBL db
one = ONE(password='international') #add password argument if connecting to the public db

#print(one.search_terms()) # prints what we can search by
#help(one.search) # prints documentation for search method

#returns a list of all brainwide experiment eids
brain_wide_sessions = one.search(project='brainwide')

#lets use a random one as an example
eid = brain_wide_sessions[23];
#dsets = one.list_datasets(eid, collection='raw_ephys_data') #list all datasets associated with this experiment
#for dset in dsets:
#    print(dset)

locations = one.load_dataset(eid, 'electrodeSites.brainLocationIds_ccf_2017.npy', collection='alf/probe00')
for location in locations:
    print(location)