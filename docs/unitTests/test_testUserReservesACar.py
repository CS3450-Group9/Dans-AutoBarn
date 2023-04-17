# Generated by Selenium IDE
import pytest
import time
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

class TestTestUserReservesACar():
  def setup_method(self, method):
    self.driver = webdriver.Chrome()
    self.vars = {}
  
  def teardown_method(self, method):
    self.driver.quit()
  
  def test_testUserReservesACar(self):
    self.driver.get("http://127.0.0.1:8000/")
    self.driver.set_window_size(1848, 1053)
    self.driver.find_element(By.LINK_TEXT, "Login").click()
    self.driver.find_element(By.CSS_SELECTOR, ".text-center:nth-child(2) > a").click()
    self.driver.find_element(By.ID, "id_username").click()
    self.driver.find_element(By.ID, "id_username").send_keys("TestUser1")
    self.driver.find_element(By.ID, "id_password1").click()
    self.driver.find_element(By.ID, "id_password1").send_keys("TestPassword")
    self.driver.find_element(By.ID, "id_password2").click()
    self.driver.find_element(By.ID, "id_password2").send_keys("TestPassword")
    self.driver.find_element(By.CSS_SELECTOR, ".btn").click()
    self.driver.find_element(By.ID, "navbarDarkDropdownMenuLink").click()
    self.driver.find_element(By.LINK_TEXT, "Profile").click()
    self.driver.find_element(By.LINK_TEXT, "Add Balance").click()
    self.driver.find_element(By.ID, "inputBal").click()
    self.driver.find_element(By.ID, "inputBal").send_keys("200")
    self.driver.find_element(By.CSS_SELECTOR, ".btn-secondary").click()
    self.driver.find_element(By.LINK_TEXT, "Find Reservation").click()
    self.driver.find_element(By.CSS_SELECTOR, ".card:nth-child(1) > .nav-item").click()
    self.driver.find_element(By.ID, "start-date").click()
    self.driver.find_element(By.CSS_SELECTOR, ".flex-column:nth-child(1) > div > p").click()
    self.driver.find_element(By.LINK_TEXT, "Home").click()
    self.driver.find_element(By.LINK_TEXT, "Find Reservation").click()
    self.driver.find_element(By.CSS_SELECTOR, ".card:nth-child(3) > .nav-item").click()
    self.driver.find_element(By.ID, "start-date").click()
    self.driver.find_element(By.ID, "start-date").send_keys("0002-04-12")
    self.driver.find_element(By.ID, "start-date").send_keys("0020-04-12")
    self.driver.find_element(By.ID, "start-date").send_keys("0202-04-12")
    self.driver.find_element(By.ID, "start-date").send_keys("2023-04-12")
    self.driver.find_element(By.ID, "end-date").click()
    self.driver.find_element(By.ID, "end-date").send_keys("0002-04-13")
    self.driver.find_element(By.ID, "end-date").send_keys("0020-04-13")
    self.driver.find_element(By.ID, "end-date").send_keys("0202-04-13")
    self.driver.find_element(By.ID, "end-date").send_keys("2023-04-13")
    self.driver.find_element(By.CSS_SELECTOR, ".btn-secondary").click()
    self.driver.find_element(By.CSS_SELECTOR, ".btn").click()
    self.driver.find_element(By.ID, "navbarDarkDropdownMenuLink").click()
    self.driver.find_element(By.LINK_TEXT, "Profile").click()
    self.driver.find_element(By.LINK_TEXT, "Current Reservations").click()
    self.driver.find_element(By.ID, "car_location").click()
    self.driver.find_element(By.ID, "car_location").send_keys("Your Moms House")
    self.driver.find_element(By.CSS_SELECTOR, ".btn-secondary").click()
  
