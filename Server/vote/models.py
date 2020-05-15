from django.db import models

# Create your models here.
"""
id：默认id
vote：消息内容
action：行为类型，group（群消息），private（私聊）
target_id：群消息为群id，私聊为目标qq号
next_time：下次发送消息时间，这个不直接
"""


# 用户
class User(models.Model):
    qq = models.CharField(
        max_length=14,
        help_text='qq'
    )
    has_voted = models.CharField(
        max_length=1,
        default='0',
        help_text='是否已投票，0未投，1已投'
    )
    vote_action = models.CharField(
        max_length=255,
        help_text='投票行为，数据格式为【投票选项id,分数|投票选项id,分数|投票选项id,分数】这样'
    )
    vote_id = models.IntegerField(
        default=0,
        help_text='问卷编号'
    )

    def vote(self, action):
        self.has_voted = '1'
        self.vote_action = action


# 投票选项
class VoteOptions(models.Model):
    option = models.CharField(
        max_length=255,
        help_text='选项文字内容'
    )
    score = models.IntegerField(
        default=0,
        help_text='投票总分数'
    )
    vote_people = models.IntegerField(
        default=0,
        help_text='投票人数'
    )
    vote_id = models.IntegerField(
        default=0,
        help_text='问卷编号'
    )
