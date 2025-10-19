import math

# 基础数值插值（模仿UE4的FInterpTo）
class Math:
    def interpolate_to(self,current, target, delta_time, interp_speed):
        if interp_speed <= 0:
            return target

        delta = target - current
        if math.isclose(delta, 0, abs_tol=1e-6):
            return target

        # 计算最大可移动步长（防止超调）
        step_scale = min(interp_speed * delta_time, 1)
        return current + delta * step_scale

    # 矢量插值（处理X/Y/Z分量）
    def vector_interpolate_to(self,current, target, delta_time, interp_speed):
        return tuple(
            self.interpolate_to(c, t, delta_time, interp_speed)
            for c, t in zip(current, target)
        )


