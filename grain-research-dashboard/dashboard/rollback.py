import shutil

src = 'c:/Users/administer/WorkBuddy/20260315144604/grain-research-dashboard/dashboard/spreads_v1.4.html'
dst = 'c:/Users/administer/WorkBuddy/20260315144604/grain-research-dashboard/dashboard/spreads.html'

shutil.copy(src, dst)
print('Rollback completed!')
