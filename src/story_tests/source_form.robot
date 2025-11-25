*** Settings ***
Resource  resource.robot
Library   Collections
Library   String
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

Sources Are Alphabetically Ordered By Key
    [Documentation]    Adds three references in mixed order and checks that
    ...                the source cards on the front page are alphabetically ordered by key.

    Add Source With Title    key-c    Cerkko, Calle    C-otsikko
    Add Source With Title    key-a    Aapo, Aatu      A-otsikko
    Add Source With Title    key-b    Berta, Bertta   B-otsikko

    Go To Starting Page
    Home Page Should Be Open

    @{elements}=    Get WebElements    css:div.code-box p
    @{keys}=        Create List

    FOR    ${el}    IN    @{elements}
        ${text}=    Get Text    ${el}
        ${tmp}=     Split String    ${text}    {
        ${tmp2}=    Split String    ${tmp}[1]    ,
        ${key}=     Strip String    ${tmp2}[0]
        Append To List    ${keys}    ${key}
    END

    @{sorted}=      Copy List    ${keys}
    Sort List       ${sorted}

    Lists Should Be Equal    ${keys}    ${sorted}


*** Keywords ***
Reset Sources And Go To New Source Page
    Reset Sources
    Go To New Source Page

Add Source With Title
    [Arguments]    ${key}    ${author}    ${title}
    Go To New Source Page
    New Source Form Should Be Open
    Input Text    key         ${key}
    Select From List By Value    ref_type    article
    Input Text    author      ${author}
    Input Text    title       ${title}
    Input Text    year        2024
    Input Text    journal     Testilehti
    Input Text    publisher   Testikustantaja
    Click Button  Tallenna viite
    Home Page Should Be Open
