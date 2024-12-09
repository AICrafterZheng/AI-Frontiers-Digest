import { test, expect } from '@playwright/test'
import { ai } from '@zerostep/playwright'
const website = 'https://zerostep.com/'
const website2 = 'https://google.com/'
// const website3 = 'https://aicrafter.info/'
const website3 = 'http://localhost:5173'
test('zerostep example', async ({ page }) => {
  await page.goto(website3)

  // An object with page and test must be passed into every call
  const aiArgs = { page, test }
  const headerText = await ai('Get the buttons', aiArgs)
  console.log(headerText)
  // await expect(headerText).toBe('AI Crafter')
  await page.goto(website2)
  await ai(`Type "${headerText}" in the search box`, aiArgs)
  const searchtext = await ai('Press enter', aiArgs)
  console.log(searchtext)
})
