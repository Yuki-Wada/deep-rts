from DeepRTS import Engine
from DeepRTS import util
from DeepRTS import GUI
import os
import numpy as np
import shutil
import random

dir_path = os.path.dirname(os.path.realpath(__file__))


class DeepRTSGame(Engine.Game):

    @staticmethod
    def setup_data_files():
        template_data = os.path.join(os.getcwd(), "..", "assets")  # TODO getcwd
        target_data = os.path.join(os.getcwd(), "assets")
        util.copytree(template_data, target_data, ignore=shutil.ignore_patterns('config.json'))

    def __init__(self, map_name, n_players=2, config=None, tile_size=32):
        DeepRTSGame.setup_data_files()
        if not config:
            super(DeepRTSGame, self).__init__(map_name)
        else:
            super(DeepRTSGame, self).__init__(map_name, config)

        # Create players
        for i in range(n_players):
            self.add_player()

        # Select first player as default
        self.set_player(self.players[0])

        self.gui = GUI(self, tile_size=tile_size)
        self._render_every = 1
        self._view_every = 1
        self._capture_every = 1

    def sample_action(self):
        return random.randint(Engine.Constants.action_min, Engine.Constants.action_max)

    def render_every(self, interval):
        self._render_every = interval

    def tick(self):
        super().tick()

    def _render(self):
        if self.get_ticks() % self._render_every == 0:
            self.gui.render()

    def view(self):
        if self.get_ticks() % self._view_every == 0:
            self.gui.view()

    def capture(self):
        if self.get_ticks() % self._capture_every == 0:
            return self.gui.capture()
        return None

    def set_player(self, player):
        self.set_selected_player(player)

    def get_state(self, image=False, copy=False):
        return self.gui.capture() if image else np.array(self.state, copy=copy)

    def view_every(self, n):
        self._view_every = n

    def capture_every(self, n):
        self._capture_every = n

    def _caption(self):
        pass
        """self.gui.set_caption("DeepRTS v2.0 - [FPS=%d UPS=%d MUL=x%d]" %
                             (
                                 self.get_fps(),
                                 self.get_ups(),
                                 self.get_ups() / self.get_ticks_modifier()
                             ))"""

    def _on_unit_create(self, unit):
        pass

    def _on_unit_destroy(self, unit):
        pass

    def _on_episode_start(self):
        for tile in self.tilemap.tiles:
            self.gui.gui_tiles.set_tile(tile.x, tile.y, tile.get_type_id())

    def _on_episode_end(self):
        pass

    def _on_tile_deplete(self, tile):
        self.gui.gui_tiles.set_tile(tile.x, tile.y, tile.get_type_id())




