import csv
import argparse
import torch
import torch.nn.functional as F

from collections import defaultdict
from utils.data import las_to_lm
from configs import DEVICE, rr_agrs, args


def rerank(model_path, csv_path):
    lm = torch.load(model_path).to(DEVICE)
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
            targets = torch.LongTensor([lm.vocab[tok] for tok in _sent[1:]])
            logits = lm(_sent)
            loss = F.cross_entropy(logits, targets).item()
            res.append((loss, sent))
        res.sort(key=lambda x: x[0])
        transcripts[id] = [_[1] for _ in res]
        for _ in transcripts[id]:
            print("{}, {}".format(id, _))
    return transcripts


if __name__ == '__main__':
    reranked = rerank(rr_agrs.lm_path, rr_agrs.res_path)
