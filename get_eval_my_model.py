from eval import Evaluation
from utils import read_img_features
from vlnbert.vlnbert_init import get_tokenizer
from param_for_eval_my_model import args
from env_wf_one_sample import R2RBatch
from agent import Seq2SeqAgent
import json
# todo how to get route
# run this code get result. Then get some bad samples, then replace objector by https://conceptnet.io/c/en/bedroom
# if it is have some examples right this idea will be work.


args.model_name = 'wf_test_all_sample_VLN_bert'
args.vlnbert = 'prevalent'
args.result_file = f'./result/{args.model_name}_score_summary.json'
args.result_path_file = f'./result/{args.model_name}_predict_path.json'
args.result_error_path_file = f'./result/{args.model_name}_predict_error_path.json'
args.trained_model_state_dir = './snap/VLNBERT-train-Prevalent/state_dict/best_val_unseen'


tok = get_tokenizer(args)


features = 'img_features/ResNet-152-places365.tsv'
feat_dict = read_img_features(features, test_only=False)

# init env and eval
val_unseen_env = R2RBatch(feat_dict, batch_size=args.batchSize, splits=['val_unseen'], tokenizer=tok)
featurized_scans = set([key.split("_")[0] for key in list(feat_dict.keys())])
evaluator = Evaluation(['val_unseen'], featurized_scans, tok)

# init listner

# model.load_state_dict(state)
listner = Seq2SeqAgent(val_unseen_env, "", tok, args.maxAction)
listner.load(args.trained_model_state_dir)


listner.test(use_dropout=False, feedback='argmax', iters=None)
result = listner.get_results()
score_summary, _ = evaluator.score(result)

with open(args.result_path_file,'w') as f:
    f.write(json.dumps(result,ensure_ascii=False))

with open(args.result_file,'w') as f:
    f.write(json.dumps(score_summary,ensure_ascii=False))

error_pred_example=[]
for sample in result:
    if [v[0] for v in sample['trajectory']] != sample['trajectory_true']:
        error_pred_example.append(sample)
print(len(error_pred_example),' : ',len(result))


for sample in error_pred_example:
    # if len(sample['trajectory']) != len(sample['trajectory_true']):
    #     continue
    print(sample['instr_id'])
    print(len(sample['trajectory']),' : ',len(sample['trajectory_true']))
    print()
    print(sample['insturction'])
    if len(sample['trajectory']) == len(sample['trajectory_true']):
        for idx in range(len(sample['trajectory'])):
            print(sample['trajectory'][idx][0],' : ',sample['trajectory_true'][idx])
    else:
        for idx in range(min(len(sample['trajectory']),len(sample['trajectory_true']))):
            print(sample['trajectory'][idx][0],' : ',sample['trajectory_true'][idx])
    print()

with open(args.result_error_path_file,'w') as f:
    f.write(json.dumps(error_pred_example,ensure_ascii=False))





