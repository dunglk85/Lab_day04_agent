(venv) PS D:\AI In Action\lab4_agent> pytest -v
======================================================= test session starts =======================================================
platform win32 -- Python 3.11.9, pytest-9.0.2, pluggy-1.6.0 -- D:\AI In Action\lab4_agent\venv\Scripts\python.exe
cachedir: .pytest_cache
rootdir: D:\AI In Action\lab4_agent
plugins: anyio-4.13.0, langsmith-0.7.26
collected 5 items                                                                                                                  

tests/test_agent.py::test_direct_answer_no_tool PASSED                                                                       [ 20%] 
tests/test_agent.py::test_single_tool_call_search_flights PASSED                                                             [ 40%] 
tests/test_agent.py::test_multi_step_tool_chaining PASSED                                                                    [ 60%] 
tests/test_agent.py::test_missing_info_clarification PASSED                                                                  [ 80%] 
tests/test_agent.py::test_guardrail_refusal PASSED  