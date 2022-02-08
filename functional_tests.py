import time

from selenium import webdriver
import unittest

from selenium.webdriver import Keys
from selenium.webdriver.common.by import By


class NewVisitorTest(unittest.TestCase):
    def setUp(self) -> None:
        self.browser = webdriver.Chrome()

    def tearDown(self) -> None:
        self.browser.quit()

    def test_can_start_a_list_and_retrieve_it_later(self):
        # Joe wants to check out the homepage of the to-do app
        self.browser.get("http://localhost:8000")

        # He notices the page title and header mention to-do lists
        self.assertIn("To-Do", self.browser.title)
        header_text = self.browser.find_element(By.CSS_SELECTOR, "h1").text
        self.assertIn("To-Do", header_text)

        # He is invited to enter a to-do item straight away
        inputbox = self.browser.find_element(value="id_new_item")
        self.assertEqual(inputbox.get_attribute("placeholder"), "Enter a to-do item")

        # He types "Buy peacock feathers" into a text box (Joe's hobby is tying fly-fishing lures)
        inputbox.send_keys("Buy peacock feathers")

        # When he hits enter, the page updates, and now the page lists
        # "1: Buy peacock feathers" as an item in a to-do list
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)

        # There is still a text box inviting him to add another item. He
        # enters "Use peacock feathers to make a fly"
        inputbox = self.browser.find_element(value="id_new_item")
        inputbox.send_keys("Use peacock feathers to make a fly")
        inputbox.send_keys(Keys.ENTER)
        time.sleep(1)

        # The page updates again, and now shows both items on his list
        rows = self.browser.find_elements(By.CSS_SELECTOR, "#id_list_table tr")
        self.assertIn("1: Buy peacock feathers", [row.text for row in rows])
        self.assertIn(
            "2: Use peacock feathers to make a fly", [row.text for row in rows]
        )

        # There is still a text box inviting her to add another item. He enters "Use peacock feathers to make a fly"
        # (Joe is very methodical)

        # The page updates again, and now shows both items on his list

        # Joe wonders whether the site will remember her list. Then he sees that the site has generated a unique URL for him
        # -- there is some explanatory text to that effect.

        # He visits that URL - his to-do list is still there.

        # Satisfied, He goes back to sleep
        self.fail("Finish the test!")


if __name__ == "__main__":
    unittest.main()
