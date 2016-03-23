from __future__ import division
import sys
import pickle
import json
from pprint import pprint
from features import *
#m = MaxentModel()
import zlib
import io
from nltk import MaxentClassifier


			
#read json input
def read_jsonfile(json_file):
	objects=[]
	data=''
	with io.open(json_file,'r', encoding='utf8') as f:
		for line in f:
			if line in ['\n','\n\r']:
				objects.append(json.loads(data))
				data=''
			else:
				data+=line
		try:
			objects.append(json.loads(data))
		except:
			return objects
	return objects

def read_tiny_jsonfile(json_file):
	with open(json_file) as f:
		data = json.load(f)
		return data

#get sentence(id,sentence,nodes, edges, NE)
def get_idsentence(object):
	return object['graph']['id']
	
def get_sentence(object):
	return object['graph']['sentence']
	
def get_nodes(object):
	nodes=[]
	for i in range(len(object['graph']['node'])):
		nodes.append(object['graph']['node'][i])
	return nodes

def get_edges(object):
	edges=[]
	for i in range(len(object['graph']['edge'])):
		edges.append(object['graph']['edge'][i])
	return edges

def get_name_entity(object):
	name_entity=[]
	for i in range(len(object['graph']['entity_mention'])):
		name_entity.append(object['graph']['entity_mention'][i])
	return name_entity

#get nodes(form, words, gender, head_word_index) in sentence
def get_form_in_node(node):
	return node['form']

def get_words_in_node(node):
	return node['word']

def get_gender_in_node(node):
	return node['gender']

def get_headwordindex_in_node(node):
	return node['head_word_index']
	
#get words in nodes
def get_words_id_form_tag(words_in_form):
	words_from_form=[]
	for i in range(len(words_in_form)):
		(id,form,stem,tag)=(words_in_form[i]['id'],words_in_form[i]['form'],words_in_form[i]['stem'],words_in_form[i]['tag'])
		words_from_form.append((id,form,stem,tag))
	return words_from_form
	
#get edges' elements in sentence 
def get_elements_in_edge(edge):
	return (edge['parent_id'],edge['child_id'],edge['label'])

#get entity's elements 
def get_elements_in_NE(name_entity):
	return (name_entity['start'], name_entity['end'], name_entity['head'], name_entity['name'], name_entity['type'], name_entity['is_proper_name_entity'])

#get compression (text, edges)
def get_compression_text(object):
	return object['compression']['text']

def get_compression_edges(object):
	return object['compression']['edge']

#get compression's edge element
def get_compression_edge_element(edge):
	return(edge['parent_id'],edge['child_id'])

#read input json
def readfile(filename):
	with open(filename) as f:
		for line in f:
			while line in ['\n', '\r\n']:
				try:
					data =json.loads(line)
				except ValueError:
					line+=next(f)

				id = data['graph']['sentence']
				print(id)
		
		
def main_tiny_data():
	
	data =  read_tiny_jsonfile('testdata.json')
	#get nodes, edges
	nodes = get_nodes(data)
	edges = get_edges(data)
	name_entity = get_name_entity(data)
	compress_edges=get_compression_edges(data)

	id_word ={}	
	id_tag = {}
	pa_ch_label={}
	NEs_NEe_Neh_name_type_is={}
	words_form=[]
	compress_pa_ch=[]
	context_all=[]
	for node in nodes:
		word_in_form = get_words_in_node(node)
		words_form.append(word_in_form)
		for item in get_words_id_form_tag(word_in_form):
			id_word[item[0]] = item[2]
			id_tag[item[0]] = item[3]
	for edge in edges:
		(parent_id, child_id, label) = get_elements_in_edge(edge)
		pa_ch_label[(parent_id,child_id)]=label
	for entity in name_entity:
		(start,end,head,name,type,is_ne) = get_elements_in_NE(entity)
		NEs_NEe_Neh_name_type_is[(start,end,head)]=(name,type,is_ne)
	
	for compress_edge in compress_edges:
		compress_pa_ch.append(get_compression_edge_element(compress_edge))

	for edge in edges:
		(parent_id, child_id, label) = get_elements_in_edge(edge)
		if (parent_id,child_id) in compress_pa_ch:
			compress_tag=1
		else:
			compress_tag=0
		(feature,tag)=(getContextall(parent_id,child_id,pa_ch_label, id_word, id_tag, NEs_NEe_Neh_name_type_is, words_form),compress_tag)
		context_all.append((feature,tag))

	m = MaxentClassifier.train(context_all, max_iter=10)
	with open('compress_model', 'wb') as fmodel:
		pickle.dump(m, fmodel)

