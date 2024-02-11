import pytest

import GetData
from GetData import VarData
from WebTest.Flows.login_flow import LoginFlow
from WebTest.WebInfra.web_driver_factory import WebDriverFactory


# Assuming get_test_data is a function you have to fetch test data based on keys


class TestLoginWeb(WebDriverFactory):
    def __init__(self):
        super().__init__()
        self.url = GetData.loaded_data[VarData.WebUrl]
        self.web_user_name = GetData.loaded_data[VarData.WebUserName]
        self.web_password = GetData.loaded_data[VarData.WebPassword]


    # @pytest.mark.allure.feature("Login")
    # @pytest.mark.allure.story("Web Login")
    # @pytest.mark.parametrize("category", [("UiWeb"), ("Level_1")])
    def test_login_web(self):
        login_flow = LoginFlow(self.driver)
        xx = self.url
        login_flow.open_page(True, url=self.url)
        login_flow.do_valid_login(self.web_user_name, self.web_password)

        is_home_page_open = login_flow.is_home_page_open()

        assert is_home_page_open, "Home page was open, Home page failed to open"

    def teardown_method(self):
        self.driver.quit()
def test_login():
    run_test = TestLoginWeb()
    run_test.test_login_web()
    pass

