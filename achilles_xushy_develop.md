# 对比CDN或者CDS媒资信息

## 2017-11-07 扫描甘肃分平台的媒资信息
    1. python get_dir_all_file_list.py, 服务器配置信息在parameters_json.json
    2. get_dir_all_file_list.py --get_cmd_str 添加挂在硬盘功能
    3. 更新字符串解析函数，获取日期与文件名采用正则表达式
    
## 2017-11-08 扫描甘肃分平台的媒资信息 与总平台对比
    1. 输出码率超过五种，或者ifo超过五种的，或者ifo个数与ts不匹配的
    2. 只对比含有国网字样的ts文件以及ifo文件
  
## 2017-11-09 扫描甘肃分平台的媒资信息 与总平台对比 
    1. 完成 main_ssh_loop_compare.py 直接运行，运算时间比较长
    2. 对比总平台与甘肃平台的目录get_parent_child_more_dir.py