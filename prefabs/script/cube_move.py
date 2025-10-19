import math

class PrefabScript():
    def __init__(self, sdk):
        self.engine = sdk

    def interpolate_to(self, current, target, delta_time, interp_speed):
        if interp_speed <= 0:
            return target

        delta = target - current
        # 根据步长动态调整容差
        step_scale = min(interp_speed * delta_time, 1)
        effective_tolerance = max(1e-3, abs(delta * step_scale))
        if math.isclose(delta, 0, abs_tol=effective_tolerance):
            return target
        return current + delta * step_scale

    def start(self):
        self.target = self.engine.scene.game_objects[1]
        self.initial_y = self.target.rect.y  # 保存初始Y坐标
        self.target_y = self.initial_y - 50  # 设置固定目标位置
        self.engine.engine.log.add_log("CubeMove script started", "INFO")

    def update(self):
        delta_time = 0.0167
        current_y = self.target.rect.y
        new_y = self.interpolate_to(current_y, self.target_y, delta_time, 5)
        # 调试日志
        print(f"Current: {current_y:.6f}, Target: {self.target_y}, Delta: {self.target_y - current_y:.6f}")
        self.target.rect.y = new_y