#context(data, option_train=0, option_test=1)
def get_context_all(data,option):
	nodes = get_nodes(data)
	edges = get_edges(data)
	name_entity = get_name_entity(data)
	compress_edges=get_compression_edges(data)
	compress_text=get_compression_text(data)

	id_word ={}	
	id_tag = {}
	pa_ch_label={}
	NEs_NEe_Neh_name_type_is={}
	words_form=[]
	compress_pa_ch=[]
	context_all=[]
	for node in nodes:
		word_in_form = get_words_in_node(node)
		words_form.append(word_in_form)
		for item in get_words_id_form_tag(word_in_form):
			id_word[item[0]] = item[2]
			id_tag[item[0]] = item[3]
	for edge in edges:
		(parent_id, child_id, label) = get_elements_in_edge(edge)
		pa_ch_label[(parent_id,child_id)]=label
	for entity in name_entity:
		(start,end,head,name,type,is_ne) = get_elements_in_NE(entity)
		NEs_NEe_Neh_name_type_is[(start,end,head)]=(name,type,is_ne)

	for compress_edge in compress_edges:
		compress_pa_ch.append(get_compression_edge_element(compress_edge))

	for edge in edges:
		(parent_id, child_id, label) = get_elements_in_edge(edge)
		if (parent_id,child_id) in compress_pa_ch:
			compress_tag=1
		else:
			compress_tag=0
		co = getContextall(parent_id,child_id,pa_ch_label, id_word, id_tag, NEs_NEe_Neh_name_type_is, words_form)
		(feature,tag)=(co,compress_tag)
		#print(getContextall(parent_id,child_id,pa_ch_label, id_word, id_tag, NEs_NEe_Neh_name_type_is, words_form))
		if option == 0:
			context_all.append((feature,tag))
		else:
			context_all.append(co)
			
	return context_all

def training(list_filename,model_name):
	#training in large data
	context_all=[]
	for filename in list_filename:
		objects=read_jsonfile(filename)
		for data in objects:
			#get nodes, edges
			context_all.extend(get_context_all(data,0))
	print('Done list files for training')
	m = MaxentClassifier.train(context_all, max_iter=100)
	with open(model_name, 'wb') as fmodel:
		pickle.dump(m, fmodel)

def test(filename_test,model, output):
	#test data
	objects=read_jsonfile(filename_test)
	with open(model, 'rb') as fmodel:
		maxent = pickle.load(fmodel)
	maxent.show_most_informative_features()
	print('Read model')
	com_rate=0
	with io.open(output,'w',encoding='utf8') as fout, io.open('data/gold','w',encoding='utf8') as fgold:
		
		for data in objects:
			pred= maxent.classify_many(get_context_all(data,1))

			nodes = get_nodes(data)
			edges = get_edges(data)
			name_entity = get_name_entity(data)
			compress_edges=get_compression_edges(data)
			compress_text=get_compression_text(data)

			id_word ={}	
			id_form={}
			id_tag = {}
			pa_ch_label={}
			NEs_NEe_Neh_name_type_is={}
			words_form=[]
			compress_pa_ch=[]
			context_all=[]
			s_compress_id_list=[]
			for node in nodes:
				word_in_form = get_words_in_node(node)
				words_form.append(word_in_form)
				for item in get_words_id_form_tag(word_in_form):
					id_form[item[0]] = item[1]
					id_word[item[0]] = item[2]
					id_tag[item[0]] = item[3]
			for edge in edges:
				(parent_id, child_id, label) = get_elements_in_edge(edge)
				pa_ch_label[(parent_id,child_id)]=label
			for entity in name_entity:
				(start,end,head,name,type,is_ne) = get_elements_in_NE(entity)
				NEs_NEe_Neh_name_type_is[(start,end,head)]=(name,type,is_ne)

			for compress_edge in compress_edges:
				compress_pa_ch.append(get_compression_edge_element(compress_edge))


			for i in range(len(edges)):
				(parent_id, child_id, label) = get_elements_in_edge(edges[i])
				if pred[i] ==1:
					for form in words_form:
					    for item in form:
						if item['id']==child_id:
						    for i in form:
						        s_compress_id_list.append(i['id'])
            		s_compress_id_list.sort()
			for x in s_compress_id_list:
				fout.write('%s '%id_form[x])
		    	fout.write('%s\n'%compress_text[-1])
		    	fgold.write('%s %s\n'%(compress_text[:-1],compress_text[-1]))
			rate=len(s_compress_id_list)/len(id_word)
			com_rate+=rate/2
			print(rate)
		print(com_rate)
	print('Done test')

if __name__ == "__main__":

	#test('testdata.json','compress_model')
	"""list_train=[]
	for i in range(len(sys.argv)-1):
		list_train.append('data/compression_data_%s.json'%sys.argv[i+1])
	print(list_train)
	training(list_train,'compress_model_0123_100')"""
	test('data/compression_data_4.json','compress_model_0123_100','data/output_4_100')


		
