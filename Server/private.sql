-- 执行这行语句的时候，用root账号执行。意思是创建一个用户，允许他在任何ip访问 simple_vote 这个数据库，密码是后面BY里面的
create schema if not exists simple_vote collate utf8mb4_general_ci;
GRANT ALL ON simple_vote.* to vote_user@'%' IDENTIFIED BY 'fg42fgvfgt2435!yt5t1f2f_12329';
FLUSH PRIVILEGES;
