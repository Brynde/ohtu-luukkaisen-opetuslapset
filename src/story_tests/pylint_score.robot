*** Settings ***
Library    Process
Library    BuiltIn
Library    Collections

*** Variables ***
${PYLINT_TARGET}    src
${MIN_SCORE}        8.0
${PYTHON}    ${CURDIR}${/}..${/}..${/}.venv${/}Scripts${/}python.exe

*** Test Cases ***
Pylint score meets minimum threshold (8.0)
    [Tags]    ci-skip
    Check Pylint Score Is At Least    ${PYLINT_TARGET}    ${MIN_SCORE}

*** Keywords ***
Run Pylint And Return Output
    [Arguments]    ${target}
    ${res}=    Run Process    ${PYTHON}    -m    pylint    ${target}    --exit-zero    stdout=PIPE    stderr=PIPE
    ${combined}=    Set Variable    ${res.stdout}\n${res.stderr}
    RETURN    ${combined}

Parse Pylint Score From Output
    [Arguments]    ${text}
    ${matches}=    Evaluate    __import__('re').findall(r'([0-9]+(?:\\.[0-9]+)?)\\s*/\\s*10', r'''${text}''', __import__('re').IGNORECASE)
    ${count}=      Get Length    ${matches}
    Run Keyword If    ${count} == 0    Fail    Could not find pylint score in output. Full output:\n${text}
    ${score_str}=  Get From List    ${matches}    -1
    ${score}=      Convert To Number    ${score_str}
    RETURN    ${score}

Check Pylint Score Is At Least
    [Arguments]    ${target}    ${required_score}
    ${output}=    Run Pylint And Return Output    ${target}
    ${score}=     Parse Pylint Score From Output    ${output}
    Should Be True    ${score} >= ${required_score}    Pylint score ${score} is less than required ${required_score}. Full output:\n${output}
    RETURN    ${score}