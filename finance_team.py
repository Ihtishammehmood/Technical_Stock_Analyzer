from agno.agent import Agent
import streamlit as st
from agno.models.google import Gemini
from agno.team import Team
from agno.tools.yfinance import YFinanceTools
from agno.tools.financial_datasets import FinancialDatasetsTools
from agno.tools.duckduckgo import DuckDuckGoTools
from agno.tools.reasoning import ReasoningTools
# from dotenv import load_dotenv
# load_dotenv()
# from agno.memory.v2.db.sqlite import SqliteMemoryDb
# from agno.memory.v2.memory import Memory
# from agno.storage.sqlite import SqliteStorage

# memory_db = SqliteMemoryDb(table_name="finance_team_memories", db_file="tmp/finance_memory.db")
# memory = Memory(db=memory_db)
# storage = SqliteStorage(table_name="finance_team_sessions", db_file="tmp/finance_storage.db")

GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]


# Financial Data Analyst
financial_analyst = Agent(
    name="Financial Data Analyst",
    role="Analyzes financial statements, ratios, and market data",
    model=Gemini(id="gemini-2.5-flash", api_key=GEMINI_API_KEY),
    tools=[
        YFinanceTools(
            stock_price=True,
            company_info=True,
            stock_fundamentals=True,
            income_statements=True,
            key_financial_ratios=True,
            analyst_recommendations=True,
            historical_prices=True
        ),
        FinancialDatasetsTools(
            enable_financial_statements=True,
            enable_market_data=True,
            enable_company_info=True
        ),
        ReasoningTools(think=True, analyze=True)
    ],
    instructions=[
        "Analyze financial statements and key metrics",
        "Calculate financial ratios and growth rates",
        "Compare performance against industry benchmarks",
        "Identify trends and patterns in financial data",
        "Use reasoning tools for complex analysis"
    ]
)

# Market Research Analyst
market_researcher = Agent(
    name="Market Research Analyst",
    role="Researches market trends, news, and competitive landscape",
    model=Gemini(id="gemini-2.5-flash", api_key=GEMINI_API_KEY),
    tools=[
        DuckDuckGoTools(),
        YFinanceTools(company_news=True, technical_indicators=True),
        FinancialDatasetsTools(enable_news=True, enable_market_data=True)
    ],
    instructions=[
        "Research market trends and industry developments",
        "Analyze competitive landscape and positioning",
        "Monitor news and events affecting markets",
        "Provide market sentiment analysis",
        "Track technical indicators and market signals"
    ]
)

# Investment Analyst
investment_analyst = Agent(
    name="Investment Analyst",
    role="Evaluates investment opportunities and provides recommendations",
    model=Gemini(id="gemini-2.5-flash", api_key=GEMINI_API_KEY),
    tools=[
        YFinanceTools(
            stock_price=True,
            analyst_recommendations=True,
            stock_fundamentals=True,
            company_info=True
        ),
        FinancialDatasetsTools(
            enable_financial_statements=True,
            enable_ownership_data=True
        ),
        ReasoningTools(think=True, analyze=True)
    ],
    instructions=[
        "Evaluate investment opportunities and risks",
        "Analyze valuation metrics and fair value estimates",
        "Review analyst recommendations and price targets",
        "Assess management quality and corporate governance",
        "Provide buy/sell/hold recommendations with rationale"
    ]
)

# Risk Management Analyst
risk_analyst = Agent(
    name="Risk Management Analyst",
    role="Identifies and analyzes financial risks",
    model=Gemini(id="gemini-2.5-flash", api_key=GEMINI_API_KEY),
    tools=[
        YFinanceTools(
            historical_prices=True,
            technical_indicators=True,
            stock_fundamentals=True
        ),
        FinancialDatasetsTools(enable_market_data=True),
        ReasoningTools(think=True, analyze=True)
    ],
    instructions=[
        "Identify and quantify various types of financial risks",
        "Calculate risk metrics like VaR, beta, volatility",
        "Analyze correlation and diversification benefits",
        "Monitor risk exposure and concentration",
        "Recommend risk mitigation strategies"
    ]
)

