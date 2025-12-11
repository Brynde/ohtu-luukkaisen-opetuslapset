*** Settings ***
Library    SeleniumLibrary

*** Variables ***
${SERVER}         localhost:5001
${HOME_URL}       http://${SERVER}/
${NEW_URL}        http://${SERVER}/sources/new
${RESET_URL}      http://${SERVER}/reset_db
${BROWSER}        chrome
${HEADLESS}       false
${WINDOW_SIZE}    1280,2000

*** Keywords ***
Open And Configure Browser
    [Arguments]    ${headless}=${HEADLESS}    ${browser}=${BROWSER}
    IF    '${browser}'=='chrome'
        Open Chrome    ${headless}
    ELSE IF    '${browser}'=='firefox'
        Open Firefox    ${headless}
    ELSE
        Fail    Unsupported browser: ${browser}
    END
    Set Selenium Timeout    10 s
    Go To    ${HOME_URL}

Open Chrome
    [Arguments]    ${headless}=false
    ${opts}=    Evaluate    __import__('selenium.webdriver', fromlist=['ChromeOptions']).ChromeOptions()
    ${size_arg}=    Set Variable    --window-size=${WINDOW_SIZE}
    Call Method    ${opts}    add_argument    ${size_arg}
    IF    '${headless}'=='true'
        ${flag}=    Set Variable    --headless=new
        Call Method    ${opts}    add_argument    ${flag}
    END
    Create Webdriver    Chrome    options=${opts}

Open Firefox
    [Arguments]    ${headless}=false
    ${opts}=    Evaluate    __import__('selenium.webdriver', fromlist=['FirefoxOptions']).FirefoxOptions()
    IF    '${headless}'=='true'
        ${ff_flag}=    Set Variable    -headless
        Call Method    ${opts}    add_argument    ${ff_flag}
    END
    Create Webdriver    Firefox    options=${opts}
    ${w}=    Split String    ${WINDOW_SIZE}    ,
    ${w0}=   Get From List    ${w}    0
    ${w1}=   Get From List    ${w}    1
    Set Window Size    ${w0}    ${w1}

Scroll And Click
    [Arguments]    ${locator}
    Scroll Element Into View    ${locator}
    Sleep    0.2
    Click Element    ${locator}

Force Click With JS
    [Arguments]    ${locator}
    ${el}=    Get WebElement    ${locator}
    Execute Javascript    arguments[0].click();    ${el}

Submit Sort Form Safely
    [Arguments]    ${submit_locator}=css:#sort input[type="submit"]
    # ensure the element exists and is visible
    Wait Until Element Is Visible    ${submit_locator}    5 s
    # blur any focused input to avoid intercept
    Execute Javascript    if (document.activeElement) document.activeElement.blur();
    Scroll Element Into View    ${submit_locator}
    Sleep    0.2
    ${status}    ${msg}=    Run Keyword And Ignore Error    Click Element    ${submit_locator}
    Run Keyword If    '${status}'=='FAIL'    ${el}=    Get WebElement    ${submit_locator}
    Run Keyword If    '${status}'=='FAIL'    Execute Javascript    arguments[0].click();    ${el}

Reset Sources
    Go To    ${RESET_URL}

New Source Form Should Be Open
    Title Should Be    Lisää uusi viite

Home Page Should Be Open
    Wait Until Location Is    ${HOME_URL}    3 s
    Title Should Be      Source Penguin

Go To Starting Page
    Go To    ${HOME_URL}

Go To New Source Page
    Go To    ${NEW_URL}
