*** Settings ***
Resource  resource.robot
Suite Setup      Open And Configure Browser
Suite Teardown   Close Browser
Test Setup       Reset Sources And Go To Starting Page

*** Test Cases ***
Click Add Sources
    Go To New Source Page
    New Source Form Should Be Open

*** Keywords ***
Reset Sources And Go To Starting Page
    Reset Sources
    Go To Starting Page
