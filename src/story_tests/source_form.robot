*** Settings ***
Resource  resource.robot
Suite Setup      Open And Configure Browser
Suite Teardown   Close Browser
Test Setup       Reset Sources And Go To New Source Page

*** Test Cases ***
Add New Reference With Required Fields
    Go To New Source Page
    New Source Form Should Be Open
    Input Text    key         testikey1
    Select From List By Value    ref_type    article
    Input Text    author      Testaaja, Tero
    Input Text    title       Testiartikkeli
    Input Text    year        2024
    Input Text    journal     Testilehti
    Input Text    publisher   Testikustantaja
    Click Button  Tallenna viite
    Home Page Should Be Open

Missing Required Title Keeps Form Open
    Go To New Source Page
    New Source Form Should Be Open
    Input Text    key         puuttuva_title
    Select From List By Value    ref_type    book
    Input Text    author      Tekijä Testaaja
    Input Text    year        2024
    Click Button  Tallenna viite
    New Source Form Should Be Open

Back To Home Page Works
    Go To New Source Page
    New Source Form Should Be Open
    Go To Starting Page
    Home Page Should Be Open


*** Keywords ***
Reset Sources And Go To New Source Page
    Reset Sources
    Go To New Source Page