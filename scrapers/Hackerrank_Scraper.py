import json
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def scrape_hackerrank_all():
    # ✅ Add all the public domain URLs here
    domains = {
        "Algorithms": "https://www.hackerrank.com/domains/algorithms?badge_type=problem-solving",
        "Data Structures": "https://www.hackerrank.com/domains/data-structures?badge_type=problem-solving",
        "Mathematics": "https://www.hackerrank.com/domains/mathematics?badge_type=problem-solving",
        "C++": "https://www.hackerrank.com/domains/cpp?badge_type=problem-solving",
        "Java": "https://www.hackerrank.com/domains/java?badge_type=problem-solving",
    }

    driver = webdriver.Chrome()
    all_problems = []
    difficulty_keywords = ["Easy", "Medium", "Hard"]

    try:
        for domain_name, domain_url in domains.items():
            print(f"\n🌍 Scraping domain: {domain_name}")
            driver.get(domain_url)
            time.sleep(3)  # wait for initial load

            while True:
                # Scroll to load all problems on the current page
                last_height = driver.execute_script("return document.body.scrollHeight")
                while True:
                    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    time.sleep(2)
                    new_height = driver.execute_script("return document.body.scrollHeight")
                    if new_height == last_height:
                        break
                    last_height = new_height

                # Wait for problem links to appear
                WebDriverWait(driver, 20).until(
                    EC.presence_of_all_elements_located((By.CSS_SELECTOR, "a[data-analytics='ChallengeListChallengeName']"))
                )
                cards = driver.find_elements(By.CSS_SELECTOR, "a[data-analytics='ChallengeListChallengeName']")

                for card in cards:
                    title_text = card.text.strip()
                    url = card.get_attribute("href")

                    # Extract difficulty tag if present
                    tag = "Unknown"
                    title = title_text
                    for kw in difficulty_keywords:
                        if kw in title_text:
                            idx = title_text.index(kw)
                            title = title_text[:idx].strip()
                            tag = kw
                            break

                    all_problems.append({
                        "Domain": domain_name,
                        "Title": title,
                        "Tag": tag,
                        "URL": url
                    })

                # Try to go to next page
                try:
                    next_button = WebDriverWait(driver, 5).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, "a[aria-label='Next']"))
                    )
                    driver.execute_script("arguments[0].click();", next_button)
                    time.sleep(3)  # wait for new page load
                except:
                    break  # no next page, exit loop for this domain

        # Save JSON
        with open("hackerrank_all_domains.json", "w", encoding="utf-8") as f:
            json.dump(all_problems, f, indent=2, ensure_ascii=False)

        print(f"\n✅ Scraped and saved {len(all_problems)} problems to hackerrank_all_domains.json")

    finally:
        driver.quit()


if __name__ == "__main__":
    scrape_hackerrank_all()