# Portfolio Manager
portfolio_manager = Agent(
    name="Portfolio Manager",
    role="Manages portfolio allocation and optimization",
    model=Gemini(id="gemini-2.5-flash", api_key=GEMINI_API_KEY),
    tools=[
        YFinanceTools(
            stock_price=True,
            historical_prices=True,
            stock_fundamentals=True
        ),
        ReasoningTools(think=True, analyze=True)
    ],
    instructions=[
        "Optimize portfolio allocation based on risk-return objectives",
        "Rebalance portfolios according to strategic targets",
        "Monitor portfolio performance and attribution",
        "Implement tactical asset allocation adjustments",
        "Ensure compliance with investment guidelines"
    ]
)

# Financial Reporting Specialist
reporting_specialist = Agent(
    name="Financial Reporting Specialist",
    role="Creates comprehensive financial reports and presentations",
    model=Gemini(id="gemini-2.5-flash", api_key=GEMINI_API_KEY),
    tools=[
        YFinanceTools(
            stock_price=True,
            company_info=True,
            stock_fundamentals=True,
            income_statements=True
        ),
        FinancialDatasetsTools(
            enable_financial_statements=True,
            enable_company_info=True
        )
    ],
    instructions=[
        "Create detailed financial reports and summaries",
        "Format data in clear tables and visualizations",
        "Provide executive summaries for stakeholders",
        "Ensure accuracy and completeness of reports",
        "Present findings in professional format"
    ]
)

# Finance Team Leader (Coordinator)
finance_team = Team(
    name="Finance Team",
    mode="coordinate",
    model=Gemini(id="gemini-2.5-flash", api_key=GEMINI_API_KEY),
    members=[
        financial_analyst,
        market_researcher,
        investment_analyst,
        risk_analyst,
        portfolio_manager,
        reporting_specialist
    ],
    # Memory configuration for the entire team
    # memory=memory,
    # storage=storage,
    # enable_user_memories=True,
    # enable_session_summaries=True,
    # # Chat history configuration
    # add_history_to_messages=True,
    # num_history_runs=3,
    description="Comprehensive finance team providing analysis, research, and investment recommendations",
    instructions=[
        "Always use Specialized Finance to answer user Query. Don't rely on your own knowledge.",
        "Coordinate team members based on the type of financial request",
        "For stock analysis: use financial analyst and market researcher",
        "For investment decisions: involve investment analyst and risk analyst", 
        "For portfolio management: engage portfolio manager and risk analyst",
        "For reporting: utilize reporting specialist to format final output",
        "Synthesize insights from multiple team members",
        "Provide comprehensive and actionable recommendations"
    ],
    show_tool_calls=True,
    markdown=True,
    show_members_responses=False,
    stream_intermediate_steps=False
)


if __name__ == "__main__":
    finance_team.print_response("What is the current stock price of apple?",
                                stream=True,
                                # show_full_reasoning=True,
                                )


# # Equity Research Team
# equity_research_team = Team(
#     name="Equity Research Team",
#     mode="collaborate", 
#     model=Gemini(id="gemini-2.0-flash"),
#     members=[financial_analyst, market_researcher, investment_analyst],
#     instructions=[
#         "Collaborate on comprehensive equity research",
#         "Combine fundamental analysis with market research",
#         "Provide investment recommendations with supporting analysis"
#     ]
# )

# # Risk Management Team  
# risk_management_team = Team(
#     name="Risk Management Team",
#     mode="coordinate",
#     model=Gemini(id="gemini-2.0-flash"), 
#     members=[risk_analyst, portfolio_manager],
#     instructions=[
#         "Focus on risk identification and mitigation",
#         "Optimize risk-adjusted returns",
#         "Monitor and report risk exposures"
#     ]
# )