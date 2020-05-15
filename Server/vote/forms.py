#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from package.form import Form, forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from .models import VoteOptions

# 单个选项最多10分，总分最多30分
SCORE_ONE_MAX = 10
SCORE_TOTAL_MAX = 30
# 最多可以选多少个选项
OPTIONS_MAX_COUNT = 5


def validate_even(value):
    # 先将原始数据以 | 作为分割符分割为一个list
    split_list = [x for x in value.split('|') if x]
    total_score = 0
    if len(split_list) > OPTIONS_MAX_COUNT:
        raise ValidationError(
            _('最多只能选择%s个选项' % OPTIONS_MAX_COUNT),
            params={'value': value},
        )

    for item in split_list:
        # 再讲数据以逗号形式分割，第一个元素是投票id，第二个元素是分数
        id_score = [y for y in item.split(',') if y]
        # 缺少一个元素则报错
        if len(id_score) < 2:
            raise ValidationError(
                _('数据格式错误'),
                params={'value': value},
            )
        id = id_score[0]
        score = id_score[1]
        if len(VoteOptions.objects.filter(id=id)) == 0:
            raise ValidationError(
                _('添加的选项不在目标列表里'),
                params={'value': value},
            )
        if int(score) > SCORE_ONE_MAX:
            raise ValidationError(
                _('单个选项最多%s分' % SCORE_ONE_MAX),
                params={'value': value},
            )
        total_score += int(score)
    if int(total_score) > SCORE_TOTAL_MAX:
        raise ValidationError(
            _('所有选项总分最多%s分' % SCORE_TOTAL_MAX),
            params={'value': value},
        )


# 添加投票选项
class AddVoteOptionForm(Form):
    option = forms.CharField(
        min_length=2,
        max_length=255,
        required=True,
        error_messages={
            'min_length': '选项描述必须在2~255字之间',
            'max_length': '选项描述必须在2~255字之间',
            'required': '选项描述必须在2~255字之间'
        }
    )
    vote_id = forms.IntegerField(
        required=True,
        help_text='问卷编号',
        error_messages={
            'required': '需要填写问卷编号'
        }
    )


# 投票
class VoteForm(Form):
    qq = forms.CharField(
        min_length=6,
        max_length=14,
        required=True,
        error_messages={
            'min_length': 'QQ号错误',
            'max_length': 'QQ号错误',
            'required': '需要填写QQ号'
        }
    )
    # 数据格式【投票选项id,分数|投票选项id,分数|投票选项id,分数】
    score = forms.CharField(max_length=255,
                            required=True,
                            validators=[
                                validate_even
                            ],
                            error_messages={
                                'max_length': '评分数据错误',
                                'required': '需要填写QQ号'
                            }
                            )
    vote_id = forms.IntegerField(
        required=True,
        help_text='问卷编号',
        error_messages={
            'required': '需要填写问卷编号'
        }
    )


# 添加投票选项
class AddVoteUserForm(Form):
    qq = forms.CharField(
        min_length=6,
        max_length=14,
        required=True,
        error_messages={
            'min_length': 'QQ号错误',
            'max_length': 'QQ号错误',
            'required': '需要填写QQ号'
        }
    )
    vote_id = forms.IntegerField(
        required=True,
        help_text='问卷编号',
        error_messages={
            'required': '需要填写问卷编号'
        }
    )
