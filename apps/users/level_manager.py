"""
统一管理经验的处理
"""
from apps.users.model2 import UserProfile
from exceptions.custom_excptions.level_error import LevelError
from exceptions.custom_excptions.user_error import UserError
from utils.base_tools import Singleton


@Singleton
class LevelManager:

    def get_user_level(self, user_id):
        pass

    def get_user_exp(self, user_id):
        pass

    def inc_level(self, user_profile: UserProfile, add_exp: float, next_exp: float):
        """
        升级

        1、升级之前要判断：
            1、是否经验已经达到了；2、是否已经到顶级
        2、升级后，经验值需要归零
        """
        user_profile.user_level += 1
        user_profile.has_exp = add_exp - next_exp
        user_profile.save()

    def inc_exp(self, user_id, operator: str):
        """
        增加经验
        """
        user_profile = UserProfile.logic_objects.filter(user__id=user_id).first()
        if not user_profile:
            raise UserError.ErrProfileNoExist
        upgrade_methods = {um.upgrade_name: um for um in user_profile.level_group.upgrade_method.all()}
        if operator not in upgrade_methods:
            err = LevelError.ErrWrongOperator
            err.set_message(f"操作{operator}错误，不在规定的操作中，{upgrade_methods.keys()}")
            raise err
        um = upgrade_methods[operator]
        # 获得的经验
        exp = um.base_exp_value
        # 目前的等级
        # user_level = user_profile.user_level
        # 在目前的等级已经拥有的经验
        has_exp = user_profile.has_exp
        # 增加后的经验
        add_exp = has_exp + exp
        levels = {level.level: level for level in um.levels.all()}
        next_level = None
        if user_profile.user_level == 0:
            next_level = levels[1]  # 如果用户是0级，则下一极就是1极
        elif user_profile.user_level == len(levels):
            # 如果是最大级，那么就不需要再升级了
            return
        else:
            for level in um.levels.all():
                if level.level == user_profile.user_level:
                    next_level = level.next_level
                    break
            if not next_level:
                raise LevelError.ErrWrongUserLevel
        next_exp = next_level.base_upgrade_exp  # 要升级到这个level所需要的经验
        if add_exp >= next_exp:
            # 升级
            self.inc_level(user_profile, add_exp, next_exp)
        else:
            user_profile.has_exp = add_exp
            user_profile.save()
