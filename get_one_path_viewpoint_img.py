'''
根据给定的path生成这个path的所有视图
'''
from pytorch_transformers import (BertConfig, BertTokenizer)
from env_wf_one_sample import R2RBatch
class onePathImg(object):
    def __init__(self,scanid, path) -> None:
        self.scanid = scanid
        self.path = path
        self.tok = BertTokenizer.from_pretrained('./bert-base-uncased')
        self.env = R2RBatch(feature_store=None, splits=['val_unseen'], batch_size=1, tokenizer=self.tok)
        self.episode_len = len(self.path)
        self.env_actions = {
            'left': ([0],[-1], [0]), # left
            'right': ([0], [1], [0]), # right
            'up': ([0], [0], [1]), # up
            'down': ([0], [0],[-1]), # down
            'forward': ([1], [0], [0]), # forward
            '<end>': ([0], [0], [0]), # <end>
            '<start>': ([0], [0], [0]), # <start>
            '<ignore>': ([0], [0], [0])  # <ignore>
        }
    
    def make_equiv_action(self, a_t, ob, traj=None):
        """
        Interface between Panoramic view and Egocentric view
        It will convert the action panoramic view action a_t to equivalent egocentric view actions for the simulator
        """
        def take_action(idx, name):
            if type(name) is int:       # Go to the next view
                self.env.env.sims[idx].makeAction([name], [0], [0])
            else:                       # Adjust
                self.env.env.sims[idx].makeAction(*[x for x in self.env_actions[name]])

        action = a_t
        cur_action_lis = []
        if action != -1:
            select_candidate = ob['candidate'][action]
            src_point = ob['viewIndex']
            trg_point = select_candidate['pointId']
            src_level = (src_point ) // 12  # The point idx started from 0
            trg_level = (trg_point ) // 12
            while src_level < trg_level:    # Tune up
                take_action(0, 'up')
                src_level += 1
                cur_action_lis.append('up')
            while src_level > trg_level:    # Tune down
                take_action(0, 'down')
                src_level -= 1
                cur_action_lis.append('down')
            while self.env.env.sims[0].getState()[0].viewIndex != trg_point:    # Turn right until the target
                take_action(0, 'right')
                cur_action_lis.append('right')
            assert select_candidate['viewpointId'] == \
                    self.env.env.sims[0].getState()[0].navigableLocations[select_candidate['idx']].viewpointId
            # exit()
            take_action(0, select_candidate['idx'])

        state = self.env.env.sims[0].getState()[0]

        if traj is not None:
            traj['path'].append((state.location.viewpointId, state.heading, state.elevation))
            traj['decisions'].append(cur_action_lis)


    def _teacher_action(self, ob, ended, traj=None):
        """
        Extract teacher actions into variable.
        :param obs: The observation.
        :param ended: Whether the action seq is ended
        :return:
        """
        a = 0
        if ended:
            a = -100
        else:
            for k, candidate in enumerate(ob['candidate']):
                if candidate['viewpointId'] == ob['teacher']:   # Next view point
                    a = k
                    cur_heading = candidate['heading']
                    break
            else:   # Stop here
                assert ob['teacher'] == ob['viewpoint']         # The teacher action should be "STAY HERE"
                cur_heading = candidate['heading']
                a = len(ob['candidate'])
        if traj is not None:
            traj['gold_heading_lis'].append(cur_heading)
        return a
    def rollPath(self):
        ob=self.env.reset()[0]
        
        traj = {
            'scan_id' : ob['scan'],
            'instr_id': ob['instr_id'],
            'instruction': ob['instructions'],
            'gt_path' : ob['gt_path'],
            'path': [(ob['viewpoint'], ob['heading'], ob['elevation'])],
            'decisions' : [],
            'gold_heading_lis' : [ob['heading']]
        }

        ended = False
        for t in range(self.episode_len):
            target = self._teacher_action(ob, ended, traj)
            if ended or target==len(ob['candidate']):
                break
            self.make_equiv_action(target, ob, traj)
            ob = self.env._get_obs()[0]
            if target == -1:
                ended = True
            
        return traj
    
curscan = 'QUCTc6BB5sX'
curp = ["bff5229aad06472f95d480577eb26d1d", "b882d05cc8d842879c647824f537a17c", "5b0d8b21eb2c4b98a576235617e3ce43", \
        "2be6e0ba13644a8a8b472c7a9278e237", "94a1b7b629e74ddb9b0ecd4ae15edb67", "fdfdc7cadd8a4ecb9718c124526b14f8"]
Engine=onePathImg(scanid=curscan,path=curp)

traj = Engine.rollPath()

print('heading list',[headc[1] for headc in traj['path']])


    
