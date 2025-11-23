*** Settings ***
Resource  resource.robot
Suite Setup      Open And Configure Browser
Suite Teardown   Close Browser
Test Setup       Reset Sources And Go To Starting Page

*** Test Cases ***
Click Add Sources
    Go To New Source Page
    New Source Form Should Be Open

Add New Reference With Required Fields
    Go To New Source Page
    New Source Form Should Be Open
    Input Text    id=key         testikey1
    Select From List By Value    id=ref_type    article
    Input Text    id=author      Testaaja, Tero
    Input Text    id=title       Testiartikkeli
    Input Text    id=year        2024
    Input Text    id=journal     Testilehti
    Input Text    id=publisher   Testikustantaja
    Click Button  Tallenna viite
    Location Should Be    ${NEW_URL}
    Page Should Contain   Testiartikkeli

Missing Required Title Keeps Form Open
    Go To New Source Page
    New Source Form Should Be Open
    Input Text    id=key         puuttuva_title
    Select From List By Value    id=ref_type    book
    Input Text    id=author      Tekijä Testaaja
    Input Text    id=year        2024
    Click Button  Tallenna viite
    Location Should Be    ${NEW_URL}
    Title Should Be       Lisää uusi viite

Back To Home Page Works
    Go To New Source Page
    New Source Form Should Be Open
    Go To Starting Page
    Location Should Be    ${HOME_URL}

*** Keywords ***
Reset Sources And Go To Starting Page
    Reset Sources
    Go To Starting Page
