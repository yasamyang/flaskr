head=[]
domain=[]
operators=[]
methods=[]
init=[]
act=[]
plan=[]

def rlisp(lispfile='basictmp.lisp', s_head = True, s_domain= False, s_init = False, s_act = False):
	'''read lisp file'''
	filein = [line.strip() for line in open(lispfile).readlines()]    #read file
	for ln in filein:
	    if ln.find('(defdomain housework') != -1:
	        s_domain = True
	        s_head = False
	    if ln.find(';;;initial state;;;') != -1:
	        s_init = True
	        s_domain = False
	    if ln.find(';;;action;;;') != -1:
	        s_init = False
	        s_act = True    
	    if ln.find('(find-plans') != -1:
	        s_act = False

	    if s_head:
	    	    head.append(ln)
	    if s_domain:
	    	    domain.append(ln)
	    if s_init:
	    	    init.append(ln)        
	    if s_act:
	        act.append(ln)	    
	    if s_head or s_domain or s_init or s_act:
	        pass
	    else:
	        plan.append(ln)
	#print head
	#if put op & me in there, will just get last data
	#op={}
	#me={}
	for ditem in domain:
		#put op & me in there, will get different data each time
		op={}
		me={}
		if ":operator" in ditem:
			op['name'], op['input'] = om_strip(ditem)
			operators.append(op)
			print op
		if ":method" in ditem:
			me['name'], me['input']= om_strip(ditem)
			methods.append(me)
			print me
	#print init
	#print act
	#print plan

def om_strip(ditem):
	ditem=ditem.replace('(','')
	ditem=ditem.replace(')','')
	item=ditem.split()
	return item[1],item[2:]

def wlisp(lispfile='basic.lisp'):
	'''write lisp file'''
	fileout = open (lispfile,'w')
	[fileout.write(h+'\n') for h in head]
	[fileout.write(d+'\n') for d in domain]
	[fileout.write(i+'\n') for i in init]
	[fileout.write(a+'\n') for a in act]
	[fileout.write(p+'\n') for p in plan]
	fileout.close()
	fileout = open ('command','w')
	[fileout.write(com+'\n') for com in domain if ":operator" in com or ":method" in com]
	fileout.close()

if __name__ == '__main__':
	rlisp()
	wlisp()
