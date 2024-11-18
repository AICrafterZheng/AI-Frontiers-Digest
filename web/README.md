# Newsletter-Digest-Web

[Edit in StackBlitz next generation editor ⚡️](https://stackblitz.com/~/github.com/AICrafterZheng/Newsletter-Digest-Web)

## Run the Cloudflare Functions locally:
### Copy the .dev.vars.example file to .dev.vars and fill in the values:
```bash
cp .dev.vars.example .dev.vars
```
### Copy .env.example to .env.development and fill in the values:
```bash
cp .env.example .env.development
```
### First, build your frontend (assuming you're in the project root):

```bash
npm run dev
```
> This will use VITE_BACKEND_API_URL from .env.development, which is served by the Cloudflare Functions.

### Then run Cloudflare Pages locally:

```bash
npm run preview:wrangler

# Or
npx wrangler pages dev ./

```

## Deploy to Cloudflare Pages:
```bash
npx wrangler login
npm run build
npx wrangler pages deploy dist --project-name newsletter-digest-web
npx wrangler pages project list
```