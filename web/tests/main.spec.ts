import { test, expect } from '@playwright/test';

test('Has title', async ({ page }) => {
  await page.goto('https://aicrafter.info/');

  // Expect a title "to contain" a substring.
  await expect(page).toHaveTitle(/AI Frontiers Digest/);
});

// test('get started link', async ({ page }) => {
//   await page.goto('https://aicrafter.info/');

//   // Click the get started link.
//   await page.getByRole('link', { name: 'Subscribe' }).click();

//   // Expects page to have a heading with the name of Installation.
//   await expect(page.getByRole('link', { name: 'Subscribe Now' })).toBeVisible();
// });
