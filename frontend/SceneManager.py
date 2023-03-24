from frontend.TitleScene import TitleScene

class SceneMananger():
    def __init__(self):
        self.go_to(TitleScene())

    def go_to(self, scene):
        self.scene = scene
        self.scene.manager = self
