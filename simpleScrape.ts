import * as dotenv from 'dotenv';
dotenv.config();

// Declare a type for puppeteer that will handle both 'puppeteer' and 'puppeteer-core'
type PuppeteerInstance = typeof import('puppeteer');

let puppeteerBrowser: PuppeteerInstance;

// Check if the LOCAL_TEST environment variable is set to 'true'
if (process.env.LOCAL_TEST === 'true') {
    puppeteerBrowser = require('puppeteer');
} else {
    // Casting 'require('puppeteer-core')' as PuppeteerInstance
    puppeteerBrowser = require('puppeteer-core') as PuppeteerInstance;
}

async function simpleScrape() {
    // Retrieve the executable path based on the environment
    const executablePath = process.env.LOCAL_TEST === 'true'
        ? puppeteerBrowser.executablePath()
        : process.env.CHROMIUM_PATH; // Use an environment variable for the Chromium path

    // Launch the browser with the correct executable path
    const browser = await puppeteerBrowser.launch({
        executablePath,
        headless: true,
    });

    try {
        // Open a new page in the browser
        const page = await browser.newPage();
        // Navigate to 'https://example.com'
        await page.goto('https://smartbordercoalition.com/border-wait-times');
        // Retrieve the page's title
        const title = await page.title();
        // Log the title to the console
        console.log(`Title of the page: ${title}`);
    } catch (error) {
        // Log any errors that occur during page navigation or title retrieval
        console.error('An error occurred:', error);
    } finally {
        // Ensure the browser is closed when done
        await browser.close();
    }
}

// Run the simpleScrape function
simpleScrape();
