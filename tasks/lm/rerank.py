import csv
import argparse
import torch
import torch.nn.functional as F
import pdb

from collections import defaultdict
from utils.data import las_to_lm
from configs import *


def rerank(model_path, csv_path):
    if DEVICE == torch.device('cpu'):
        lm = torch.load(model_path, map_location='cpu')
    else:
        lm = torch.load(model_path)
    lm.to(DEVICE)
    lm.eval()
    transcripts = defaultdict(list)
    with open(csv_path, 'r') as csv_file:
        raw_csv = csv.reader(csv_file)
        for row in raw_csv:
            transcripts[row[0]].append(row[1])
    for id, sents in transcripts.items():
        res = []
        if any(len(sent) == 0 for sent in sents):
            for _ in sents:
                print("{} {}".format(id, _))
            continue
        for sent in sents:
            _sent = las_to_lm(sent.split())
            targets = torch.LongTensor([lm.vocab[tok] for tok in _sent[1:]]).to(DEVICE)
            logits = lm(_sent)
            try:
                loss = F.cross_entropy(logits, targets).item()
            except Exception as ex:
                print(ex)
                pdb.set_trace()
            res.append((loss, sent))
        res.sort(key=lambda x: x[0])
        transcripts[id] = [_[1] for _ in res]
        for _ in transcripts[id]:
            print("{}, {}".format(id, _))
        lm.detach()
    return transcripts


if __name__ == '__main__':
    reranked = rerank('models/best_hd_1024.pt', 'data/submission_beam_5_all.csv')