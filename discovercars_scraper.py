#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DiscoverCars Scraper - AI Price Comparison
Uses Playwright to scrape rental car prices from discovercars.com
"""

import asyncio
import json
import logging
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from playwright.async_api import async_playwright, Page, Browser, TimeoutError as PlaywrightTimeout

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Location mappings (similar to CarJet)
LOCATION_MAPPINGS = {
    "Aeroporto de Faro": "Aeroporto de Faro (FAO)",
    "Faro Airport": "Aeroporto de Faro (FAO)",
    "Faro Aeroporto": "Aeroporto de Faro (FAO)",
    "FAO": "Aeroporto de Faro (FAO)",
    
    "Albufeira": "Albufeira Centro da cidade",
    "Albufeira Downtown": "Albufeira Centro da cidade",
    "Albufeira Centro": "Albufeira Centro da cidade",
}

def normalize_location(location: str) -> str:
    """Normalize location name to match DiscoverCars format"""
    location = location.strip()
    return LOCATION_MAPPINGS.get(location, location)

async def wait_for_network_idle(page: Page, timeout: int = 5000):
    """Wait for network to become idle"""
    try:
        await page.wait_for_load_state('networkidle', timeout=timeout)
    except PlaywrightTimeout:
        logger.warning("Network idle timeout - continuing anyway")

async def fill_location_input(page: Page, input_selector: str, location: str) -> bool:
    """
    Fill location input and select first dropdown item
    CORRECT ORDER (as per user demo):
    1. Click input (to open dropdown)
    2. Fill with text
    3. Select first item from dropdown
    """
    try:
        # STEP 1: Click input first to open dropdown
        logger.info(f"Step 1: Clicking input to open dropdown...")
        # Use JavaScript click to completely bypass viewport restrictions
        await page.evaluate('''(selector) => {
            const input = document.querySelector(selector);
            if (input) {
                input.click();
                input.focus();
            }
        }''', input_selector)
        await asyncio.sleep(0.5)
        
        # STEP 2: Fill input with full location text
        logger.info(f"Step 2: Filling input with: {location}")
        await page.fill(input_selector, location)
        await asyncio.sleep(1.5)
        
        # Screenshot after filling
        await page.screenshot(path='/tmp/discovercars_after_fill.png', full_page=True)
        logger.info("Screenshot saved: /tmp/discovercars_after_fill.png")
        
        # STEP 3: Wait for dropdown to appear and click FIRST item
        logger.info("Step 3: Waiting for dropdown and clicking first item...")
        
        # Wait a bit more for dropdown to appear
        await asyncio.sleep(2)
        
        # Try JavaScript detection and click (avoids bot detection)
        try:
            dropdown_found = await page.evaluate('''() => {
                // Try to find dropdown with various selectors
                const selectors = [
                    '.Autocomplete-Results li',
                    'ul[role="listbox"] li',
                    '.dropdown-menu li',
                    '.suggestions-list li',
                    'div[class*="suggestion"] li',
                    'div[class*="autocomplete"] li'
                ];
                
                for (const sel of selectors) {
                    const items = document.querySelectorAll(sel);
                    if (items && items.length > 0) {
                        // Click first item
                        items[0].click();
                        return {found: true, selector: sel, count: items.length};
                    }
                }
                return {found: false};
            }''')
            
            if dropdown_found and dropdown_found.get('found'):
                logger.info(f"✅ JavaScript clicked dropdown! Selector: {dropdown_found.get('selector')}, Items: {dropdown_found.get('count')}")
                await asyncio.sleep(1)
                return True
            else:
                logger.warning("JavaScript didn't find dropdown - trying Playwright selectors...")
        except Exception as e:
            logger.warning(f"JavaScript approach failed: {e}")
        
        # Fallback: Try Playwright selectors
        dropdown_selectors = [
            '.Autocomplete-Results li:first-child',
            '.Autocomplete-Results li',
            'ul[role="listbox"] li:first-child',
            '.dropdown-menu li:first-child',
            '.suggestions-list li:first-child',
        ]
        
        for selector in dropdown_selectors:
            try:
                first_item = await page.wait_for_selector(selector, state='visible', timeout=2000)
                if first_item:
                    await page.screenshot(path='/tmp/discovercars_dropdown_visible.png', full_page=True)
                    logger.info("Dropdown visible - screenshot saved")
                    
                    await first_item.click()
                    logger.info(f"✅ Clicked dropdown with Playwright: {selector}")
                    await asyncio.sleep(1)
                    return True
            except:
                continue
        
        logger.error(f"❌ Could not find dropdown - checking if location accepted anyway...")
        # Sometimes DiscoverCars accepts without clicking dropdown
        return True  # Try to continue anyway
        
    except Exception as e:
        logger.error(f"Error filling location: {e}")
        import traceback
        traceback.print_exc()
        return False

async def fill_search_form(
    page: Page,
    pickup_location: str,
    dropoff_location: str,
    pickup_date: str,
    dropoff_date: str,
    pickup_time: str = "10:00",
    dropoff_time: str = "10:00"
) -> bool:
    """
    Fill DiscoverCars search form
    """
    try:
        logger.info("Filling search form...")
        
        # Normalize locations
        pickup_location = normalize_location(pickup_location)
        dropoff_location = normalize_location(dropoff_location)
        
        # Wait for page to load
        await wait_for_network_idle(page)
        
        # Debug: Save HTML
        html_content = await page.content()
        with open('/tmp/discovercars_page.html', 'w', encoding='utf-8') as f:
            f.write(html_content)
        logger.info("HTML saved to: /tmp/discovercars_page.html")
        
        # Screenshot before searching
        await page.screenshot(path='/tmp/discovercars_03_before_search.png', full_page=True)
        logger.info("Screenshot saved: /tmp/discovercars_03_before_search.png")
        
        # Find pickup location input
        # DiscoverCars typically uses specific IDs or classes
        pickup_selectors = [
            'input[type="text"]',  # Try generic first
            'input[name="pickupLocation"]',
            'input[placeholder*="Local de recolha"]',
            'input[placeholder*="Pick-up"]',
            'input[placeholder*="recolha"]',
            '#pickupLocation',
            '[data-testid="pickup-location"]',
            'input[id*="pickup"]',
            'input[class*="location"]',
        ]
        
        pickup_input = None
        for selector in pickup_selectors:
            try:
                elements = await page.query_selector_all(selector)
                if elements:
                    logger.info(f"Found {len(elements)} elements with selector: {selector}")
                    pickup_input = elements[0]
                    # Log element attributes
                    attrs = await pickup_input.evaluate('el => Array.from(el.attributes).map(a => `${a.name}="${a.value}"`).join(" ")')
                    logger.info(f"First element attributes: {attrs}")
                    break
            except Exception as e:
                logger.debug(f"Selector {selector} failed: {e}")
                continue
        
        if not pickup_input:
            logger.error("Could not find pickup location input")
            # List all input elements for debug
            all_inputs = await page.query_selector_all('input')
            logger.error(f"Found {len(all_inputs)} total input elements on page")
            for idx, inp in enumerate(all_inputs[:10]):
                try:
                    attrs = await inp.evaluate('el => Array.from(el.attributes).map(a => `${a.name}="${a.value}"`).join(" ")')
                    logger.error(f"Input {idx}: {attrs}")
                except:
                    pass
            return False
        
        # Fill pickup location
        # Use name="PickupLocation" which we found in debug
        pickup_input_selector = 'input[name="PickupLocation"]'
        
        success = await fill_location_input(page, pickup_input_selector, pickup_location)
        if not success:
            logger.error("Failed to fill pickup location")
            return False
        
        await asyncio.sleep(1)
        
        # Dropoff location (same as pickup for now - simplify)
        # If different, enable checkbox and fill
        if pickup_location != dropoff_location:
            logger.info("Different dropoff not implemented yet - using same as pickup")
            # TODO: Enable checkbox and fill dropoff if needed
        
        # Dates and times - let DiscoverCars use defaults for now
        # User demo showed dates were filled automatically or via calendar
        logger.info("Using default dates from DiscoverCars (or clicking calendar if needed)")
        
        # Screenshot before search
        await page.screenshot(path='/tmp/discovercars_04_before_search_button.png', full_page=True)
        logger.info("Screenshot saved: /tmp/discovercars_04_before_search_button.png")
        
        # Click search button
        search_button_selectors = [
            'button:has-text("Pesquisar")',
            'button:has-text("Pesquisar agora")',
            'button:has-text("Search")',
            'button[type="submit"]',
            '[data-testid="search-button"]',
            'button.SearchForm-Submit',
        ]
        
        search_clicked = False
        for selector in search_button_selectors:
            try:
                button = await page.query_selector(selector)
                if button:
                    await button.click()
                    logger.info(f"Clicked search button: {selector}")
                    search_clicked = True
                    break
            except Exception as e:
                logger.debug(f"Search button selector {selector} failed: {e}")
                continue
        
        if not search_clicked:
            logger.warning("Could not find search button - trying enter key")
            await page.keyboard.press('Enter')
        
        # Wait for results page to load
        logger.info("Waiting for results page...")
        await asyncio.sleep(5)
        await wait_for_network_idle(page, timeout=15000)
        
        # Screenshot after search (results page)
        await page.screenshot(path='/tmp/discovercars_05_results_page.png', full_page=True)
        logger.info("Screenshot saved: /tmp/discovercars_05_results_page.png")
        logger.info(f"Current URL: {page.url}")
        
        return True
        
    except Exception as e:
        logger.error(f"Error filling search form: {e}")
        import traceback
        traceback.print_exc()
        return False

async def extract_car_results(page: Page) -> List[Dict[str, Any]]:
    """
    Extract car rental results from DiscoverCars results page
    """
    try:
        logger.info("Extracting car results...")
        logger.info(f"Page URL: {page.url}")
        logger.info(f"Page title: {await page.title()}")
        
        # Wait for results to load
        await asyncio.sleep(2)
        
        # Save HTML for debugging
        html_content = await page.content()
        with open('/tmp/discovercars_results.html', 'w', encoding='utf-8') as f:
            f.write(html_content)
        logger.info("Results HTML saved to: /tmp/discovercars_results.html")
        
        # Common selectors for car listings
        result_selectors = [
            'div[data-testid="vehicle-card"]',  # Try specific testid
            '.VehicleCard',  # DiscoverCars specific
            '.car-list-item',
            '[data-testid="car-result"]',
            '.vehicle-card',
            '.car-item',
            '.result-item',
            'article',  # Generic article tags
            'div[class*="vehicle"]',  # Any div with "vehicle" in class
            'div[class*="car"]',  # Any div with "car" in class
        ]
        
        results = []
        
        for selector in result_selectors:
            try:
                car_elements = await page.query_selector_all(selector)
                if car_elements:
                    logger.info(f"Found {len(car_elements)} results with selector: {selector}")
                    
                    for idx, car_elem in enumerate(car_elements[:20]):  # Limit to 20 results
                        try:
                            # Extract car name
                            car_name = None
                            name_selectors = [
                                '.car-name',
                                '.vehicle-name',
                                'h3',
                                'h4',
                                '[data-testid="car-name"]',
                            ]
                            
                            for name_sel in name_selectors:
                                try:
                                    name_elem = await car_elem.query_selector(name_sel)
                                    if name_elem:
                                        car_name = await name_elem.inner_text()
                                        car_name = car_name.strip()
                                        break
                                except:
                                    continue
                            
                            # Extract price
                            price = None
                            price_selectors = [
                                '.price',
                                '.total-price',
                                '[data-testid="price"]',
                                '.price-value',
                            ]
                            
                            for price_sel in price_selectors:
                                try:
                                    price_elem = await car_elem.query_selector(price_sel)
                                    if price_elem:
                                        price_text = await price_elem.inner_text()
                                        # Extract numeric value
                                        import re
                                        price_match = re.search(r'[\d,\.]+', price_text.replace(' ', ''))
                                        if price_match:
                                            price = float(price_match.group().replace(',', '.'))
                                            break
                                except:
                                    continue
                            
                            # Extract supplier
                            supplier = None
                            supplier_selectors = [
                                '.supplier-name',
                                '.company-name',
                                '[data-testid="supplier"]',
                                '.provider',
                            ]
                            
                            for sup_sel in supplier_selectors:
                                try:
                                    sup_elem = await car_elem.query_selector(sup_sel)
                                    if sup_elem:
                                        supplier = await sup_elem.inner_text()
                                        supplier = supplier.strip()
                                        break
                                except:
                                    continue
                            
                            if car_name and price:
                                results.append({
                                    'car_name': car_name,
                                    'price': price,
                                    'supplier': supplier or 'Unknown',
                                    'source': 'DiscoverCars',
                                    'position': idx + 1
                                })
                        
                        except Exception as e:
                            logger.warning(f"Error extracting car {idx}: {e}")
                            continue
                    
                    if results:
                        break  # Found results, stop trying other selectors
            
            except Exception as e:
                logger.warning(f"Error with selector {selector}: {e}")
                continue
        
        logger.info(f"Extracted {len(results)} car results")
        return results
        
    except Exception as e:
        logger.error(f"Error extracting results: {e}")
        import traceback
        traceback.print_exc()
        return []

async def scrape_discovercars(
    pickup_location: str,
    dropoff_location: str,
    pickup_date: str,
    dropoff_date: str,
    pickup_time: str = "10:00",
    dropoff_time: str = "10:00",
    headless: bool = True
) -> Dict[str, Any]:
    """
    Main scraping function for DiscoverCars
    
    Args:
        pickup_location: Pickup location (e.g., "Aeroporto de Faro")
        dropoff_location: Dropoff location
        pickup_date: Pickup date in DD/MM/YYYY format
        dropoff_date: Dropoff date in DD/MM/YYYY format
        pickup_time: Pickup time (HH:MM)
        dropoff_time: Dropoff time (HH:MM)
        headless: Run browser in headless mode
    
    Returns:
        Dictionary with results
    """
    browser = None
    
    try:
        logger.info(f"Starting DiscoverCars scraper...")
        logger.info(f"Pickup: {pickup_location} @ {pickup_date} {pickup_time}")
        logger.info(f"Dropoff: {dropoff_location} @ {dropoff_date} {dropoff_time}")
        
        async with async_playwright() as p:
            # Launch browser (like CarJet - mobile iPhone)
            browser = await p.chromium.launch(
                headless=headless,
                args=[
                    '--no-sandbox',
                    '--disable-setuid-sandbox',
                    '--disable-dev-shm-usage',
                    '--disable-blink-features=AutomationControlled',
                ]
            )
            
            # Create context with iPhone mobile user agent (like CarJet)
            context = await browser.new_context(
                viewport={'width': 390, 'height': 844},  # iPhone 13/14 viewport
                user_agent='Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1',
                device_scale_factor=3,
                is_mobile=True,
                has_touch=True
            )
            
            # Create page
            page = await context.new_page()
            
            # Navigate to DiscoverCars
            logger.info("Navigating to DiscoverCars...")
            await page.goto('https://www.discovercars.com/pt', wait_until='domcontentloaded')
            await asyncio.sleep(3)
            
            # Screenshot for debug
            await page.screenshot(path='/tmp/discovercars_01_initial.png', full_page=True)
            logger.info("Screenshot saved: /tmp/discovercars_01_initial.png")
            
            # Handle cookie consent if present
            try:
                cookie_selectors = [
                    'button:has-text("Aceitar")',
                    'button:has-text("Accept")',
                    'button:has-text("Aceito")',
                    '[data-testid="cookie-accept"]',
                    '#onetrust-accept-btn-handler',
                    '.accept-cookies',
                ]
                for selector in cookie_selectors:
                    try:
                        await page.click(selector, timeout=2000)
                        logger.info(f"Accepted cookies with: {selector}")
                        await asyncio.sleep(0.5)
                        break
                    except:
                        continue
            except:
                pass
            
            # Screenshot after cookies
            await page.screenshot(path='/tmp/discovercars_02_after_cookies.png', full_page=True)
            logger.info("Screenshot saved: /tmp/discovercars_02_after_cookies.png")
            
            # Fill search form
            success = await fill_search_form(
                page,
                pickup_location,
                dropoff_location,
                pickup_date,
                dropoff_date,
                pickup_time,
                dropoff_time
            )
            
            if not success:
                logger.error("Failed to fill search form")
                return {
                    'success': False,
                    'error': 'Failed to fill search form',
                    'results': []
                }
            
            # Extract results
            results = await extract_car_results(page)
            
            # Close browser
            await browser.close()
            
            return {
                'success': True,
                'source': 'DiscoverCars',
                'pickup_location': pickup_location,
                'dropoff_location': dropoff_location,
                'pickup_date': pickup_date,
                'dropoff_date': dropoff_date,
                'total_results': len(results),
                'results': results,
                'scraped_at': datetime.now().isoformat()
            }
    
    except Exception as e:
        logger.error(f"Error in scrape_discovercars: {e}")
        import traceback
        traceback.print_exc()
        
        if browser:
            try:
                await browser.close()
            except:
                pass
        
        return {
            'success': False,
            'error': str(e),
            'results': []
        }

# Test function
async def test_scraper():
    """Test the scraper"""
    # Test dates (7 days from now)
    pickup = (datetime.now() + timedelta(days=7)).strftime('%d/%m/%Y')
    dropoff = (datetime.now() + timedelta(days=14)).strftime('%d/%m/%Y')
    
    result = await scrape_discovercars(
        pickup_location="Aeroporto de Faro",
        dropoff_location="Aeroporto de Faro",  # Same location for now
        pickup_date=pickup,
        dropoff_date=dropoff,
        headless=False  # VISIBLE for demo!
    )
    
    print(json.dumps(result, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    asyncio.run(test_scraper())
