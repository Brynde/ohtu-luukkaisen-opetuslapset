*** Settings ***
Resource  resource.robot
Library   Collections
Library   String
Suite Setup      Open And Configure Browser
Suite Teardown   Close Browser
Test Setup       Reset Sources And Go To Starting Page

*** Test Cases ***
Click Add Sources
    Go To New Source Page
    New Source Form Should Be Open

Sources Are Alphabetically Ordered By Title

    Add Source   key-c    Cerkko, Calle    C-otsikko    2025
    Add Source   key-a    Aapo, Aatu      A-otsikko    2025
    Add Source   key-b    Berta, Bertta   B-otsikko    2025

    Go To Starting Page
    Home Page Should Be Open
    Select From List By Label  sort  Otsikon mukaan A-Ö
    Submit Form  id:sort

    Titles Should Be In Alphabetical Order

Sources Are In Reverse Alphabetically Order By Title

    Add Source   key-c    Cerkko, Calle    C-otsikko    2025
    Add Source   key-a    Aapo, Aatu      A-otsikko    2025
    Add Source   key-b    Berta, Bertta   B-otsikko    2025

    Go To Starting Page
    Home Page Should Be Open
    Select From List By Label  sort  Otsikon mukaan Ö-A
    Submit Form  id:sort


    Titles Should Be In Reverse Alphabetical Order

Sources Are Ordered By Year Newest First

    Add Source   key-c    Cerkko, Calle    C-otsikko    2025
    Add Source   key-a    Aapo, Aatu      A-otsikko    2020
    Add Source   key-b    Berta, Bertta   B-otsikko    2000

    Go To Starting Page
    Home Page Should Be Open
    Select From List By Label  sort  Uusin ensin
    Submit Form  id:sort

    Newest Should Be First

Sources Are Ordered By Year Oldest First

    Add Source   key-c    Cerkko, Calle    C-otsikko    2025
    Add Source   key-a    Aapo, Aatu      A-otsikko    2020
    Add Source   key-b    Berta, Bertta   B-otsikko    2000

    Go To Starting Page
    Home Page Should Be Open
    Select From List By Label  sort  Vanhin ensin
    Submit Form  id:sort

    Oldest Should Be First



*** Keywords ***
Reset Sources And Go To Starting Page
    Reset Sources
    Go To Starting Page

Add Source
    [Arguments]    ${key}    ${author}    ${title}    ${year}
    Go To New Source Page
    New Source Form Should Be Open
    Input Text    key         ${key}
    Select From List By Value    ref_type    article
    Input Text    author      ${author}
    Input Text    title       ${title}
    Input Text    year        ${year}
    Input Text    journal     Testilehti
    Input Text    publisher   Testikustantaja
    Click Button  Tallenna viite
    Home Page Should Be Open

Titles Should Be In Alphabetical Order
    @{elements}=    Get WebElements    css:div.code-box p
    @{titles}=        Create List

    FOR    ${el}    IN    @{elements}
        ${text}=    Get Text    ${el}
        ${tmp}=     Split String    ${text}    
        ${tmp2}=    Split String    ${tmp}[1]    
        ${title}=     Strip String    ${tmp2}[2]
        Append To List    ${titles}    ${title}
    END

    @{sorted}=      Copy List    ${titles}
    Sort List       ${sorted}

    Lists Should Be Equal    ${titles}    ${sorted}

Titles Should Be In Reverse Alphabetical Order
    @{elements}=    Get WebElements    css:div.code-box p
    @{titles}=        Create List

    FOR    ${el}    IN    @{elements}
        ${text}=    Get Text    ${el}
        ${tmp}=     Split String    ${text}    
        ${tmp2}=    Split String    ${tmp}[1]    
        ${title}=     Strip String    ${tmp2}[2]
        Append To List    ${titles}    ${title}
    END

    @{sorted}=      Copy List    ${titles}
    Sort List       ${sorted}
    Reverse List    ${sorted}
    Reverse List    ${titles}

    Lists Should Be Equal    ${titles}    ${sorted}

Newest Should Be First
    @{elements}=    Get WebElements    css:div.code-box p
    @{years}=        Create List

    FOR    ${el}    IN    @{elements}
        ${text}=    Get Text    ${el}
        ${tmp}=     Split String    ${text}    
        ${tmp2}=    Split String    ${tmp}[1]    
        ${year}=     Strip String    ${tmp2}[3]
        Append To List    ${years}    ${year}
    END

    @{sorted}=      Copy List    ${years}
    Sort List       ${sorted}

    Lists Should Be Equal    ${years}    ${sorted}

Oldest Should Be First
    @{elements}=    Get WebElements    css:div.code-box p
    @{years}=        Create List

    FOR    ${el}    IN    @{elements}
        ${text}=    Get Text    ${el}
        ${tmp}=     Split String    ${text}    
        ${tmp2}=    Split String    ${tmp}[1]    
        ${year}=     Strip String    ${tmp2}[3]
        Append To List    ${years}    ${year}
    END

    @{sorted}=      Copy List    ${years}
    Sort List       ${sorted}
    Reverse List    ${sorted}
    Reverse List    ${years}

    Lists Should Be Equal    ${years}    ${sorted}