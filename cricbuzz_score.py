
from playwright.sync_api import sync_playwright

# Start Playwright
with sync_playwright() as p:

    print("Starting Playwright...")

    # Launch Chromium browser
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()

    print("Chromium launched successfully!")

    # 1. NAVIGATION: Open Cricbuzz
    page.goto("https://www.cricbuzz.com/")

    print("Cricbuzz homepage opened!")

    # Pause to demonstrate Cricbuzz homepage
    page.wait_for_timeout(5000)

    # 2. CLICKING: Click Live Scores
    page.get_by_role("link", name="Live Scores").click()

    print("Clicked Live Scores!")

    # Pause to demonstrate Live Scores page
    page.wait_for_timeout(5000)

    # 3. WAITING: Wait for page content
    page.locator("body").wait_for(state="visible")

    print("Live Scores page loaded!")

    # 4. EXTRACTING: Get only ZIM vs AFG match
    page_text = page.locator("body").inner_text()

    lines = page_text.splitlines()

    zim_afg_details = []
    capture = False

    for line in lines:

        # Start capturing when ZIM vs AFG is found
        if "ZIM vs AFG" in line.upper():
            capture = True

        # Collect match information
        if capture:
            zim_afg_details.append(line)

            # Stop when the next match starts
            if len(zim_afg_details) > 1 and " vs " in line.lower():
                break

    # Convert extracted lines into text
    score_text = "\n".join(zim_afg_details).strip()

    # Print the score
    print("\n========== ZIM vs AFG SCORE ==========")
    print(score_text if score_text else "ZIM vs AFG match not found")
    print("======================================")

    # 5. SAVE SCORE TO TXT FILE
    if score_text:
        with open("score.txt", "w", encoding="utf-8") as file:
            file.write(score_text)

        print("\nScore saved successfully as score.txt")

    # 6. SCREENSHOT
    page.screenshot(path="score.png", full_page=True)

    print("Screenshot saved as score.png")

    # Pause to show the final result before closing
    page.wait_for_timeout(5000)

    # 7. CLOSE BROWSER
    browser.close()

    print("\nBrowser closed successfully!")
    print("Automation completed!")
