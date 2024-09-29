# 核心功能:实现了一个基于CrewAI的多Agent协作，主要功能包括:
# (1)Crew项目初始化:定义了CrewtestprojectCrew类，使用@CrewBase装饰器将其标记为CrewAI项目。此类管理代理和任务的配置
# (2)模型初始化：在构造函数中，创建一个使用ChatOpenAI模型的实例，以便后续的任务执行
# (3)任务和代理定义：
# 使用@agent装饰器定义多个代理（如市场分析师、营销策略师和内容创作者），每个代理都配置了特定的工具和模型
# 使用@task装饰器定义多个任务，包括研究任务、项目理解任务、营销策略任务、活动创意任务和文案创作任务，并为每个任务设置回调函数
# Crew调度：通过@crew装饰器创建一个Crew实例，将定义的代理和任务组合，并指定其执行顺序
# (4)启动Crew：定义kickoff方法，该方法接受输入，启动Crew执行，并处理任务的开始、完成和错误事件的记录
# (5)事件记录：在任务执行过程中，通过append_event_callback和其他地方记录任务状态和输出，便于跟踪作业进度和结果


# 导入第三方库
from crewai import Agent, Crew, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai_tools import SerperDevTool, ScrapeWebsiteTool
# 导入本应用程序提供的方法
from utils.models import MarketStrategy, CampaignIdea, Copy
from utils.job_manager import append_event



# 定义了一个CrewtestprojectCrew类并应用了@CrewBase装饰器初始化项目
# 这个类代表一个完整的CrewAI项目
@CrewBase
class CrewtestprojectCrew():
	agents_config = 'config/agents.yaml'
	tasks_config = 'config/tasks.yaml'
	# 构造初始化函数，接受job_id作为参数，用于标识作业
	def __init__(self, job_id, llm):
		self.job_id = job_id
		self.llm = llm

	# 定义task的回调函数，在任务完成后记录输出事件
	def append_event_callback(self,task_output):
		print("Callback called: %s", task_output)
		append_event(self.job_id, task_output.expected_output)

	# 通过@agent装饰器定义一个函数，返回一个Agent实例
	@agent
	def lead_market_analyst(self) -> Agent:
		return Agent(
			config=self.agents_config['lead_market_analyst'],
			verbose=True,
			llm=self.llm,
			tools=[SerperDevTool(), ScrapeWebsiteTool()],
		)
	@agent
	def chief_marketing_strategist(self) -> Agent:
		return Agent(
			config=self.agents_config['chief_marketing_strategist'],
			verbose=True,
			llm=self.llm,
			tools=[SerperDevTool(), ScrapeWebsiteTool()],
		)
	@agent
	def creative_content_creator(self) -> Agent:
		return Agent(
			config=self.agents_config['creative_content_creator'],
			verbose=True,
			llm=self.llm
		)

	# 通过@task装饰器定义一个函数，返回一个Task实例
	@task
	def research_task(self) -> Task:
		return Task(
			config=self.tasks_config['research_task'],
			callback=self.append_event_callback,
		)
	@task
	def project_understanding_task(self) -> Task:
		return Task(
			config=self.tasks_config['project_understanding_task'],
			callback=self.append_event_callback,

		)
	@task
	def marketing_strategy_task(self) -> Task:
		return Task(
			config=self.tasks_config['marketing_strategy_task'],
			callback=self.append_event_callback,
			output_json=MarketStrategy
		)
	@task
	def campaign_idea_task(self) -> Task:
		return Task(
			config=self.tasks_config['campaign_idea_task'],
			callback=self.append_event_callback,
			output_json=CampaignIdea

		)
	@task
	def copy_creation_task(self) -> Task:
		return Task(
			config=self.tasks_config['copy_creation_task'],
			callback=self.append_event_callback,
			context=[self.marketing_strategy_task(), self.campaign_idea_task()],
			output_json=Copy
		)

	# Crew类将agent和task组合成一个执行队列，并根据指定的执行流程进行任务调度
	# 通过@crew装饰器定义crew，创建一个Crew实例
	# agents=self.agents和tasks=self.tasks分别自动获取@agent和@task装饰器生成的agent和task
	# process=Process.sequential指定agent执行顺序为顺序执行模式
	# process=Process.hierarchical指定agent执行顺序为层次化执行
	@crew
	def crew(self) -> Crew:
		return Crew(
			agents=self.agents,
			tasks=self.tasks,
			process=Process.sequential,
			verbose=True
		)

	# 定义启动Crew的函数，接受输入参数inputs
	def kickoff(self,inputs):
		if not self.crew():
			append_event(self.job_id, "Crew not set up")
			return "Crew not set up"

		append_event(self.job_id, "Task Started")
		try:
			results = self.crew().kickoff(inputs=inputs)
			print("crew中最终生成结果results：", results)
			append_event(self.job_id, "Task Complete")

			return results
		except Exception as e:
			append_event(self.job_id, f"An error occurred: {e}")
			return str(e)

