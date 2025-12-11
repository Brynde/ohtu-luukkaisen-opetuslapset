*** Settings ***
Resource  resource.robot
Suite Setup      Open And Configure Browser
Suite Teardown   Close Browser
Test Setup       Go To Starting Page

*** Test Cases ***
Home loads and shows header and toolbar
    Home Page Should Be Open

New source page is reachable
    Go To    ${NEW_URL}
    New Source Form Should Be Open

Search page opens properly
    Go To    ${SEARCH_URL}
    Search Page Should Be Open