import { test, expect } from '@playwright/test';
import { ai } from '@zerostep/playwright';

const website = 'http://localhost:5173';
// const website = "https://aicrafter.info"
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

    await page.goto(website);
    await page.waitForLoadState('domcontentloaded');
    // Set desktop viewport by default
    await page.setViewportSize({ width: 1280, height: 720 });
  });

  test('subscribe button is visible and clickable', async ({ page }) => {
    const aiArgs = { page, test}
    const subscribeButton = await ai('Get the subscribe button', aiArgs);
    console.log(subscribeButton)
    await expect(subscribeButton).toBe("Subscribe")
  });

  test('discord button is visible and clickable', async ({ page }) => {
    const aiArgs = { page, test}
    const discordButton = await ai('Get the discord button', aiArgs);
    console.log(discordButton)
    await expect(discordButton).toBe("Discord")
  });

  test('archive button is visible and clickable', async ({ page }) => {
    const aiArgs = { page, test}
    const archiveButton = await ai('Get the archive button', aiArgs);
    console.log(archiveButton)
    await expect(archiveButton).toBe("Archive")
  }); 

  test('github link is visible and has correct href and stars', async ({ page }) => {
    const aiArgs = { page, test}
    const githubLink = await ai('Get the github link', aiArgs);
    console.log(githubLink)
    await expect(githubLink).toHaveAttribute('href', 'https://github.com/AICrafterZheng/AI-Frontiers-Digest')
    await expect(githubLink).toHaveText('GitHub')
    await expect(githubLink).toHaveAttribute('aria-label', 'GitHub repository')
  });

  test('menu button is visible and clickable', async ({ page }) => {
    const aiArgs = { page, test}
    const menuButton = await ai('Get the menu button', aiArgs);
    console.log(menuButton)
    await expect(menuButton).toBe("Menu")
  });

  test('close menu button is visible and clickable', async ({ page }) => {
    const aiArgs = { page, test}
    const closeMenuButton = await ai('Get the close menu button', aiArgs);
    console.log(closeMenuButton)
    await expect(closeMenuButton).toBe("Close menu")
  });

});
