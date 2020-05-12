import React from 'react';
import ReactDOM from 'react-dom';
import 'common/css/reset.css';
import './style.scss';
import 'antd/dist/antd.css';
import $ajax from 'api/ajax.js';
import {
    Layout, Menu,
    PageHeader,
    Breadcrumb,
    Button,
    Form,
    Input,
    List
} from 'antd';

const {Header, Content, Footer} = Layout;

// window.options = [{'id': 1, 'option': '\u5b9e\u6218\uff08\u524d\u7aef\uff09', 'score': 0, 'vote_people': 0}]

class Root extends React.Component {
    state = {
        options: window.vote_options.map(item => {
            return Object.assign({}, item, {
                myScore: 0
            }) || []
        }),

        myOption: '',
        qq: ''
    };

    render () {
        let total = 0;
        let select = 0;
        this.state.options.forEach(item => {
            total += Number(item.myScore)
            if (Number(item.myScore) > 0) {
                select += 1
            }
        })
        return <Layout>
            <Header style={{position: 'fixed', zIndex: 1, width: '100%'}}
                    id='header'>
                <Menu theme="dark"
                      mode="horizontal"
                      selectedKeys={'01'}
                      onSelect={this.onTabChange}>
                    <Menu.Item key={'01'}>投票</Menu.Item>
                </Menu>
            </Header>
            <Content className="site-layout" style={{padding: '0 50px', marginTop: 64}}>
                <Breadcrumb style={{margin: '16px 0'}}>
                </Breadcrumb>
                <div className="site-layout-background" style={{padding: 24, minHeight: 380}}>
                    <div id='order-list'>
                        <PageHeader
                            className="site-page-header"
                            title="投票"/>
                        <div className='list'>
                            <List
                                header={<div>说明：</div>}
                                itemLayout="horizontal"
                                dataSource={[
                                    '1、最多选择5项进行打分',
                                    '2、每项打分最多10分',
                                    '3、总分最多30分',
                                    '4、不打分的选项，请使用默认分数0',
                                    '5、如果需要提交自定义选项，请先增加，再打分'
                                ]}
                                renderItem={item => <List.Item>{item}</List.Item>}
                            />
                            <p>
                                当前总分：
                                <span style={{color: total > 30 ? 'red' : '#333'}}>{total}</span>
                            </p>
                            <p>
                                当前总计选择：
                                <span style={{color: select > 5 ? 'red' : '#333'}}>{select}</span> 项
                            </p>
                            <Form.Item label={'请输入你的QQ号（必填）'}
                                       rules={[{required: true}]}
                                       labelCol={{
                                           span: 4
                                       }}>
                                <Input placeholder="请输入你的QQ号"
                                       value={this.state.qq}
                                       style={{
                                           width: '200px'
                                       }}
                                       onChange={e => this.setState({
                                           qq: e.target.value
                                       })}/>
                            </Form.Item>
                            <Form>
                                {
                                    this.state.options.map((option, index) => {
                                        return <Form.Item label={option.option}
                                                          labelCol={{
                                                              span: 4
                                                          }}
                                                          key={option.id}>
                                            <Input placeholder="请输入分数"
                                                   value={option.myScore}
                                                   style={{
                                                       width: '200px'
                                                   }}
                                                   onChange={e => this.changeMyScore(e.target.value, index)}/>
                                            <span
                                                style={{marginLeft: '20px'}}>当前总分 {option.score}，投票人数 {option.vote_people}</span>
                                        </Form.Item>
                                    })
                                }
                                <Form.Item label={'添加自定义选项'}
                                           labelCol={{
                                               span: 4
                                           }}>
                                    <Input placeholder="请输入选项描述（2~20字）"
                                           value={this.state.myOption}
                                           style={{
                                               width: '200px'
                                           }}
                                           onChange={e => this.changeMyOption(e.target.value)}/>
                                    <Button type="primary"
                                            style={{marginLeft: '20px'}}
                                            onClick={this.addOption}>新增自定义选项</Button>
                                </Form.Item>
                                <Button type="primary"
                                        style={{marginLeft: '20px'}}
                                        onClick={this.vote}>提交</Button>
                            </Form>
                        </div>
                    </div>
                </div>
            </Content>
            <Footer style={{textAlign: 'center'}}>开发人：零零水（QQ：20004604，微信：qq20004604）</Footer>
        </Layout>
    }

    changeMyScore = (value, index) => {
        const list = [
            ...this.state.options.slice(0, index),
            Object.assign({}, this.state.options[index], {
                myScore: value
            }),
            ...this.state.options.slice(index + 1)
        ]
        console.log(list)
        this.setState({
            options: list
        })
    }

    changeMyOption = v => {
        this.setState({
            myOption: v
        })
    }

    addOption = () => {
        $ajax.addOption({
            option: this.state.myOption
        }).then(result => {
            console.log(result)
            if (result.code === 200) {
                window.location.reload()
            } else {
                alert(result.msg)
            }
        })
    }

    vote = () => {
        let total = 0;
        let isOverOneMax = false;

        let list = [];
        this.state.options.forEach(item => {
            // 只取其整数部分
            const s = parseInt(item.myScore)
            // 0~10，并且不能是非法数字
            if (s > 10 || Number.isNaN(s) || s < 0) {
                isOverOneMax = true
                return;
            }
            total += s
            list.push(`${item.id},${s}`)
        })
        if (isOverOneMax) {
            return alert('单项分数不能超过10分，并且只能是大于等于0的正整数整数')
        }
        if (list.length > 5) {
            return alert('最多只能选5个')
        }
        if (total > 30) {
            return alert('总分最多只能30分')
        }
        console.log(list.join('|'));

        $ajax.vote({
            qq: this.state.qq,
            score: list.join('|')
        }).then(result => {
            console.log(result)
            if (result.code === 200) {
                alert('提交成功')
            } else {
                alert(result.msg)
            }
        })
    }
}

ReactDOM.render(
    <Root/>,
    document.getElementById('root'));
