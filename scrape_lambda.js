"use strict";
var __awaiter = (this && this.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
var __generator = (this && this.__generator) || function (thisArg, body) {
    var _ = { label: 0, sent: function() { if (t[0] & 1) throw t[1]; return t[1]; }, trys: [], ops: [] }, f, y, t, g;
    return g = { next: verb(0), "throw": verb(1), "return": verb(2) }, typeof Symbol === "function" && (g[Symbol.iterator] = function() { return this; }), g;
    function verb(n) { return function (v) { return step([n, v]); }; }
    function step(op) {
        if (f) throw new TypeError("Generator is already executing.");
        while (g && (g = 0, op[0] && (_ = 0)), _) try {
            if (f = 1, y && (t = op[0] & 2 ? y["return"] : op[0] ? y["throw"] || ((t = y["return"]) && t.call(y), 0) : y.next) && !(t = t.call(y, op[1])).done) return t;
            if (y = 0, t) op = [op[0] & 2, t.value];
            switch (op[0]) {
                case 0: case 1: t = op; break;
                case 4: _.label++; return { value: op[1], done: false };
                case 5: _.label++; y = op[1]; op = [0]; continue;
                case 7: op = _.ops.pop(); _.trys.pop(); continue;
                default:
                    if (!(t = _.trys, t = t.length > 0 && t[t.length - 1]) && (op[0] === 6 || op[0] === 2)) { _ = 0; continue; }
                    if (op[0] === 3 && (!t || (op[1] > t[0] && op[1] < t[3]))) { _.label = op[1]; break; }
                    if (op[0] === 6 && _.label < t[1]) { _.label = t[1]; t = op; break; }
                    if (t && _.label < t[2]) { _.label = t[2]; _.ops.push(op); break; }
                    if (t[2]) _.ops.pop();
                    _.trys.pop(); continue;
            }
            op = body.call(thisArg, _);
        } catch (e) { op = [6, e]; y = 0; } finally { f = t = 0; }
        if (op[0] & 5) throw op[1]; return { value: op[0] ? op[1] : void 0, done: true };
    }
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.handler = void 0;
var puppeteerCore = require("puppeteer-core"); // Changed to 'puppeteerCore' to avoid naming collision
var chrome_aws_lambda_1 = require("chrome-aws-lambda");
var dotenv = require("dotenv");
dotenv.config();
var isLocal = process.env.LOCAL_TEST === 'true'; // Set this env var in your local environment
var getExecutablePath = function () { return __awaiter(void 0, void 0, void 0, function () {
    var puppeteer;
    return __generator(this, function (_a) {
        if (isLocal) {
            puppeteer = require('puppeteer');
            return [2 /*return*/, puppeteer.executablePath()];
        }
        else {
            // Chromium's executable path for Lambda environment
            return [2 /*return*/, chrome_aws_lambda_1.default.executablePath]; // Note: not calling it as a function
        }
        return [2 /*return*/];
    });
}); };
var processWaitTimes = function (waitTimes, lanes) {
    var count = 0;
    var filteredWaitTimes = [lanes[0]];
    for (var _i = 0, waitTimes_1 = waitTimes; _i < waitTimes_1.length; _i++) {
        var waitTime = waitTimes_1[_i];
        if (waitTime.endsWith(":") || waitTime.startsWith("N")) {
            continue;
        }
        if (waitTime.includes('No Delay')) {
            filteredWaitTimes.push(waitTime);
        }
        else if (waitTime.includes('Status')) {
            var adjustedTime = 'Vehicles: 0.05';
            filteredWaitTimes.push(adjustedTime);
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
var scrapeWaitTimes = function () { return __awaiter(void 0, void 0, void 0, function () {
    var puppeteer, browser, _a, _b, page, lanes_sy, lanes_otay, syWaitTimes, otayWaitTimes, filteredWaitTimesSY, filteredWaitTimesOtay;
    var _c;
    return __generator(this, function (_d) {
        switch (_d.label) {
            case 0:
                puppeteer = isLocal ? require('puppeteer') : puppeteerCore;
                _b = (_a = puppeteer).launch;
                _c = {};
                return [4 /*yield*/, getExecutablePath()];
            case 1: return [4 /*yield*/, _b.apply(_a, [(_c.executablePath = _d.sent(),
                        _c.args = chrome_aws_lambda_1.default.args,
                        _c.headless = true,
                        _c.defaultViewport = { width: 1920, height: 1080 },
                        _c)])];
            case 2:
                browser = _d.sent();
                return [4 /*yield*/, browser.newPage()];
            case 3:
                page = _d.sent();
                return [4 /*yield*/, page.goto("https://www.smartbordercoalition.com/border-wait-times")];
            case 4:
                _d.sent();
                return [4 /*yield*/, page.waitForSelector("div.ticker__item:nth-of-type(2) span", { timeout: 10000 })];
            case 5:
                _d.sent();
                lanes_sy = ['SAN YSIDRO:', 'All Traffic >>', 'Ready Lanes >>', 'Sentri >>'];
                lanes_otay = ['OTAY:', 'All Traffic >>', 'Ready Lanes >>', 'Sentri >>'];
                return [4 /*yield*/, page.evaluate(function () {
                        return Array.from(document.querySelectorAll("div.ticker__item:nth-of-type(2) span")).map(function (span) { return span.innerText; });
                    })];
            case 6:
                syWaitTimes = _d.sent();
                return [4 /*yield*/, page.evaluate(function () {
                        return Array.from(document.querySelectorAll("div.ticker__item:nth-of-type(3) span")).map(function (span) { return span.innerText; });
                    })];
            case 7:
                otayWaitTimes = _d.sent();
                filteredWaitTimesSY = processWaitTimes(syWaitTimes, lanes_sy);
                filteredWaitTimesOtay = processWaitTimes(otayWaitTimes, lanes_otay);
                return [4 /*yield*/, browser.close()];
            case 8:
                _d.sent();
                return [2 /*return*/, [filteredWaitTimesSY, filteredWaitTimesOtay]];
        }
    });
}); };
var handler = function (event, context) { return __awaiter(void 0, void 0, void 0, function () {
    var results, e_1;
    return __generator(this, function (_a) {
        switch (_a.label) {
            case 0:
                console.log("Handler started");
                _a.label = 1;
            case 1:
                _a.trys.push([1, 3, , 4]);
                return [4 /*yield*/, scrapeWaitTimes()];
            case 2:
                results = _a.sent();
                console.log("Data processed successfully");
                return [2 /*return*/, {
                        statusCode: 200,
                        body: JSON.stringify(results)
                    }];
            case 3:
                e_1 = _a.sent();
                console.error("An error occurred:", e_1);
                return [2 /*return*/, {
                        statusCode: 500,
                        body: JSON.stringify({ error: "Failed to process data" })
                    }];
            case 4: return [2 /*return*/];
        }
    });
}); };
exports.handler = handler;
if (require.main === module) {
    (function () { return __awaiter(void 0, void 0, void 0, function () {
        var results, e_2;
        return __generator(this, function (_a) {
            switch (_a.label) {
                case 0:
                    _a.trys.push([0, 2, , 3]);
                    return [4 /*yield*/, scrapeWaitTimes()];
                case 1:
                    results = _a.sent();
                    console.log(results);
                    return [3 /*break*/, 3];
                case 2:
                    e_2 = _a.sent();
                    console.error("An error occurred:", e_2);
                    return [3 /*break*/, 3];
                case 3: return [2 /*return*/];
            }
        });
    }); })();
}
