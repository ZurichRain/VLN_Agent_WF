'''
实现 给定一个句子输出mask object之后的句子
'''
import numpy as np

class MaskSentence(object):
    def __init__(self,args,env,tokenizer) -> None:
        self.env = env 
        self.args = args
        self.tokenizer = tokenizer
        self.get_all_env_instruct_object()
    def get_one_mask_senctence(self,sen):
        sen_tok = self.tokenizer.token()
       
    def get_all_env_instruct_object(self,**kwargs):
        '''
            using inference stage method
        '''
        
        while True:
            obs = np.array(self.env.reset())
            if(obs[0].get('obj_idx')):
                break
            batch_instruct = [{
                    'scan_id' : ob['scan'],
                    'instr_id': ob['instr_id'],
                    'instruction': ob['instructions'],
                    'gt_path' : ob['gt_path'],
                    'path': [(ob['viewpoint'], ob['heading'], ob['elevation'])],
                    'decisions' : []
                } for ob in obs]
            obj_idx =  self.find_obj_in_one_sentence(batch_instruct)
            for example in batch_instruct:
                for envExample in self.env.data:
                    if envExample['scan'] == example['scan_id'] and envExample['instr_id'] == example['instr_id']:
                        envExample['obj_idx']=example['obj_idx']
    
    def find_obj_in_one_sentence(self,batch_instruct):
        obj_idx = [[] for _ in range(len(batch_instruct))]
        # 使用某个模型获得某个object在文本中的位置
        
        return obj_idx
            

        