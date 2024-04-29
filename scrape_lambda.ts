import * as puppeteerCore from 'puppeteer-core'; // Used for typing and lambda execution
const chromium = require('chrome-aws-lambda'); // CommonJS import for specific functionalities not available as ES6 module
import { APIGatewayProxyHandler } from 'aws-lambda';
import dotenv from 'dotenv';
import pino from 'pino'; // Correct way to import pino when using ES6 syntax

dotenv.config();

// Configure logger
const logger = pino({
  level: process.env.LOG_LEVEL || 'info'
});
logger.info('Logger initialized.');

const isLocal = process.env.LOCAL_TEST === 'true'; // Set this environment variable locally

// Helper function to get executable path
const getExecutablePath = async () => {
    if (isLocal) {
        const puppeteer = require('puppeteer');
        return puppeteer.executablePath();
    } else {
        return chromium.executablePath; // Note: not calling it as a function
    }
};

// Function to process wait times data
const processWaitTimes = (waitTimes: string[], lanes: string[]): string[] => {
    let count = 0;
    const filteredWaitTimes: string[] = [lanes[0]];
    for (const waitTime of waitTimes) {
        if (waitTime.endsWith(":") || waitTime.startsWith("N")) {
            continue;
        }
        if (waitTime.includes('No Delay')) {
            filteredWaitTimes.push(waitTime);
        } else if (waitTime.includes('Status')) {
            filteredWaitTimes.push('Vehicles: 0.05');
        } else {
            filteredWaitTimes.push(waitTime);
        }
        if (waitTime.includes('Pedestrians') && count < lanes.length - 1) {
            count++;
            filteredWaitTimes.push("\n" + lanes[count]);
        }
    }
    return filteredWaitTimes;
};

// Main function to scrape wait times
const scrapeWaitTimes = async (): Promise<string[][]> => {
    const puppeteer = isLocal ? require('puppeteer') : puppeteerCore;
    let browser: any;

    try {
        browser = await puppeteer.launch({
            executablePath: await getExecutablePath(),
            args: [...chromium.args, '--enable-logging', '--v=1'],
            headless: true,
            defaultViewport: { width: 1920, height: 1080 },
            timeout: 90000 // Adjust timeout settings as needed
        });
        logger.info('Browser launched successfully');

        const page = await browser.newPage();
        await page.goto("https://www.smartbordercoalition.com/border-wait-times", {
            waitUntil: 'networkidle0',
            timeout: 90000 // Adjust timeout settings as needed
        });
        logger.info('Page loaded successfully');

        await page.waitForSelector("div.ticker__item:nth-of-type(2) span", { timeout: 45000 });
        logger.info('Selector found');

        const lanes_sy = ['SAN YSIDRO:', 'All Traffic >>', 'Ready Lanes >>', 'Sentri >>'];
        const lanes_otay = ['OTAY:', 'All Traffic >>', 'Ready Lanes >>', 'Sentri >>'];

        const syWaitTimes = await page.evaluate(() =>
            Array.from(document.querySelectorAll("div.ticker__item:nth-of-type(2) span")).map(span => (span as HTMLElement).innerText)
        );

        const otayWaitTimes = await page.evaluate(() =>
            Array.from(document.querySelectorAll("div.ticker__item:nth-of-type(3) span")).map(span => (span as HTMLElement).innerText)
        );

        const filteredWaitTimesSY = processWaitTimes(syWaitTimes, lanes_sy);
        const filteredWaitTimesOtay = processWaitTimes(otayWaitTimes, lanes_otay);

        await browser.close();
        logger.info('Browser closed');

        return [filteredWaitTimesSY, filteredWaitTimesOtay]; // Ensure return value on success
    } catch (error) {
        logger.error('Failed to execute scraping:', error);
        if (browser) await browser.close();
        throw error; // Rethrow after cleanup to handle the error further up the call stack
    }
};

export const handler: APIGatewayProxyHandler = async (event, context) => {
  logger.info("Handler started");
  try {
    const results = await scrapeWaitTimes();
    logger.info("Data processed successfully");
    return {
      statusCode: 200,
      body: JSON.stringify(results)
    };
  } catch (e) {
    logger.error("An error occurred:", e);
    return {
      statusCode: 500,
      body: JSON.stringify({ error: "Failed to process data" })
    };
  }
};

if (require.main === module) {
  (async () => {
    try {
      const results = await scrapeWaitTimes();
      console.log(results);
    } catch (e) {
      console.error("An error occurred:", e);
    }
  })();
}
