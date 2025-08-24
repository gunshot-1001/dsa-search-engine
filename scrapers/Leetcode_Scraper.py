import json
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


def init_driver(headless=True):
    options = webdriver.ChromeOptions()
    if headless:
        options.add_argument("--headless=new")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)


# ✅ Define domains with their LeetCode tag URLs
DOMAIN_URLS = {
    "Array": "https://leetcode.com/tag/array/",
    "String": "https://leetcode.com/tag/string/",
    "Hash Table": "https://leetcode.com/tag/hash-table/",
    "Dynamic Programming": "https://leetcode.com/tag/dynamic-programming/",
    "Math": "https://leetcode.com/tag/math/",
    "Sorting": "https://leetcode.com/tag/sorting/",
    "Greedy": "https://leetcode.com/tag/greedy/",
    "Depth-First Search": "https://leetcode.com/tag/depth-first-search/",
    "Binary Search": "https://leetcode.com/tag/binary-search/",
    "Tree": "https://leetcode.com/tag/tree/",
    "Matrix": "https://leetcode.com/tag/matrix/",
    "Two Pointers": "https://leetcode.com/tag/two-pointers/",
    "Stack": "https://leetcode.com/tag/stack/",
    "Graph": "https://leetcode.com/tag/graph/",
    "Heap (Priority Queue)": "https://leetcode.com/tag/heap-priority-queue/",
    "Breadth-First Search": "https://leetcode.com/tag/breadth-first-search/",
    "Union Find": "https://leetcode.com/tag/union-find/",
    "Binary Tree": "https://leetcode.com/tag/binary-tree/",
    "Binary Search Tree": "https://leetcode.com/tag/binary-search-tree/",
    "Recursion": "https://leetcode.com/tag/recursion/",
    "Queue": "https://leetcode.com/tag/queue/",
    "Linked List": "https://leetcode.com/tag/linked-list/",
    "Backtracking": "https://leetcode.com/tag/backtracking/",
    "Bit Manipulation": "https://leetcode.com/tag/bit-manipulation/",
    "Prefix Sum": "https://leetcode.com/tag/prefix-sum/",
    "Simulation": "https://leetcode.com/tag/simulation/",
    "Design": "https://leetcode.com/tag/design/",
    "Sliding Window": "https://leetcode.com/tag/sliding-window/",
    "Counting": "https://leetcode.com/tag/counting/",
    "Segment Tree": "https://leetcode.com/tag/segment-tree/",
    "Hashing": "https://leetcode.com/tag/hashing/"
}


def scrape_leetcode_tags(limit_per_domain=5, headless=True):
    driver = init_driver(headless)
    problems = []

    try:
        for domain, url in DOMAIN_URLS.items():
            print(f"\n🌍 Scraping domain: {domain} ({url})")

            driver.get(url)

            # Wait until problem list loads
            try:
                WebDriverWait(driver, 30).until(
                    EC.presence_of_all_elements_located((By.CSS_SELECTOR, "a[href^='/problems/']"))
                )
            except:
                print(f"⚠️ Timeout for {domain}, skipping...")
                continue

            prev_count = 0
            retries = 0

            while len([p for p in problems if p["Domain"] == domain]) < limit_per_domain:
                # Scroll to load more
                driver.execute_script("window.scrollBy(0, 4000);")
                time.sleep(2)

                cards = driver.find_elements(By.CSS_SELECTOR, "a[href^='/problems/']")

                for card in cards:
                    if len([p for p in problems if p["Domain"] == domain]) >= limit_per_domain:
                        break

                    try:
                        href = card.get_attribute("href")
                        title = card.text.split("\n")[0].strip()

                        # Difficulty
                        diff = "Unknown"
                        for d in ["Easy", "Medium", "Hard"]:
                            if d in card.text:
                                diff = d
                                break

                        problems.append({
                            "Domain": domain,
                            "Title": title,
                            "Tag": diff,
                            "URL": href if href.startswith("http") else "https://leetcode.com" + href
                        })
                    except:
                        continue

                # Stop if no new problems are loading
                if len(problems) == prev_count:
                    retries += 1
                    if retries >= 2:
                        break
                else:
                    retries = 0
                    prev_count = len(problems)

            # ✅ Save JSON live after each domain
            with open("leetcode_problems.json", "w", encoding="utf-8") as f:
                json.dump(problems, f, indent=2, ensure_ascii=False)

            print(f"✅ Finished {domain}: {len([p for p in problems if p['Domain']==domain])} problems")

    finally:
        driver.quit()

    return problems


if __name__ == "__main__":
    data = scrape_leetcode_tags(limit_per_domain=5, headless=False)
    print("💾 Total Saved:", len(data), "problems")
