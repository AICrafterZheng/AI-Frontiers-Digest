import { test, expect } from '@playwright/test';

test.describe('Header Component', () => {
  test.beforeEach(async ({ page }) => {
    // Navigate to your site before each test
    await page.goto('https://aicrafter.info/');
  });

  test('displays logo and main navigation elements', async ({ page }) => {
    // Check if logo is visible
    await expect(page.getByRole('link', { name: 'AI Frontiers' })).toBeVisible();
    
    // Check main navigation links
    await expect(page.getByRole('navigation')).toBeVisible();
    await expect(page.getByRole('link', { name: 'Home' })).toBeVisible();
    await expect(page.getByRole('link', { name: 'Subscribe' })).toBeVisible();
  });

  test('mobile menu functionality', async ({ page }) => {
    // Test mobile viewport
    await page.setViewportSize({ width: 375, height: 667 });

    // Check if hamburger menu button appears
    const menuButton = page.getByRole('button', { name: /menu/i });
    await expect(menuButton).toBeVisible();

    // Click menu button and verify menu opens
    await menuButton.click();
    await expect(page.getByRole('navigation')).toBeVisible();
  });

  test('navigation links work correctly', async ({ page }) => {
    // Click Subscribe and verify navigation
    await page.getByRole('link', { name: 'Subscribe' }).click();
    await expect(page).toHaveURL(/.*subscribe/);

    // Navigate back to home
    await page.getByRole('link', { name: 'Home' }).click();
    await expect(page).toHaveURL('https://aicrafter.info/');
  });

  test('header remains visible when scrolling', async ({ page }) => {
    // Scroll down the page
    await page.evaluate(() => window.scrollTo(0, 500));
    
    // Verify header is still visible
    await expect(page.getByRole('banner')).toBeVisible();
  });
}); 