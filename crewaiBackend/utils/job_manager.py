# 核心功能：
# (1)管理多个作业及其状态，通过锁机制确保线程安全。
# (2)定义作业和事件的结构，并提供一个函数来追加事件，同时在作业开始时初始化新的作业实例。


# 导入python标准库
from dataclasses import dataclass
from datetime import datetime
from typing import List, Dict
from threading import Lock


# 创建一个锁，用于保护jobs字典，确保在多线程操作时的安全性
jobs_lock = Lock()
# 一个字典，用于存储以job_id为键的Job实例
jobs: Dict[str, "Job"] = {}



# 使用@dataclass定义一个Event类，表示事件的结
# timestamp：事件发生的时间
# data：与事件相关的数据
@dataclass
class Event:
    timestamp: datetime
    data: str


# 使用@dataclass定义一个Job类，表示一个作业的结构
# status：表示作业的状态（如"STARTED"、"COMPLETE"等）
# events：一个列表，包含与该作业相关的事件
# result：作业完成后的结果
@dataclass
class Job:
    status: str
    events: List[Event]
    result: str


# 定义函数append_event，接受job_id和事件数据event_data作为参数
def append_event(job_id: str, event_data: str):
    # 使用上下文管理器with来确保在锁定期间执行代码，避免多线程冲突
    with jobs_lock:
        # 检查jobs字典中是否存在job_id
        # 如果不存在，创建一个新的Job实例，将其状态设置为STARTED，事件列表初始化为空，结果初始化为空字符串
        if job_id not in jobs:
            print("Job %s started", job_id)
            jobs[job_id] = Job(
                status='STARTED',
                events=[],
                result='')
        else:
            # 如果job_id已存在，打印信息表示正在为该作业附加事件
            print("Appending event for job %s: %s", job_id, event_data)

        # 创建一个新的Event实例，记录当前时间和事件数据，然后将其追加到相应Job实例的事件列表中
        jobs[job_id].events.append(
            Event(timestamp=datetime.now(), data=event_data))
