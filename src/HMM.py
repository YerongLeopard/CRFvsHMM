import numpy as np#
def ln(num):
	import numpy as np
	if num>0:
		return np.log(num)
	else: 
		return -np.inf

def load_data(FILE_NAME):
	'''
	Load data from a text file
	Input : filename
	Output: the number of records, dictionary of TAGs and dictionary of observations, sequence of tags and observations 
	'''
	count=0; DICT_TAG={}; DICT_OBS={}
	srm_tag=[]; srm_obs=[]
	NUM_TAG=0; NUM_OBS=0
	f_in=open(FILE_NAME,'r')
	record=f_in.readline()
	while record!="" :		
		count+=1
		tag, obs=record.split() # every record is a tag followed by an observation
		record = f_in.readline()
		if not tag in DICT_TAG.keys():
			DICT_TAG[tag]=NUM_TAG
			NUM_TAG+=1
			srm_tag
		if not obs in DICT_OBS.keys():
			DICT_OBS[obs]=NUM_OBS
			NUM_OBS+=1
		srm_tag=srm_tag+[DICT_TAG[tag]]
		srm_obs=srm_obs+[DICT_OBS[obs]]		
	return count, DICT_TAG, DICT_OBS, srm_tag, srm_obs

def sup_train_HMM(DICT_TAG, DICT_OBS,srm_tag, srm_obs):
	'''
	Input : srm_tag. srm_obs
	Outpur: Length of the sequence, dictionaries and trained matrices
	'''
	## Loading data, determing the dimensions and building dictionaries

	LENG=len(srm_tag)
	assert LENG == len(srm_obs), 'Tag and observation sequences do not match.'
	NUM_TAG=len(DICT_TAG); NUM_OBS=len(DICT_OBS)
	A=np.zeros([NUM_TAG+1, NUM_TAG+1])# A is arranged in the order of 0, 1, 2 ,START END
	O=np.zeros([NUM_TAG, NUM_OBS])

	## Starting state
	tag2_v=srm_tag[0]; obs2_v=srm_obs[0]
	A[NUM_TAG,tag2_v]+=1;
	## Starting state
	count=1
	while count < LENG:
		tag1_v=srm_tag[count-1]; obs1_v=srm_obs[count-1]
		tag2_v=srm_tag[count]  ; obs2_v=srm_obs[count]
		A[tag1_v,tag2_v]+=1;
		O[tag1_v,obs1_v]+=1;
		count+=1
	tag1_v=srm_tag[count-1]; obs1_v=srm_obs[count-1]

	A[tag1_v,NUM_TAG]+=1;
	O[tag1_v,obs1_v]+=1;
	### normalization
	for idx, numer in enumerate(A):
		deno=sum(numer)
		A[idx]=numer/deno
	for idx, numer in enumerate(O):
		deno=sum(numer)
		O[idx]=numer/deno
	A[NUM_TAG,NUM_TAG]=-1
	### normalization
	return A, O

def rm_START(A):
	NUM_TAG=A.__len__()-1
	for idx in range(NUM_TAG):
		A[-1,idx]=1.0/NUM_TAG
	return A

def rm_END(A):
	NUM_TAG=A.__len__()-1
	for idx in range(NUM_TAG):
		A[idx,-1]=1.0/NUM_TAG
	return A	

def viterbi_HMM(A, O, srm_obs, srm_tag):
	assert A.__len__()-1==O.__len__(), "Dimensions of A and O mismatch."
	NUM_TAG=O.__len__()
	gen_Lprob=np.array([-ln(A[-1, tag_v])-ln(O[tag_v,srm_obs[0]]) for tag_v in range(NUM_TAG)])
	ending=np.zeros(NUM_TAG)
	gen_table=[]; it=0; srm_pdc=[]

	omit_Lprob=-ln(A[-1, srm_tag[0]])-ln(O[srm_tag[0],srm_obs[0]])
	LENG=len(srm_obs)

	for it in range(LENG-1):#LENG-1
		bkup_gen_Lprob=np.zeros(NUM_TAG)
		for tag_v in range(NUM_TAG):
			tmp_Lprob=[Lprob_it-ln(A[pre_tag, tag_v])-ln(O[tag_v,srm_obs[it+1]]) for pre_tag ,Lprob_it in enumerate(gen_Lprob)]
			bkup_gen_Lprob[tag_v]=min(tmp_Lprob)
			ending[tag_v]=np.argmin(tmp_Lprob)
        
		gen_Lprob=bkup_gen_Lprob
		omit_Lprob+=-ln(A[srm_tag[it], srm_tag[it+1]])-ln(O[srm_tag[it+1],srm_obs[it+1]])
		gen_table=gen_table+[[int(tag_v) for tag_v in ending]]

	end_tag_v=np.argmin(gen_Lprob)
	srm_pdc=backtrack(end_tag_v,gen_table)
	return srm_pdc

def	backtrack(end_tag_v, gen_table):

	LENGm1=len(gen_table)
	srm_pdc=[end_tag_v]# index is LENG-1
	current_tag_v=end_tag_v
	gen_table.reverse()
	for it in range(LENGm1):
		current_tag_v=gen_table[it][current_tag_v]
		srm_pdc=[current_tag_v]+srm_pdc
	return srm_pdc

def loss_Hamming(srm_pdc, srm_tag):
	LENG=len(srm_pdc)
	assert LENG==len(srm_tag), 'Predicted sequence and observed sequence have difference length.'
	return np.count_nonzero([x-y for x,y in zip(srm_pdc, srm_tag)])/float(LENG)

def main():
	FILE_NAME="../hw4data/ron.txt"
	LENG, DICT_TAG, DICT_OBS, srm_tag, srm_obs=load_data(FILE_NAME)
	A, O=sup_train_HMM(DICT_TAG, DICT_OBS,srm_tag, srm_obs)

	A=rm_START(A); A=rm_END(A)
	srm_pdc=viterbi_HMM(A, O, srm_obs, srm_tag)
	print loss_Hamming(srm_pdc,srm_tag)

if __name__== "__main__":
  main()

