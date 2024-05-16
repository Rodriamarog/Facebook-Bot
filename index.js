const chromium = require('chrome-aws-lambda');
const puppeteer = chromium.puppeteer;

exports.handler = async (event) => {
  let browser = null;
  try {
    console.log('Launching headless browser...');
    browser = await puppeteer.launch({
      args: chromium.args,
      defaultViewport: chromium.defaultViewport,
      executablePath: await chromium.executablePath,
      headless: chromium.headless,
    });

    console.log('Opening new page...');
    const page = await browser.newPage();
    console.log('Navigating to https://example.com...');
    await page.goto('https://example.com');
    const title = await page.title();
    console.log(`Title of the page: ${title}`);

    return {
      statusCode: 200,
      body: JSON.stringify({
        message: 'Page title fetched successfully',
        title: title,
      }),
    };
  } catch (error) {
    console.error('Error during browser automation:', error);
    return {
      statusCode: 500,
      body: JSON.stringify({
        error: 'Failed to complete browser automation',
        details: error.toString(),
      }),
    };
  } finally {
    if (browser !== null) {
      console.log('Closing browser...');
      await browser.close();
    }
  }
};
