from bandolier.nomad_tools import NomadWrapper

nw = NomadWrapper(url='http://localhost:4646')
allocations = nw.allocations('recommender')
# print('allocations',allocations)
alloc_ids = []
for allocation in allocations:
  print('id',allocation['ID'],'status',allocation['ClientStatus'])
  alloc_ids.append(allocation['ID'])
results = nw.restart_allocations(alloc_ids)
print('restart results',results)