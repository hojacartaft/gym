import numpy as np
from gym import utils
from gym.envs.mujoco import mujoco_env

class HalfCheetahEnv(mujoco_env.MujocoEnv, utils.EzPickle):
    def __init__(self):
        mujoco_env.MujocoEnv.__init__(self, 'half_cheetah.xml', 5)
        utils.EzPickle.__init__(self)
        self.finalize()

    def _step(self, action):
        xposbefore = self.model.data.qpos[0,0]
        self.do_simulation(action, self.frame_skip)
        xposafter = self.model.data.qpos[0,0]
        ob = self._get_obs()
        reward_ctrl = - 0.1 * np.square(action).sum()
        reward_run = (xposafter - xposbefore)/self.dt
        reward = reward_ctrl + reward_run
        done = False
        return ob, reward, done, dict(reward_run = reward_run, reward_ctrl=reward_ctrl)

    def _get_obs(self):
        return np.concatenate([
            self.model.data.qpos.flat[1:],
            self.model.data.qvel.flat,
        ])

    def _reset(self):
        self.model.data.qpos = self.init_qpos + np.random.uniform(size=(self.model.nq,1),low=-.1,high=.1)
        self.model.data.qvel = self.init_qvel + np.random.randn(self.model.nv,1)*.1
        self.reset_viewer_if_necessary()        
        return self._get_obs()

    def viewer_setup(self):
        self.viewer.cam.distance = self.model.stat.extent * 0.5
