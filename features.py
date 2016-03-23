#! /usr/bin/env python

#label e(n,m)
def getContext1(n, m, edges_dict):
	context=[]
	context.append('label_e=' + str(edges_dict[(n,m)]))
	return context

def getContext2(n, edges_dict):
	context=[]
	for item in edges_dict.keys():
		if item[0]==n:
			context.append('label_e_star=' + str(edges_dict[item]))
	return context

def getContext3_4(n, m, pos_dict):
	context = []
	context.append('n_pos=' + pos_dict[n])
	context.append('m_pos=' + pos_dict[m])
	return context

def getContext5(n, m, edges_dict):
	context = []
	depth=0
	parent_id=n
	while(parent_id!=-1):
		depth+=1
		for item in edges_dict.keys():
			if parent_id==item[1]:
				parent_id=item[0]
				break
	context.append('depth_root_m=' + str(depth))
	return context

def getContext6_7(n, m, edges_dict):
	context=[]
	count_n=0
	count_m=0
	for item in edges_dict.keys():
		if item[0] == n:
			count_n+=1
		if item[0] == m:
			count_m+=1
	context.append('Num_children_n=' + str(count_n))
	context.append('Num_children_m=' + str(count_m))
	return context

def getContext8(m, words_form_list):
	context=[]
	for form in words_form_list:
		for item in form:
			for i in item.items():
				if i[0]=='id' and i[1] == m:
					context.append('node_len_m=' + str(len(form)))
					break
	return context
	
def getContext9_10(n, m, NE_dict):
	context=[]
	for item in NE_dict.keys():
		if n in range(item[0],item[1]+1) and NE_dict[item][1] != '':
			context.append('NE_tag_n=' +str(NE_dict[item][2])+ '_' +str(NE_dict[item][1]))
		if m in range(item[0],item[1]+1) and NE_dict[item][1] != '': 
			context.append('NE_tag_m=' +str(NE_dict[item][2])+ '_' +str(NE_dict[item][1]))
	return context

def getContext11(m, word_form_list):
	context=[]
	return context

def getContext12_13(n, m, word_dict):
	context=[]
	context.append('lemma_n=' + str(word_dict[n]))
	context.append('lemma_m=' + str(word_dict[m]))
	return context

def getContext14(n, m, edges_dict, word_dict):
	context=[]
	context.append('lemma_n_label_e=' + str(word_dict[n]) + '|' + str(edges_dict[(n,m)]))
	return context
	
def getContext15(n,m, edges_dict,word_dict):
	context=[]
	for item in edges_dict.keys():
		if item[0] ==n and item[1]!=m:
			context.append('lemma_m_label_e_star=' + str(word_dict[m]) + '|' + str(edges_dict[(n,item[1])]))
	return context

def getContext16(m, word_dict):
	context=[]
	context.append('char_len_m=' + str(len(str(word_dict[m]))))
	return context

#edges_dict[(parent_id,child_id)]=label
#word_dict[id]=word
#pos_dict[id]=pos_tag
#NE_dict[(start,end,head)]=(name,type,is_ne)
#word_form[form[i]], form[i]=
def getContextall(n, m, edges_dict, word_dict, pos_dict, NE_dict, words_form_list):
	context={}
	#1
	context.update({'label_e':edges_dict[(n,m)]})

	#2
	for item in edges_dict.keys():
		if item[0]==n:
			context.update({'label_e_star':edges_dict[item]})
	#3_4
	context.update({'n_pos':pos_dict[n]})
	context.update({'m_pos':pos_dict[m]})
	#5
	depth=0
	parent_id=n
	while(parent_id!=-1):
		depth+=1
		for item in edges_dict.keys():
			if parent_id==item[1]:
				parent_id=item[0]
				break
	context.update({'depth_root_m':str(depth)})
	#6_7
	count_n=0
	count_m=0
	for item in edges_dict.keys():
		if n == item[0]:
			count_n+=1
		if m == item[0]:
			count_m+=1
	context.update({'Num_children_n': str(count_n)})
	context.update({'Num_children_m':str(count_m)})
	#8
	for form in words_form_list:
		for item in form:
			for i in item.items():
				if i[0]=='id' and i[1] == m:
					context.update({'node_len_m':str(len(form))})
					
	#9_10
	for item in NE_dict.keys():
		if n in range(item[0],item[1]+1) and NE_dict[item][1] != '':
			context.update({'NE_tag_n': str(NE_dict[item][2])+ '_' + NE_dict[item][1]})
		if m in range(item[0],item[1]+1) and NE_dict[item][1] != '': 
			context.update({'NE_tag_m':str(NE_dict[item][2])+ '_' +NE_dict[item][1]})
	#12_13
	context.update({'lemma_n': word_dict[n]})
	context.update({'lemma_m': word_dict[m]})
	#14
	context.update({'lemma_n_label_e':word_dict[n] + '|' + edges_dict[(n,m)]})
	#15
	for item in edges_dict.keys():
		if item[0] ==n and item[1]!=m:
			context.update({'lemma_m_label_e_star': word_dict[m] + '|' + edges_dict[(n,item[1])]})
	#16
	context.update({'char_len_m':  str(len(word_dict[m]))})
	return context
