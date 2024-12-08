import { test, expect } from '@playwright/test';

test.describe('Header Component', () => {
  test.beforeEach(async ({ page }) => {
    // Mock GitHub API response
    await page.route('https://api.github.com/repos/AICrafterZheng/AI-Frontiers-Digest', async route => {
      await route.fulfill({
        status: 200,
        contentType: 'application/json',
        body: JSON.stringify({
          stargazers_count: 123,
          forks_count: 45
        })
      });
    });

    await page.goto('http://localhost:5173');
    await page.waitForLoadState('domcontentloaded');
    // Set desktop viewport by default
    await page.setViewportSize({ width: 1280, height: 720 });
  });

  test('subscribe button is visible and clickable', async ({ page }) => {
    const subscribeButton = page.getByTestId('subscribe-button').first();
    await expect(subscribeButton).toBeVisible({ timeout: 10000 });
    await expect(subscribeButton).toBeEnabled();
  });

  test('discord button is visible and clickable', async ({ page }) => {
    const discordButton = page.getByTestId('discord-button').first();
    await expect(discordButton).toBeVisible({ timeout: 10000 });
    await expect(discordButton).toBeEnabled();
    
    // Verify Discord icon
    const discordIcon = discordButton.locator('.lucide-message-square');
    await expect(discordIcon).toBeVisible();
  });

  test('archive button is visible and clickable', async ({ page }) => {
    const archiveButton = page.getByTestId('archive-button').first();
    await expect(archiveButton).toBeVisible({ timeout: 10000 });
    await expect(archiveButton).toBeEnabled();
    
    // Verify Archive icon
    const archiveIcon = archiveButton.locator('.lucide-archive');
    await expect(archiveIcon).toBeVisible();
  });

  test('github link is visible and has correct href and stars', async ({ page }) => {
    const githubLink = page.getByTestId('github-link').first();
    await expect(githubLink).toBeVisible({ timeout: 10000 });
    await expect(githubLink).toHaveAttribute('href', 'https://github.com/AICrafterZheng/AI-Frontiers-Digest');
    
    // Verify GitHub icon
    const githubIcon = githubLink.locator('.lucide-github');
    await expect(githubIcon).toBeVisible();

    // Verify stars count text
    const starsCount = githubLink.locator('span:has-text("★")').first();
    await expect(starsCount).toBeVisible();
    
    // Verify the exact star count
    const starsText = await starsCount.textContent();
    expect(starsText).toContain('★ 123');
  });

  test('theme toggle button is visible and functional', async ({ page }) => {
    const themeToggle = page.getByTestId('theme-toggle').first();
    await expect(themeToggle).toBeVisible({ timeout: 10000 });
    await expect(themeToggle).toBeEnabled();

    // Get initial theme icon
    const initialIcon = await themeToggle.locator('.lucide-sun, .lucide-moon').first();
    await expect(initialIcon).toBeVisible();
    
    // Click theme toggle
    await themeToggle.click();
    await page.waitForTimeout(500); // Wait for theme transition
    
    // Verify theme changed
    const newIcon = await themeToggle.locator('.lucide-sun, .lucide-moon').first();
    await expect(newIcon).toBeVisible();
  });

  test('mobile menu functionality', async ({ page }) => {
    // Set mobile viewport and wait for layout to adjust
    await page.setViewportSize({ width: 375, height: 667 });
    await page.waitForTimeout(500);
    
    // Check hamburger menu button
    const menuButton = page.getByTestId('menu-button');
    await expect(menuButton).toBeVisible({ timeout: 10000 });
    
    // Open menu and wait for animation
    await menuButton.click();
    await page.waitForTimeout(500);
    
    // Check if mobile menu items are visible
    const mobileMenuItems = [
      'subscribe-button-mobile',
      'discord-button-mobile',
      'archive-button-mobile',
      'github-link-mobile',
      'theme-toggle-mobile'
    ];

    for (const testId of mobileMenuItems) {
      await expect(page.getByTestId(testId)).toBeVisible({ timeout: 5000 });
    }
    
    // Close menu using close button
    const closeButton = page.getByTestId('menu-button');
    await expect(closeButton).toBeVisible({ timeout: 10000 });
    await closeButton.click();
    await page.waitForTimeout(500);
    
    // Verify menu is closed
    await expect(page.getByTestId('subscribe-button-mobile')).not.toBeVisible();
  });

  test('navigation functionality', async ({ page }) => {
    // Click Archive button and wait for navigation
    const archiveButton = page.getByTestId('archive-button').first();
    await expect(archiveButton).toBeVisible({ timeout: 10000 });
    await archiveButton.click();
    await page.waitForURL(/.*\/archive$/);
    
    // Click logo to go back home
    const logo = page.locator('a:has-text("AI Frontiers")');
    await expect(logo).toBeVisible();
    await logo.click();
    await page.waitForURL(/.*\/$/);
  });

  test('click outside closes mobile menu', async ({ page }) => {
    // Set mobile viewport and wait for layout
    await page.setViewportSize({ width: 375, height: 667 });
    await page.waitForTimeout(500);
    
    // Open menu and wait for animation
    const menuButton = page.getByTestId('menu-button');
    await expect(menuButton).toBeVisible({ timeout: 10000 });
    await menuButton.click();
    await page.waitForTimeout(500);
    
    // Verify menu is open
    await expect(page.getByTestId('subscribe-button-mobile')).toBeVisible();
    
    // Click outside menu and wait for close animation
    await page.mouse.click(10, 10);
    await page.waitForTimeout(500);
    
    // Verify menu is closed
    await expect(page.getByTestId('subscribe-button-mobile')).not.toBeVisible();
  });
});