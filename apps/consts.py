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


class SourceType(TextChoices):
    ISSUES = "issues", "动态消息"
    USER = "user", "用户私信"
    SHOP = "shop", "商城消息"
    SYSTEM = "system", "系统消息"
    COMMENT = "comment", "评论消息"
    THUMB_UP = "thumbs_up", "点赞消息"


class PaymentType(TextChoices):
    WEIXIN = "weixin", "微信支付"
    ALIPAY = "alipay", "支付宝"
    UNION_PAY = "union_pay", "银联支付"


class UpgradeUserLevelMethod(TextChoices):
    ISSUES = "发布动态", "发布动态"
    COMMENT = "评论", "评论"
    THUMBS_UP = "点赞", "点赞"
    ART = "发表作品", "发表作品"
    BE_COMMENTED = "被评论", "被评论"
    BE_THUMBS_UP = "被点赞", "被点赞"
