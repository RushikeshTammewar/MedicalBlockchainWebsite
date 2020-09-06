import torch
import torch.nn as nn
from transformers import *
from transformers import BertModel, BertConfig
from torch.utils.data import Dataset, DataLoader, SequentialSampler, TensorDataset
import json

class RecommenderDL(nn.Module):
	def __init__(self, max_seq_length=128, batch_size=32):
		super().__init__()
		self.model = AutoModel.from_pretrained("emilyalsentzer/Bio_ClinicalBERT")
		# self.config = BertConfig(vocab_size=28996)
		# self.model = BertModel(self.config).from_pretrained("bio_bert.bin")
			
		self.dataloader = LoadingData(max_seq_length=max_seq_length,
								batch_size=batch_size)
		
	def forward(self, text_data, batch_size=32):
		self.model.eval()
		torch_dataloader = self.dataloader.transform_text(text_data, batch_size=batch_size)

		logits_all = []
		for input_ids, input_mask, segment_ids in torch_dataloader:
			input_ids = input_ids
			input_mask = input_mask
			segment_ids = segment_ids

			with torch.no_grad():
				inputs = {'input_ids': input_ids, 'attention_mask': input_mask, 'token_type_ids': segment_ids}
				outputs = self.model(**inputs)
				logits = outputs[0]
				logits_all.append(logits)

		return torch.cat(logits_all, dim=0)


class InputFeatures(object):
	"""A single set of features of data."""

	def __init__(self, input_ids, input_mask, segment_ids):
		self.input_ids = input_ids
		self.input_mask = input_mask
		self.segment_ids = segment_ids


class LoadingData(Dataset):
	def __init__(self, max_seq_length=128, batch_size=32):
		"""
		Args:
			tokenizer: The tokenizer corresponding to the type of non-autoregressive model used.
			padding_idx: An integer indicating the index being used for the
				padding token in the preprocessed data. Defaults to 0.
			batch_size: The size of mini-batch of the data used.
			max_sequence_length: An integer indicating the maximum length
				accepted for the sequences in the set. If set to None,
				the length of the longest premise in 'data' is used.
				Defaults to None.
		"""
		# self.tokenizer = BertTokenizer.from_pretrained(pretrained_dir, do_lower_case=True)
		self.tokenizer = AutoTokenizer.from_pretrained("emilyalsentzer/Bio_ClinicalBERT")
		self.max_seq_length = max_seq_length
		self.batch_size = batch_size

	def convert_examples_to_features(self, examples, max_seq_length, tokenizer):
		"""Loads a data file into a list of `InputBatch`s."""

		features = []
		for (ex_index, text_a) in enumerate(examples):
			tokens_a = tokenizer.tokenize(text_a)

			# Account for [CLS] and [SEP] with "- 2"
			if len(tokens_a) > max_seq_length - 2:
				tokens_a = tokens_a[:(max_seq_length - 2)]

			tokens = ["[CLS]"] + tokens_a + ["[SEP]"]
			segment_ids = [0] * len(tokens)

			input_ids = tokenizer.convert_tokens_to_ids(tokens)

			# The mask has 1 for real tokens and 0 for padding tokens. Only real
			# tokens are attended to.
			input_mask = [1] * len(input_ids)

			# Zero-pad up to the sequence length.
			padding = [0] * (max_seq_length - len(input_ids))
			input_ids += padding
			input_mask += padding
			segment_ids += padding

			assert len(input_ids) == max_seq_length
			assert len(input_mask) == max_seq_length
			assert len(segment_ids) == max_seq_length

			features.append(
				InputFeatures(input_ids=input_ids,
							  input_mask=input_mask,
							  segment_ids=segment_ids))
		return features

	def _truncate_seq_pair(self, tokens_a, tokens_b, max_length):
		"""Truncates a sequence pair in place to the maximum length."""

		# This is a simple heuristic which will always truncate the longer sequence
		# one token at a time. This makes more sense than truncating an equal percent
		# of tokens from each, since if one sequence is very short then each token
		# that's truncated likely contains more information than a longer sequence.
		while True:
			total_length = len(tokens_a) + len(tokens_b)
			if total_length <= max_length:
				break
			if len(tokens_a) > len(tokens_b):
				tokens_a.pop()
			else:
				tokens_b.pop()

	def transform_text(self, data, batch_size=32):
		# transform data into seq of embeddings
		eval_features = self.convert_examples_to_features(data, self.max_seq_length, self.tokenizer)

		all_input_ids = torch.tensor([f.input_ids for f in eval_features], dtype=torch.long)
		all_input_mask = torch.tensor([f.input_mask for f in eval_features], dtype=torch.long)
		all_segment_ids = torch.tensor([f.segment_ids for f in eval_features], dtype=torch.long)
		eval_data = TensorDataset(all_input_ids, all_input_mask, all_segment_ids)

		# Run prediction for full data
		eval_sampler = SequentialSampler(eval_data)
		eval_dataloader = DataLoader(eval_data, sampler=eval_sampler, batch_size=batch_size)

		return eval_dataloader


def get_cosine_scores(logits):
	logits_mean = torch.mean(logits, dim=1)
	patient = logits_mean[0, :].view(1, -1)
	doctors = logits_mean[1:, :]

	if len(doctors.shape) < 2:
		doctors = doctors.view(1, -1)

	matching = torch.sum(patient.repeat(doctors.shape[0], 1) * doctors, dim=1).view(-1).numpy()
	# print("Cosine scores of patient and doctor features = ", matching.cpu())
	# print("Best matched doctor is -> ", all_doctors[torch.argmax(matching).cpu().data.item()])
	rankings = np.argsort(-matching)
	# with open("rank_outs.txt", 'w') as f:
	# 	for idx in rankings:
	# 		f.write(str(idx) + '\n')
	
	### {'rankings': [5, 7, 10, .....]}

	sample = {'rankings': list(rankings)}
	with open('rank_outs.json', 'w') as fp:
		json.dump(sample, fp)

if __name__ == '__main__':
	model = RecommenderDL()
	# patient = ["High blood pressure. Blood clotting. Hypertension. Heart strokes "]
	# all_doctors = ["Gynaecologist", "Urologist", "Cardiologist.Heart surgery"]
	# outs = model(patient + all_doctors)
	# get_cosine_scores(outs, all_doctors)

	model_inputs = []
	with open("inp.txt", 'r') as f:
		for line in f:
			model_inputs.append(line.strip())

	outs = model(model_inputs)
	get_cosine_scores(outs)