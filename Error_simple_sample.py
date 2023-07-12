import json
import sys
import os

# error_predict_sample=[]

# with open('/home/zhhz/sxu/fw_project/VLN_bert/result/wf_test_one_sample_predict_error_path.json','r') as f:
#     error_predict_sample = json.load(f)

with open('./result/wf_test_all_sample_VLN_bert_predict_error_path.json','r') as f:
    error_predict_sample = json.load(f)

# reach_num = 0
# for sample in error_predict_sample:
#     pred_traj = [v[0] for v in sample['trajectory']]
#     if pred_traj[-1] == sample['trajectory_true'][-1]:
#         reach_num+=1
# print(reach_num*1.0/len(error_predict_sample))

# last_step_error_num = 0
# for sample in error_predict_sample:
#     if len(sample['trajectory']) == len(sample['trajectory_true']):
#         pred_traj = [v[0] for v in sample['trajectory']]
#         if pred_traj[:-1] != sample['trajectory_true'][:-1] and pred_traj[-1] == sample['trajectory_true'][-1]:
#             last_step_error_num+=1
#     else:
#         pred_traj = [v[0] for v in sample['trajectory']]
#         if pred_traj[-1] == sample['trajectory_true'][-1]:
#             last_step_error_num+=1
# print(last_step_error_num*1.0/len(error_predict_sample))


error360EnvPath = './ErrorAnalysis/VLN_Bert/UnseenExample'

# print(len(error_predict_sample))
# exit()
for sample in error_predict_sample[20:30]:
    # if len(sample['trajectory']) != len(sample['trajectory_true']):
    #     continue
    # if sample['scan_id'] == '2azQ1b91cZZ' and sample['instr_id'] == '6822_2':

    #     print(sample['instr_id'])
    #     print(sample['scan_id'])
    #     # exit()
    #     print(sample['insturction'])
    #     print(len(sample['trajectory']),' : ',len(sample['trajectory_true']))
    #     print()
    #     if len(sample['trajectory']) == len(sample['trajectory_true']):
            
    #         for idx in range(len(sample['trajectory'])):
    #             print(sample['trajectory'][idx][0],' : ',sample['trajectory_true'][idx])
    #     else:
    #         for idx in range(min(len(sample['trajectory']),len(sample['trajectory_true']))):
    #             print(sample['trajectory'][idx][0],' : ',sample['trajectory_true'][idx])
    #     print()
    #     break

    print(sample['instr_id'])
    print(sample['scan_id'])
    # exit()
    print(sample['insturction'])
    print(len(sample['trajectory']),' : ',len(sample['trajectory_true']))
    print()
    if len(sample['trajectory']) == len(sample['trajectory_true']):
        
        for idx in range(len(sample['trajectory'])):
            print(sample['trajectory'][idx][0],' : ',sample['trajectory_true'][idx])
    else:
        for idx in range(min(len(sample['trajectory']),len(sample['trajectory_true']))):
            print(sample['trajectory'][idx][0],' : ',sample['trajectory_true'][idx])
    print()

# with open('/home/zhhz/sxu/fw_project/VLN_bert/result/wf_test_predict_path.json','r') as f:
#     predict_sample = json.load(f)

# long_path_num, short_path_num, err_equal_path_num = 0, 0, 0
# right_equal_path_num = 0
# for sample in predict_sample:
#     if len(sample['trajectory']) > len(sample['trajectory_true']):
#         long_path_num+=1
#     elif len(sample['trajectory']) < len(sample['trajectory_true']):
#         short_path_num+=1
#     elif len(sample['trajectory']) == len(sample['trajectory_true']) and [v[0] for v in sample['trajectory']] != sample['trajectory_true']:
#         err_equal_path_num+=1
#     elif len(sample['trajectory']) == len(sample['trajectory_true']) and [v[0] for v in sample['trajectory']] == sample['trajectory_true']:
#         right_equal_path_num+=1

# print(long_path_num*1.0/len(predict_sample))
# print(short_path_num*1.0/len(predict_sample))
# print(err_equal_path_num*1.0/len(predict_sample))
# print(right_equal_path_num*1.0/len(predict_sample))
# print(len(predict_sample))
    