本项目带大家搭建一个完整的AI应用全栈项目,Flask+Vue.js+CrewAI                                                                                  
本项目主要分为三期视频介绍，第一期视频主要实现后端服务(Flask)的实现并使用ApiFox进行前后端联调，第二期视频主要给大家读一下源码，第三期视频主要实现前端页面与后端服务做交互           
项目简介:在“营销战略策划协作智能体”这个项目的基础上进行迭代，这里也会再重新介绍下该项目，关于此项目更多细节可以查看这期视频                           
https://www.bilibili.com/video/BV1i5bAeAEWn/?vd_source=30acb5331e4f5739ebbad50f7cc6b949              
https://youtu.be/w8uxBuVQVlg               
**定义了3个Agent**        
**lead_market_analyst:**                      
  role: >            
    首席市场分析师               
  goal: >              
    以敏锐的洞察力对客户提供的产品和竞争对手进行深入的剖析，并为营销战略的制定提供专业指导。              
  backstory: >               
    你任职在一家一流数字营销公司，你的职位是首席市场分析师。               
    你的专长是以敏锐的洞察力对客户提供的产品和竞争对手进行深入的剖析。                     
**chief_marketing_strategist:**                            
  role: >               
    首席营销战略师                 
  goal: >               
    基于产品的市场分析内容，以敏锐的洞察力制定出令人惊喜的营销战略。                   
  backstory: >                 
    你任职在一家一流数字营销公司，你的职位是首席营销战略师。                  
    你的专长是能够制定出成功的定制营销战略。               
**creative_content_creator:**                     
  role: >               
    首席创意内容创作师               
  goal: >                  
    基于产品的营销战略内容，为社交媒体活动开发有吸引力的创新内容。               
    重点是创建高影响力的广告文案。                 
  backstory: >               
    你任职在一家一流数字营销公司，你的职位是首席创意内容创作师。             
    你的专长是能够将营销战略转化为引人入胜的故事和视觉内容，吸引注意力并激发行动。               
**定义了5个Task**                   
**research_task:**             
  description: >                
    基于客户提供的{customer_domain}对客户提供的产品和竞争对手进行深入的剖析。请确保找到任何有趣的相关信息，日期限定为2024年。                
    我们正在就以下项目与他们合作：            
    {project_description}。            
  expected_output: >              
    关于客户、客户提供的产品和竞争对手的完整报告、包括指标统计、偏好、市场定位和受众参与度。              
  agent: lead_market_analyst                      
**project_understanding_task:**                 
  description: >                    
    了解{project_description}的项目细节和目标受众。查看提供的任何材料，并根据需要收集更多信息。                 
  expected_output: >                  
    项目的详细摘要和目标受众的简介。                 
  agent: chief_marketing_strategist                   
**marketing_strategy_task:**               
  description: >                 
    基于客户提供的{customer_domain}和{project_description}为项目制定全面的营销战略。                   
    充分使用从研究任务和项目理解任务中获得的见解来制定高质量的战略。               
  expected_output: >                  
    一份详细的营销战略文件，概述目标、目标受众、关键信息和建议的策略，确保包含名称、策略、渠道和关键绩效指标。                   
  agent: chief_marketing_strategist                
**campaign_idea_task:**                  
  description: >                  
    为{project_description}开发富有创意的营销活动构思。               
    确保创意新颖、吸引人，并与整体营销战略保持一致。                 
  expected_output: >                  
    列出 5 个活动设想，每个设想都有简要说明和预期影响。                   
  agent: creative_content_creator                      
**copy_creation_task:**                
  description: >                  
    根据已获批准的{project_description}活动创意制作营销文案。                   
    确保文案引人注目、清晰明了，并适合目标受众。                  
  expected_output: >                 
    每个活动创意的营销副本。                  
  agent: creative_content_creator                                                                     

**相关更多CrewAI相关视频如下:**                             
**(1)【Agent应用案例1-基础】使用CrewAI+FastAPI打造多Agent协作应用并对外提供API服务，支持gpt、通义千问、Ollama本地大模型对比测试**                   
对应工程文件夹为:crewaitest                   
https://www.bilibili.com/video/BV1N44reDEt3/?vd_source=30acb5331e4f5739ebbad50f7cc6b949                    
https://youtu.be/2TE5DlYlvGw                   
**(2)【Agent应用案例2-进阶】技术研究员智能体案例，Agent支持调用外部工具实现将生成的报告保存至PDF文件并下载至本地，CrewAI+FastAPI打造多Agent协作应用并对外提供API服务**                
对应工程文件夹为:crewAIWithResearcher               
https://www.bilibili.com/video/BV1Sy4HeiEBn/?vd_source=30acb5331e4f5739ebbad50f7cc6b949                   
https://youtu.be/MGEdzUUKISw                    
**(3)【Agent应用案例3-进阶】健康档案助手智能体案例，Agent调用外部工具使用RAG，CrewAI+FastAPI打造多Agent协作应用并对外提供API服务**                   
https://www.bilibili.com/video/BV1j94oe7ESy/?vd_source=30acb5331e4f5739ebbad50f7cc6b949                  
https://youtu.be/YYxgE4i7-OE                
**(4)【Agent应用案例4-进阶】多个Agent协作完成高效软件编码，CrewAI+FastAPI打造多Agent协作应用并对外提供API服务**                   
https://www.bilibili.com/video/BV1cNtJeJEPA/?vd_source=30acb5331e4f5739ebbad50f7cc6b949                  
https://youtu.be/U_CzuyKNKkY                     
**(5)【Agent应用案例5-进阶】让任务以JSON数据格式并最终任务以JSON格式输出，CrewAI+FastAPI打造多Agent协作应用并对外提供API服务**                     
https://www.bilibili.com/video/BV1i5bAeAEWn/?vd_source=30acb5331e4f5739ebbad50f7cc6b949                
https://youtu.be/w8uxBuVQVlg                    
**(6)【Agent应用案例6-进阶】在任务执行中做HumanFeedback(人类反馈)，CrewAI+FastAPI打造多Agent协作应用并对外提供API服务**                  
https://www.bilibili.com/video/BV1qcxgeVEuF/?vd_source=30acb5331e4f5739ebbad50f7cc6b949                      
https://youtu.be/ltu34eawkvA               
