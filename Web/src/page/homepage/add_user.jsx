/**
 * Created by 王冬 on 2020/5/15.
 * QQ: 20004604
 * weChat: qq20004604
 * 功能说明：
 *
 */
import React, {useState} from 'react';
import $ajax from 'api/ajax.js';
import {
    Button,
    Input,
    notification
} from 'antd';

function AddUser (props) {
    const {voteId} = props;
    const [qq, setQQ] = useState('');

    const addUser = function () {
        $ajax.addUser({
            qq,
            vote_id: voteId
        }).then(result => {
            console.log(result)
            if (result.code === 200) {
                setQQ('');
                notification.success({
                    message: result.msg
                })
            } else {
                alert(result.msg)
            }
        })
    }

    return <p>
        QQ：<Input placeholder="请输入你的QQ号"
                  value={qq}
                  style={{
                      width: '200px'
                  }}
                  onChange={e => setQQ(e.target.value)}/>
        <Button type='primary' onClick={addUser}>添加</Button>
    </p>
}

export default AddUser
