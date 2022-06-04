from django.db.models import TextChoices


class UserGender(TextChoices):
    """
    用户性别
    """
    MALE = "male", "男性"
    FEMALE = "female", "女性"


class PublishStatus(TextChoices):
    """
    发布状态
    """
    DRAFT = "draft", "草稿"  # 草稿
    PUBLISHED = "published", "发布"  # 发布
    ABANDONED = "abandoned", "废弃"  # 废弃


class FileType(TextChoices):
    """
    文件类型
    """
    NONE = "", "无类型"
    VIDEO = "video", "视频"
    IMAGE = "image", "图像"
    AUDIO = "audio", "音频"
    OTHER = "other", "其他"
