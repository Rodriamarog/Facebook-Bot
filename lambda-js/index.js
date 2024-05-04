const chromium = require('chrome-aws-lambda');
const puppeteer = chromium.puppeteer;

exports.handler = async (event) => {
  let browser = null;
  try {
    // Setup Puppeteer to use the bundled Chromium from chrome-aws-lambda
    browser = await puppeteer.launch({
      args: chromium.args,
      defaultViewport: chromium.defaultViewport,
      executablePath: await chromium.executablePath,
      headless: chromium.headless,
    });

    const page = await browser.newPage();
    await page.goto('https://example.com');
    const title = await page.title();
    console.log(`Title of the page: ${title}`);

    // Return a response from the Lambda function
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
    // Ensure the browser is closed when the function execution is complete.
    if (browser !== null) {
      await browser.close();
    }
  }
};
