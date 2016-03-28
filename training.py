from __future__ import division
import sys
import pickle
import json
from pprint import pprint
from features import *
import zlib
import io
from nltk import MaxentClassifier


# read json input
def read_jsonfile(json_file):
    objects = []
    data = ''
    with io.open(json_file, 'r', encoding='utf8') as f:
        for line in f:
            if line in ['\n', '\n\r']:
                objects.append(json.loads(data))
                data = ''
            else:
                data += line
        try:
            objects.append(json.loads(data))
        except:
            return objects
    return objects


def read_tiny_jsonfile(json_file):
    with open(json_file) as f:
        data = json.load(f)
        return data


# get sentence(id,sentence,nodes, edges, NE)
def get_idsentence(object):
    return object['graph']['id']


def get_sentence(object):
    return object['graph']['sentence']


def get_nodes(object):
    nodes = []
    for i in range(len(object['graph']['node'])):
        nodes.append(object['graph']['node'][i])
    return nodes


def get_edges(object):
    edges = []
    for i in range(len(object['graph']['edge'])):
        edges.append(object['graph']['edge'][i])
    return edges


def get_name_entity(object):
    name_entity = []
    for i in range(len(object['graph']['entity_mention'])):
        name_entity.append(object['graph']['entity_mention'][i])
    return name_entity


# get nodes(form, words, gender, head_word_index) in sentence
def get_form_in_node(node):
    return node['form']


def get_words_in_node(node):
    return node['word']


def get_gender_in_node(node):
    return node['gender']


def get_headwordindex_in_node(node):
    return node['head_word_index']


# get words in nodes
def get_words_id_form_tag(words_in_form):
    words_from_form = []
    for i in range(len(words_in_form)):
        (id, form, stem, tag) = (
            words_in_form[i]['id'], words_in_form[i]['form'], words_in_form[i]['stem'], words_in_form[i]['tag'])
        words_from_form.append((id, form, stem, tag))
    return words_from_form


# get edges' elements in sentence
def get_elements_in_edge(edge):
    return (edge['parent_id'], edge['child_id'], edge['label'])


# get entity's elements
def get_elements_in_NE(name_entity):
    return (name_entity['start'], name_entity['end'], name_entity['head'], name_entity['name'], name_entity['type'],
            name_entity['is_proper_name_entity'])


# get compression (text, edges)
def get_compression_text(object):
    return object['compression']['text']


def get_compression_edges(object):
    return object['compression']['edge']


# get compression's edge element
def get_compression_edge_element(edge):
    return (edge['parent_id'], edge['child_id'])


# read input json
def readfile(filename):
    with open(filename) as f:
        for line in f:
            while line in ['\n', '\r\n']:
                try:
                    data = json.loads(line)
                except ValueError:
                    line += next(f)

                id = data['graph']['sentence']
                print(id)


# get context for 1 edge (json_object, egde,  option_train=0, option_test=1)
def get_context_1_edge(json_object, edge_n_m, context_option):
	nodes = get_nodes(json_object)
	edges = get_edges(json_object)
	name_entity = get_name_entity(json_object)
	compress_edges = get_compression_edges(json_object)
	words_form = []
	compress_pa_ch = []
	id_word = {}
	id_tag = {}
	nes_nee_neh_name_type_proper= {}
	pa_ch_label = {}
	for node in nodes:
		word_in_form = get_words_in_node(node)
		words_form.append(word_in_form)
		for item in get_words_id_form_tag(word_in_form):
			id_word[item[0]] = item[2]
			id_tag[item[0]] = item[3]
	for edge in edges:
		(parent_id, child_id, label) = get_elements_in_edge(edge)
		pa_ch_label[(parent_id, child_id)] = label
	for entity in name_entity:
		(start, end, head, name, type, is_ne) = get_elements_in_NE(entity)
		nes_nee_neh_name_type_proper[(start, end, head)] = (name, type, is_ne)
	for compress_edge in compress_edges:
		compress_pa_ch.append(get_compression_edge_element(compress_edge))
	(parent_id, child_id) = edge_n_m
	if (parent_id, child_id) in compress_pa_ch:
		compress_tag = 1
	else:
		compress_tag = 0
	co = getContextall(parent_id, child_id, pa_ch_label, id_word, id_tag, nes_nee_neh_name_type_proper, words_form)

	if context_option == 0:
		return (co, compress_tag)
	else:
		return co


def get_context_sentence(json_object, context_option):
    edges = get_edges(json_object)
    context_sentence = []
    for edge in edges:
        (parent_id, child_id, label) = get_elements_in_edge(edge)
        context_sentence.append(get_context_1_edge(json_object, (parent_id, child_id), context_option))
    return context_sentence


def training(list_filename, model_name):
    # training in large data
    context_data = []
    for filename in list_filename:
        json_objects = read_jsonfile(filename)
        for json_object in json_objects:
            context_data.extend(get_context_sentence(json_object, 0))
    print('Done get contexts')
    m = MaxentClassifier.train(context_data, max_iter=100)
    with open(model_name, 'wb') as fmodel:
        pickle.dump(m, fmodel)
    print('Finish training maxent model')


if __name__ == "__main__":
    # test('testdata.json','compress_model')
    list_train = []
    for i in range(len(sys.argv) - 1):
        list_train.append('data/compression_data_%s.json' % sys.argv[i + 1])
    print(list_train)
    training(list_train, 'compress_model_0123_100')
# test('data/compression_data_4.json','compress_model_0123_100','data/output_4_100')
