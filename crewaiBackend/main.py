# 核心功能:实现了一个基于Flask的API后端服务，主要功能包括:
# (1)创建Flask应用：实例化Flask应用并启用CORS，以支持跨域请求
# (2)环境变量设置：设置SERPER_API_KEY环境变量，用于Google搜索引擎API的访问
# (3)作业管理：通过jobs字典管理并存储作业的状态和事件，确保在多线程环境中安全访问
# (4)启动Crew:
# kickoff_crew函数接受作业ID和输入参数，创建CrewtestprojectCrew实例并调用其kickoff方法
# 在执行过程中捕获异常并更新作业状态
# 使用线程异步执行作业，允许同时处理多个请求
# (5)POST接口 /api/crew：接收客户请求，验证输入数据，生成作业ID，启动kickoff_crew函数，并返回作业ID和HTTP状态码202
# (6)GET接口 /api/crew/<job_id>：根据作业ID查询作业状态，返回作业的状态、结果和相关事件


# 导入python标准库
from datetime import datetime
import json
from threading import Thread
from uuid import uuid4
import os
# 导入第三方库
from flask import Flask, jsonify, request, abort
from flask_cors import CORS
# 导入本应用程序提供的方法
from crew import CrewtestprojectCrew
from utils.job_manager import append_event, jobs, jobs_lock, Event
from utils.myLLM import my_llm


# 服务访问的端口
PORT = 8012
# 设置SERPER_API_KEY环境变量，用于Google搜索引擎的API
os.environ["SERPER_API_KEY"] = "9d2aa95f5a0831110a3ec837996ff37b906e99dd"
# 选择大模型类型 openai:调用gpt大模型;oneapi:调用非gpt大模型;ollama:调用本地大模型
LLM_TYPE = "openai"


# 创建Flask应用实例
app = Flask(__name__)
# 启用CORS，处理跨域资源共享以便任何来源的请求可以访问以/api/开头的接口
CORS(app, resources={r"/api/*": {"origins": "*"}})


# 定义函数kickoff_crew实现运行crew
# 接受job_id和inputs作为参数
def kickoff_crew(job_id, inputs):
    global LLM_TYPE
    print(f"Crew for job {job_id} is starting")
    # 定义变量 存放结果
    results = None
    try:
        # 创建CrewtestprojectCrew实例并调用其kickoff方法，处理输入并获取结果
        # openai:调用gpt大模型;oneapi:调用非gpt大模型;ollama:调用本地大模型
        results = CrewtestprojectCrew(job_id, my_llm(LLM_TYPE)).kickoff(inputs)
        print(f"Crew for job {job_id} is complete", results)

    except Exception as e:
        # 捕获异常，记录错误并更新作业状态为ERROR
        print(f"Error in kickoff_crew for job {job_id}: {e}")
        append_event(job_id, f"An error occurred: {e}")
        with jobs_lock:
            jobs[job_id].status = 'ERROR'
            jobs[job_id].result = str(e)
    # 在任务锁下，将任务状态更新为COMPLETE，存储结果并记录完成事件
    with jobs_lock:
        jobs[job_id].status = 'COMPLETE'
        jobs[job_id].result = results
        jobs[job_id].events.append(
            Event(timestamp=datetime.now(), data="Crew complete"))


# 定义POST接口/api/crew，运行crew
@app.route('/api/crew', methods=['POST'])
def run_crew():
    print(f"Received request to run crew")
    # 从请求中提取JSON数据，进行验证
    data = request.json
    if not data or 'customer_domain' not in data or 'project_description' not in data:
        abort(400, description="Invalid input data provided.")
    print(f"接收到的信息customer_domain: {data['customer_domain']},接收到的信息project_description: {data['project_description']}")
    # 构建参数调用kickoff_crew函数运行crew
    inputs = {
        "customer_domain": data['customer_domain'],
        "project_description": data['project_description']
    }
    job_id = str(uuid4())
    # 启动一个新线程来执行kickoff_crew函数
    thread = Thread(target=kickoff_crew, args=(
        job_id, inputs))
    thread.start()
    # 返回作业ID和HTTP状态码202（接受）
    return jsonify({"job_id": job_id}), 202


# 定义GET接口/api/crew/<job_id>，获取特定作业的状态
@app.route('/api/crew/<job_id>', methods=['GET'])
def get_status(job_id):
    # 检查作业是否存在jobs字典中
    with jobs_lock:
        job = jobs.get(job_id)
        if job is None:
            abort(404, description="Job not found")
     # 尝试解析作业结果为JSON格式。如果解析失败，保持原始字符串
    try:
        result_json = json.loads(str(job.result))
    except json.JSONDecodeError:
        result_json = str(job.result)
    # 返回作业ID、状态、结果和事件的JSON响应
    return jsonify({
        "job_id": job_id,
        "status": job.status,
        "result": result_json,
        "events": [{"timestamp": event.timestamp.isoformat(), "data": event.data} for event in job.events]
    })


if __name__ == '__main__':
    print(f"在端口 {PORT} 上启动服务器")
    app.run(debug=True, port=PORT)
