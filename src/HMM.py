import numpy as np
def load_data(FILE_NAME):
	"""
	Load data from a text file
	Input : filename
	Output: the number of records, dictionary of TAGs and dictionary of observations 
	"""
	count=0; DICT_TAG={}; DICT_OBS={}
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
		if not obs in DICT_OBS.keys():
			DICT_OBS[obs]=NUM_OBS
			NUM_OBS+=1
	return count, DICT_TAG, DICT_OBS

def sup_train_HMM(FILE_NAME):
	'''
	Input : file name
	Outpur: Length of the sequence, dictionaries and trained matrices
	'''
	# Loading data, determing the dimensions and building dictionaries
	LENG, DICT_TAG, DICT_OBS=load_data(FILE_NAME)

	NUM_TAG=len(DICT_TAG); NUM_OBS=len(DICT_OBS)
	A=np.zeros([NUM_TAG+1, NUM_TAG+2])# A is arranged in the order of 0, 1, 2 ,START END
	O=np.zeros([NUM_TAG, NUM_OBS])
	f_in=open(FILE_NAME,'r')
	record1=""
	record2=f_in.readline()
	## Starting state
	tag2, obs2=record2.split()
	A[NUM_TAG,DICT_TAG[tag2]]+=1;
	record1=record2
	record2=f_in.readline()
	## Starting state
	count=1

	while count < LENG:
		count+=1
		tag1, obs1=record1.split()
		tag2, obs2=record2.split()
		A[DICT_TAG[tag1],DICT_TAG[tag2]]+=1;
		O[DICT_TAG[tag1],DICT_OBS[obs1]]+=1;

		record1=record2
		record2 =f_in.readline()
	tag1, obs1=record1.split()
	A[DICT_TAG[tag1],NUM_TAG+1]+=1;
	assert record2=="", "Have NOT reached the EOF"
	### normalization
	for idx, numer in enumerate(A):
		deno=sum(numer)
		A[idx]=numer/deno
	for idx, numer in enumerate(O):
		deno=sum(numer)
		O[idx]=numer/deno
	print O
	### normalization
	return LENG, DICT_TAG, DICT_OBS, A, O

def viterbi_HMM(A, O, sequence):
	assert A.__len__()-1==O.__len__(), "Dimensions of A and O mismatch."
	gen_prob=np.zeros([1,O.__len__()])
	
	return

def main():
	FILE_NAME="../hw4data/ron.txt"
	LENG, DICT_TAG, DICT_OBS, A, O= sup_train_HMM(FILE_NAME)
	viterbi_HMM(A, O, [1])
	

if __name__== "__main__":
  main()

