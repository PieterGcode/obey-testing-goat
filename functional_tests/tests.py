import time
from selenium import webdriver
import unittest
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException
from django.test import LiveServerTestCase

MAX_WAIT = 5


class NewVisitorTest(LiveServerTestCase):
    def setUp(self) -> None:
        self.browser = webdriver.Chrome()

    def tearDown(self) -> None:
        self.browser.quit()

    def check_for_row_in_list_table(self, row_text):
        rows = self.browser.find_elements(By.CSS_SELECTOR, "#id_list_table tr")
        self.assertIn(row_text, [row.text for row in rows])

    def wait_for_row_in_list_table(self, row_text):
        start_time = time.time()
        while True:
            try:
                self.check_for_row_in_list_table(row_text)
                return
            except (AssertionError, WebDriverException) as e:
                if time.time() - start_time > MAX_WAIT:
                    raise e
                time.sleep(0.5)

    def enter_item_to_list(self, item_text):
        inputbox = self.browser.find_element(By.ID, "id_new_item")
        inputbox.send_keys(item_text)
        inputbox.send_keys(Keys.ENTER)

    def test_can_start_a_list_for_one_user(self):
        # John wants to check out the homepage of the to-do app
        self.browser.get(self.live_server_url)

        # He notices the page title and header mention to-do lists
        self.assertIn("To-Do", self.browser.title)
        header_text = self.browser.find_element(By.CSS_SELECTOR, "h1").text
        self.assertIn("To-Do", header_text)

        # He is invited to enter a to-do item straight away
        inputbox = self.browser.find_element(value="id_new_item")
        self.assertEqual(inputbox.get_attribute("placeholder"), "Enter a to-do item")

        # He types "Buy peacock feathers" into a text box (John's hobby is tying fly-fishing lures)
        inputbox.send_keys("Buy peacock feathers")

        # When he hits enter, the page updates, and now the page lists
        # "1: Buy peacock feathers" as an item in a to-do list
        inputbox.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table("1: Buy peacock feathers")

        # There is still a text box inviting him to add another item. He
        # enters "Use peacock feathers to make a fly"
        inputbox = self.browser.find_element(value="id_new_item")
        inputbox.send_keys("Use peacock feathers to make a fly")
        inputbox.send_keys(Keys.ENTER)

        # The page updates again, and now shows both items on his list
        self.wait_for_row_in_list_table("1: Buy peacock feathers")
        self.wait_for_row_in_list_table("2: Use peacock feathers to make a fly")

        # John wonders whether the site will remember her list. Then he sees that the site has generated a unique URL for him
        # -- there is some explanatory text to that effect.

        # He visits that URL - his to-do list is still there.

        # Satisfied, He goes back to sleep
        self.fail("Finish the test!")

    def test_multiple_users_can_start_lists_at_different_urls(self):
        # John starts a new to-do list
        self.browser.get(self.live_server_url)
        self.enter_item_to_list("Buy peacock feathers")
        self.wait_for_row_in_list_table("1: Buy peacock feathers")

        # He notices that his list has a unique URL
        john_list_url = self.browser.current_url
        self.assertRegex(john_list_url, "/lists/.+")

        # Now a new user, Jane, comes along to the site.

        ## We use a new browser session to make sure that no information
        ## of John's is coming through from cookies etc
        self.browser.quit()
        self.browser = webdriver.Chrome()

        # Jane visits the home page.  There is no sign of John's list
        self.browser.get(self.live_server_url)
        page_text = self.browser.find_element(By.TAG_NAME, "body").text
        self.assertNotIn("Buy peacock feathers", page_text)
        self.assertNotIn("make a fly", page_text)

        # Jane starts a new list by entering a new item. She
        # is less interesting than John...
        self.enter_item_to_list("Buy milk")
        self.wait_for_row_in_list_table("1: Buy milk")

        # Jane gets her own unique URL
        jane_list_url = self.browser.current_url
        self.assertRegex(jane_list_url, "/lists/.+")
        self.assertNotEqual(jane_list_url, john_list_url)

        # Again, there is no trace of John's list
        page_text = self.browser.find_element(By.TAG_NAME, "body").text
        self.assertNotIn("Buy peacock feathers", page_text)
        self.assertIn("Buy milk", page_text)

        # Satisfied, they both go back to sleep

if __name__ == "__main__":
    unittest.main()
