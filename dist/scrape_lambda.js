"use strict";
var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    var desc = Object.getOwnPropertyDescriptor(m, k);
    if (!desc || ("get" in desc ? !m.__esModule : desc.writable || desc.configurable)) {
      desc = { enumerable: true, get: function() { return m[k]; } };
    }
    Object.defineProperty(o, k2, desc);
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __setModuleDefault = (this && this.__setModuleDefault) || (Object.create ? (function(o, v) {
    Object.defineProperty(o, "default", { enumerable: true, value: v });
}) : function(o, v) {
    o["default"] = v;
});
var __importStar = (this && this.__importStar) || function (mod) {
    if (mod && mod.__esModule) return mod;
    var result = {};
    if (mod != null) for (var k in mod) if (k !== "default" && Object.prototype.hasOwnProperty.call(mod, k)) __createBinding(result, mod, k);
    __setModuleDefault(result, mod);
    return result;
};
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.handler = void 0;
const puppeteer = __importStar(require("puppeteer")); // Use puppeteer for local execution
const dotenv_1 = __importDefault(require("dotenv"));
const pino_1 = __importDefault(require("pino"));
dotenv_1.default.config();
const logger = (0, pino_1.default)({
    level: process.env.LOG_LEVEL || 'info'
});
logger.info('Logger initialized.');
const processWaitTimes = (waitTimes, lanes) => {
    let count = 1;
    const filteredWaitTimes = [lanes[0], lanes[1]];
    for (const waitTime of waitTimes) {
        if (waitTime.endsWith(":") || waitTime.startsWith("N")) {
            continue;
        }
        if (waitTime.includes('No Delay')) {
            filteredWaitTimes.push(waitTime);
        }
        else if (waitTime.includes('Status')) {
            filteredWaitTimes.push('Vehicles: 0.05');
        }
        else {
            filteredWaitTimes.push(waitTime);
        }
        if (waitTime.includes('Pedestrians') && count < lanes.length - 1) {
            count++;
            filteredWaitTimes.push("\n" + lanes[count]);
        }
    }
    return filteredWaitTimes;
};
const scrapeWaitTimes = async () => {
    let browser = null;
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
        const syWaitTimes = await page.evaluate(() => Array.from(document.querySelectorAll("div.ticker__item:nth-of-type(2) span")).map(span => span.innerText));
        const otayWaitTimes = await page.evaluate(() => Array.from(document.querySelectorAll("div.ticker__item:nth-of-type(3) span")).map(span => span.innerText));
        const filteredWaitTimesSY = processWaitTimes(syWaitTimes, lanes_sy);
        const filteredWaitTimesOtay = processWaitTimes(otayWaitTimes, lanes_otay);
        filteredWaitTimesOtay.pop();
        await browser.close();
        logger.info('Browser closed');
        return [filteredWaitTimesSY, filteredWaitTimesOtay];
    }
    catch (error) {
        logger.error('Failed to execute scraping:', error);
        if (browser)
            await browser.close();
        throw error;
    }
};
const handler = async (event, context) => {
    logger.info("Handler started");
    try {
        const results = await scrapeWaitTimes();
        logger.info("Data processed successfully");
        return {
            statusCode: 200,
            body: JSON.stringify(results)
        };
    }
    catch (e) {
        logger.error("An error occurred:", e);
        return {
            statusCode: 500,
            body: JSON.stringify({ error: "Failed to process data" })
        };
    }
};
exports.handler = handler;
if (require.main === module) {
    (async () => {
        try {
            const results = await scrapeWaitTimes();
            console.log(results);
        }
        catch (e) {
            console.error("An error occurred:", e);
        }
    })();
}
