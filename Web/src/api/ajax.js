/**
 * Created by 王冬 on 2019/5/23.
 * QQ: 20004604
 * weChat: qq20004604
 * 功能说明：
 *
 */
import {get, post} from '../config/http';

const $ajax = {
    addOption (payload) {
        return post('/vote_add_option/', payload);
    },
    addUser (payload) {
        return post('/add_user/', payload);
    },
    vote (payload) {
        return post('/vote/', payload);
    }
};

export default $ajax;
