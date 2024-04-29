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
Object.defineProperty(exports, "__esModule", { value: true });
const dotenv = __importStar(require("dotenv"));
dotenv.config();
let puppeteerBrowser;
// Check if the LOCAL_TEST environment variable is set to 'true'
if (process.env.LOCAL_TEST === 'true') {
    puppeteerBrowser = require('puppeteer');
}
else {
    // Casting 'require('puppeteer-core')' as PuppeteerInstance
    puppeteerBrowser = require('puppeteer-core');
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
    }
    catch (error) {
        // Log any errors that occur during page navigation or title retrieval
        console.error('An error occurred:', error);
    }
    finally {
        // Ensure the browser is closed when done
        await browser.close();
    }
}
// Run the simpleScrape function
simpleScrape();
