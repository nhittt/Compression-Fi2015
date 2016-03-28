from __future__ import division
import sys
import pickle
import json
from pprint import pprint
from features import *
from training import *
import zlib
import io
from nltk import MaxentClassifier
from itertools import *


def powerset(iterable):
	"powerset([1,2,3]) --> () (1,) (2,) (3,) (1,2) (1,3) (2,3) (1,2,3)"
	s = list(iterable)
	return chain.from_iterable(combinations(s, r) for r in range(len(s) + 1))


def prob_deletion_1_edge(json_object, maxent_model, edge_n_m):
	context_option = 1
	featureset = get_context_1_edge(json_object, edge_n_m, context_option)
	return maxent_model.prob_classify(featureset).prob(0)


def prob_deletion_sentence(json_object, maxent_model):
	context_option = 1
	featuresets = get_context_sentence(json_object, context_option)
	return maxent_model.prob_classify_many(featuresets).prob(0)


def search_children(json_object, node_n):
	children_list = []
	edges = get_edges(json_object)
	for edge in edges:
		(parent_id, child_id, label) = get_elements_in_edge(edge)
		if parent_id == node_n:
			children_list.append(child_id)
	return children_list


def search_highest_child_root(json_object, maxent_model):
	edges = get_edges(json_object)
	children_root = []
	for edge in edges:
		(parent_id, child_id, label) = get_elements_in_edge(edge)
		if parent_id == -1:
			children_root = search_children(json_object, parent_id)
			break
	highest_score_child_root = prob_deletion_1_edge(json_object, maxent_model, (-1, children_root[0]))
	highest_child_root = children_root[0]
	for i in range(1, len(children_root)):
		if prob_deletion_1_edge(json_object, maxent_model, (-1, children_root[i])) > highest_score_child_root:
			highest_score_child_root = prob_deletion_1_edge(json_object, maxent_model, (-1, children_root[i]))
			highest_child_root = children_root[i]
	return highest_child_root


# top scoring compression

def max_subset(json_object, maxent_model, node_n):
	children_n = search_children(json_object, node_n)
	subset_children = list(powerset(children_n))
	prob_max = 0
	for child in children_n:
		prob_max += 1 - prob_deletion_1_edge(json_object, maxent_model, (node_n, child))
	max_score_C_n = prob_max
	max_subset = tuple(children_n)

	for subset in subset_children:
		score_C_n = 0
		for child in children_n:
			prob = prob_deletion_1_edge(json_object, maxent_model, (node_n, child))
			if child in subset:
				prob = 1 - prob
			score_C_n += prob
		if max_score_C_n < score_C_n:
			max_score_C_n = score_C_n
			max_subset = subset
	return max_subset


max_subsets = []


def max_subset_sentence(json_object, maxent_model, node_n):
	if not search_children(json_object, node_n):
		global max_subsets
		max_subsets = []
		max_subsets.append(node_n)
	else:
		for child in max_subset(json_object, maxent_model, node_n):
			max_subset_sentence(json_object, maxent_model, child)
			max_subsets.extend(max_subset(json_object, maxent_model, node_n))
	return max_subsets


def top_scoring_compression(json_object, maxent_model):
	top_best_compress_edges = []
	node_n = search_highest_child_root(json_object, maxent_model)
	top_best_compress_edges.append(node_n)
	top_best_compress_edges.extend(max_subset_sentence(json_object, maxent_model, node_n))
	return top_best_compress_edges


def top_scoring_compression_sentence(json_object, maxent_model):
	nodes = get_nodes(json_object)
	words_form = []
	id_form = {}
	for node in nodes:
		word_in_form = get_words_in_node(node)
		words_form.append(word_in_form)
		for item in get_words_id_form_tag(word_in_form):
			id_form[item[0]] = item[1]
	top_best_compress = sorted(top_scoring_compression(json_object, maxent_model))
	top_best_compress_edges = []
	for edge in top_best_compress:
		if edge not in top_best_compress_edges:
			top_best_compress_edges.append(edge)
	return top_best_compress_edges


if __name__ == '__main__':
	with open('model/compress_model_0123_test', 'rb') as fmodel:
		maxent = pickle.load(fmodel)
	# maxent.show_most_informative_features()
	for json_object in read_jsonfile('data/compression_data_0.json'):
		print top_scoring_compression_sentence(json_object, maxent)
