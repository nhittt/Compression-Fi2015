from __future__ import division
from training import *
import io
import pickle
import json

def search_children(node_n, json_object):
    children_list = []
    edges = get_edges(json_object)
    for edge in edges:
        (parent_id, child_id, label) = get_elements_in_edge(edge)
        if parent_id == node_n:
            children_list.append(child_id)
    return children_list


def prob_deletion_1_edge(json_object, maxent_model, edge_n_m):
    context_option = 1
    featureset = get_context_1_edge(json_object, edge_n_m, context_option)
    return maxent_model.prob_classify(featureset).prob(0)

def prob_retain_1_edge(json_object, maxent_model, edge_n_m):
    context_option = 1
    featureset = get_context_1_edge(json_object, edge_n_m, context_option)
    return maxent_model.prob_classify(featureset).prob(1)

def find_best_result(n, json_object, maxent_model):
    c_0_n = []
    c_0_n.append((n, 0))
    for m in search_children(n, json_object):
        if prob_retain_1_edge(json_object, maxent_model, (n, m)) > 0.5:
            c_0_n.extend(find_best_result(m, json_object, maxent_model))
        else:
            c_0_n.append((m, -1))
    return c_0_n

def find_best_compression(json_object, maxent_model):
    c_0_r=[]
    best = -1
    max_pret=-1
    root=-1
    c_0_r.append((root, 0))
    for n in search_children(root, json_object):
        c_0_r.extend(find_best_result(n, json_object, maxent_model))
        p_pret_root_n=prob_retain_1_edge(json_object, maxent_model, (root, n))
        if p_pret_root_n>max_pret:
            max_pret=p_pret_root_n
            best = n
    for n in search_children(root, json_object):
        if n is not best:
            c_0_r[n]=(n, -1)
    return c_0_r

def find_next_best(c_k_n, heaps):
    for (k_i, m_i) in c_k_n:
        if k_i>-1:
            c_k_star_n=c_k_n
            (k_i + 1,m_i) = find_next_best([(k_i, m_i)], heaps)
            c_k_star_n[m_i]=



if __name__ == '__main__':
    with io.open('model/compress_model_0123_test', 'rb') as fmodel:
        maxent = pickle.load(fmodel)
    for json_object in read_jsonfile('data/compression_data_0.json'):
        print find_best_compression(json_object, maxent)
        break
