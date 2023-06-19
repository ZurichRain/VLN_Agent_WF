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

for sample in error_predict_sample:
    # if len(sample['trajectory']) != len(sample['trajectory_true']):
    #     continue
    print(sample['instr_id'])
    print(sample['scan_id'])
    scan_path = error360EnvPath+'/'+ sample['scan_id']
    if not os.path.isdir(scan_path):
        os.makedirs(scan_path)
        # os.makedirs(scan_path+'/Pred')
        # os.makedirs(scan_path+'/Gold')

    if not os.path.isdir(scan_path+'/'+sample['instr_id']):
        os.makedirs(scan_path+'/'+sample['instr_id'])
        os.makedirs(scan_path+'/'+sample['instr_id']+'/Pred')
        for viewpoint in sample['trajectory']:
            if not os.path.isdir(scan_path+'/'+sample['instr_id']+'/Pred/'+viewpoint[0]):
                os.makedirs(scan_path+'/'+sample['instr_id']+'/Pred/'+viewpoint[0])
                
        os.makedirs(scan_path+'/'+sample['instr_id']+'/Gold')
        for viewpoint in sample['trajectory_true']:
            if not os.path.isdir(scan_path+'/'+sample['instr_id']+'/Gold/'+viewpoint):
                os.makedirs(scan_path+'/'+sample['instr_id']+'/Gold/'+viewpoint)
                
    MetaFile = scan_path+'/'+sample['instr_id']+'/meta.json'
    with open(MetaFile,'w') as f:
        f.write(json.dumps(sample,ensure_ascii=False))
    for viewpoint in sample['trajectory']:
        status = os.system(f"bash ./get_one_scan_path_360images.sh {sample['scan_id']} \
                                    {sample['instr_id']} {viewpoint[0]} pred")
    for viewpoint in sample['trajectory_true']:
        status = os.system(f"bash ./get_one_scan_path_360images.sh {sample['scan_id']} \
                                   {sample['instr_id']} {viewpoint} gold")
    # exit()
    # print(len(sample['trajectory']),' : ',len(sample['trajectory_true']))
    # print()
    # if len(sample['trajectory']) == len(sample['trajectory_true']):
    #     print(sample['insturction'])
    #     for idx in range(len(sample['trajectory'])):
    #         print(sample['trajectory'][idx][0],' : ',sample['trajectory_true'][idx])
    # else:
    #     for idx in range(min(len(sample['trajectory']),len(sample['trajectory_true']))):
    #         print(sample['trajectory'][idx][0],' : ',sample['trajectory_true'][idx])
    # print()
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
    