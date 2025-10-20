from engine.core import sound
from engine.core.game_object import GameObject
import json
import os
from typing import List, Dict, Optional

class Scene:
    REQUIRED_CONFIGS = {
        "scripts": "scripts.json",
        "transform": "transfrom.json",
        "render": "rendrer.json",
        "main": "main.json"
    }

    def __init__(self, path: str, dirpath: str, logger):
        self.logger = logger
        self.path = path
        self.game_objects: List[GameObject] = []
        self.camera = None
        self.background_color = (255,255,255)
        self.dirpath = ""
        self._load_scene(path, dirpath)

    def _load_game_object(self, go_name: str) -> Optional['GameObjectInfo']:
        """安全加载游戏对象配置"""
        global module
        base_path = os.path.join(self.dirpath, "GameObjects_info", go_name)

        try:
            # 加载并验证所有配置文件
            configs = {
                key: self._load_single_config(base_path, filename)
                for key, filename in self.REQUIRED_CONFIGS.items()
            }

            # 检查必要配置完整性
            missing_configs = [k for k, v in configs.items() if v is None]
            if missing_configs:
                self.logger.add_log(
                    f"GameObject {go_name} 缺失配置文件: {', '.join(missing_configs)}",
                    "WARNING"
                )
                return None

            # 执行数据验证
            validated_transform = self._validate_transform(configs["transform"])
            validated_render = self._validate_render(configs["render"])
            scripts = []
            return GameObjectInfo(
                name=go_name,
                scripts=[None],
                transform=validated_transform,
                render=validated_render,
                main=configs["main"]
            )

        except Exception as e:
            self.logger.add_log(f"加载 {go_name} 失败: {str(e)}", "ERROR")
            return None

    def _load_single_config(self, base_path: str, filename: str) -> Optional[dict]:
        """安全加载单个配置文件"""
        path = os.path.join(base_path, filename)
        try:
            with open(path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            self.logger.add_log(f"配置文件缺失: {filename}", "WARNING")
            return None
        except json.JSONDecodeError as e:
            self.logger.add_log(f"配置文件 {filename} 格式错误: {str(e)}", "ERROR")
            return None
        except Exception as e:
            self.logger.add_log(f"加载 {filename} 异常: {str(e)}", "ERROR")
            return None

    def _validate_transform(self, transform: dict) -> dict:
        """Transform配置验证"""
        validated = transform.copy()
        # 位置参数
        validated.setdefault("x", 0)
        validated.setdefault("y", 0)

        # 尺寸兼容处理
        validated["width"] = validated.get("width", validated.get("w", 10))
        validated["height"] = validated.get("height", validated.get("h", 10))

        # 移除临时字段
        validated.pop("w", None)
        validated.pop("h", None)

        return validated

    def _validate_render(self, render: dict) -> dict:
        """Render配置验证"""
        validated = render.copy()
        # 颜色格式处理
        color = validated.get("color", (0, 0, 0))
        if isinstance(color, str):
            validated["color"] = self._parse_color(color)
        return validated

    def _parse_color(self, color_str: str) -> tuple:
        """将#RRGGBB字符串转换为颜色元组"""
        try:
            return (
                int(color_str[1:3], 16),
                int(color_str[3:5], 16),
                int(color_str[5:7], 16)
            )
        except:
            self.logger.add_log(f"颜色格式错误: {color_str}", "WARNING")
            return (0, 0, 0)

    def _load_scene(self, path: str, dirpath: str) -> None:
        """场景加载主流程"""
        self.game_objects.clear()
        self.dirpath = dirpath

        try:
            # 加载场景主配置
            with open(path, 'r') as file:
                scene_config = json.load(file)

            # 解析场景元数据
            self.info = SceneInfoCompat.parse(scene_config)
            self.logger.add_log(f"开始加载场景: {self.info.name}", "INFO")

            # 顺序加载游戏对象
            success_count = 0
            for go_name in self.info.game_objects_name:
                if go_info := self._load_game_object(go_name):
                    game_object = self._create_game_object(go_info)
                    if self._add_game_object_safe(game_object):
                        success_count += 1

            # 记录加载结果
            log_level = "INFO" if success_count == len(self.info.game_objects_name) else "WARNING"
            self.logger.add_log(
                f"场景加载完成: 成功加载 {success_count}/{len(self.info.game_objects_name)} 个对象",
                log_level
            )

        except json.JSONDecodeError as e:
            self.logger.add_log(f"场景配置文件格式错误: {str(e)}", "CRITICAL")
            raise
        except KeyError as e:
            self.logger.add_log(f"场景配置缺少必要字段: {str(e)}", "CRITICAL")
            raise
        except Exception as e:
            self.logger.add_log(f"场景加载未知错误: {str(e)}", "CRITICAL")
            raise

    def _create_game_object(self, go_info: 'GameObjectInfo') -> GameObject:
        """游戏对象工厂方法"""
        return GameObject(
            x=go_info.transform["x"],
            y=go_info.transform["y"],
            width=go_info.transform["width"],
            height=go_info.transform["height"],
            color=go_info.render["color"],
            scripts=go_info.scripts,
            logger=self.logger
        )

    def _add_game_object_safe(self, game_object: GameObject) -> bool:
        """安全添加游戏对象"""
        try:
            self.game_objects.append(game_object)
            game_object.start()
            self.logger.add_log(f"对象初始化成功: {game_object.name}", "DEBUG")
            return True
        except AttributeError as e:
            self.logger.add_log(f"对象属性缺失: {game_object.name} - {str(e)}", "ERROR")
        except Exception as e:
            self.logger.add_log(f"对象初始化异常: {game_object.name} - {str(e)}", "ERROR")
        return False

    def draw(self, screen) -> None:
        """增强渲染容错"""
        screen.fill(self.background_color)
        for game_object in self.game_objects:
            try:
                game_object.draw(screen)
            except Exception as e:
                self.logger.add_log(
                    f"渲染失败: {game_object.name} - {str(e)}",
                    "ERROR"
                )
                # 防止单个对象导致渲染中断
                continue

class SceneInfoCompat:
    """场景配置解析器（支持新旧格式）"""

    def __init__(self, name: str, game_objects_name: List[str]):
        self.name = name
        self.game_objects_name = game_objects_name

    @classmethod
    def parse(cls, scene_config: dict) -> 'SceneInfoCompat':
        """配置解析入口"""
        try:
            return cls(
                name=scene_config["name"],
                game_objects_name=cls._parse_game_objects(
                    scene_config.get("game_objects", [])
                )
            )
        except KeyError as e:
            raise ValueError(f"缺少必要字段: {str(e)}") from e

    @staticmethod
    def _parse_game_objects(game_objects: list) -> List[str]:
        """智能解析对象列表"""
        if not game_objects:
            return []

        first_item = game_objects[0]
        if isinstance(first_item, dict):
            return [go["name"] for go in game_objects if "name" in go]
        elif isinstance(first_item, str):
            return [go for go in game_objects if isinstance(go, str)]

        raise ValueError(f"不支持的game_objects格式: {type(first_item)}")

class GameObjectInfo:
    """强类型游戏对象配置"""

    __slots__ = ['name', 'scripts', 'transform', 'render', 'main']

    def __init__(self,
                 name: str,
                 scripts: list,
                 transform: dict,
                 render: dict,
                 main: dict):
        self.name = name
        self.scripts = scripts
        self.transform = transform
        self.render = render
        self.main = main



