import json
import sys
import os

'''
    实现给定
    scan_id = '2azQ1b91cZZ'
    instr_id = '6822_2'
    viewpointid = '1320ad480d434d1d8d6d7304dc5f7854'
    生成对应的一个样本的预测和真实的图片
'''

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

scan_id = 'QUCTc6BB5sX'
instr_id = '5820_0'
# viewpointid = '1320ad480d434d1d8d6d7304dc5f7854'

sample = None 

for curs in error_predict_sample:
    if curs['scan_id'] == scan_id and curs['instr_id'] == instr_id:
        sample = curs
        break

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

pred_heading_lis = [curs[1] for curs in sample['trajectory']]
gold_heading_lis = sample['gold_heading_lis'][1:]


for idx, viewpoint in enumerate(sample['trajectory']):
    # status = os.system(f"bash ./get_one_scan_path_360images.sh {sample['scan_id']} \
    #                             {sample['instr_id']} {viewpoint[0]} pred {[pred_heading_lis[idx]]}")
    status = os.system(f"bash ./get_one_scan_path_360images.sh {sample['scan_id']} \
                                {sample['instr_id']} {viewpoint[0]} pred 0,1,2,3,4,5 stand_heading")
    status = os.system(f"bash ./get_one_scan_path_360images.sh {sample['scan_id']} \
                                {sample['instr_id']} {viewpoint[0]} pred {str([pred_heading_lis[idx]])} nostand_heading")
for idx,viewpoint in enumerate(sample['trajectory_true']):
    status = os.system(f"bash ./get_one_scan_path_360images.sh {sample['scan_id']} \
                                {sample['instr_id']} {viewpoint} gold 0,1,2,3,4,5 stand_heading")
    status = os.system(f"bash ./get_one_scan_path_360images.sh {sample['scan_id']} \
                                {sample['instr_id']} {viewpoint} gold {str([gold_heading_lis[idx]])} nostand_heading")
    