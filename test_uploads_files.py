import pytest
import os
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait


class TestUploadFiles:
    # Paths for directories with samples
    PATH = os.getcwd()
    PATH_SAMPLES = os.path.join(PATH,  "part_samples")
    PATH_SAMPLES_3M = os.path.join(PATH, "part_samples_more_3m")
    PATH_SHEET = os.path.join(PATH, "part_samples_sheet_metal")
    PATH_SHEET_3M = os.path.join(PATH,  "part_samples_sheet_metal_3m")
    PATH_ERRORS =  os.path.join(PATH, 'part_errors')

    # Fake Email
    FAKE_EMAIL = 'lol@kek.com'

    @pytest.fixture()
    def test_setup(self):
        from selenium import webdriver
        from webdriver_manager.chrome import ChromeDriverManager
        global driver
        driver = webdriver.Chrome(ChromeDriverManager().install())
        driver.get("https://www.hubs.com/manufacture/")
        driver.implicitly_wait(10)
        yield
        driver.close()
        driver.quit()

    @pytest.mark.parametrize('upload_file',
                             os.listdir(PATH_SAMPLES))
    def test_upload_cnc(self, test_setup, upload_file):
        path_to_file = self.PATH_SAMPLES + "\\{}".format(upload_file)
        self.upload_file(path_to_file)
        self.close_email_window()
        self.close_pop_window()
        assert driver.find_elements_by_xpath(
            "//*[contains(text(), '1 of your parts contains an error')]"
        ) == []

    @pytest.mark.parametrize('upload_file',
                             os.listdir(PATH_SHEET))
    def test_upload_sheet(self, test_setup, upload_file):
        driver.find_element_by_css_selector('div.technology-item:nth-child(3)').click()
        path_to_file = self.PATH_SHEET + "\\{}".format(upload_file)
        self.upload_file(path_to_file)
        self.close_email_window()
        self.close_pop_window()
        assert driver.find_elements_by_xpath(
            "//*[contains(text(), '1 of your parts contains an error')]"
        ) == []

    # This case has no assertions due to expected rc is not define
    @pytest.mark.parametrize('upload_file',
                             os.listdir(PATH_SHEET))
                             # [(os.listdir(PATH_SHEET)[0])])
    def test_upload_sheet_as_cnc(self, test_setup, upload_file):
        path_to_file = self.PATH_SHEET + "\\{}".format(upload_file)
        self.upload_file(path_to_file)
        self.close_email_window()
        self.close_pop_window()

    @pytest.mark.parametrize('upload_file',
                             os.listdir(PATH_SAMPLES))
    # [(os.listdir(PATH_SAMPLES)[0])])
    def test_upload_cnc_as_sheet(self, test_setup, upload_file):
        driver.find_element_by_css_selector('div.technology-item:nth-child(3)').click()
        path_to_file = self.PATH_SAMPLES + "\\{}".format(upload_file)
        self.upload_file(path_to_file)
        self.close_email_window()
        self.close_pop_window()
        assert driver.find_elements_by_xpath(
            "//*[contains(text(), '1 of your parts contains an error')]"
        )

    @pytest.mark.parametrize('upload_file',
                             os.listdir(PATH_SAMPLES_3M))
                             # [(os.listdir(PATH_SAMPLES_3M)[0])])
    def test_upload_3m_files_cnc(self, test_setup, upload_file):
        path_to_file = self.PATH_SAMPLES_3M + "\\{}".format(upload_file)
        self.upload_file(path_to_file)
        self.close_email_window()
        self.close_pop_window()
        assert driver.find_elements_by_xpath(
            "//*[contains(text(), '1 of your parts contains an error')]"
        )

    @pytest.mark.parametrize('upload_file',
                             os.listdir(PATH_SHEET_3M))
    # [(os.listdir(PATH_SHEET_3M)[0])])
    def test_upload_3m_files_cnc(self, test_setup, upload_file):
        driver.find_element_by_css_selector('div.technology-item:nth-child(3)').click()
        path_to_file = self.PATH_SHEET_3M + "\\{}".format(upload_file)
        self.upload_file(path_to_file)
        self.close_email_window()
        self.close_pop_window()
        assert driver.find_elements_by_xpath(
            "//*[contains(text(), ' This part is too big to manufacture with sheet metal.')]"
        )

    def test_upload_large_file(self, test_setup):
        path_to_file = self.PATH_ERRORS + '\\sample_128m.IGS'
        self.upload_file(path_to_file,
                         wait_for_new_page=False)
        driver.implicitly_wait(1)
        assert driver.find_elements_by_xpath(
            "//*[contains(text(), 'This file is too large')]"
        )



    # +======Support Functions ======#

    def upload_file(
            self,
            file_path: str = PATH_SAMPLES + '\\sample.SLDPRT',
            wait_for_new_page: bool = True
    ):
        """
        simple function for upload file on server
        :param file_path: full path to file
        :return:
        """
        print(file_path)
        # file_path_for_send = file_path.replace('\\', '/' )
        select_file_btn = driver.find_element(By.XPATH, '//*[@id="file-btn"]')
        select_file_btn.send_keys(
            file_path
        )
        if wait_for_new_page:
            WebDriverWait(driver, 60).until(
                expected_conditions.presence_of_element_located((By.XPATH, '//*[@id="email"]'))
            )

    def close_email_window(self):
        """
        function for work with email window
        :return:
        """
        driver.find_element_by_xpath('//*[@id="email"]').send_keys(self.FAKE_EMAIL)
        driver.implicitly_wait(3)
        driver.find_element_by_xpath('//*[@id="emailWallForm"]/div[1]/mat-dialog-actions/button').click()

    def close_pop_window(self):
        """
        function for close pop window
        :return:
        """
        WebDriverWait(driver, 60).until(
            expected_conditions.presence_of_element_located(
                (By.XPATH, '//*[@id="mat-dialog-1"]/h3d-new-feature-walkthrough-dialog/div/button/i')
            )
        )
        driver.find_element_by_xpath(
            '//*[@id="mat-dialog-1"]/h3d-new-feature-walkthrough-dialog/div/button/i'
        ).click()

        # ActionChains(driver=driver).click(
        #     driver.find_element_by_xpath('//*[@id="emailWallForm"]/div[1]/mat-dialog-actions/button')
        # ).pause(
        #     seconds=10
        # ).click(
        #     driver.find_element_by_xpath('//*[@id="mat-dialog-1"]/h3d-new-feature-walkthrough-dialog/div/button/i')
        # ).perform()
