import json
from django.shortcuts import render
from django.http import HttpResponse
from package.response_data import get_res_json
from .models import User, VoteOptions
from .forms import AddVoteOptionForm, VoteForm
from bulk_update.helper import bulk_update


# Create your views here.
def index(request):
    list = VoteOptions.objects.all()
    result = [
        {
            'id': item.id,
            'option': item.option,
            'score': item.score,
            'vote_people': item.vote_people
        } for item in list
    ]
    return render(request, 'homepage.html', {
        'vote_options': json.dumps(result)
    })


# 添加选项
def vote_add_option(request):
    # 加载数据
    post_data = json.loads(request.body)
    # 表单校验
    uf = AddVoteOptionForm(post_data)
    # 数据是否合法
    if uf.is_valid() is False:
        # 返回错误信息
        return get_res_json(code=0, msg=uf.get_form_error_msg())

    option = uf.data['option']
    data = VoteOptions.objects.create(
        option=option
    )
    data.save()

    return get_res_json(code=200, msg='添加成功')


# 投票
def vote(request):
    # 加载数据
    post_data = json.loads(request.body)
    # 表单校验
    uf = VoteForm(post_data)
    # 数据是否合法
    if uf.is_valid() is False:
        # 返回错误信息
        return get_res_json(code=0, msg=uf.get_form_error_msg())
    # 拿到数据
    qq = uf.data['qq']
    score = uf.data['score']
    # 获取当前用户
    user = User.objects.filter(qq=qq)
    if len(user) == 0:
        return get_res_json(code=0, msg='该用户不存在')
    user = user[0]
    if user.has_voted == '1':
        return get_res_json(code=0, msg='你已经投过票了')

    # 拆分
    split_list = [x for x in score.split('|') if x]

    # 获取投票选项
    vote_options = VoteOptions.objects.all()

    for item in split_list:
        # 再讲数据以逗号形式分割，第一个元素是投票id，第二个元素是分数
        id_score = [y for y in item.split(',') if y]
        # 分别拿到选项id和评分
        id = int(id_score[0])
        s = int(id_score[1])
        # 更新数据
        one = vote_options.filter(id=id)[0]
        one.score = one.score + s
        one.vote_people = one.vote_people + 1
        one.save()

    # 数据全部更新完毕
    # bulk_update(vote_options)

    # 更新数据
    user.vote(score)
    user.save()

    return get_res_json(code=200, msg='投票成功')
