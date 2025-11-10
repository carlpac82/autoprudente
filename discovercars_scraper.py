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

async def click_dropdown_and_select(page: Page, input_selector: str, location: str, dropdown_selector: str) -> bool:
    """
    Click on dropdown input and select location from dropdown menu
    Similar to CarJet scraper methodology
    """
    try:
        # Try to scroll to make element visible
        try:
            await page.evaluate('''(selector) => {
                const el = document.querySelector(selector);
                if (el) {
                    el.scrollIntoView({behavior: "auto", block: "center", inline: "center"});
                    window.scrollBy(0, -100); // Adjust for fixed header
                }
            }''', input_selector)
            await asyncio.sleep(0.8)
        except:
            pass
        
        # Force click (bypasses viewport checks - useful for fixed headers)
        await page.click(input_selector, timeout=5000, force=True)
        await asyncio.sleep(1)
        
        # Wait for dropdown to appear
        await page.wait_for_selector(dropdown_selector, state='visible', timeout=5000)
        
        # Type location to filter results
        await page.fill(input_selector, location)
        await asyncio.sleep(1.5)
        
        # Click on first matching result
        # Try multiple selectors for dropdown items
        dropdown_item_selectors = [
            f"{dropdown_selector} li:has-text('{location}')",
            f"{dropdown_selector} div:has-text('{location}')",
            f"{dropdown_selector} [role='option']:has-text('{location}')",
            f"{dropdown_selector} button:has-text('{location}')",
        ]
        
        for selector in dropdown_item_selectors:
            try:
                elements = await page.query_selector_all(selector)
                if elements:
                    await elements[0].click(timeout=3000)
                    logger.info(f"Selected location: {location}")
                    await asyncio.sleep(1)
                    return True
            except Exception as e:
                continue
        
        logger.error(f"Could not find dropdown item for: {location}")
        return False
        
    except Exception as e:
        logger.error(f"Error in click_dropdown_and_select: {e}")
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
        
        # Click and select pickup location
        # Use name="PickupLocation" which we found in debug
        pickup_input_selector = 'input[name="PickupLocation"]'
        
        pickup_dropdown_selectors = [
            'ul[role="listbox"]',
            '.dropdown-menu',
            '[data-testid="location-dropdown"]',
            '.suggestions-list',
            '.Autocomplete-Results',  # DiscoverCars specific
        ]
        
        success = False
        for dropdown_sel in pickup_dropdown_selectors:
            try:
                success = await click_dropdown_and_select(
                    page,
                    pickup_input_selector,
                    pickup_location,
                    dropdown_sel
                )
                if success:
                    break
            except Exception as e:
                logger.warning(f"Dropdown selector {dropdown_sel} failed: {e}")
                continue
        
        if not success:
            logger.error("Failed to select pickup location")
            return False
        
        await asyncio.sleep(1)
        
        # Check if different dropoff location
        if pickup_location != dropoff_location:
            # Enable "Different dropoff location" if available
            try:
                different_location_checkbox = await page.query_selector('input[type="checkbox"]')
                if different_location_checkbox:
                    await different_location_checkbox.click()
                    await asyncio.sleep(0.5)
            except:
                pass
            
            # Find dropoff location input
            dropoff_selectors = [
                'input[name="dropoffLocation"]',
                'input[placeholder*="Local de devolução"]',
                'input[placeholder*="Drop-off"]',
                '#dropoffLocation',
            ]
            
            for selector in dropoff_selectors:
                try:
                    dropoff_input = await page.wait_for_selector(selector, timeout=3000)
                    if dropoff_input:
                        for dropdown_sel in pickup_dropdown_selectors:
                            try:
                                await click_dropdown_and_select(
                                    page,
                                    selector,
                                    dropoff_location,
                                    dropdown_sel
                                )
                                break
                            except:
                                continue
                        break
                except:
                    continue
        
        # Fill dates
        # Date pickers usually have specific formats
        pickup_date_obj = datetime.strptime(pickup_date, '%d/%m/%Y')
        dropoff_date_obj = datetime.strptime(dropoff_date, '%d/%m/%Y')
        
        # Try to fill date inputs
        date_selectors = [
            'input[name="pickupDate"]',
            'input[placeholder*="Data de recolha"]',
            'input[type="date"]',
        ]
        
        for selector in date_selectors:
            try:
                await page.fill(selector, pickup_date_obj.strftime('%Y-%m-%d'))
                break
            except:
                continue
        
        await asyncio.sleep(0.5)
        
        # Fill times if available
        time_selectors = [
            'select[name="pickupTime"]',
            'input[name="pickupTime"]',
        ]
        
        for selector in time_selectors:
            try:
                await page.select_option(selector, pickup_time)
                break
            except:
                try:
                    await page.fill(selector, pickup_time)
                    break
                except:
                    continue
        
        # Submit search
        search_button_selectors = [
            'button[type="submit"]',
            'button:has-text("Pesquisar")',
            'button:has-text("Search")',
            '[data-testid="search-button"]',
        ]
        
        for selector in search_button_selectors:
            try:
                await page.click(selector, timeout=3000)
                logger.info("Clicked search button")
                break
            except:
                continue
        
        # Wait for results page
        await asyncio.sleep(3)
        await wait_for_network_idle(page, timeout=10000)
        
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
        
        # Wait for results to load
        await asyncio.sleep(2)
        
        # Common selectors for car listings
        result_selectors = [
            '.car-list-item',
            '[data-testid="car-result"]',
            '.vehicle-card',
            '.car-item',
            '.result-item',
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
        dropoff_location="Albufeira Centro da cidade",
        pickup_date=pickup,
        dropoff_date=dropoff,
        headless=False  # Set to True for production
    )
    
    print(json.dumps(result, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    asyncio.run(test_scraper())
