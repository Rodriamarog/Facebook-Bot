import * as puppeteer from 'puppeteer-core';
import chromium from 'chrome-aws-lambda';
import { APIGatewayProxyHandler } from 'aws-lambda';
import * as dotenv from 'dotenv';

dotenv.config();

const isLocal = process.env.LOCAL_TEST === 'true';  // Set this env var in your local environment

const getExecutablePath = async () => {
  return isLocal ? puppeteer.executablePath() : await chromium.executablePath;
};

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
            const adjustedTime = 'Vehicles: 0.05';
            filteredWaitTimes.push(adjustedTime);
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
    const browser = await puppeteer.launch({
        executablePath: await getExecutablePath(), // Use the function to dynamically set the path
        args: chromium.args,
        headless: true,
        defaultViewport: { width: 1920, height: 1080 }
    });

    const page = await browser.newPage();
    await page.goto("https://www.smartbordercoalition.com/border-wait-times");
    await page.waitForSelector("div.ticker__item:nth-of-type(2) span", { timeout: 10000 });

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

    return [filteredWaitTimesSY, filteredWaitTimesOtay];
};

export const handler: APIGatewayProxyHandler = async (event, context) => {
    console.log("Handler started");
    try {
        const results = await scrapeWaitTimes();
        console.log("Data processed successfully");
        return {
            statusCode: 200,
            body: JSON.stringify(results)
        };
    } catch (e) {
        console.error("An error occurred:", e);
        return {
            statusCode: 500,
            body: JSON.stringify({ error: "Failed to process data" })
        };
    }
};
