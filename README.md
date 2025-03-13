# Abnormal_data_detection

## 一、异常检测-打分过滤

### Step 0:

+ 在config中修改测试数据集的qa的input key，比如data/test_350_dep.json中提供的question是"problem"对应的内容, answer对应的是"solution"和"answer"中的内容，对应的config修改为:CONTENT_FIELD_NAME = ["problem", "solution", "answer"]


### Step 1：

```

cd prompt_quality_evaluatio/

python eval.py --api_key 1 --api_url http://127.0.0.1:18000/v1 --data_path ../data/test_350_score.json --save_abnormal_data_path ./0.json --save_new_data_path ./1.json

## 参数解释：
api_key：符合openai接口openai的api key
api_url：符合openai接口的api url
data_path：需要检测的数据集路径
save_abnormal_data_path：异常的数据集保存路径，自定义
save_new_data_path：正常的数据集路径，自定义
```

## 二、异常检测-去重过滤

### Step 0:

+ 在config中修改测试数据集的qa的input key，比如data/test_350_score.json中提供的question是"problem"对应的内容, answer对应的是"solution"和"answer"中的内容，对应的config修改为:QUESTIONS = ["problem"] ANSWER = ["solution", "answer"]

### Step 1:
```
cd deduplication/

python eval.py --file_path ../data/test_350_dep.json --save_dep_path ./0.json --save_data_path ./1.json


## 参数解释：

file_path：需要检测的数据集路径
save_dep_path：异常的数据集保存路径，自定义
save_data_path：正常的数据集路径，自定义
```
