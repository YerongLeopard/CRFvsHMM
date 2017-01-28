import numpy as np
def load_data(FILE_NAME):
	'''
	Load data from a text file
	Input : filename
	Output: the number of records, dictionary of TAGs and dictionary of observations, sequence of tags and observations 
	'''
	count=0; DICT_TAG={}; DICT_OBS={}
	seq_tag=[]; seq_obs=[]
	NUM_TAG=0; NUM_OBS=0
	f_in=open(FILE_NAME,'r')
	record=f_in.readline()
	while record!="":		
		count+=1
		tag, obs=record.split() # every record is a tag followed by an observation
		record = f_in.readline()
		if not tag in DICT_TAG.keys():
			DICT_TAG[tag]=NUM_TAG
			NUM_TAG+=1
			seq_tag
		if not obs in DICT_OBS.keys():
			DICT_OBS[obs]=NUM_OBS
			NUM_OBS+=1
		seq_tag=seq_tag+[DICT_TAG[tag]]
		seq_obs=seq_obs+[DICT_OBS[obs]]		
	return count, DICT_TAG, DICT_OBS, seq_tag, seq_obs

def sup_train_HMM(DICT_TAG, DICT_OBS,seq_tag, seq_obs):
	'''
	Input : seq_tag. seq_obs
	Outpur: Length of the sequence, dictionaries and trained matrices
	'''
	## Loading data, determing the dimensions and building dictionaries

	LENG=len(seq_tag)
	assert LENG == len(seq_obs), 'Tag and observation sequences do not match.'
	NUM_TAG=len(DICT_TAG); NUM_OBS=len(DICT_OBS)
	A=np.zeros([NUM_TAG+1, NUM_TAG+1])# A is arranged in the order of 0, 1, 2 ,START END
	O=np.zeros([NUM_TAG, NUM_OBS])

	## Starting state
	tag2_v=seq_tag[0]; obs2_v=seq_obs[0]
	A[NUM_TAG,tag2_v]+=1;
	## Starting state
	count=1

	while count < LENG:
		tag1_v=seq_tag[count-1]; obs1_v=seq_obs[count-1]
		tag2_v=seq_tag[count]  ; obs2_v=seq_obs[count]
		A[tag1_v,tag2_v]+=1;
		O[tag1_v,obs1_v]+=1;
		count+=1
	tag1_v=seq_tag[count-1]; obs1_v=seq_obs[count-1]

	A[tag1_v,NUM_TAG]+=1;
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

def eq_START(A):
	NUM_TAG=A.__len__()-1
	for idx in range(NUM_TAG):
		A[-1,idx]=1.0/NUM_TAG
	return A

def eq_END(A):
	NUM_TAG=A.__len__()-1
	for idx in range(NUM_TAG):
		A[idx,-1]=1.0/NUM_TAG
	return A	

def viterbi_HMM(A, O, seq_obs):
	assert A.__len__()-1==O.__len__(), "Dimensions of A and O mismatch."
	NUM_TAG=O.__len__()
	gen_Lprob=np.array([-np.log(A[-1, tag_v])-np.log(O[tag_v,seq_obs[0]]) for tag_v in range(NUM_TAG)])
	ending=np.zeros(NUM_TAG)
	gen_table=[]
	seq_tag=[]

	LENG=len(seq_obs)
	for it in range(12-1):#LENG-1
		bkup_gen_Lprob=np.zeros(NUM_TAG)
		print it
		print gen_Lprob,'gen_Lprob'
		for tag_v in range(NUM_TAG):
			tmp_Lprob=[Lprob_it-np.log(A[pre_tag, tag_v])-np.log(O[tag_v,seq_obs[it+1]]) for pre_tag ,Lprob_it in enumerate(gen_Lprob)]
			bkup_gen_Lprob[tag_v]=min(tmp_Lprob)
			ending[tag_v]=np.argmin(tmp_Lprob)
		gen_Lprob=bkup_gen_Lprob
		print gen_Lprob,'gen_Lprob'
		print ending, 'ending'
		gen_table=gen_table+[[int(tag_v) for tag_v in ending]]

	end_tag=np.argmin(gen_Lprob)

	seq_pdc=backtrack(end_tag,gen_table)
	return seq_pdc

def	backtrack(end_tag_v, gen_table):

	LENGm1=len(gen_table)
	seq_pdc=[end_tag_v]# index is LENG-1
	current_tag_v=end_tag_v
	gen_table.reverse()
	for it in range(LENGm1):
		current_tag_v=gen_table[it][current_tag_v]
		seq_pdc=[current_tag_v]+seq_pdc
	return seq_pdc

def loss_Hamming(seq_pdc, seq_tag):
	#assert len(seq_pdc)==len(seq_obs), 'Predicted sequence and observed sequence have difference length.'
	print seq_pdc[0:11],'seq_pdc[0:11]'
	print seq_tag[0:11],'seq_obs[0:11]'
	#return np.count_nonzero([x-y for x,y in zip(seq_pdc, seq_obs)])

def main():
	FILE_NAME="../hw4data/ron.txt"
	LENG, DICT_TAG, DICT_OBS, seq_tag, seq_obs=load_data(FILE_NAME)
	A, O=sup_train_HMM(DICT_TAG, DICT_OBS,seq_tag, seq_obs)
	A=eq_START(A); A=eq_END(A)

	seq_pdc=viterbi_HMM(A, O, seq_obs)
	print loss_Hamming(seq_pdc,seq_tag)

if __name__== "__main__":
  main()

