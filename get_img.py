import os
import sys
import MatterSim
import math
import numpy as np
import cv2


WIDTH = 640
HEIGHT = 480
VFOV = math.radians(60)
HFOV = VFOV*WIDTH/HEIGHT
TEXT_COLOR = [230, 40, 40]

def get_image_each_viewpoint(vid,scanid,instr_id,viewpointid,mod):
    sim = MatterSim.Simulator()
    # sim.setRenderingEnabled(True)
    sim.setDiscretizedViewingAngles(True)   # Set increment/decrement to 30 degree. (otherwise by radians)

    # sim.setCameraResolution(640, 480)
    # sim.setPreloadingEnabled(True)
    sim.setDepthEnabled(False)
    sim.setCameraResolution(WIDTH, HEIGHT)
    sim.setCameraVFOV(math.radians(60))
    # sim.setDepthEnabled(False) # Turn on depth only after running ./scripts/depth_to_skybox.py (see README.md)
    sim.initialize()
    #sim.newEpisode(['2t7WUuJeko7'], ['1e6b606b44df4a6086c0f97e826d4d15'], [0], [0])
    sim.newEpisode([scanid], [viewpointid], [vid], [0])
    # sim.newRandomEpisode(['1LXtFkjw3qL'])
    # sim.makeAction([0], [0], [0])
    state = sim.getState()[0]
    locations = state.navigableLocations
    # print(locations)
    rgb = np.array(state.rgb, copy=False)
    for idx, loc in enumerate(locations[1:]):
        # Draw actions on the screen
        fontScale = 3.0/loc.rel_distance
        x = int(WIDTH/2 + loc.rel_heading/HFOV*WIDTH)
        y = int(HEIGHT/2 - loc.rel_elevation/VFOV*HEIGHT)
        cv2.putText(rgb, str(idx + 1), (x, y), cv2.FONT_HERSHEY_SIMPLEX, 
            fontScale, TEXT_COLOR, thickness=3)
        
    # print(rgb.shape)
    if mod == 'pred':
        viewdir = './ErrorAnalysis/VLN_Bert/UnseenExample/' + scanid + '/' + instr_id + '/Pred/' + viewpointid
    elif mod == 'gold':
        viewdir = './ErrorAnalysis/VLN_Bert/UnseenExample/' + scanid + '/' + instr_id + '/Gold/' + viewpointid
    else:
        raise ValueError("mod 必须是 pred 或者 gold, 你输入了非法的mod字段")

    if not os.path.isdir(viewdir):
        os.makedirs(viewdir)
    if vid<0:
        cv2.imwrite(f'{viewdir}/_{abs(vid)}.jpg', rgb)
    else:
        cv2.imwrite(f'{viewdir}/{vid}.jpg', rgb)
    return rgb
    


def get_image_each_viewpoint_1(vid,scanid,viewpointid):
    sim = MatterSim.Simulator()
    sim.setCameraResolution(WIDTH, HEIGHT)
    sim.setCameraVFOV(VFOV)
    sim.setDepthEnabled(False) # Turn on depth only after running ./scripts/depth_to_skybox.py (see README.md)
    sim.initialize()
    #sim.newEpisode(['2t7WUuJeko7'], ['1e6b606b44df4a6086c0f97e826d4d15'], [0], [0])
    # sim.newEpisode(['1LXtFkjw3qL'], ['0b22fa63d0f54a529c525afbf2e8bb25'], [0], [0])
    sim.newRandomEpisode(['1LXtFkjw3qL'])
    sim.makeAction([0], [0], [0])
    state = sim.getState()[0]
    locations = state.navigableLocations
    rgb = np.array(state.rgb, copy=False)
    for idx, loc in enumerate(locations[1:]):
        # Draw actions on the screen
        fontScale = 3.0/loc.rel_distance
        x = int(WIDTH/2 + loc.rel_heading/HFOV*WIDTH)
        y = int(HEIGHT/2 - loc.rel_elevation/VFOV*HEIGHT)
        cv2.putText(rgb, str(idx + 1), (x, y), cv2.FONT_HERSHEY_SIMPLEX, 
            fontScale, TEXT_COLOR, thickness=3)
    cv2.imwrite('2.jpg', rgb)



# print()
if __name__ == '__main__':
    scanid = sys.argv[1]
    instr_id = sys.argv[2]
    viewpointid = sys.argv[3]
    mod = sys.argv[4]
    print(scanid)
    print(instr_id)
    print(viewpointid)
    print(mod)
    # vidlis = [0,1,2,3,4,5]
    vidlis = eval(sys.argv[5])
    # print(vidlis)
    is_stand_heading = sys.argv[6] == 'stand_heading'
    # vidlis = [2.0943951023931953]
    viewlis = []
    if len(vidlis)>=2 and vidlis[1]==',':
        vidlis = [int(vid) for vid in vidlis.split(',')]
    for vid in vidlis:
        curview=get_image_each_viewpoint(vid, scanid, instr_id, viewpointid, mod)
        viewlis.append(curview)
        if vid != vidlis[-1]:
            bar = np.zeros((curview.shape[0],20,curview.shape[2]))
            for Xidx in range(len(bar)):
                for Yidx in range(20):
                    bar[Xidx][Yidx][1] = 255
            viewlis.append(bar)

    if is_stand_heading:
        if mod == 'pred':
            viewdir = './ErrorAnalysis/VLN_Bert/UnseenExample/' + scanid + '/' + instr_id + '/Pred/' + viewpointid
        elif mod == 'gold':
            viewdir = './ErrorAnalysis/VLN_Bert/UnseenExample/' + scanid + '/' + instr_id + '/Gold/' + viewpointid
        else:
            raise ValueError("mod 必须是 pred 或者 gold, 你输入了非法的mod字段")

        if not os.path.isdir(viewdir):
            os.makedirs(viewdir)
        cv2.imwrite(f'{viewdir}/overview.jpg', np.hstack(viewlis))