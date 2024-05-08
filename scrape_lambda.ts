import * as puppeteer from 'puppeteer'; // Use puppeteer for local execution
import { APIGatewayProxyHandler } from 'aws-lambda';
import dotenv from 'dotenv';
import pino from 'pino';

dotenv.config();

const logger = pino({
  level: process.env.LOG_LEVEL || 'info'
});
logger.info('Logger initialized.');

const processWaitTimes = (waitTimes: string[], lanes: string[]): string[] => {
    let count = 1;
    const filteredWaitTimes: string[] = [lanes[0], lanes[1]];
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

const scrapeWaitTimes = async (): Promise<string[][]> => {
    let browser: puppeteer.Browser | null = null;

    try {
        browser = await puppeteer.launch({
            headless: true,
            defaultViewport: { width: 1920, height: 1080 }
        });
        logger.info('Browser launched successfully');

        const page = await browser.newPage();
        await page.goto("https://www.smartbordercoalition.com/border-wait-times", {
            waitUntil: 'networkidle0',
            timeout: 90000
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
        filteredWaitTimesOtay.pop();
        
        await browser.close();
        logger.info('Browser closed');

        return [filteredWaitTimesSY, filteredWaitTimesOtay];
    } catch (error) {
        logger.error('Failed to execute scraping:', error);
        if (browser) await browser.close();
        throw error;
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
